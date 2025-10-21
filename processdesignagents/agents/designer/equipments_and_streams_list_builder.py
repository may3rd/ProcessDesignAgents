import json

from langchain_core.messages import AIMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from dotenv import load_dotenv

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import jinja_raw
from processdesignagents.agents.utils.equipment_stream_markdown import (
    equipments_and_streams_dict_to_markdown,
)

load_dotenv()

def create_equipments_and_streams_list_builder(llm):
    def equipments_and_streams_list_builder(state: DesignState) -> DesignState:
        """Equipments and Streams List Builder: Produces a JSON stream inventory template for process streams."""
        print("\n# Create Equipments and Streams List Template", flush=True)
        llm.temperature = 0
        basic_pfd_markdown = state.get("basic_pfd", "")
        design_basis_markdown = state.get("design_basis", "")
        requirements_markdown = state.get("requirements", "")
        concept_details_markdown = state.get("selected_concept_details", "")
        base_prompt = equipments_and_streams_list_prompt(
            basic_pfd_markdown,
            design_basis_markdown,
            requirements_markdown,
            concept_details_markdown,
        )
        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | llm.with_structured_output(method="json_mode")
        is_done = False
        try_count = 0
        while not is_done:
            try_count += 1
            if try_count > 10:
                print("+ Maximum try is reach.")
                exit(-1)
            try:
                response_dict = chain.invoke({"messages": list(state.get("messages", []))})
                cleaned_response_content = json.dumps(response_dict, ensure_ascii=False)
                is_done = True
            except Exception as e:
                print(f"Attempt {try_count} failed.")
        combined_md, equipment_md, streams_md = equipments_and_streams_dict_to_markdown(response_dict)
        if combined_md:
            print(combined_md, flush=True)
        ai_message = AIMessage(content=cleaned_response_content)
        updated_messages = list(state.get("messages", [])) + [ai_message]
        return {
            "equipment_and_stream_list": cleaned_response_content,
            "messages": updated_messages,
        }
    return equipments_and_streams_list_builder


def equipments_and_streams_list_prompt(
    basic_pfd_markdown: str,
    design_basis_markdown: str,
    requirements_markdown: str,
    concept_details_markdown: str,
) -> ChatPromptTemplate:
    system_content = f"""
You are a **Process Data Engineer** responsible for establishing the foundational major equipment and stream data for a new project as it moves from conceptual design to process simulation.

**Context:**

    * You are provided with the approved conceptual design documents (PFD, Design Basis, Requirements).
    * Your task is to create the canonical equipmest and stream list template as a structured JSON payload. This document is critical as it serves as the single source of truth for downstream teams who will perform detailed simulations, size equipment, and verify the process flow paths.
    * You have to focus on the connectivity and continuty of streams. The actual value of properties is not important, it will be handled by downstream agents.
    * Every process, utility, recycle, bypass, and vent stream must be captured to ensure a complete and accurate basis for the next project phase.

**Instructions:**

    * **Synthesize Inputs:** Review the provided `DESIGN_DOCUMENTS` to identify and extract every stream mentioned or implied by the process flow.
    * **Assign IDs:** Preserve any existing equipment and stream identifiers. For streams without an ID, assign a new sequential number (e.g., E-110, E-120 for equipment). For streams without an ID, assign a new sequential number (e.g., 1001, 1002 for process; 2001, 2002 for utilities).
    * **Build JSON Structure:** Return a single JSON object with the following schema:
    - Top-level keys: `"equipments"`, and `"streams"`.
    - Each entry in `equipments` must iclude:
        * `"id"`, `"name"`, `"description"`, `"service"`, `"type"`.
        * `"streams_in"`, `"stream_out"`: the list of stream id that connected to this equipment.
        * `"design_criteria"`: the information for equipment sizing, i.e. heat duty for heat exchanger, volume or hold up time for vessel.
        * `"sizing_parameters"`: a placeholder for sizing tool or agents.
        * `"notes"`: brief text capturing unique considerations for that equipment.
    - Each entry in `"streams"` must include:
        * `"id"`, `"name"`, `"description"`, `"from"`, `"to"`, `"phase"`.
        * `"properties"`: an object keyed by the same identifiers used in `"property_order"` with string values (include units using `000` placeholders where unknown, e.g., `{{"value": 000, "unit": "kg/h"}}`).
        * `"components"`: an object mapping unique component names defined in the design basis to their fraction value (placeholders [null or 000] allowed). **Prefer: molar fraction**
        * `"notes"`: brief text capturing unique considerations for that stream.
    * **Use Placeholders:** For numeric data that requires later calculation, use the `000` format and include the units inside the placeholder. For known design values, record the number directly.
    * You **MUST** following the template strictly. No a little bit deviate, it will lead to failure.
    * **Output Discipline:** Respond with a single valid JSON object using double quotes and UTF-8 safe characters. Do NOT wrap the response in Markdown, code fences, or provide commentary.
      * **Equipment List:** You MUST list only equipment in PFD description, not add new equipment.

-----

**Example:**

  * **DESIGN DOCUMENTS:**

    ```
    "A heat exchanger (E-101) cools 10,000 kg/h of 95 mol% ethanol from 80°C to 40°C. It is fed from an upstream blender and pumped to storage. Plant cooling water is used, entering at 25°C and returning to the header at 35°C."
    ```

  * **Response:**

    {{
        "equipments": [
            {{
                "id": "E-101",
                "name": "Ethanol Cooler",
                "service": "Reduce hot ethanol temperature prior to storage.",
                "type": "Shell-and-tube exchanger",
                "streams_in": ["1001, 2001"],
                "streams_out": ["1002, 2002"],
                "design_criteria": "<0.28 MW>",
                "sizing_parameters": [
                    {{
                        "name": "Area",
                        "quantity": {{"value": 120.0, "unit": "m²"}}
                    }},
                    {{
                        "name": "lmtd",
                        "quantity": {{"value": 40.0, "unit": "°C"}}
                    }},
                    {{
                        "name": "U-value",
                        "quantity": {{"value": 450.0, "unit": "W/m²-K"}}
                    }}
                ],
                "notes": "Design for a minimum 5°C approach temperature. Ensure sufficient space for bundle pull during maintenance."
            }}
        ],
      "streams": [
        {{
          "id": "1001",
          "name": "Hot Ethanol Feed",
          "description": "Feed entering exchanger E-101 shell side",
          "from": "Upstream Blender",
          "to": "E-101",
          "phase": "Liquid",
          "properties": {{
            "mass_flow": {{"value": 10000, "unit": "kg/h"}},
            "temperature": {{"value": 80, "unit": "°C"}},
            "pressure": {{"value": 1.7, "unit": "barg"}}
          }},
          "compositions": {{
            "Ethanol (C2H8O)": {{"value": 0.95, "unit": "molar fraction"}},
            "Water (H2O)": {{"value": 0.05, "unit": "molar fraction"}}
          }},
          "notes": "Tie-in from upstream blender."
        }},
        {{
          "id": "1002",
          "name": "Ethanol Cooler Return",
          "description": "Feed from exchanger E-101 shell side",
          "from": "E-101",
          "to": "Downstream Storage",
          "phase": "Liquid",
          "properties": {{
            "mass_flow": {{"value": 10000, "unit": "kg/h"}},
            "temperature": {{"value": 40, "unit": "°C"}},
            "pressure": {{"value": 1.0, "unit": "barg"}}
          }},
          "compositions": {{
            "Ethanol (C2H8O)": {{"value": 0.95, "unit": "molar fraction"}},
            "Water (H2O)": {{"value": 0.05, "unit": "molar fraction"}}
          }},
          "notes": "Cool feed to storage."
        }},
        {{
          "id": "2001",
          "name": "Cooling Water Supply",
          "description": "Utility water to exchanger tubes",
          "from": "Cooling Water Header",
          "to": "E-101",
          "phase": "Liquid",
          "properties": {{
            "mass_flow": {{"value": 24000, "unit": "kg/h"}},
            "temperature": {{"value": 25, "unit": "°C"}},
            "pressure": {{"value": 2.5, "unit": "barg"}}
          }},
          "compositions": {{
            "Water (H2O)": {{"value": 1.00, "unit": "molar fraction"}}
          }},
          "notes": "Return stream 2002 closes utility loop."
        }},
        {{
          "id": "2002",
          "name": "Cooling Water Return",
          "description": "Utility water from exchanger tubes",
          "from": "E-101",
          "to": "Cooling Water Return Header",
          "phase": "Liquid",
          "properties": {{
            "mass_flow": {{"value": 24000, "unit": "kg/h"}},
            "temperature": {{"value": 35, "unit": "°C"}},
            "pressure": {{"value": 1.8, "unit": "barg"}}
          }},
          "compositions": {{
            "Water (H2O)": {{"value": 1.00, "unit": "molar fraction"}}
          }},
          "notes": "Return stream 2002 closes utility loop."
        }}
      ],
      "notes and assumptions": [
          "The following critical information must be resolved during the Front-End Engineering Design (FEED) phase:",
          "1.  **Cooling Utility Definition:** The type, temperature profile (inlet/outlet), and available pressure of the cooling medium are **TBD**. This is the single most important factor for sizing E-101.",
          "2.  **Process Pressure:** The operating pressure of the 100°C ethanol stream is **TBD**. This defines the required design pressure rating for the exchanger shell and tubes.",
          "3.  **Specific Heat (Cp):** The specific heat capacity for 99.5 mol% ethanol at 100°C is assumed for the preliminary duty calculation (Q ≈ 100 kW). This must be verified using thermodynamic property data specific to the final composition."
      ]
    }}

-----

**Ensure that all `"value"` is float, not text.**

**Your Task:** Based on the provided `DESIGN_DOCUMENTS`, generate ONLY the JSON object described above. Do not include code fences or additional narrative.
"""

    human_content = f"""
# DATA FOR ANALYSIS
---
**Basic PFD Description (Markdown):**
{basic_pfd_markdown}

**Design Basis (Markdown):**
{design_basis_markdown}

**Requirements Summary (Markdown):**
{requirements_markdown}

**Concept Details (Markdown):**
{concept_details_markdown}

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
