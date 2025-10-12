from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv

load_dotenv()


def create_stream_data_builder(llm):
    def stream_data_builder(state: DesignState) -> DesignState:
        """Stream Data Builder: Produces a transposed markdown table template for process streams."""
        print("\n# Stream Data Template\n")
        
        llm.temperature = 0.7

        basic_pdf_markdown = _coerce_str(state.get("basic_pdf", ""))
        design_basis_markdown = _coerce_str(state.get("design_basis", ""))
        requirements_markdown = _coerce_str(state.get("requirements", ""))
        concept_details_markdown = _coerce_str(state.get("selected_concept_details", ""))

        system_message = system_prompt(
            basic_pdf_markdown,
            design_basis_markdown,
            requirements_markdown,
            concept_details_markdown,
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])

        response = (prompt.partial(system_message=system_message) | llm).invoke(state.get("messages", []))
        table_markdown = response.content if isinstance(response.content, str) else str(response.content)

        print(table_markdown)

        return {
            "basic_stream_data": table_markdown,
            "messages": [response],
        }

    return stream_data_builder


def system_prompt(
    basic_pdf_markdown: str,
    design_basis_markdown: str,
    requirements_markdown: str,
    concept_details_markdown: str,
) -> str:
    return f"""
# ROLE
You are a process engineer compiling preliminary stream definitions for a chemical process. Create a clear MARKDOWN TABLE that captures every stream referenced in the available design information.

# TASK
For each stream, provide identifiers, origin/destination, qualitative description, and placeholder operating data that will later be filled by the simulator.

# MARKDOWN TEMPLATE:
Respond with a Markdown table only (no additional commentary) using a structure where stream identifiers are columns and attributes are rows:
```
| Attribute | 1001 | 1002 | ... |
|-----------|-------------|-------------|-----|
| Name / Description | Feed from T-101 | <value> | ... |
| From | T-101 | <value> | ... |
| To | E-101 | <value> | ... |
| Phase | <value> | <value> | ... |
| Mass Flow [kg/h] | <value> | <value> | ... |
| Temperature [°C] | <value> | <value> | ... |
| Pressure [barg] | <value> | <value> | ... |
| Key Components | mol% | mol% | ... |
| Nitrogen (N2) | <value> | <value> | ... |
| Oxygen (O2) | <value> | <value> | ... |
| Notes | <value> | <value> | ... |
```
- Use `<value>` placeholders where numbers are unknown.
- Add additional stream columns for every stream implied by the concept (utilities, recycle, vent, product, etc.).

# CRITICALS
- **MUST** return the full stream data table in markdown format.

# EXAMPLE
In a heat exchanger that cools ethanol from 80 C to 40 C with cooling water, create streams for hot ethanol feed, cooled ethanol product, cooling water supply, and cooling water return, assigning IDs and placeholder temperatures that reflect the duty.

**EXPECTED MARKDOWN OUTPUT:**
<md_output>
# Stream Data Table
| Attribute | 1001 | 1002 | 2001 | 2002 |
|-----------|------|------|------|------|
| Name / Description | Hot ethanol feed | Cooled ethanol product | Cooling water supply | Cooling water return |
| From | Upstream blender | E-101 outlet | CW header | E-101 |
| To | E-101 shell | Storage tank via P-101 | E-101 tubes | CW header |
| Phase | Liquid | Liquid | Liquid | Liquid |
| Mass Flow [kg/h] | <10,000> | <10,000> | <24,000> | <24,000> |
| Temperature [degC] | <80> | <40> | <25> | <35> |
| Pressure [barg] | <1.5> | <1.3> | <2.5> | <2.3> |
| Key Components | mol% | mol% | mol% | mol% |
| Ethanol (C2H6O) | <95> | <95> | <0> | <0> |
| Water (H2O) | <5> | <5> | <100> | <100> |
| Notes | Tie-in from upstream blender | To fixed-roof storage | Shared cooling water header | Returned to utility system |
</md_output>

# DATA AVAILABLE
---
**BASIC PDF DESCRIPTION:**
{basic_pdf_markdown}

**DESIGN BASIS (Markdown):**
{design_basis_markdown}

**REQUIREMENTS SUMMARY:**
{requirements_markdown}

**CONCEPT DETAIL (Markdown):**
{concept_details_markdown}
"""


def _coerce_str(value: object) -> str:
    if isinstance(value, str):
        return value
    return str(value or "")
