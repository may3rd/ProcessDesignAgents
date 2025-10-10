from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import re

load_dotenv()


def create_project_manager(llm):
    def project_manager(state: DesignState) -> DesignState:
        """Project Manager: Reviews design for approval and generates implementation plan."""
        print("\n=========================== Project Review ===========================\n")

        requirements_markdown = state.get("requirements", "")
        flowsheet_markdown = state.get("flowsheet", "")
        validation_markdown = state.get("validation_results", "")
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)
        if not isinstance(flowsheet_markdown, str):
            flowsheet_markdown = str(flowsheet_markdown)
        if not isinstance(validation_markdown, str):
            validation_markdown = str(validation_markdown)

        system_message = system_prompt(requirements_markdown, flowsheet_markdown, validation_markdown)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])

        chain = prompt.partial(system_message=system_message) | llm
        response = chain.invoke(state.get("messages", []))

        approval_markdown = response.content if isinstance(response.content, str) else str(response.content)
        approval_status = _extract_status(approval_markdown)

        print(f"Project review completed. Status: {approval_status or 'Unknown'}")
        print(approval_markdown)

        updated_approval = approval_markdown

        return {
            "approval": updated_approval,
            "project_manager_report": approval_markdown,
            "messages": [response],
        }

    return project_manager


def _extract_status(markdown_text: str) -> str | None:
    match = re.search(r"Approval Status\s*[:\-]\s*([A-Za-z ]+)", markdown_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def system_prompt(requirements_markdown: str, flowsheet_markdown: str, validation_markdown: str) -> str:
    return f"""
# ROLE
You are the project manager responsible for final stage-gate approval of the process design.

# TASK
Review the provided requirements, flowsheet summary, validation results, and safety and risk results. Decide whether to approve, conditionally approve, or reject the project. Summarize financial estimates and outline the immediate implementation plan.

# OUTPUT FORMAT
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
```

# DATA FOR REVIEW
---
**REQUIREMENTS SUMMARY (Markdown):**
{requirements_markdown}

**FLOWSHEET SUMMARY (Markdown):**
{flowsheet_markdown}

**VALIDATION RESULTS (Markdown):**
{validation_markdown}

# FINAL MARKDOWN OUTPUT:
"""
