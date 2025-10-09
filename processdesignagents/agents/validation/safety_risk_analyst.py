from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.markdown_validators import require_heading_prefix, require_sections
from dotenv import load_dotenv
import json

load_dotenv()


def create_safety_risk_analyst(llm):
    def safety_risk_analyst(state: DesignState) -> DesignState:
        """Safety and Risk Analyst: Performs HAZOP-inspired risk assessment on optimized flowsheet."""
        print("\n=========================== Safety and Risk Assessment ===========================\n")
        validation_results = state.get("validation_results", {})
        flowsheet = state.get("flowsheet", {})
        requirements = state.get("requirements", {})

        flowsheet_markdown = _extract_markdown(flowsheet)
        validation_markdown = _extract_markdown(validation_results)
        requirements_markdown = _extract_markdown(requirements)

        system_message = system_prompt(
            flowsheet_markdown,
            validation_markdown,
            requirements_markdown,
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])
        chain = prompt.partial(system_message=system_message) | llm
        response = chain.invoke(state.get("messages", []))

        risk_markdown = response.content if isinstance(response.content, str) else str(response.content)
        require_heading_prefix(risk_markdown, "Hazard", "Risk assessment report")
        require_sections(risk_markdown, ["Overall Assessment"], "Risk assessment report")

        print("Risk assessment generated (markdown).")
        print(risk_markdown)

        existing_validation = state.get("validation_results", {})
        if not isinstance(existing_validation, dict):
            existing_validation = {}
        updated_validation_results = {
            **existing_validation,
            "risk_assessment_markdown": risk_markdown,
        }

        return {
            "validation_results": updated_validation_results,
            "safety_risk_analyst_report": risk_markdown,
            "messages": [response],
        }

    return safety_risk_analyst


def _extract_markdown(section: object) -> str:
    if isinstance(section, dict):
        collected = []
        for key, title in (
            ("risk_assessment_markdown", "Risk Assessment"),
            ("equipment_sizing_markdown", "Equipment Sizing"),
            ("stream_summary_markdown", "Stream Summary"),
            ("markdown", "Details"),
        ):
            value = section.get(key)
            if isinstance(value, str):
                collected.append(f"## {title}\n{value}")
        if collected:
            return "\n\n".join(collected)
        return json.dumps(section, indent=2, default=str)
    if isinstance(section, str):
        return section
    return str(section)


def system_prompt(flowsheet_markdown: str, validation_markdown: str, requirements_markdown: str) -> str:
    return f"""
# ROLE
You are a Certified Process Safety Professional (CPSP) with 20 years of experience facilitating Hazard and Operability (HAZOP) studies for the chemical industry.

# TASK
Conduct a preliminary, HAZOP-style risk assessment based on the provided process flowsheet, simulated stream conditions, and operational constraints. Your analysis must identify 3-5 critical process hazards, assess their risks, and propose actionable mitigations. The final output must be a Markdown report.

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
**FLOWSHEET (Markdown):**
{flowsheet_markdown}

**STREAM CONDITIONS (Markdown Table):**
{validation_markdown}

**REQUIREMENTS / CONSTRAINTS (Markdown):**
{requirements_markdown}

# FINAL MARKDOWN OUTPUT:
"""
