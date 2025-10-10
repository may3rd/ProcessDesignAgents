from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv

load_dotenv()


def create_process_simulator(llm):
    def process_simulator(state: DesignState) -> DesignState:
        """Process Simulator: Generates preliminary Heat and Material Balance (H&MB) from flowsheet."""
        print("\n=========================== Create Prelim H&MB ===========================")

        flowsheet_markdown = state.get("flowsheet", "")
        requirements_markdown = state.get("requirements", "")
        literature_markdown = state.get("literature_data", "")
        if not isinstance(flowsheet_markdown, str):
            flowsheet_markdown = str(flowsheet_markdown)
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)
        if not isinstance(literature_markdown, str):
            literature_markdown = str(literature_markdown)

        system_message = system_prompt(flowsheet_markdown, requirements_markdown, literature_markdown)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])
        chain = prompt.partial(system_message=system_message) | llm
        response = chain.invoke(state.get("messages", []))

        simulation_markdown = response.content if isinstance(response.content, str) else str(response.content)

        print(simulation_markdown)

        existing_validation = state.get("validation_results", "")
        if not isinstance(existing_validation, str):
            existing_validation = str(existing_validation or "")
        validation_segments = []
        if existing_validation.strip():
            validation_segments.append(existing_validation.strip())
        validation_segments.append(simulation_markdown.strip())
        updated_validation = "\n\n".join(validation_segments)

        return {
            "validation_results": updated_validation,
            "process_simulator_report": simulation_markdown,
            "messages": [response],
        }

    return process_simulator


def system_prompt(flowsheet_markdown: str, requirements_markdown: str, literature_markdown: str) -> str:
    return f"""
# ROLE
You are a Senior Process Simulation Engineer. Your task is to complete a preliminary, steady-state Heat and Material Balance (H&MB) using the provided flowsheet summary, requirements, and literature data.

# TASK
Create a markdown table that summarizes the thermodynamic conditions and compositions for each process stream. Present the data in a clear, engineer-friendly format suitable for downstream validation.

# OUTPUT FORMAT
Structure your Markdown exactly as follows:
```
## Stream Summary
| Property | Stream 1 | Stream 2 | Stream 3 |
|----------|----------|----------|----------|
| Temperature (°C) | ... | ... | ... |
| Pressure (bar) | ... | ... | ... |
| Mass Flow (kg/h) | ... | ... | ... |
| Composition: Component A | ... | ... | ... |
| Composition: Component B | ... | ... | ... |
| Composition: Component C | ... | ... | ... |
| Notes | ... | ... | ... |
```
- The first column lists properties. Subsequent columns correspond to each stream (use the stream IDs from the flowsheet connections).
- Include all relevant components mentioned in the requirements or literature.
- Add a “Notes” row with key assumptions or balances.
- If a value is unknown, provide a reasonable engineering estimate and mark it with `(est.)`.

# DATA FOR ANALYSIS
---
**FLOWSHEET SUMMARY (Markdown):**
{flowsheet_markdown}

**REQUIREMENTS SUMMARY (Markdown):**
{requirements_markdown}

**LITERATURE SUMMARY (Markdown):**
{literature_markdown}

# FINAL MARKDOWN OUTPUT:
"""
