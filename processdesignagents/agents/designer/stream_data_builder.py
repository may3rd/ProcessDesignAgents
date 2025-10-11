from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv

load_dotenv()


def create_stream_data_builder(llm):
    def stream_data_builder(state: DesignState) -> DesignState:
        """Stream Data Builder: Produces a transposed markdown table template for process streams."""
        print("\n# Stream Data Template\n")

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

        print("Generated stream template (transposed markdown table).")
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

# OUTPUT FORMAT
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
