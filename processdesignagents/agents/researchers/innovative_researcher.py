import json

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_core.messages import AIMessage

from dotenv import load_dotenv

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.agent_utils import (
    ConceptsList
)
from processdesignagents.agents.utils.prompt_utils import jinja_raw
from processdesignagents.agents.utils.json_tools import extract_first_json_document

load_dotenv()

def create_innovative_researcher(llm):
    def innovative_researcher(state: DesignState) -> DesignState:
        """Innovative Researcher: Proposes novel process concepts using LLM."""
        print("\n# Innovative Research Concepts", flush=True)

        requirements_summary = state.get("requirements", "")
        if not isinstance(requirements_summary, str):
            requirements_summary = str(requirements_summary)
        base_prompt = innovative_researcher_prompt(requirements_summary)
        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        
        # Create the LLM chain that will force the output to match Pydantic schema
        structured_llm = llm.with_structured_output(ConceptsList)
        chain = prompt | structured_llm
        
        is_done = False
        try_count = 0
        while not is_done:
            response = chain.invoke({"messages": list(state.get("messages", []))})
            # research_json = (
            #     response.content if isinstance(response.content, str) else str(response.content)
            # ).strip()
            
            # print(f"--- Output ---\n{response.model_dump_json(indent=2)}", flush=True)
            research_json = response.model_dump_json(indent=2)
            is_done = len(research_json) > 100
            try_count += 1
            if not is_done:
                print("- False to create more concepts. Try again.", flush=True)
                print(response, flush=True)
                if try_count > 10:
                    print("+ Max try count reached.", flush=True)
                    exit(-1)

        research_markdown = convert_concepts_json_to_markdown(research_json)
        print(research_markdown, flush=True)
        return {
            "research_concepts": research_json,
            "messages": [AIMessage(content=research_json)],
        }

    return innovative_researcher


def convert_concepts_json_to_markdown(concepts_json: str) -> str:
    """Convert structured JSON concept output into a readable Markdown summary."""
    sanitized_json, payload = extract_first_json_document(concepts_json)
    if payload is None:
        return sanitized_json

    concepts = payload if isinstance(payload, list) else payload.get("concepts")
    if not isinstance(concepts, list):
        return sanitized_json

    lines: list[str] = []
    concept_counter = 0
    for concept in concepts:
        if not isinstance(concept, dict):
            continue

        concept_counter += 1
        name = concept.get("name", "Untitled Concept")
        maturity = concept.get("maturity")
        description = concept.get("description")
        unit_operations = concept.get("unit_operations") or []
        key_benefits = concept.get("key_benefits") or []

        lines.append("---")
        lines.append(f"## Concept {concept_counter}. {name}")
        if isinstance(maturity, str) and maturity:
            normalized_maturity = maturity.replace("_", " ").title()
            lines.append(f"**Maturity:** {normalized_maturity}")
        if isinstance(description, str) and description:
            lines.append(f"**Description:** {description}")

        if isinstance(unit_operations, list) and unit_operations:
            lines.append("**Unit Operations:**")
            for unit in unit_operations:
                lines.append(f"- {unit}")

        if isinstance(key_benefits, list) and key_benefits:
            lines.append("**Key Benefits:**")
            for benefit in key_benefits:
                lines.append(f"- {benefit}")

    if not lines:
        return sanitized_json

    return "\n".join(lines)


def innovative_researcher_prompt(requirements_markdown: str) -> ChatPromptTemplate:
    system_content = f"""
You are a Senior R&D Process Engineer specializing in conceptual design and process innovation. Your expertise lies in brainstorming novel, sustainable, and efficient chemical processes to solve a given problem.

**Context:**

  * You will be provided with a set of `REQUIREMENTS` for a new or modified chemical process.
  * Your task is to generate multiple distinct process concepts that fulfill these requirements.
  * The concepts you generate will be evaluated by a critique agent to determine the most feasible option for further design.
  * The concepts must span a range of technological maturity, including conventional industry standards, innovative improvements, and state-of-the-art approaches.

**Instructions:**

  * Analyze the provided `REQUIREMENTS` to fully understand the core objective, key components, and constraints.
  * Generate between 3 and 6 distinct process concepts that meet the requirements.
  * For each concept provide a descriptive name, a concise paragraph explaining the idea, a maturity classification, plus lists of essential unit operations and key benefits.
  * Ensure the range of concepts includes at least one conventional/standard process, one innovative/complex process, and one state-of-the-art process.
  * Respond with a single valid JSON object using double quotes and UTF-8 safe characters. Do not include Markdown, comments, code fences, or explanatory prose.
  * The JSON must contain a top-level key `"concepts"` whose value is a list of objects. Each concept object MUST include the keys: `"name"` (string), `"maturity"` (one of `"conventional"`, `"innovative"`, `"state_of_the_art"`), `"description"` (string), `"unit_operations"` (list of strings), and `"key_benefits"` (list of strings).
  * Ensure at least one concept is marked `"maturity": "conventional"`, one `"innovative"`, and one `"state_of_the_art"`.

-----

  * **REQUIREMENTS:**
    ```
    {{requirements}}
    ```

-----

**Example:**

  * **REQUIREMENTS:**

    ```
    "We need a process to cool a hot ethanol stream from 80°C to 40°C. The primary cooling utility available is the plant's standard cooling water loop."
    ```

  * **Response:**

    {{
      "concepts": [
        {{
          "name": "Shell-and-Tube Ethanol Cooler",
          "maturity": "conventional",
          "description": "A standard shell-and-tube heat exchanger cools the hot ethanol stream from 80°C to 40°C using the existing cooling water loop, offering the most common industry approach.",
          "unit_operations": [
            "Feed/Product Pumps",
            "Shell-and-Tube Heat Exchanger"
          ],
          "key_benefits": [
            "Proven, reliable technology with low operational and capital cost.",
            "Simple to design, operate, and maintain with readily available parts."
          ]
        }},
        {{
          "name": "Plate-and-Frame Modular Cooler",
          "maturity": "innovative",
          "description": "A compact plate-and-frame exchanger on a modular skid delivers higher thermal efficiency and allows staged plates for optimized heat transfer with rapid maintenance turnaround.",
          "unit_operations": [
            "Modular Plate-and-Frame Exchanger",
            "Bypass and Isolation Valving"
          ],
          "key_benefits": [
            "Higher heat-transfer coefficients reduce required surface area and footprint.",
            "Modular plates can be added or cleaned offline, minimizing downtime."
          ]
        }},
        {{
          "name": "Heat Pump Assisted Cooling",
          "maturity": "state_of_the_art",
          "description": "A vapor-compression heat pump recovers low-grade heat from the ethanol stream, enabling sub-ambient cooling and decoupling the process from cooling water limitations.",
          "unit_operations": [
            "Heat Pump Evaporator/Condenser",
            "Chilled-Water Loop Heat Exchanger",
            "Cooling Tower Interface"
          ],
          "key_benefits": [
            "Achieves product temperatures below the cooling water temperature.",
            "Reduces load on the main cooling tower during peak conditions."
          ]
        }}
      ]
    }}

-----

**Your Task:** Output ONLY a valid JSON object matching the schema described above. Do not wrap the JSON in a code block. Do not add any comment text.
"""

    human_content = f"""
# DATA FOR ANALYSIS:
---
**REQUIREMENTS:**
{requirements_markdown}

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
