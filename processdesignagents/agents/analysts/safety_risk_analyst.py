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
    convert_risk_json_to_markdown,
    extract_first_json_document,
)

load_dotenv()


def create_safety_risk_analyst(llm):
    def safety_risk_analyst(state: DesignState) -> DesignState:
        """Safety and Risk Analyst: Performs HAZOP-inspired risk assessment on current concept."""
        print("\n# Safety and Risk Assessment", flush=True)
        requirements_markdown = state.get("requirements", "")
        design_basis_markdown = state.get("design_basis", "")
        basic_pfd_markdown = state.get("basic_pfd", "")
        equipment_json = state.get("equipment_list_results", "") or state.get("equipment_list_template", "")
        stream_data = state.get("stream_list_results", "")
        if not isinstance(stream_data, str):
            stream_data = str(stream_data)
        if not isinstance(basic_pfd_markdown, str):
            basic_pfd_markdown = str(basic_pfd_markdown)
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)
        if not isinstance(equipment_json, str):
            equipment_json = json.dumps(equipment_json, indent=2)
        if not isinstance(design_basis_markdown, str):
            design_basis_markdown = str(design_basis_markdown)
        sanitized_stream_json, stream_payload = extract_first_json_document(stream_data) if stream_data else ("", None)
        sanitized_equipment_json, equipment_payload = extract_first_json_document(equipment_json) if equipment_json else ("", None)

        if stream_payload is None:
            raise ValueError("Safety analyst requires stream results JSON from the estimator.")
        if equipment_payload is None:
            raise ValueError("Safety analyst requires equipment JSON from the sizing workflow.")

        stream_json_formatted = json.dumps(stream_payload, ensure_ascii=False, indent=2)
        equipment_json_formatted = json.dumps(equipment_payload, ensure_ascii=False, indent=2)

        stream_markdown = convert_streams_json_to_markdown(sanitized_stream_json)
        equipment_markdown = convert_equipment_json_to_markdown(sanitized_equipment_json)

        base_prompt = safety_risk_prompt(
            requirements_markdown,
            design_basis_markdown,
            basic_pfd_markdown,
            stream_json_formatted,
            stream_markdown,
            equipment_json_formatted,
            equipment_markdown,
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
            hazards = None
            if isinstance(payload, dict):
                hazards = payload.get("hazards")
            elif isinstance(payload, list):
                hazards = payload
            has_hazards = isinstance(hazards, list) and len(hazards) > 0
            is_done = has_hazards
            try_count += 1
            if not is_done:
                print("- Failed to generate safety assessment. Retrying...", flush=True)
                if try_count > 10:
                    print("+ Max try count reached.", flush=True)
                    exit(-1)

        risk_markdown = convert_risk_json_to_markdown(sanitized_output)
        print(risk_markdown, flush=True)
        return {
            "safety_risk_analyst_report": sanitized_output,
            "messages": [response] if response else [],
        }

    return safety_risk_analyst


def safety_risk_prompt(
    process_requirement: str,
    design_basis_markdown: str,
    basic_pfd_markdown: str,
    stream_data_json: str,
    stream_data_markdown: str,
    equipment_data_json: str,
    equipment_data_markdown: str,
) -> ChatPromptTemplate:
    system_content = """
You are a **Certified Process Safety Professional (CPSP)** with 20 years of experience facilitating Hazard and Operability (HAZOP) studies for the chemical industry.

**Context:**

  * You are given structured `DESIGN_DOCUMENTS` covering the process narrative, stream inventory, and equipment list.
  * Your task is to produce a preliminary HAZOP-style assessment highlighting the most critical hazards.
  * Stakeholders require the results as a JSON dossier that can be tracked programmatically.

**Instructions:**

  * Review the provided information to map unit operations, stream connectivity, and operating envelopes.
  * Identify at least three and at most five hazards covering credible deviations (e.g., loss of flow, high pressure, contamination, utility failure).
  * For each hazard provide:
      - `title`
      - `severity` (integer 1–5)
      - `likelihood` (integer 1–5)
      - `risk_score` (severity × likelihood)
      - `causes`, `consequences`, `mitigations`, `notes` (arrays of concise statements referencing stream IDs/equipment tags where relevant)
  * Summarize the overall risk posture in `overall_assessment` with `risk_level` (Low | Medium | High) and `compliance_notes` (array of follow-up actions or reminders).
  * Use `"TBD"` where data is genuinely unavailable; otherwise provide reasoned estimates.
  * Return a single JSON object matching the schema shown below. Do **not** include code fences, comments, or explanatory prose.

**Example Output:**

{
  "hazards": [
    {
      "title": "Loss of Cooling Water Flow",
      "severity": 3,
      "likelihood": 3,
      "risk_score": 9,
      "causes": ["Cooling water control valve XV-201 fails closed", "Utility header pressure drops during maintenance"],
      "consequences": ["Ethanol outlet > 50 °C causing vapor in downstream storage", "Potential overpressure at vent system"],
      "mitigations": ["Install redundant cooling water pumps with automatic switchover", "Add high-temperature alarm TAH-101 with shutdown logic"],
      "notes": ["Streams 1001/1002 and equipment E-101 impacted; verify relief design for temperature excursion."]
    }
  ],
  "overall_assessment": {
    "risk_level": "Medium",
    "compliance_notes": [
      "Confirm redundancy test for cooling water network before commissioning.",
      "Finalize corrosion monitoring program for E-101 tubes."
    ]
  }
}

**Output Requirements:**

  * All numeric ratings must be integers.
  * Lists may be empty but should remain present.
  * Do not wrap the JSON in code fences or add commentary outside the JSON object.
"""
    human_content = f"""
# DATA FOR HAZOP ANALYSIS
---
**REQUIREMENTS / CONSTRAINTS (Markdown):**
{process_requirement}

**DESIGN BASIS (Markdown):**
{design_basis_markdown}

**BASIC PROCESS FLOW DIAGRAM (Markdown):**
{basic_pfd_markdown}

**STREAM DATA (JSON):**
{stream_data_json}

**EQUIPMENT DETAILS (JSON):**
{equipment_data_json}

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
