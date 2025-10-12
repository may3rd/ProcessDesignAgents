from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv

load_dotenv()


def create_stream_data_estimator(llm):
    def stream_data_estimator(state: DesignState) -> DesignState:
        """Stream Data Estimator: Generates stream and H&MB tables with estimated conditions."""
        print("\n# Stream Data Estimator\n")

        llm.temperature = 0.7
        
        basic_pdf_markdown = _coerce_str(state.get("basic_pdf", ""))
        requirements_markdown = _coerce_str(state.get("requirements", ""))
        design_basis_markdown = _coerce_str(state.get("design_basis", ""))
        concept_details_markdown = _coerce_str(state.get("selected_concept_details", ""))
        stream_template = _coerce_str(state.get("basic_stream_data", ""))

        if not stream_template.strip():
            raise ValueError("Stream template not available. Ensure stream_data_builder executed successfully.")

        system_message = system_prompt(
            basic_pdf_markdown,
            requirements_markdown,
            design_basis_markdown,
            concept_details_markdown,
            stream_template,
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])
        response = (prompt.partial(system_message=system_message) | llm).invoke(state.get("messages", []))

        markdown_output = response.content if isinstance(response.content, str) else str(response.content)

        print(markdown_output)

        return {
            "basic_stream_data": markdown_output,
            "basic_hmb_results": markdown_output,
            "messages": [response],
        }

    return stream_data_estimator


def system_prompt(
    basic_pdf_markdown: str,
    requirements_markdown: str,
    design_basis_markdown: str,
    concept_details_markdown: str,
    stream_template: str,
) -> str:
    return f"""
# ROLE
You are a Senior Process Simulation Engineer. Generate estimated operating conditions for every process stream and summarize the overall heat and material balance.

# TASK
Using the provided information and the 'STREAM TEMPLATE', replace `<value>` placeholders with realistic estimates (include units). Highlight assumptions in notes. Present results strictly as Markdown.

# EXAMPLE
When refining a heat exchanger that cools ethanol from 80 C to 40 C with cooling water, estimate consistent temperatures and flow rates for the ethanol and cooling water streams, ensuring the heat removed from ethanol matches the heat absorbed by the utility and documenting any assumed specific heat values.

# INSTRUCTIONS
- For every unit operation implied by the stream connectivity, ensure total mass flow entering equals the total leaving.
- Reconcile component balances so key species entering a unit match the sum leaving that unit, accounting for accumulation or loss only when explicitly justified.
- Confirm the overall process inputs equal outputs across the full flowsheet; highlight any reconciliation assumptions in the Notes section.
- When balance adjustments are required, document the rationale and affected streams directly in the Notes entries.
- Ensure stream IDs and names align with the template below.
- Ensure that summation of mol% for each component equals 100%.
- Add additional properties/rows as needed for clarity.

# CRITICALS
- **MUST** return the full stream data table in markdown format.

# MARKDOWN TEMPLATE:
Your Markdown output must follow this structure:
|          | 1001 | 1002 | 1003 | ... | <only show stream ID>
| Description | ------ | ------ | ------ | ----- |
| ---------- | ------ | ------ | ------ | ----- |
| Temperature (°C) | ... | ... | ... | ... |
| Pressure (barg) | ... | ... | ... | ... |
| Mass Flow (kg/h) | ... | ... | ... | ... |
| Key Component | (mol %) | (mol %) | (mol %) | ... |
| Component A | ... | ... | ... | ... | ... |
| Component B | ... | ... | ... | ... | ... |
| Component C | ... | ... | ... | ... | ... |

## Notes
- <note 1>
- <note 2>
- ...

---

**EXPECTED MARKDOWN OUTPUT:**
<md_output>
# Stream Data Table
|          | 1001 | 1002 | 2001 | 2002 |
| Description | Hot ethanol feed | Cooled ethanol product | Cooling water supply | Cooling water return |
| ---------- | ------ | ------ | ------ | ------ |
| Temperature (degC) | 80 | 40 | 25 | 35 |
| Pressure (barg) | 1.5 | 1.3 | 2.5 | 2.3 |
| Mass Flow (kg/h) | 10,000 | 10,000 | 24,000 | 24,000 |
| Key Component | (mol %) | (mol %) | (mol %) | (mol %) |
| Ethanol (C2H6O) | 93 | 93 | 0 | 0 |
| Water (H2O) | 7 | 7 | 100 | 100 |

## Notes
- Cooling water duty balances ethanol heat removal at approx. 0.28 MW.
- Monitoring differential pressure across E-101 ensures early fouling detection.
</md_output>

# STREAM TEMPLATE
{stream_template}

# REFERENCE MATERIAL
---
**BASIC PROCESS DESCRIPTION:**
{basic_pdf_markdown}

**DESIGN BASIS:**
{design_basis_markdown}

**REQUIREMENTS SUMMARY:**
{requirements_markdown}

**CONCEPT DETAIL:**
{concept_details_markdown}
"""


def _coerce_str(value: object) -> str:
    if isinstance(value, str):
        return value
    return str(value or "")
