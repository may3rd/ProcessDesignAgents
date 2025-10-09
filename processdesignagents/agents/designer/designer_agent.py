from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.markdown_validators import require_sections, require_table_headers
from dotenv import load_dotenv
import json
import re

load_dotenv()


def create_designer_agent(llm):
    def designer_agent(state: DesignState) -> DesignState:
        """Designer Agent: Synthesizes preliminary flowsheet from research concepts."""
        print("\n=========================== Selected Concept ===========================\n")

        concepts_markdown = _extract_markdown(state.get("research_concepts", {}))
        requirements_markdown = _extract_markdown(state.get("requirements", {}))
        literature_markdown = _extract_markdown(state.get("literature_data", {}))

        selected_concept_title = _select_top_concept(concepts_markdown)
        print(f"Selected concept for design: {selected_concept_title}")

        system_message = system_prompt(selected_concept_title, requirements_markdown, literature_markdown)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])
        chain = prompt.partial(system_message=system_message) | llm
        response = chain.invoke(state.get("messages", []))

        flowsheet_markdown = response.content if isinstance(response.content, str) else str(response.content)
        require_sections(
            flowsheet_markdown,
            ["Flowsheet Summary", "Units", "Connections", "Overall Description"],
            "Flowsheet design report",
        )
        require_table_headers(
            flowsheet_markdown,
            ["ID", "Name", "Type", "Description"],
            "Flowsheet units table",
        )
        require_table_headers(
            flowsheet_markdown,
            ["ID", "Stream", "From", "To", "Description"],
            "Flowsheet connections table",
        )

        print(f"Synthesized flowsheet for {selected_concept_title}.")
        print("---")
        print(flowsheet_markdown)
        print("---")

        return {
            "flowsheet": {
                "markdown": flowsheet_markdown,
                "concept": selected_concept_title,
            },
            "designer_report": flowsheet_markdown,
            "messages": [response],
        }

    return designer_agent


def _extract_markdown(section: object) -> str:
    if isinstance(section, dict):
        if "markdown" in section and isinstance(section["markdown"], str):
            return section["markdown"]
        return json.dumps(section, indent=2, default=str)
    if isinstance(section, str):
        return section
    return str(section)


def _select_top_concept(concepts_markdown: str) -> str:
    titles = []
    for line in concepts_markdown.splitlines():
        match = re.match(r"^##\s+(.*)", line.strip())
        if match:
            titles.append(match.group(1).strip())
    return titles[0] if titles else "Unnamed Concept"


def system_prompt(concept_name: str, requirements_markdown: str, literature_markdown: str) -> str:
    return f"""
# ROLE
You are a senior process design engineer. Your task is to create a conceptual process flowsheet based on a selected design concept, technical requirements, and supporting literature.

# TASK
Synthesize a preliminary process flowsheet for the selected concept: '{concept_name}'.
Incorporate requirements from the Markdown summary and literature insights provided below. Your output must be a Markdown document.

# FORMAT
Structure your Markdown exactly as follows:
```
## Flowsheet Summary
- Concept: <concept name>
- Objective: <one-sentence objective>
- Key Drivers: <one sentence>

## Units
| ID | Name | Type | Description |
|----|------|------|-------------|
| ... | ... | ... | ... |

## Connections
| ID | Stream | From | To | Description |
| --- |--------|------|----|-------------|
| ... | ... | ... | ... | ... |

## Overall Description
<One paragraph describing the process flow>
```
Ensure the tables are complete and readable.

Units ID, e.g. T-101, E-101, C-101, etc.
Connections ID, 1001, 1002, etc.

# DATA FOR ANALYSIS
---
**SELECTED CONCEPT:**
{concept_name}

**REQUIREMENTS SUMMARY:**
{requirements_markdown}

**LITERATURE SUMMARY:**
{literature_markdown}

# FINAL MARKDOWN OUTPUT:
"""
