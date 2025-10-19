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


def create_equipment_sizing_agent(llm):
    def equipment_sizing_agent(state: DesignState) -> DesignState:
        """Equipment Sizing Agent: populates the equipment table using tool-assisted estimates."""
        print("\n# Equipment Sizing", flush=True)
        llm.temperature = 0.7
        design_basis_markdown = state.get("design_basis", "")
        basic_pfd_markdown = state.get("basic_pfd", "")
        equipment_and_stream_list = state.get("equipment_and_stream_list", "")
        base_prompt = equipment_sizing_prompt(
            design_basis_markdown,
            basic_pfd_markdown,
            equipment_and_stream_list,
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
            equipment_list_result = {"equipments": payload.get("equipments")}
        except Exception as e:
            raise ValueError(f"{e}")
        _, markdown_tables, _ = convert_to_markdown(response)
        print(markdown_tables, flush=True)
        return {
            "equipment_and_stream_list": response.model_dump_json(),
            "equipment_list_results": json.dumps(equipment_list_result),
            "messages": [AIMessage(content=output_json)],
        }

    return equipment_sizing_agent


def equipment_sizing_prompt(
    design_basis_markdown: str,
    basic_pfd_markdown: str,
    equipment_and_stream_list_json: str,
) -> ChatPromptTemplate:
    system_content = f"""
You are a **Lead Equipment Sizing Engineer** responsible for performing first-pass sizing calculations for a conceptual process design.

**Context:**

  * You are provided with a preliminary `EQUIPMESTS_AND_STREAMS_LIST` (containing placeholders), the overall `DESIGN_BASIS`, and the `BASIC_PROCESS_FLOW_DIAGRAM`.
  * The project is transitioning from conceptual to preliminary engineering. Your task is to provide the first set of quantitative estimates for major equipment, a critical step for enabling cost estimation, detailed design, and risk assessment.

**Instructions:**

    * **Analyze Inputs:** Thoroughly review the `EQUIPMESTS_AND_STREAMS_LIST`, `DESIGN_BASIS`, and `BASIC_PROCESS_FLOW_DIAGRAM` to understand the service, connectivity, and performance requirements for each equipment item.
    * **Perform Sizing Calculations:** For each piece of equipment, perform preliminary sizing calculations. For examples:
        * **heat exchangers:** calculate the required heat transfer duty, LMTD, and required area,
        * **pumps:** calculate the required flow, head, and ydraulic power.
        * **pressurized vessels:** calculate hold up time, required volume, diameter, length or hegiht.
        * **column:** calculate diameter, number of trays, height.
        * **etc.**
    * **Populate the JSON:** Replace every placeholder in the `EQUIPMESTS_AND_STREAMS_LIST` with your calculated numeric estimate (including units). If a value cannot be reasonably estimated, use the value _null_.
    * **Document Methods and Assumptions:** In the `notes` field for each item, concisely state the calculation method or key assumption (e.g., "Sized using LMTD method," "Power based on 75% efficiency"). Add any new global assumptions to the `metadata.assumptions` list.
    * **Format Adherence:** Your final output must be a single, PURE JSON object matching the provided schema. Do not wrap the JSON in code fences or add any commentary outside of the JSON object itself.

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
      ]
    }}

-----

**Your Task:** Based on the provided `DESIGN_DOCUMENTS`, generate ONLY the JSON object described above. Do not include code fences or additional narrative.
"""

    human_content = f"""
# DATA FOR ANALYSIS:
---
**Design Basis (Markdown):**
{design_basis_markdown}

**Basic Process Flow Diagram (Markdown):**
{basic_pfd_markdown}

**Equipment Template (JSON):**
{equipment_and_stream_list_json}

---

# **NEGATIVES:**

Your response MUST be a single, raw JSON object.
Do NOT add any conversational text, explanations, or markdown code blocks like ```json before or after the JSON output.
Your output must start with {{ and end with }}.

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
