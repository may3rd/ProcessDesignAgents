from __future__ import annotations

import json
from json_repair import repair_json
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from dotenv import load_dotenv

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import jinja_raw, strip_markdown_code_fences, load_prompt

load_dotenv()


def create_concept_detailer(llm, selection_provider_getter=None):
    def concept_detailer(state: DesignState) -> DesignState:
        """Concept Detailer: Picks the highest-feasibility concept and elaborates it for downstream design."""
        print("\n# Concept Selection", flush=True)
        
        # Get the input data
        evaluations_json_raw = state.get("research_rating_results")
        requirements_markdown = state.get("process_requirements", "")

        try:
            evaluation_payload = json.loads(repair_json(evaluations_json_raw))
        except Exception as e:
            print(f"Error: {e}")
            print(evaluations_json_raw)
            raise ValueError("Concept detailer expected JSON evaluations from conservative researcher.")

        if isinstance(evaluation_payload, dict):
            evaluations = evaluation_payload.get("concepts")
        elif isinstance(evaluation_payload, list):
            evaluations = evaluation_payload
        else:
            evaluations = None

        if not isinstance(evaluations, list) or not evaluations:
            print(evaluation_payload)
            raise ValueError("Concept detailer could not find any concept evaluations to consider.")

        concept_options = []
        for idx, evaluation in enumerate(evaluations, start=1):
            name = evaluation.get("name", f"Concept {idx}")
            score = _safe_int(evaluation.get("feasibility_score"))
            concept_options.append(
                {
                    "title": name,
                    "score": score,
                    "evaluation": evaluation,
                }
            )

        selected_index: int | None = None
        selection_provider = selection_provider_getter() if selection_provider_getter else None
        if selection_provider:
            try:
                selected_index = selection_provider(concept_options)
            except Exception as exc:  # noqa: BLE001
                print(
                    f"Concept selection input failed ({exc}); defaulting to best score.",
                    flush=True,
                )
                selected_index = None

        if selected_index is not None and 0 <= selected_index < len(concept_options):
            chosen = concept_options[selected_index]
        else:
            chosen = _select_best_evaluation(concept_options)

        best_evaluation = chosen["evaluation"]
        selected_concept_title = best_evaluation.get("name", chosen["title"])
        best_score = chosen["score"]
        selected_concept_evaluations_json = json.dumps(best_evaluation, ensure_ascii=False)

        print(
            f"Chosen concept: {selected_concept_title}\n(Feasibility Score: {best_score if best_score is not None else 'N/A'})",
            flush=True,
        )
        # print("DEBUG: Call LLM to generate detailed concept brief...", flush=True)
        base_prompt = concept_detailer_prompt(best_evaluation, requirements_markdown)
        prompt_messages = base_prompt.messages # + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | llm
        is_done = False
        try_count = 0
        concept_description_markdown = ""
        while not is_done:
            try_count += 1
            if try_count > 3:
                print("+ Max try count reached.", flush=True)
                exit(-1)
            try:
                response = chain.invoke({"messages": list(state.get("messages", []))})
                concept_description_markdown = (
                    response.content if isinstance(response.content, str) else str(response.content)
                ).strip()
                concept_description_markdown = strip_markdown_code_fences(concept_description_markdown)
                if len(concept_description_markdown) > 50:
                    is_done = True
                else:
                    print("DEBUG: The respones message is too short. Try again.")
            except Exception as e:
                print(f"Attemp {try_count}: {e}")
        print(concept_description_markdown, flush=True)
        return {
            "selected_concept_name": selected_concept_title,
            "selected_concept_details": concept_description_markdown,
            "selected_concept_evaluation": selected_concept_evaluations_json,
            "messages": [response],
        }
    return concept_detailer


def _select_best_evaluation(options: list[dict]) -> dict:
    if not options:
        raise ValueError("No concept evaluations supplied.")

    best_option = options[0]
    best_score = _safe_int(best_option.get("score"))

    for option in options[1:]:
        score = _safe_int(option.get("score"))
        if score is None:
            continue
        if best_score is None or score > best_score:
            best_option = option
            best_score = score

    return best_option


def _safe_int(value) -> int | None:
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        try:
            return int(value.strip())
        except ValueError:
            return None
    return None


def concept_detailer_prompt(
    selected_evaluation: dict,
    requirements_markdown: str,
) -> ChatPromptTemplate:
    
    selected_concept_json = json.dumps(selected_evaluation, ensure_ascii=False, indent=2)

    system_content = load_prompt("detail_concept_researcher_system.xml")

    human_content = f"""
# DATA FOR ANALYSIS:
---
**SELECTED CONCEPT EVALUATION (JSON):**
{selected_concept_json}

**PROJECT REQUIREMENTS:**
{requirements_markdown}

# FINAL MARKDOWN OUTPUT:
"""

    messages = [
        SystemMessagePromptTemplate.from_template(
            jinja_raw(system_content),
            template_format="jinja2",
        ),
        HumanMessagePromptTemplate.from_template(
            jinja_raw(human_content),
            template_format="jinja2",
        ),
    ]

    return ChatPromptTemplate.from_messages(messages)
