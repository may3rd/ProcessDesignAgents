from __future__ import annotations

import json

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv

load_dotenv()


def create_safety_risk_analyst(llm):
    def safety_risk_analyst(state: DesignState) -> DesignState:
        """Safety and Risk Analyst: Performs HAZOP-inspired risk assessment on current concept."""
        print("\n# Safety and Risk Assessment \n")
        validation_markdown = state.get("basic_hmb_results", "")
        basic_pdf_markdown = state.get("basic_pdf", "")
        requirements_markdown = state.get("requirements", "")
        equipment_json = state.get("basic_equipment_template", "")
        if not isinstance(validation_markdown, str):
            validation_markdown = str(validation_markdown)
        if not isinstance(basic_pdf_markdown, str):
            basic_pdf_markdown = str(basic_pdf_markdown)
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)
        if not isinstance(equipment_json, str):
            equipment_json = json.dumps(equipment_json, indent=2)

        system_message = system_prompt(
            basic_pdf_markdown,
            validation_markdown,
            requirements_markdown,
            equipment_json,
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])
        chain = prompt.partial(system_message=system_message) | llm
        response = chain.invoke(state.get("messages", []))

        risk_markdown = response.content if isinstance(response.content, str) else str(response.content)

        print("Risk assessment generated (markdown).")
        print(risk_markdown)

        existing_validation = state.get("basic_hmb_results", "")
        if not isinstance(existing_validation, str):
            existing_validation = str(existing_validation or "")
        validation_segments = []
        if existing_validation.strip():
            validation_segments.append(existing_validation.strip())
        validation_segments.append(risk_markdown.strip())
        updated_hmb_results = "\n\n".join(validation_segments)

        return {
            "basic_hmb_results": updated_hmb_results,
            "safety_risk_analyst_report": risk_markdown,
            "messages": [response],
        }

    return safety_risk_analyst


def system_prompt(
    basic_pdf_markdown: str,
    validation_markdown: str,
    requirements_markdown: str,
    equipment_json: str,
) -> str:
    return f"""
# ROLE
You are a Certified Process Safety Professional (CPSP) with 20 years of experience facilitating Hazard and Operability (HAZOP) studies for the chemical industry.

# TASK
Conduct a preliminary, HAZOP-style risk assessment based on the provided basic process description, simulated stream conditions, and operational constraints. Your analysis must identify 3-5 critical process hazards, assess their risks, and propose actionable mitigations. The final output must be a Markdown report.

# OUTPUT FORMAT
Your Markdown must follow this structure exactly:
```
## Hazard 1: <Hazard Title>
**Severity:** <1-5>
**Likelihood:** <1-5>
**Risk Score:** <integer>

### Causes
- <cause 1>
- <cause 2>

### Consequences
- <consequence 1>
- <consequence 2>

### Mitigations
- <mitigation 1>
- <mitigation 2>

### Notes
- <brief commentary referencing streams or units>
```
Repeat for each hazard (Hazard 1, Hazard 2, etc.). After listing hazards, add:
```
## Overall Assessment
- Overall Risk Level: <Low | Medium | High>
- Compliance Notes: <summary>
```

# DATA FOR HAZOP ANALYSIS
---
**BASIC PROCESS DESCRIPTION (Markdown):**
{basic_pdf_markdown}

**STREAM CONDITIONS (Markdown Table):**
{validation_markdown}

**REQUIREMENTS / CONSTRAINTS (Markdown):**
{requirements_markdown}

**EQUIPMENT DETAILS (JSON):**
{equipment_json}

# FINAL MARKDOWN OUTPUT:
"""
