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
    convert_streams_json_to_markdown,
)

load_dotenv()


def create_stream_data_builder(llm):
    def stream_data_builder(state: DesignState) -> DesignState:
        """Stream Data Builder: Produces a JSON stream inventory template for process streams."""
        print("\n# Stream Data Template", flush=True)
        
        llm.temperature = 0.7

        basic_pfd_markdown = state.get("basic_pfd", "")
        design_basis_markdown = state.get("design_basis", "")
        requirements_markdown = state.get("requirements", "")
        concept_details_markdown = state.get("selected_concept_details", "")

        base_prompt = stream_data_prompt(
            basic_pfd_markdown,
            design_basis_markdown,
            requirements_markdown,
            concept_details_markdown,
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
            if try_count > 10:
                print("+ Maximum try is reach.")
                exit(-1)

        stream_markdown = convert_streams_json_to_markdown(sanitized_json)
        print(stream_markdown, flush=True)
        return {
            "basic_stream_data": sanitized_json,
            "messages": [response],
        }

    return stream_data_builder


def stream_data_prompt(
    basic_pfd_markdown: str,
    design_basis_markdown: str,
    requirements_markdown: str,
    concept_details_markdown: str,
) -> ChatPromptTemplate:
    system_content = f"""
You are a **Process Data Engineer** responsible for establishing the foundational stream data for a new project as it moves from conceptual design to process simulation.

**Context:**

  * You are provided with the approved conceptual design documents (PFD, Design Basis, Requirements).
  * Your task is to create the canonical stream summary as a structured JSON payload. This document is critical as it serves as the single source of truth for downstream teams who will perform detailed simulations, size equipment, and verify the process flow paths.
  * Every process, utility, recycle, bypass, and vent stream must be captured to ensure a complete and accurate basis for the next project phase.

**Instructions:**

  * **Synthesize Inputs:** Review the provided `DESIGN_DOCUMENTS` to identify and extract every stream mentioned or implied by the process flow.
  * **Assign IDs:** Preserve any existing stream identifiers. For streams without an ID, assign a new sequential number (e.g., 1001, 1002 for process; 2001, 2002 for utilities).
  * **Build JSON Structure:** Return a single JSON object with the following schema:
    - Top-level keys: `"metadata"` and `"streams"`.
    - `"metadata"` must include:
        * `"property_order"`: ordered list of objects `{{ "key": "...", "label": "...", "units": "..." }}` describing each numeric/thermodynamic property column.
        * `"component_basis"`: text such as `"mol %"` or `"mass %"`.
        * `"component_order"`: ordered list of component names as they should appear in tabular form.
        * `"assumptions"`: list of project-wide notes or `[]` if none.
    - Each entry in `"streams"` must include:
        * `"id"`, `"name"`, `"description"`, `"from"`, `"to"`, `"phase"`.
        * `"properties"`: an object keyed by the same identifiers used in `"property_order"` with string values (include units using `<value>` placeholders where unknown, e.g., `"<8500 kg/h>"`).
        * `"components"`: an object mapping component names to their percentage/fraction strings (placeholders allowed).
        * `"notes"`: brief text capturing unique considerations for that stream.
  * **Use Placeholders:** For numeric data that requires later calculation, use the `<value>` format and include the units inside the placeholder. For known design values, record the number directly.
  * **Output Discipline:** Respond with a single valid JSON object using double quotes and UTF-8 safe characters. Do NOT wrap the response in Markdown, code fences, or provide commentary.

-----

**Example:**

  * **DESIGN DOCUMENTS:**

    ```
    "A heat exchanger (E-101) cools 10,000 kg/h of 95 mol% ethanol from 80°C to 40°C. It is fed from an upstream blender and pumped to storage. Plant cooling water is used, entering at 25°C and returning to the header at 35°C."
    ```

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
        "assumptions": []
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
            "mass_flow": "10000",
            "temperature": "80",
            "pressure": "<1.5>"
          }},
          "components": {{
            "Ethanol (C₂H₆O)": "95",
            "Water (H₂O)": "5"
          }},
          "notes": "Tie-in from upstream blender."
        }},
        {{
          "id": "2001",
          "name": "Cooling Water Supply",
          "description": "Utility water to exchanger tubes",
          "from": "Cooling Water Header",
          "to": "E-101 Tube Inlet",
          "phase": "Liquid",
          "properties": {{
            "mass_flow": "<24000 kg/h>",
            "temperature": "25",
            "pressure": "<2.5>"
          }},
          "components": {{
            "Water (H₂O)": "100"
          }},
          "notes": "Return stream 2002 closes utility loop."
        }}
      ]
    }}

-----

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
