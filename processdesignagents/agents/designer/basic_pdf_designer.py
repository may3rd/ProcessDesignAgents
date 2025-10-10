from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import re

load_dotenv()


def create_basic_pdf_designer(llm):
    def basic_pdf_designer(state: DesignState) -> DesignState:
        """Basic PDF Designer: Synthesizes preliminary flowsheet consistent with the detailed concept and design basis."""
        print("\n=========================== Basic PDF Design ===========================\n")

        requirements_markdown = state.get("requirements", "")
        selected_concept_name = state.get("selected_concept_name", "")
        concept_details_markdown = state.get("selected_concept_details", "")
        design_basis_markdown = state.get("design_basis", "")
        
        if not isinstance(concept_details_markdown, str):
            concept_details_markdown = str(concept_details_markdown)
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)
        if not isinstance(selected_concept_name, str):
            selected_concept_name = str(selected_concept_name)
        if not isinstance(design_basis_markdown, str):
            design_basis_markdown = str(design_basis_markdown)

        selected_concept_title = selected_concept_name.strip() or "Unnamed Concept"
        print(f"Selected concept for design: {selected_concept_title}")

        system_message = system_prompt(
            selected_concept_title,
            concept_details_markdown,
            requirements_markdown,
            design_basis_markdown,
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])
        chain = prompt.partial(system_message=system_message) | llm
        response = chain.invoke(state.get("messages", []))

        flowsheet_markdown = response.content if isinstance(response.content, str) else str(response.content)

        print(f"Synthesized flowsheet for {selected_concept_title}.")
        print("---")
        print(flowsheet_markdown)
        print("---")

        return {
            "flowsheet": flowsheet_markdown,
            "designer_report": flowsheet_markdown,
            "messages": [response],
        }

    return basic_pdf_designer


def system_prompt(
    concept_name: str,
    concept_details: str,
    requirements: str,
    design_basis: str,
) -> str:
    return f"""
# ROLE
You are a senior process design engineer. Your task is to create a conceptual process flowsheet based on a selected design concept, technical requirements, and supporting literature.

# TASK
Synthesize a preliminary process flowsheet for the selected concept: '{concept_name}'. The flowsheet must align with the approved design basis and highlight how the concept executes that basis.

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
<Paragraphs describing the process flow>
```
Ensure the tables are complete and readable.

Units ID, e.g. T-101, E-101, C-101, etc.
Connections ID, 1001, 1002, etc.
Reference any design basis assumptions directly in the summary or notes.

# DATA FOR ANALYSIS
---
**SELECTED CONCEPT:**
{concept_name}

**DETAILED CONCEPT BRIEF:**
{concept_details}

**REQUIREMENTS SUMMARY:**
{requirements}

**DESIGN BASIS (Markdown):**
{design_basis}

# FINAL MARKDOWN OUTPUT:
"""
