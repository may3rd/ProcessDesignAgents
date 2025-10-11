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
        requirements_markdown = state.get("requirements", "")
        design_basis_markdown = state.get("design_basis", "")
        basic_pdf_markdown = state.get("basic_pdf", "")
        equipment_json = state.get("basic_equipment_template", "")
        stream_data = state.get("basic_hmb_results", "")
        if not isinstance(stream_data, str):
            stream_data = str(stream_data)
        if not isinstance(basic_pdf_markdown, str):
            basic_pdf_markdown = str(basic_pdf_markdown)
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)
        if not isinstance(equipment_json, str):
            equipment_json = json.dumps(equipment_json, indent=2)
        if not isinstance(design_basis_markdown, str):
            design_basis_markdown = str(design_basis_markdown)

        system_message = system_prompt(
            requirements_markdown,
            design_basis_markdown,
            basic_pdf_markdown,
            stream_data,
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

        return {
            "safety_risk_analyst_report": risk_markdown,
            "messages": [response],
        }

    return safety_risk_analyst


def system_prompt(
    process_requirement: str,
    design_basis_markdown: str,
    basic_pdf_markdown: str,
    stream_data: str,
    equipment_data: str,
) -> str:
    return f"""
# ROLE
You are a Certified Process Safety Professional (CPSP) with 20 years of experience facilitating Hazard and Operability (HAZOP) studies for the chemical industry.

# TASK
Conduct a preliminary, HAZOP-style risk assessment based on the provided basic process description, simulated stream conditions, and operational constraints. Your analysis must identify 3-5 critical process hazards, assess their risks, and propose actionable mitigations. The final output must be a Markdown report.

# INSTRUCTIONS
- Start by scanning the process overview and stream/equipment data to map each major unit operation and its feed/product streams.
- For every unit, enumerate credible deviations (flow, temperature, pressure, composition) using standard HAZOP guide words and link them to potential causes.
- Quantify severity and likelihood on the 1–5 scale using the provided operating envelopes and requirements; show your reasoning in brief notes.
- Propose mitigations that directly address the identified causes or consequences and cross-reference existing safeguards where applicable.
- Ensure each hazard references the specific stream IDs, equipment tags, or operating conditions involved.
- Finish with an overall risk conclusion that reconciles the individual findings and highlights any required follow-up actions or confirmations.

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
**REQUIREMENTS / CONSTRAINTS (Markdown):**
{process_requirement}

**DESIGN BASIS (Markdown):**
{design_basis_markdown}

**BASIC PROCESS DESCRIPTION (Markdown):**
{basic_pdf_markdown}

**STREAM CONDITIONS (Markdown Table):**
{stream_data}

**EQUIPMENT DETAILS (JSON):**
{equipment_data}

# FINAL MARKDOWN OUTPUT:
"""
