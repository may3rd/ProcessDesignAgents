from __future__ import annotations

from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import json
import re

load_dotenv()


def create_process_simulator(deep_think_llm: str, llm):
    def process_simulator(state: DesignState) -> DesignState:
        """Process Simulator: Generates preliminary Heat and Material Balance (H&MB) from flowsheet."""
        print("\n=========================== Create Prelim H&MB ===========================")

        flowsheet_markdown = _extract_markdown(state.get("flowsheet", {}))
        requirements_markdown = _extract_markdown(state.get("requirements", {}))
        literature_markdown = _extract_markdown(state.get("literature_data", {}))

        system_message = system_prompt(flowsheet_markdown, requirements_markdown, literature_markdown)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])
        chain = prompt.partial(system_message=system_message) | llm
        response = chain.invoke(state.get("messages", []))

        simulation_markdown = response.content if isinstance(response.content, str) else str(response.content)

        print(simulation_markdown)

        return {
            "validation_results": {
                "stream_summary_markdown": simulation_markdown,
            },
            "messages": [response],
        }

    return process_simulator


def _extract_markdown(section: object) -> str:
    if isinstance(section, dict):
        if "markdown" in section and isinstance(section["markdown"], str):
            return section["markdown"]
        return json.dumps(section, indent=2, default=str)
    if isinstance(section, str):
        return section
    return str(section)


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
