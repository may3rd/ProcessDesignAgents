from __future__ import annotations

import json

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
    convert_streams_json_to_markdown,
    convert_equipment_json_to_markdown,
    extract_first_json_document,
)

load_dotenv()


def create_equipment_sizing_agent(llm):
    def equipment_sizing_agent(state: DesignState) -> DesignState:
        """Equipment Sizing Agent: populates the equipment table using tool-assisted estimates."""
        print("\n# Equipment Sizing", flush=True)

        llm.temperature = 0.7

        requirements_markdown = state.get("requirements", "")
        design_basis_markdown = state.get("design_basis", "")
        basic_pfd_markdown = state.get("basic_pfd", "")
        stream_results_json = state.get("stream_list_results", "")
        stream_template = state.get("stream_list_template", "")
        equipment_table_template = state.get("equipment_list_template", "")

        if not equipment_table_template.strip():
            raise ValueError("Equipment template is missing. Run the equipment list builder before sizing.")

        sanitized_stream_json, stream_payload = extract_first_json_document(stream_template) if isinstance(stream_template, str) else ("", None)
        if stream_payload is None:
            raise ValueError("Equipment sizing agent requires stream template JSON from the list builder.")

        stream_json_formatted = json.dumps(stream_payload, ensure_ascii=False, indent=2)
        stream_table_markdown = convert_streams_json_to_markdown(sanitized_stream_json)

        sanitized_equipment_template, equipment_payload = extract_first_json_document(equipment_table_template)
        if equipment_payload is None:
            raise ValueError("Equipment sizing agent requires equipment template JSON from the list builder.")
        equipment_template_formatted = json.dumps(equipment_payload, ensure_ascii=False, indent=2)

        sanitized_hmb_json, hmb_payload = extract_first_json_document(stream_results_json) if isinstance(stream_results_json, str) else ("", None)
        if hmb_payload is None:
            raise ValueError("Equipment sizing agent requires stream results JSON from the estimator.")
        
        hmb_json_formatted = json.dumps(hmb_payload, ensure_ascii=False, indent=2)

        base_prompt = equipment_sizing_prompt(
            requirements_markdown,
            design_basis_markdown,
            basic_pfd_markdown,
            hmb_json_formatted,
            stream_json_formatted,
            stream_table_markdown,
            equipment_template_formatted,
        )

        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | llm

        is_done = False
        try_count = 0
        sanitized_output = ""
        response = None
        while not is_done:
            response = chain.invoke({"messages": list(state.get("messages", []))})
            raw_output = (
                response.content if isinstance(response.content, str) else str(response.content)
            ).strip()
            sanitized_output, payload = extract_first_json_document(raw_output)
            sized_entries = None
            if isinstance(payload, dict):
                sized_entries = payload.get("equipment")
            elif isinstance(payload, list):
                sized_entries = payload
            has_equipment = isinstance(sized_entries, list) and len(sized_entries) > 0
            is_done = bool(has_equipment)
            try_count += 1
            if not is_done:
                print("- Failed to generate sized equipment data. Retrying...", flush=True)
                if try_count > 10:
                    print("+ Max try count reached.", flush=True)
                    exit(-1)

        equipment_markdown = convert_equipment_json_to_markdown(sanitized_output)
        print(equipment_markdown, flush=True)
        return {
            "equipment_list_results": sanitized_output,
            "messages": [response] if response else [],
        }

    return equipment_sizing_agent


def equipment_sizing_prompt(
    requirements_markdown: str,
    design_basis_markdown: str,
    basic_pfd_markdown: str,
    basic_hmb_markdown: str,
    stream_data_json: str,
    stream_data_markdown: str,
    equipment_template_json: str,
) -> ChatPromptTemplate:
    system_content = f"""
You are a **Lead Equipment Sizing Engineer** responsible for performing first-pass sizing calculations for a conceptual process design.

**Context:**

  * You are provided with a preliminary `EQUIPMENT_TEMPLATE` (containing placeholders), a reconciled `STREAM_DATA` table, and the overall `DESIGN_BASIS`.
  * The project is transitioning from conceptual to preliminary engineering. Your task is to provide the first set of quantitative estimates for major equipment, a critical step for enabling cost estimation, detailed design, and risk assessment.

**Instructions:**

  * **Analyze Inputs:** Thoroughly review the `EQUIPMENT_TEMPLATE`, `STREAM_DATA`, and `DESIGN_BASIS` to understand the service, connectivity, and performance requirements for each equipment item.
  * **Perform Sizing Calculations:** For each piece of equipment, perform preliminary sizing calculations. For example, for heat exchangers, calculate the duty, LMTD, and required area; for pumps, calculate hydraulic power.
  * **Populate the JSON:** Replace every `<value>` placeholder in the `EQUIPMENT_TEMPLATE` with your calculated numeric estimate (including units). If a value cannot be reasonably estimated, use the string `"TBD"`.
  * **Document Methods and Assumptions:** In the `notes` field for each item, concisely state the calculation method or key assumption (e.g., "Sized using LMTD method," "Power based on 75% efficiency"). Add any new global assumptions to the `metadata.assumptions` list.
  * **Format Adherence:** Your final output must be a single, PURE JSON object matching the provided schema. Do not wrap the JSON in code fences or add any commentary outside of the JSON object itself.

-----

**Example:**

  * **DESIGN\_BASIS & STREAM\_DATA:**

    ```json
    {{
      "notes": "Ethanol stream (1001) at 10,000 kg/h cools from 80°C to 40°C. Cp is 2.5 kJ/kg-K. Cooling water (2001) enters at 25°C and leaves at 35°C. Pump P-101 provides 1.5 bar of head.",
      "streams_in": ["1001", "2001"],
      "streams_out": ["1002", "2002"]
    }}
    ```

  * **EQUIPMENT\_TEMPLATE:**

    ```json
    {{
      "metadata": {{
        "assumptions": ["Cooling water temperature rise is 10°C."]
      }},
      "equipment": [
        {{
          "id": "E-101",
          "name": "Ethanol Cooler",
          "type": "Shell-and-tube exchanger",
          "streams_in": ["1001", "2001"],
          "streams_out": ["1002", "2002"],
          "duty_or_load": "<value>",
          "sizing_parameters": ["Area: <value>", "U: <value>", "LMTD: <value>"],
          "notes": "<value>"
        }}
      ]
    }}
    ```

  * **Response:**

    ```json
    {{
      "metadata": {{
        "groups": [
          {{
            "name": "Heat Exchangers",
            "ids": [
              "E-101"
            ]
          }}
        ],
        "assumptions": [
          "Cooling water temperature rise is fixed at 10°C.",
          "Overall heat transfer coefficient (U) for shell-and-tube is assumed to be 450 W/m²-K for this service."
        ]
      }},
      "equipment": [
        {{
          "id": "E-101",
          "name": "Ethanol Cooler",
          "service": "Reduce ethanol temperature prior to storage.",
          "type": "Shell-and-tube exchanger",
          "streams_in": [
            "1001",
            "2001"
          ],
          "streams_out": [
            "1002",
            "2002"
          ],
          "duty_or_load": "0.278 MW",
          "sizing_parameters": [
            "Area: 24.7 m²",
            "U (Assumed): 450 W/m²-K",
            "LMTD (Counter-current): 25.6 °C"
          ],
          "notes": "Sized using LMTD method. Duty calculated from ethanol stream data. Area = Q / (U * LMTD)."
        }}
      ]
    }}
    ```

-----

**Your Task:** Based on the provided `DESIGN_BASIS`, `BASIC PROCESS FLOW DIAGRAM`, `STREAM_DATA`, and `EQUIPMENT_TEMPLATE`, generate ONLY the valid JSON object that precisely follows the structure and rules defined above. Do not include code fences or additional narrative.
"""

    human_content = f"""
# DATA FOR ANALYSIS:
---
**Design Basis (Markdown):**
{design_basis_markdown}

**Basic Process Flow Diagram (Markdown):**
{basic_pfd_markdown}

**Preliminary H&MB (Markdown Overview):**
{basic_hmb_markdown}

**Equipment Template (JSON):**
{equipment_template_json}

---

# EXAMPLE INPUT:
For a single exchanger that cools ethanol from 80 C to 40 C with cooling water, estimate the duty from the heat balance, size the heat transfer area using the `heat_exchanger_sizing` tool, and record cooling water inlet/outlet temperatures along with any approach temperature assumptions in the notes.

# EXPECTED JSON OUTPUT:
```
{{
  "metadata": {{
    "groups": [
      {{ "name": "Heat Exchangers", "ids": ["E-101"] }},
      {{ "name": "Pumps", "ids": ["P-101"] }}
    ],
    "assumptions": [
      "Cooling water rise fixed at 10°C.",
      "Pump efficiency assumed 75%."
    ]
  }},
  "equipment": [
    {{
      "id": "E-101",
      "name": "Ethanol Cooler",
      "service": "Reduce ethanol temperature",
      "type": "Shell-and-tube exchanger",
      "streams_in": ["1001", "2001"],
      "streams_out": ["1002", "2002"],
      "duty_or_load": "0.28 MW",
      "sizing_parameters": [
        "Area: 120 m2",
        "U: 450 W/m2-K",
        "LMTD: 25 °C"
      ],
      "notes": "Sized via heat_exchanger_sizing with 10% fouling allowance."
    }},
    {{
      "id": "P-101",
      "name": "Product Pump",
      "service": "Transfer cooled ethanol",
      "type": "Centrifugal pump",
      "streams_in": ["1002"],
      "streams_out": ["1003"],
      "duty_or_load": "45 kW",
      "sizing_parameters": [
        "Flow: 10,000 kg/h",
        "Head: 18 m",
        "Efficiency: 0.75"
      ],
      "notes": "pump_sizing(flow=10000 kg/h, head=18 m) -> brake power 42 kW, rounded to 45 kW with contingency."
    }}
  ]
}}
```
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
