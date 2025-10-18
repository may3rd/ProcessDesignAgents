from __future__ import annotations

import json
import re

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from dotenv import load_dotenv

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import jinja_raw, strip_markdown_code_fences
from processdesignagents.agents.utils.json_tools import extract_first_json_document

load_dotenv()


def create_project_manager(llm):
    def project_manager(state: DesignState) -> DesignState:
        """Project Manager: Reviews design for approval and generates implementation plan."""
        print("\n# Project Review", flush=True)

        requirements_markdown = state.get("requirements", "")
        design_basis = state.get("design_basis", "")
        basic_pfd_markdown = state.get("basic_pfd", "")
        validation_markdown = state.get("stream_list_results", "")
        equipment_table = state.get("equipment_list_results", "") or state.get("equipment_list_template", "")
        safety_report = state.get("safety_risk_analyst_report", "")
        
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)
        if not isinstance(basic_pfd_markdown, str):
            basic_pfd_markdown = str(basic_pfd_markdown)
        if not isinstance(validation_markdown, str):
            validation_markdown = str(validation_markdown)
        if not isinstance(equipment_table, str):
            equipment_table = str(equipment_table)
        if not isinstance(safety_report, str):
            safety_report = str(safety_report)

        sanitized_stream_json, stream_payload = extract_first_json_document(validation_markdown) if validation_markdown else ("", None)
        sanitized_equipment_json, equipment_payload = extract_first_json_document(equipment_table) if equipment_table else ("", None)
        sanitized_safety_json, safety_payload = extract_first_json_document(safety_report) if safety_report else ("", None)

        stream_json_formatted = json.dumps(stream_payload, ensure_ascii=False, indent=2) if stream_payload is not None else (validation_markdown or "{}")
        equipment_json_formatted = json.dumps(equipment_payload, ensure_ascii=False, indent=2) if equipment_payload is not None else (equipment_table or "{}")
        safety_json_formatted = json.dumps(safety_payload, ensure_ascii=False, indent=2) if safety_payload is not None else (safety_report or "{}")

        base_prompt = project_manager_prompt(
            requirements_markdown,
            design_basis,
            basic_pfd_markdown,
            stream_json_formatted,
            equipment_json_formatted,
            safety_json_formatted,
        )

        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)

        chain = prompt | llm
        response = chain.invoke({"messages": list(state.get("messages", []))})

        approval_markdown = (
            response.content if isinstance(response.content, str) else str(response.content)
        ).strip()
        approval_markdown = strip_markdown_code_fences(approval_markdown)
        approval_status = _extract_status(approval_markdown)

        print(f"Project review completed. Status: **{approval_status or 'Unknown'}**\n", flush=True)
        print(approval_markdown, flush=True)

        return {
            "approval": approval_status or "",
            "project_manager_report": approval_markdown,
            "messages": [response],
        }

    return project_manager


def _extract_status(markdown_text: str) -> str | None:
    match = re.search(r"Approval Status\s*[:\-]\s*([A-Za-z ]+)", markdown_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def project_manager_prompt(
    project_requirements: str,
    design_basis: str,
    basic_pfd: str,
    stream_data_json: str,
    equipment_table_json: str,
    safety_and_risk_json: str,
) -> ChatPromptTemplate:
    system_content = """
You are a **Project Manager** specializing in stage-gate approval, financial evaluation, and implementation planning for capital projects in the chemical and process industries.

**Context:**

  * You are at the final stage-gate of a conceptual design process.
  * You will receive a structured `DESIGN_PACKAGE` composed of Markdown narratives (requirements, design basis, PFD summary) plus JSON artefacts (stream data, equipment list, HAZOP dossier).
  * Your task is to synthesize this information, render the gatekeeping decision (Approve, Conditional, Reject), summarize the financial outlook, and outline near-term execution steps.
  * The approval memo you produce is the authoritative record for advancing (or pausing) the project before FEED.

**Instructions:**

  * Critically review the JSON artefacts to confirm internal consistency (streams ↔ equipment ↔ safety mitigations) and alignment with the narrative requirements/design basis.
  * Select the appropriate `Approval Status` and state a one-sentence `Key Rationale` backing your decision.
  * Populate the financial table with CAPEX, OPEX, and contingency values. Use reasonable assumptions when data is missing and flag any estimates in the `Final Notes`.
  * Draft three sequenced, actionable steps in the `Implementation Plan`, noting owners or timing when relevant.
  * Capture residual risks, compliance items, or data gaps in `Final Notes`, referencing specific stream IDs, equipment tags, or hazard IDs from the JSON where applicable.
  * Output must follow the approval memo Markdown template exactly—no supplementary prose or code fences.

-----

**Example:**

  * **DESIGN PACKAGE:**

    ```
    "The project is for a single heat exchanger (E-101) to cool 10,000 kg/h ethanol from 80°C to 40°C. The design relies on the plant's central cooling water utility. The HAZOP identified a critical risk related to 'Loss of Cooling Water Flow' (Hazard #1). The estimated cost for the modular skid is $1.2M. Annual utility and maintenance costs are estimated at $350k."
    ```

  * **Response:**

    ```markdown
    ## Executive Summary
    - Approval Status: Conditional
    - Key Rationale: Full approval is contingent upon engineering verification of safeguards for the loss of cooling water scenario identified in the HAZOP.

    ## Financial Outlook
    | Metric                       | Estimate |
    | ---------------------------- | -------- |
    | CAPEX (USD millions)         | 1.2      |
    | OPEX (USD millions per year) | 0.35     |
    | Contingency (%)              | 15       |

    ## Implementation Plan
    1.  **Finalize Detailed Design:** Complete the mechanical design for the E-101 exchanger skid and issue for procurement (Target: 4 weeks).
    2.  **Implement Safeguards:** Install and functionally test the high-temperature interlock and any required cooling water redundancy measures (Target: 3 weeks, post-procurement).
    3.  **Commissioning:** Perform a full performance test of the cooler module and complete operator training (Target: 2 weeks, post-installation).

    ## Final Notes
    - The utility contract must be reviewed to guarantee the required 24,000 kg/h cooling water supply during peak summer conditions.
    - The final design must include the corrosion coupon program recommended in the safety review before the first ethanol run.
    ```

-----

**Your Task:** Based on the provided `DESIGN_PACKAGE`, generate ONLY the valid Markdown approval report that precisely follows the structure and rules defined above. Do not include code fences or additional narrative.
"""

    human_content = f"""
# DESIGN PACKAGE (Mixed Format)

**Requirements Summary (Markdown):**
{project_requirements}

**Design Basis (Markdown):**
{design_basis}

**Basic Process Flow Diagram (Markdown):**
{basic_pfd}

**Heat & Material Balance (JSON):**
{stream_data_json}

**Equipment Summary (JSON):**
{equipment_table_json}

**Safety & Risk Dossier (JSON):**
{safety_and_risk_json}
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
