from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv

load_dotenv()


def create_equipment_list_builder(llm):
    def equipment_list_builder(state: DesignState) -> DesignState:
        """Equipment List Builder: Produces a markdown equipment template with sizing placeholders."""
        print("\n# Equipment List Template\n")

        basic_pdf_markdown = _coerce_str(state.get("basic_pdf", ""))
        design_basis_markdown = _coerce_str(state.get("design_basis", ""))
        requirements_markdown = _coerce_str(state.get("requirements", ""))
        stream_table = _coerce_str(state.get("basic_stream_data", ""))

        if not stream_table.strip():
            raise ValueError("Stream data is missing. Run the stream data builder first.")

        system_message = system_prompt(
            basic_pdf_markdown,
            design_basis_markdown,
            requirements_markdown,
            stream_table,
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])

        response = (prompt.partial(system_message=system_message) | llm).invoke(state.get("messages", []))
        table_output = response.content if isinstance(response.content, str) else str(response.content)

        print("Equipment template prepared (markdown table).")
        print(table_output)

        return {
            "basic_equipment_template": table_output,
            "basic_equipment_report": table_output,
            "messages": [response],
        }

    return equipment_list_builder


def system_prompt(
    basic_pdf_markdown: str,
    design_basis_markdown: str,
    requirements_markdown: str,
    stream_table: str,
) -> str:
    return f"""
# ROLE
You are a process equipment engineer compiling the master equipment list for a preliminary design package. Create an EQUIPMENT SUMMARY in MARKDOWN TABLE form.

# TASK
Use the process description, design basis, requirements, and stream summary to list every major unit (vessels, reactors, exchangers, towers, pumps, compressors, etc.). Provide clear placeholders for sizing data that will be filled in later.

# OUTPUT FORMAT
Respond with Markdown containing:
```
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| V-101 | Feed Surge Drum | Buffer upstream of pump | Vessel (Vertical) | 1001 | 1002 | <value> kW | Holdup: <value> m³; Orientation: Vertical | <assumptions or TBD items> |
```
- Keep placeholder values as `<value>` with units where appropriate.
- Reference stream IDs exactly as given in the stream table.
- Include all critical equipment implied by the current design.
- Grouping the equipment by type.

# INPUT DATA
---
**BASIC PROCESS DESCRIPTION:**
{basic_pdf_markdown}

**DESIGN BASIS:**
{design_basis_markdown}

**REQUIREMENTS SUMMARY:**
{requirements_markdown}

**STREAM TABLE (Markdown):**
{stream_table}
"""


def _coerce_str(value: object) -> str:
    if isinstance(value, str):
        return value
    return str(value or "")

