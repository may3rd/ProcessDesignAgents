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


def create_equipment_list_builder(llm):
    def equipment_list_builder(state: DesignState) -> DesignState:
        """Equipment List Builder: Produces an equipment template JSON with sizing placeholders."""
        print("\n# Equipment List Template", flush=True)

        llm.temperature = 0.7

        basic_pfd_markdown = state.get("basic_pfd", "")
        design_basis_markdown = state.get("design_basis", "")
        requirements_markdown = state.get("requirements", "")
        stream_table = state.get("basic_hmb_results", "")
        sanitized_stream_json, stream_payload = extract_first_json_document(stream_table) if isinstance(stream_table, str) else ("", None)
        if stream_payload is None:
            raise ValueError("Equipment list builder requires stream data JSON from the estimator.")
        formatted_stream_json = json.dumps(stream_payload, ensure_ascii=False, indent=2)
        stream_table_markdown = convert_streams_json_to_markdown(sanitized_stream_json)

        base_prompt = equipment_list_prompt(
            basic_pfd_markdown,
            design_basis_markdown,
            requirements_markdown,
            formatted_stream_json,
            stream_table_markdown,
        )

        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)

        is_done = False
        try_count = 0
        sanitized_output = ""
        response = None
        while not is_done:
            response = (prompt | llm).invoke({"messages": list(state.get("messages", []))})
            raw_output = (
                response.content if isinstance(response.content, str) else str(response.content)
            ).strip()
            sanitized_output, payload = extract_first_json_document(raw_output)
            equipment_entries = None
            if isinstance(payload, dict):
                equipment_entries = payload.get("equipment")
            elif isinstance(payload, list):
                equipment_entries = payload
            has_equipment = isinstance(equipment_entries, list) and len(equipment_entries) > 0
            is_done = has_equipment
            try_count += 1
            if not is_done:
                print("- Failed to create equipment template. Retrying...", flush=True)
                if try_count > 10:
                    print("+ Max try count reached.", flush=True)
                    exit(-1)

        equipment_markdown = convert_equipment_json_to_markdown(sanitized_output)
        print(equipment_markdown, flush=True)

        return {
            "basic_equipment_template": sanitized_output,
            "messages": [response] if response else [],
        }

    return equipment_list_builder


def equipment_list_prompt(
    basic_pfd_markdown: str,
    design_basis_markdown: str,
    requirements_markdown: str,
    stream_table_json: str,
    stream_table_markdown: str,
) -> ChatPromptTemplate:
    system_content = """
You are a **Process Equipment Engineer** responsible for creating the Master Equipment List for a preliminary design package.

**Context:**

  * You are provided with the complete conceptual design package, including the `DESIGN_DOCUMENTS` (flowsheets, stream summaries, design basis, and requirements).
  * The project is transitioning from conceptual design to the preliminary engineering phase.
  * Your task is to create the canonical list of major equipment. This list is a critical deliverable that enables downstream teams (sizing, costing, safety) to begin their work in parallel.

**Instructions:**

  * **Analyze Inputs:** Review all `DESIGN_DOCUMENTS` to identify every required piece of major equipment (vessels, reactors, exchangers, towers, pumps, compressors, etc.).
  * **Map Connectivity:** Use the stream summary to map the inlet and outlet stream IDs for each piece of equipment.
  * **Group Equipment:** Where it adds clarity, group related equipment by type (e.g., Heat Exchangers, Pumps) in the `metadata.groups` section.
  * **Use Placeholders:** Populate each equipment entry with known identifiers. For all sizing data or parameters that are not yet calculated, use the format `<value>`, ensuring you include the expected units (e.g., `<120 m²>`).
  * **Document Assumptions:** Capture any global assumptions (e.g., utility conditions, general efficiencies) in the `metadata.assumptions` section. Add item-specific assumptions or notes in the `notes` field for that piece of equipment.
  * **Format Adherence:** Your final output must be a single, PURE JSON object. Do not wrap the JSON in a code block or add any commentary outside of the JSON object itself.

-----

**Example:**

  * **DESIGN DOCUMENTS:**

    ```
    "A shell-and-tube exchanger (E-101) cools ethanol from 80°C to 40°C. A pump (P-101) transfers the cooled product to storage. Stream data: Hot ethanol is stream 1001, cooled is 1002. Cooling water supply is stream 2001, return is 2002. Assume a 10°C rise for cooling water."
    ```

  * **Response:**

    ```json
    {
      "metadata": {
        "groups": [
          {
            "name": "Heat Exchangers",
            "ids": [
              "E-101"
            ]
          },
          {
            "name": "Pumps",
            "ids": [
              "P-101"
            ]
          }
        ],
        "assumptions": [
          "Cooling water temperature rise is assumed to be 10°C.",
          "All pressure drops across equipment are placeholder estimates."
        ]
      },
      "equipment": [
        {
          "id": "E-101",
          "name": "Ethanol Cooler",
          "service": "Reduce hot ethanol temperature prior to storage.",
          "type": "Shell-and-tube exchanger",
          "streams_in": [
            "1001",
            "2001"
          ],
          "streams_out": [
            "1002",
            "2002"
          ],
          "duty_or_load": "<0.28 MW>",
          "key_parameters": [
            "Area: <120 m²>",
            "U-value: <450 W/m²-K>"
          ],
          "notes": "Design for a minimum 5°C approach temperature. Ensure sufficient space for bundle pull during maintenance."
        },
        {
          "id": "P-101",
          "name": "Ethanol Product Pump",
          "service": "Transfer cooled ethanol to storage.",
          "type": "Centrifugal pump",
          "streams_in": [
            "1002"
          ],
          "streams_out": [
            "1003"
          ],
          "duty_or_load": "<5 kW>",
          "key_parameters": [
            "Differential Head: <1.5 bar>",
            "Flow Rate: <12 m³/h>"
          ],
          "notes": "Material of construction to be stainless steel. Efficiency to be confirmed with vendor."
        }
      ]
    }
    ```

-----

**Your Task:** Based on the provided `DESIGN_DOCUMENTS`, generate ONLY the valid JSON object that precisely follows the structure and rules defined above. Do not include code fences or additional narrative.
"""
    human_content = f"""
# INPUT DATA
---
**Basic Process Flow Diagram:**
{basic_pfd_markdown}

**Design Basis:**
{design_basis_markdown}

**Stream Data (JSON):**
{stream_table_json}
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
