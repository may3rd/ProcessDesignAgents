from __future__ import annotations

from langchain_core.messages import AIMessage
import json

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from dotenv import load_dotenv

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.agent_utils import (
    EquipmentsAndStreamsListBuilder,
    convert_to_markdown,
)
from processdesignagents.agents.utils.prompt_utils import jinja_raw

load_dotenv()


def create_stream_data_estimator(llm):
    def stream_data_estimator(state: DesignState) -> DesignState:
        """Stream Data Estimator: Generates JSON stream data with reconciled estimates."""
        print("\n# Stream Data Estimator", flush=True)

        llm.temperature = 0.7
        
        basic_pfd_markdown = state.get("basic_pfd", "")
        design_basis_markdown = state.get("design_basis", "")
        equipments_and_streams_template = state.get("equipments_and_streams_template", "")
        base_prompt = stream_data_estimator_prompt(
            basic_pfd_markdown,
            design_basis_markdown,
            equipments_and_streams_template,
        )
        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | llm.with_structured_output(EquipmentsAndStreamsListBuilder)
        is_done = False
        try_count = 0
        while not is_done:
            try_count += 1
            if try_count > 10:
                print("+ Maximum try is reach.")
                exit(-1)
            try:
                response = chain.invoke({"messages": list(state.get("messages", []))})
                output_json = response.model_dump_json(indent=2)
                is_done = len(output_json) > 100
            except Exception as e:
                print(f"Attempt {try_count} failed: Parsing error - {e}")
        try:
            payload = json.loads(output_json)
            stream_list_result = {"streams": payload.get("streams")}
        except Exception as e:
            raise ValueError(f"{e}")
        _, _, markdown_tables = convert_to_markdown(response)
        print(markdown_tables, flush=True)
        return {
            "equipment_and_stream_list": response.model_dump_json(),
            "stream_list_results": json.dumps(stream_list_result),
            "messages": [AIMessage(content=output_json)],
        }

    return stream_data_estimator


def stream_data_estimator_prompt(
    basic_pfd_markdown: str,
    design_basis_markdown: str,
    equipments_and_streams_template: str,
) -> ChatPromptTemplate:
    system_content = f"""
You are a **Senior Process Simulation Engineer** specializing in developing first-pass heat and material balances for conceptual designs.

**Context:**

  * You are provided with a `EQUIPMENTS_STREAMS_TEMPLATE` JSON document containing placeholder stream information, along with supporting `DESIGN_DOCUMENTS` (concept summary, requirements, design basis).
  * Your task is to populate the template with realistic, reconciled operating conditions and document key assumptions for each streams as much as you can.
  * Leave Equipments section untouched. It will be done by downstream agents.
  * The resulting JSON becomes the authoritative dataset for downstream equipment sizing, detailed simulation, and cost estimation.

**Instructions:**

  * **Analyze Inputs:** Review the `EQUIPMENTS_STREAMS_TEMPLATE` and all supporting `DESIGN_DOCUMENTS` to understand unit operations, performance targets, and constraints.
  * **Perform Balances:** Replace every operating conditions and composisitions of each stream with a best-estimate numeric string. UOM of each value can be changed if needed. Ensure mass and component balances are conserved for each unit and overall.
  * **Work sequence:** Start by focusing on the main feed to product first, then working in the utilities (if any).
  * **Ensure Completeness:** Check that component fractions per stream sum to 100% on the stated basis. Populate `"notes"` for each stream with context or safeguards that support the estimates.
  * **Compositions:** Ensure that the mass fraction and molar fraction is consistent, means that the value of the molar fraction and mass fraction usually not the same but it is calculated based on MW of each components and calculate mass fraction from molar fraction if both existed. Put 0.0000 for the components that not presenting in stream. **Ensure that the summation of mass fraction and summation of molar fraction is 100.0% for all streams.**
  * **Output Discipline:** Respond with a single valid JSON object using double quotes and UTF-8 safe characters. Do NOT wrap the response in Markdown, code fences, or provide commentary.
  * **Equipment List:** Leave `EQUIPMENT` section untouched. It will be done by downstream agents.

-----

**Example:**

  * **DESIGN DOCUMENTS:**

    ```
    "A shell-and-tube heat exchanger (E-101) cools 10,000 kg/h of 93 mol% ethanol from 80°C to 40°C. Plant cooling water is used, entering at 25°C. Assume Cp of ethanol stream is 2.5 kJ/kg-K and water is 4.18 kJ/kg-K."
    ```

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
      ]
    }}

-----

**Your Task:** Based on the provided `DESIGN_DOCUMENTS`, generate ONLY the JSON object described above. Do not include code fences or additional narrative.
"""

    human_content = f"""

# REFERENCE MATERIAL
---
**Design Basis (Markdown):**
{design_basis_markdown}

**Basic Process Flow Diagram (Markdown):**
{basic_pfd_markdown}

# EQUIPMENTS AND STREAMS TEMPLATE (JSON)
{equipments_and_streams_template}

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
