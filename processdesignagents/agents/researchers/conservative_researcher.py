from __future__ import annotations

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from dotenv import load_dotenv

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import jinja_raw
from processdesignagents.agents.utils.json_tools import (
    extract_first_json_document,
    convert_evaluations_json_to_markdown,
)

load_dotenv()


def create_conservative_researcher(llm):
    def conservative_researcher(state: DesignState) -> DesignState:
        """Conservative Researcher: Critiques concepts for practicality using LLM."""
        print("\n# Conservatively Critiqued Concepts", flush=True)

        concepts_json_raw = state.get("research_concepts", "")
        requirements_markdown = state.get("requirements", "")
        if not isinstance(concepts_json_raw, str):
            concepts_json_raw = str(concepts_json_raw)
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)

        sanitized_concepts_json, concept_payload = extract_first_json_document(concepts_json_raw)
        if concept_payload is None:
            raise ValueError("Conservative researcher expected valid JSON concepts from innovative researcher.")

        base_prompt = conservative_researcher_prompt(sanitized_concepts_json, requirements_markdown)

        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | llm
        
        is_done = False
        try_count = 0
        while not is_done:
            response = chain.invoke({"messages": list(state.get("messages", []))})
            critique_raw = (
                response.content if isinstance(response.content, str) else str(response.content)
            ).strip()
            sanitized_output, evaluation_payload = extract_first_json_document(critique_raw)
            has_evaluations = False
            if isinstance(evaluation_payload, dict):
                evaluations = evaluation_payload.get("evaluations")
                has_evaluations = isinstance(evaluations, list) and len(evaluations) > 0
            is_done = has_evaluations
            try_count += 1
            if not is_done:
                print("- False to critique concepts. Try again.", flush=True)
                print(critique_raw, flush=True)
                if try_count > 10:
                    print("+ Max try count reached.", flush=True)
                    exit(-1)

        critique_markdown = convert_evaluations_json_to_markdown(sanitized_output)
        print(critique_markdown, flush=True)
        return {
            "research_concepts": sanitized_output,
            "innovative_concepts": sanitized_concepts_json,
            "messages": [response],
        }

    return conservative_researcher


def conservative_researcher_prompt(
    concepts_json: str,
    requirements_markdown: str,
) -> ChatPromptTemplate:
    system_content = f"""
You are a Principal Technology Analyst at a top-tier venture capital firm. Your job is to conduct rigorous due diligence on innovative process technologies to assess their investment potential. You are an expert in evaluating technical feasibility, market viability, and operational risk.

**Context:**

  * You will be provided with a set of `REQUIREMENTS / CONSTRAINTS` (as Markdown) and a structured JSON list of `PROCESS CONCEPTS`.
  * Your task is to act as a critique agent, rigorously evaluating each concept against the given requirements to determine its viability.
  * Your analysis must be returned as a single valid JSON object—no Markdown, commentary, or code fences.

**Instructions:**

  * **Analyze Inputs:** Thoroughly review the `REQUIREMENTS / CONSTRAINTS` and the source `CONCEPTS` to understand performance targets, boundary conditions, and any absolute constraints.
  * **Evaluate Each Concept:** For each concept provided, perform the following analysis:
      * **Stress-Test Claims:** Evaluate the concept's viability against conservative engineering and economic assumptions. Highlight technology maturity limits, scale-up hurdles, and hidden cost drivers.
      * **Identify Risks:** Provide at least three distinct risk entries encompassing **Technical**, **Economic**, and **Safety/Operational** themes. You may add more if warranted.
      * **Assign Score:** Based on your analysis, assign a single integer **feasibility_score** from 1 (very high risk, not viable) to 10 (low risk, ready for near-term deployment).
      * **Provide Recommendations:** Formulate clear, actionable recommendations that directly mitigate the highlighted risks or outline essential next steps for validation (e.g., pilot programs, vendor vetting).
  * **Output Schema:**
      * Respond with a JSON object containing a top-level key `"evaluations"` holding a list with one element per concept.
      * Each element must include:
          * `"name"`: the concept name (string).
          * `"maturity"`: the maturity label copied from the concept (string).
          * `"summary"`: a concise synopsis of the evaluation (string).
          * `"feasibility_score"`: an integer from 1–10.
          * `"risks"`: an object with the keys `"technical"`, `"economic"`, `"safety_operational"` (strings describing the top risks). Additional keys may be added for other risk themes.
          * `"recommendations"`: a list of actionable recommendation strings (minimum of three).
          * `"concept"`: an object echoing the original concept fields (`"name"`, `"maturity"`, `"description"`, `"unit_operations"`, `"key_benefits"`) so downstream agents have full context.
  * **Validation Rules:**
      * Include an evaluation for every concept provided—no more, no less.
      * Use double quotes and UTF-8 safe characters. No comments, Markdown, or trailing prose.

-----

  * **REQUIREMENTS / CONSTRAINTS:**
    ```
    {{requirements}}
    ```
  * **PROCESS CONCEPTS (JSON):**
    ```json
    {{concepts}}
    ```

-----

**Example:**

  * **REQUIREMENTS / CONSTRAINTS:**

    ```
    - Objective: Cool an ethanol stream.
    - Utility Constraint: Must use the existing plant cooling water loop.
    - Key Drivers: Minimize operational risk and long-term utility costs. Avoid introducing new hazardous failure modes.
    ```

  * **PROCESS CONCEPTS (JSON):**

    ```json
    {{
      "concepts": [
        {{
          "name": "Ethanol Cooling Exchanger Skid",
          "maturity": "conventional",
          "description": "Standard shell-and-tube exchanger cools hot ethanol using the existing cooling water loop.",
          "unit_operations": [
            "Feed/product pumps",
            "Shell-and-tube heat exchanger"
          ],
          "key_benefits": [
            "Proven design with low execution risk",
            "Minimal footprint and easy maintenance"
          ]
        }}
      ]
    }}
    ```

  * **Response:**

    ```json
    {{
      "evaluations": [
        {{
          "name": "Ethanol Cooling Exchanger Skid",
          "maturity": "conventional",
          "summary": "Robust baseline option with manageable fouling risk and moderate utility demand.",
          "feasibility_score": 7,
          "risks": {{
            "technical": "Potential fouling on the cooling water side could degrade heat-transfer performance over time.",
            "economic": "Higher-than-expected cooling water usage may exceed the allocated budget during peak summer operation.",
            "safety_operational": "Tube failure would mix ethanol with the cooling loop, creating a fire hazard at downstream equipment."
          }},
          "recommendations": [
            "Install differential-pressure monitoring and schedule periodic backflushing to manage fouling.",
            "Audit cooling water capacity and add contingency supply for summer peaks.",
            "Add hydrocarbon detectors and isolation valves on the cooling water return to mitigate leak scenarios."
          ],
          "concept": {{
            "name": "Ethanol Cooling Exchanger Skid",
            "maturity": "conventional",
            "description": "Standard shell-and-tube exchanger cools hot ethanol using the existing cooling water loop.",
            "unit_operations": [
              "Feed/product pumps",
              "Shell-and-tube heat exchanger"
            ],
            "key_benefits": [
              "Proven design with low execution risk",
              "Minimal footprint and easy maintenance"
            ]
          }}
        }}
      ]
    }}
    ```

-----

**Your Task:** Output ONLY the JSON object described above. Do not wrap it in a code block or add any commentary.
"""

    human_content = f"""
# DATA FOR ANALYSIS
---

**Requirements / Constraints (Markdown):**
{requirements_markdown}

**Concepts (JSON):**
{concepts_json}

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
