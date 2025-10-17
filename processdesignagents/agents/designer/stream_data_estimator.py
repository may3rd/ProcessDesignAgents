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
    extract_first_json_document,
    convert_streams_json_to_markdown,
)

load_dotenv()


def create_stream_data_estimator(llm):
    def stream_data_estimator(state: DesignState) -> DesignState:
        """Stream Data Estimator: Generates JSON stream data with reconciled estimates."""
        print("\n# Stream Data Estimator", flush=True)

        llm.temperature = 0.7
        
        basic_pfd_markdown = state.get("basic_pfd", "")
        requirements_markdown = state.get("requirements", "")
        design_basis_markdown = state.get("design_basis", "")
        concept_details_markdown = state.get("selected_concept_details", "")
        stream_template = state.get("basic_stream_data", "")

        if not isinstance(stream_template, str):
            stream_template = str(stream_template)

        template_json, template_payload = extract_first_json_document(stream_template)
        if template_payload is None:
            raise ValueError("Stream data estimator requires a JSON stream template. Run the builder first.")

        formatted_template = json.dumps(template_payload, ensure_ascii=False, indent=2)

        base_prompt = stream_data_estimator_prompt(
            basic_pfd_markdown,
            requirements_markdown,
            design_basis_markdown,
            concept_details_markdown,
            formatted_template,
        )
        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | llm
        
        is_done = False
        try_count = 0
        sanitized_json = ""
        while not is_done:
            response = chain.invoke({"messages": list(state.get("messages", []))})
            raw_output = (
                response.content if isinstance(response.content, str) else str(response.content)
            ).strip()
            sanitized_json, payload = extract_first_json_document(raw_output)
            has_streams = isinstance(payload, dict) and isinstance(payload.get("streams"), list)
            is_done = bool(has_streams)
            try_count += 1
            if not is_done:
                print("- Failed to create stream data, Retrying...", flush=True)
                if try_count > 10:
                    print("+ Max try count reached.", flush=True)
                    exit(-1)

        stream_markdown = convert_streams_json_to_markdown(sanitized_json)
        print(stream_markdown, flush=True)
        return {
            "basic_hmb_results": sanitized_json,
            "messages": [response],
        }

    return stream_data_estimator


def stream_data_estimator_prompt(
    basic_pfd_markdown: str,
    requirements_markdown: str,
    design_basis_markdown: str,
    concept_details_markdown: str,
    stream_template: str,
) -> ChatPromptTemplate:
    system_content = f"""
You are a **Senior Process Simulation Engineer** specializing in developing first-pass heat and material balances for conceptual designs.

**Context:**

  * You are provided with a `STREAM_TEMPLATE` JSON document containing placeholder stream information, along with supporting `DESIGN_DOCUMENTS` (concept summary, requirements, design basis).
  * Your task is to populate the template with realistic, reconciled operating conditions and document key assumptions.
  * The resulting JSON becomes the authoritative dataset for downstream equipment sizing, detailed simulation, and cost estimation.

**Instructions:**

  * **Analyze Inputs:** Review the `STREAM_TEMPLATE` and all supporting `DESIGN_DOCUMENTS` to understand unit operations, performance targets, and constraints.
  * **Perform Balances:** Replace every placeholder (values wrapped in `< >`) with a best-estimate numeric string. Maintain units by appending them (e.g., `"10000 kg/h"`). Ensure mass and component balances are conserved for each unit and overall.
  * **Update Metadata:** Keep the existing `"property_order"` and `"component_order"` definitions. Populate `"metadata.assumptions"` with concise bullet-style strings summarizing calculation methods (e.g., specific heats, temperature approaches, pressure drops).
  * **Ensure Completeness:** Check that component fractions per stream sum to 100% on the stated basis. Populate `"notes"` for each stream with context or safeguards that support the estimates.
  * **Output Discipline:** Respond with a single valid JSON object matching the input schema—top-level `"metadata"` and `"streams"`. Use double quotes, UTF-8 safe characters, and DO NOT wrap the response in Markdown or code fences.

-----

**Example:**

  * **DESIGN DOCUMENTS:**

    ```
    "A shell-and-tube heat exchanger (E-101) cools 10,000 kg/h of 93 mol% ethanol from 80°C to 40°C. Plant cooling water is used, entering at 25°C. Assume Cp of ethanol stream is 2.5 kJ/kg-K and water is 4.18 kJ/kg-K."
    ```

  * **STREAM TEMPLATE (excerpt):**

    {{
      "metadata": {{
        "property_order": [
          {{"key": "mass_flow", "label": "Mass Flow", "units": "kg/h"}},
          {{"key": "temperature", "label": "Temperature", "units": "°C"}},
          {{"key": "pressure", "label": "Pressure", "units": "barg"}}
        ],
        "component_basis": "mol %",
        "component_order": ["Ethanol (C₂H₆O)", "Water (H₂O)"],
        "assumptions": []
      }},
      "streams": [
        {{
          "id": "1001",
          "name": "Hot Ethanol Feed",
          "properties": {{
            "mass_flow": "<value>",
            "temperature": "<value>",
            "pressure": "<value>"
          }},
          "components": {{
            "Ethanol (C₂H₆O)": "<value>",
            "Water (H₂O)": "<value>"
          }},
          "notes": "..."
        }}
      ]
    }}

  * **Response:**

    {{
      "metadata": {{
        "property_order": [
          {{"key": "mass_flow", "label": "Mass Flow", "units": "kg/h"}},
          {{"key": "temperature", "label": "Temperature", "units": "°C"}},
          {{"key": "pressure", "label": "Pressure", "units": "barg"}}
        ],
        "component_basis": "mol %",
        "component_order": ["Ethanol (C₂H₆O)", "Water (H₂O)"],
        "assumptions": [
          "Ethanol Cp = 2.5 kJ/kg-K; Cooling water Cp = 4.18 kJ/kg-K.",
          "Cooling water temperature rise assumed at 10°C (25→35°C).",
          "Pressure drop estimated at 0.2 bar per stream through E-101."
        ]
      }},
      "streams": [
        {{
          "id": "1001",
          "name": "Hot Ethanol Feed",
          "description": "Feed entering exchanger E-101 shell side",
          "from": "Upstream Blender",
          "to": "E-101 Shell Inlet",
          "phase": "Liquid",
          "properties": {{
            "mass_flow": "10000 kg/h",
            "temperature": "80 °C",
            "pressure": "1.5 barg"
          }},
          "components": {{
            "Ethanol (C₂H₆O)": "93",
            "Water (H₂O)": "7"
          }},
          "notes": "Assumes steady feed from upstream blender with minimal heat loss."
        }},
        {{
          "id": "2001",
          "name": "Cooling Water Supply",
          "description": "Utility water to exchanger tubes",
          "from": "Cooling Water Header",
          "to": "E-101 Tube Inlet",
          "phase": "Liquid",
          "properties": {{
            "mass_flow": "23923 kg/h",
            "temperature": "25 °C",
            "pressure": "2.5 barg"
          }},
          "components": {{
            "Water (H₂O)": "100"
          }},
          "notes": "Flow sized for 10°C rise to deliver 0.278 MW heat removal."
        }}
      ]
    }}

-----

**Your Task:** Based on the provided `DESIGN_DOCUMENTS` and `STREAM_TEMPLATE`, generate ONLY the JSON object described above. Do not include code fences or additional narrative.
"""

    human_content = f"""

# REFERENCE MATERIAL
---
**Design Basis (Markdown):**
{design_basis_markdown}

**Basic Process Flow Diagram (Markdown):**
{basic_pfd_markdown}

# STREAM TEMPLATE (JSON)
{stream_template}

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
