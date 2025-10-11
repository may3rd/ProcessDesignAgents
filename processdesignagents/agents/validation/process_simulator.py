from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv

load_dotenv()


def create_process_simulator(llm):
    def process_simulator(state: DesignState) -> DesignState:
        """Process Simulator: Generates stream and H&MB tables with estimated conditions."""
        print("\n=========================== Preliminary H&MB ===========================\n")

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
            "basic_stream_report": markdown_output,
            "basic_hmb_results": markdown_output,
            "process_simulator_report": markdown_output,
            "messages": [response],
        }

    return process_simulator


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
Using the provided information and the stream template, replace `<value>` placeholders with realistic estimates (include units). Highlight assumptions in notes. Present results strictly as Markdown.

# REQUIRED OUTPUT STRUCTURE
```
## Stream Summary
| Stream ID | Name / Description | From | To | Phase | Mass Flow | Temperature | Pressure | Key Components | Notes |
|-----------|--------------------|------|----|-------|-----------|-------------|----------|----------------|-------|
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Heat & Material Balance
| Property | Stream 1 | Stream 2 | Stream 3 | ... |
|----------|----------|----------|----------|-----|
| Temperature (°C) | ... | ... | ... | ... |
| Pressure (barg) | ... | ... | ... | ... |
| Mass Flow (kg/h) | ... | ... | ... | ... |
| Key Component A (mol %) | ... | ... | ... | ... |
| Notes | ... | ... | ... | ... |
```
- Ensure stream IDs and names align with the template below.
- Keep component listings within cells separated by semicolons.
- Add additional properties/rows as needed for clarity.

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

