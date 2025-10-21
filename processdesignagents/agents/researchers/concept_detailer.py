import json
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from dotenv import load_dotenv

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import jinja_raw, strip_markdown_code_fences

load_dotenv()


def create_concept_detailer(llm, selection_provider_getter=None):
    def concept_detailer(state: DesignState) -> DesignState:
        """Concept Detailer: Picks the highest-feasibility concept and elaborates it for downstream design."""
        print("\n# Concept Selection", flush=True)
        evaluations_json_raw = state.get("research_rateing_results", "")
        if not isinstance(evaluations_json_raw, str):
            evaluations_json_raw = str(evaluations_json_raw)
        requirements_markdown = state.get("requirements", "")
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)

        evaluation_payload = json.loads(evaluations_json_raw)
        if evaluation_payload is None:
            raise ValueError("Concept detailer expected JSON evaluations from conservative researcher.")

        if isinstance(evaluation_payload, dict):
            evaluations = evaluation_payload.get("concepts")
        elif isinstance(evaluation_payload, list):
            evaluations = evaluation_payload
        else:
            evaluations = None

        if not isinstance(evaluations, list) or not evaluations:
            raise ValueError("Concept detailer could not find any concept evaluations to consider.")

        # evaluations_markdown = convert_evaluations_json_to_markdown(sanitized_evaluations_json)
        # print(evaluations_markdown, flush=True)

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
        best_title = best_evaluation.get("name", chosen["title"])
        best_score = chosen["score"]
        selected_evaluation_json = json.dumps(best_evaluation, ensure_ascii=False)

        print(
            f"Chosen concept: {best_title}\n(Feasibility Score: {best_score if best_score is not None else 'N/A'})",
            flush=True,
        )
        print("* Call LLM to generate detailed concept brief...", flush=True)
        base_prompt = concept_detailer_prompt(best_evaluation, requirements_markdown)
        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | llm
        is_done = False
        try_count = 0
        while not is_done:
            try_count += 1
            if try_count > 3:
                print("+ Max try count reached.", flush=True)
                exit(-1)
            try:
                response = chain.invoke({"messages": list(state.get("messages", []))})
                detail_markdown = (
                    response.content if isinstance(response.content, str) else str(response.content)
                ).strip()
                detail_markdown = strip_markdown_code_fences(detail_markdown)
                is_done = True
            except Exception as e:
                print(f"Attemp {try_count}: {e}")
        print(detail_markdown, flush=True)
        return {
            "selected_concept_name": best_title,
            "selected_concept_details": detail_markdown,
            "selected_concept_evaluation": selected_evaluation_json,
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

    system_content = f"""
You are a Lead Conceptual Process Engineer. Your job is to translate a winning design concept into a detailed technical brief that will serve as the design basis for downstream engineering disciplines (e.g., detailed design, safety, instrumentation).

**Context:**

  * You will be provided with the `SELECTED CONCEPT EVALUATION` (which includes the original concept definition, critiques, and feasibility score) plus the overarching `PROJECT REQUIREMENTS`.
  * Your task is to synthesize this information into a comprehensive engineering document.
  * The audience for this document is the project team who will execute the front-end engineering design (FEED). Clarity and actionable detail are crucial.

**Instructions:**

  * **Synthesize Inputs:** Thoroughly review the `SELECTED CONCEPT` and `PROJECT REQUIREMENTS` to create a cohesive design narrative.
  * **Develop Process Narrative:** Write 2-3 paragraphs describing the end-to-end process flow, from feed preparation to final product handling, including key transformations and utility interactions.
  * **Detail Major Equipment:** Create a table listing the primary equipment items, their specific function, and critical operational notes (e.g., material constraints, control targets).
  * **Define Operating Envelope:** Specify the key design parameters like capacity, pressure, and temperature ranges. Note any special utilities required.
  * **Identify Risks & Safeguards:** List the most significant process risks and propose concrete, specific safeguards or mitigation strategies for each.
  * **Acknowledge Gaps:** Explicitly list any critical information that is still needed or assumptions you had to make to complete the brief. Use `TBD` (To Be Determined) where data is unavailable.
  * **Format Adherence:** Your final output must be a PURE Markdown document. Do not wrap it in code blocks or add any text outside the specified template.

-----

**Example:**

  * **PROJECT REQUIREMENTS:**

    ```
    "Design a system to cool 10,000 kg/h of 95 wt% ethanol from 80°C to 40°C. The system must be a modular skid to minimize site installation time. Reliability is a key driver, and the system must integrate with the existing plant cooling water utility and nitrogen blanketing system for the storage tanks."
    ```

  * **SELECTED CONCEPT EVALUATION (JSON):**

    ```json
    {{
      "name": "Ethanol Cooler Module",
      "maturity": "innovative",
      "description": "A compact plate-and-frame heat exchanger skid cools ethanol using plant cooling water with modular plates enabling rapid maintenance.",
      "unit_operations": [
          "Feed/product pumps",
          "Plate-and-frame heat exchanger",
          "Isolation & bypass valves"
      ],
      "key_benefits": [
          "Higher overall heat-transfer coefficients reduce required surface area.",
          "Modular architecture supports rapid cleaning and capacity turndown."
      ]
      "summary": "Modular plate-and-frame skid offers compact footprint with manageable fouling risk.",
      "feasibility_score": 8,
      "risks": {{
        "technical": "Plate fouling and gasket degradation may erode efficiency over time.",
        "economic": "Custom skid fabrication has higher CAPEX than an in-place exchanger.",
        "safety_operational": "Requires careful isolation procedures when opening plates for cleaning."
      }},
      "recommendations": [
        "Include bypass headers and spare plate packs for rapid swap-outs.",
        "Specify corrosion-resistant gasket materials rated for ethanol service.",
        "Develop cleaning-in-place (CIP) protocol with instrumentation to monitor differential pressure buildup."
      ],
    }}
    ```

  * **Response:**

    ```markdown
    ## Concept Summary
    - Name: Ethanol Cooler Module
    - Intent: Reduce hot ethanol temperature ahead of storage using a compact exchanger skid
    - Feasibility Score (from review): 8

    ## Process Narrative
    Hot ethanol at 95 wt% exits the upstream blending unit at 80°C and approximately 1.5 barg. The stream is routed via dedicated piping to the new cooler module skid. On the skid, it flows through a shell-and-tube heat exchanger where plant cooling water on the tube side absorbs the sensible heat, bringing the ethanol's temperature down to the target of 40°C before it is sent to storage.

    Cooling water enters the exchanger at a design temperature of 25°C from the main utility header and is expected to leave at roughly 35°C. The cooled ethanol product then flows off-skid to the existing atmospheric storage tank T-201. The warmed cooling water is returned to the plant's utility loop.

    ## Major Equipment & Roles
    | Equipment | Function | Critical Operating Notes |
    |---|---|---|
    | E-101 Shell-and-Tube Exchanger | Remove sensible heat from the ethanol stream using cooling water. | Must maintain a minimum 5°C approach temperature. Monitor tube bundle for fouling. |
    | P-101A/B Ethanol Pumps | Transfer ethanol from the upstream unit through the cooler to storage. | Centrifugal pumps in a duty/standby configuration for reliability. |
    | T-201 Storage Tank (Existing) | Provide buffer storage for cooled ethanol product. | Must be connected to the nitrogen blanketing system to prevent oxygen ingress. |

    ## Operating Envelope
    - Design capacity: 10,000 kg/h ethanol (continuous basis)
    - Key pressure levels: Process inlet at 1.5 barg, outlet to tank at ~1.3 barg.
    - Key temperature levels: Ethanol inlet at 80°C, outlet at 40°C. Cooling water inlet at 25°C, outlet at ~35°C.
    - Special utilities / additives: Treated plant cooling water with standard corrosion inhibitor package.

    ## Risks & Safeguards
    - Cooling water interruption leads to high temp ethanol in tank — Install dual supply pumps with automatic switchover on low pressure. Add high-temp alarm on exchanger outlet.
    - Tube leak causing cross-contamination — Implement differential pressure monitoring between shell and tube sides. Install quick-acting isolation valves on inlet/outlet lines.
    - Over-pressurization of exchanger — Install thermal relief valve on the shell (ethanol) side.

    ## Data Gaps & Assumptions
    - Assumed ethanol specific heat is 2.5 kJ/kg-K; this must be verified based on the actual stream composition.
    - Cooling water supply pressure and fouling factor limits are pending review of the utility documentation.
    - Piping and instrumentation diagram (P&ID) for the existing T-201 tie-in point is required.
    ```

-----

**Your Task:** Output ONLY a valid Markdown document, **not in code block**. Your response must be a single, complete design brief for the `SELECTED CONCEPT`, following the structure and rules defined above.
"""

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
