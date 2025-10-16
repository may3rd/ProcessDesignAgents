from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import re

load_dotenv()


def create_project_manager(llm):
    def project_manager(state: DesignState) -> DesignState:
        """Project Manager: Reviews design for approval and generates implementation plan."""
        print("\n# Project Review\n", flush=True)

        requirements_markdown = state.get("requirements", "")
        design_basis = state.get("design_basis", "")
        basic_pfd_markdown = state.get("basic_pfd", "")
        validation_markdown = state.get("basic_hmb_results", "")
        equipment_table = state.get("basic_equipment_template", "")
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

        system_message = system_prompt(
            requirements_markdown,
            design_basis,
            basic_pfd_markdown,
            validation_markdown,
            equipment_table,
            safety_report,
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])

        chain = prompt.partial(system_message=system_message) | llm
        response = chain.invoke({"messages": list(state.get("messages", []))})

        approval_markdown = response.content if isinstance(response.content, str) else str(response.content)
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


def system_prompt(
    requirements_markdown: str,
    design_basis: str,
    basic_pfd_markdown: str,
    validation_markdown: str,
    equipment_table: str,
    safety_markdown: str,
) -> str:
    return f"""
# ROLE
You are the project manager responsible for final stage-gate approval of the process design.

# TASK
Review the provided requirements, design basis, process description, H&MB results, equipment sizing summary, and safety/risk findings. Decide whether to approve, conditionally approve, or reject the project. Summarize financial estimates and outline the immediate implementation plan.

# INSTRUCTIONS
1. **Assess alignment:** Cross-check requirements, design basis, equipment summary, and safety notes; highlight any conflicts or missing justifications in the rationale.
2. **Decide approval:** Choose `Approved`, `Conditional`, or `Rejected`, stating the gating condition(s) that drive the decision.
3. **Quantify economics:** Populate CAPEX, OPEX, and contingency with estimates (or `TBD` plus a short note) derived from the available data or reasonable scaling assumptions.
4. **Plan execution:** Provide three concrete implementation steps, each actionable and sequenced; note timing or responsibility where possible.
5. **Flag follow-ups:** Use Final Notes to capture open risks, compliance items, or data gaps, referencing the source document (streams, equipment tags, hazards) that triggered the concern.

# CRITICALS
- **follow** the MARKDOWN TEMPLATE strictly.
- **Output ONLY a valid markdown formatting text. Do not use code block.**
# MARKDOWN TEMPLATE:
Return a Markdown report with the following structure:
```
## Executive Summary
- Approval Status: <Approved | Conditional | Rejected>
- Key Rationale: <one sentence>

## Financial Outlook
| Metric | Estimate |
|--------|----------|
| CAPEX (USD millions) | ... |
| OPEX (USD millions per year) | ... |
| Contingency (%) | ... |

## Implementation Plan
1. <Step 1>
2. <Step 2>
3. <Step 3>

## Final Notes
- <risk or follow-up item>
- <compliance reminder>
---

# EXAMPLE INPUT:
If the package contains a single heat exchanger that cools ethanol from 80 C to 40 C using cooling water, ensure the summary references the utility demand, checks that safety measures cover loss of cooling, and ties the approval status to readiness of that cooler service.

# EXPECTED MARKDOWN OUTPUT:
## Executive Summary
- Approval Status: Conditional
- Key Rationale: Cooling water redundancy verification required prior to full approval

## Financial Outlook
| Metric | Estimate |
|--------|----------|
| CAPEX (USD millions) | 1.2 |
| OPEX (USD millions per year) | 0.35 |
| Contingency (%) | 15 |

## Implementation Plan
1. Finalise exchanger mechanical design and procurement (4 weeks).
2. Install cooling water redundancy instrumentation and test interlocks (3 weeks).
3. Commission cooler module with performance test and operator training (2 weeks).

## Final Notes
- Confirm corrosion coupon program before first ethanol run.
- Align utility contract to guarantee 24,000 kg/h cooling water during summer peaks.

# DATA FOR REVIEW

**REQUIREMENTS SUMMARY (Markdown):**
{requirements_markdown}

**DESIGN BASIS (Markdown):**
{design_basis}

**BASIC PROCESS FLOW DIAGRAM (Markdown):**
{basic_pfd_markdown}

**H&MB RESULTS (Markdown):**
{validation_markdown}

**EQUIPMENT SIZING (Markdown):**
{equipment_table}

**SAFETY & RISK SUMMARY (Markdown):**
{safety_markdown}

# FINAL MARKDOWN OUTPUT:
"""
