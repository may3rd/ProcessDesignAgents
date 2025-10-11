from __future__ import annotations

import re
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv

load_dotenv()


def create_concept_detailer(llm):
    def concept_detailer(state: DesignState) -> DesignState:
        """Concept Detailer: Picks the highest-feasibility concept and elaborates it for downstream design."""
        print("\n# Concept Selection\n")

        concepts_markdown = state.get("research_concepts", "")
        if not isinstance(concepts_markdown, str):
            concepts_markdown = str(concepts_markdown)
        requirements_markdown = state.get("requirements", "")
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)

        concepts = _split_concepts(concepts_markdown)
        if not concepts:
            raise ValueError("Concept detailer could not find any concept sections to evaluate.")

        best_title, best_section, best_score = _select_best_concept(concepts)
        print(f"Chosen concept: {best_title} (Feasibility Score: {best_score if best_score is not None else 'N/A'})")

        system_message = system_prompt(best_title, best_section, requirements_markdown)

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a helpful AI Assistant, collaborating with other assistants."
                "\n{system_message}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ])

        chain = prompt.partial(system_message=system_message) | llm
        response = chain.invoke(state.get("messages", []))

        detail_markdown = response.content if isinstance(response.content, str) else str(response.content)

        print("Prepared detailed concept brief.")
        print(detail_markdown)

        return {
            "selected_concept_details": detail_markdown,
            "selected_concept_name": best_title,
            "messages": [response],
        }

    return concept_detailer


def _split_concepts(markdown_text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_title: str | None = None
    current_lines: list[str] = []

    for line in markdown_text.splitlines():
        heading_match = re.match(r"^##\s+(.*)", line.strip())
        if heading_match:
            if current_title is not None:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = heading_match.group(1).strip()
            current_lines = []
        elif current_title is not None:
            current_lines.append(line)

    if current_title is not None:
        sections.append((current_title, "\n".join(current_lines).strip()))

    return sections


def _select_best_concept(concepts: list[tuple[str, str]]) -> tuple[str, str, int | None]:
    best_tuple = concepts[0]
    best_score: int | None = _extract_score(best_tuple[1])

    for title, section in concepts[1:]:
        score = _extract_score(section)
        if score is None:
            continue
        if best_score is None or score > best_score:
            best_tuple = (title, section)
            best_score = score

    return best_tuple[0], best_tuple[1], best_score


def _extract_score(section_text: str) -> int | None:
    cleaned = section_text.replace("**", "")
    match = re.search(r"Feasibility Score\s*[:\-]\s*(\d+)", cleaned, re.IGNORECASE)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return None
    return None


def system_prompt(concept_name: str, concept_section: str, requirements_markdown: str) -> str:
    return f"""
# ROLE
You are an experienced conceptual process designer. Your task is to prepare an in-depth brief for the selected concept so downstream engineers can establish a design basis.

# TASK
Using the chosen concept description and the overarching requirements, elaborate on the process flow, major equipment, operating envelopes, and key risks. Clarify the engineering rationale behind each element.

# OUTPUT FORMAT
Respond with Markdown using the exact structure below:
```
## Concept Summary
- Name: {concept_name} <without "Concept #" prefix>
- Intent: <succinct value proposition>
- Feasibility Score (from review): <value or `Not provided`>

## Process Narrative
<2-3 paragraphs describing feed preparation, core transformation steps, separations, and utilities.>

## Major Equipment & Roles
| Equipment | Function | Critical Operating Notes |
|-----------|----------|--------------------------|
| ... | ... | ... |

## Operating Envelope
- Design capacity: <value or `TBD`> (include units/basis)
- Key pressure levels: <notes>
- Key temperature levels: <notes>
- Special utilities / additives: <notes>

## Risks & Safeguards
- <primary risk> — <proposed safeguard or mitigation>
- <primary risk> — <proposed safeguard or mitigation>

## Data Gaps & Assumptions
- <information still needed or assumptions made>
```
Ensure every list or table entry is specific and actionable. If data is missing, flag it explicitly with `TBD` and add a short explanation.

# SOURCE MATERIAL
---
**SELECTED CONCEPT (Markdown):**
{concept_section}

**HIGH-LEVEL REQUIREMENTS:**
{requirements_markdown}

# FINAL MARKDOWN OUTPUT:
"""
