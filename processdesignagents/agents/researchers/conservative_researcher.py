from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import json
import re

load_dotenv()


def create_conservative_researcher(quick_think_llm: str, llm):
    def conservative_researcher(state: DesignState) -> DesignState:
        """Conservative Researcher: Critiques concepts for practicality using LLM."""
        print("\n=========================== Conservatively Critiqued Concepts ===========================\n")

        concepts_markdown = _extract_markdown(state.get("research_concepts", {}))
        requirements_markdown = _extract_markdown(state.get("requirements", {}))
        system_message = system_prompt(concepts_markdown, requirements_markdown)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])
        chain = prompt.partial(system_message=system_message) | llm
        response = chain.invoke(state.get("messages", []))

        critique_markdown = response.content if isinstance(response.content, str) else str(response.content)
        concept_blocks = _split_concept_sections(critique_markdown)

        print("Applied conservative critiques to research concepts.")
        if not concept_blocks:
            print("- No concept sections detected")
        for title, block in concept_blocks.items():
            score = _extract_score(block)
            risks = _extract_bullets(block, heading="Risks")
            print(f"---\nConcept: {title}")
            print(f"Risks: {', '.join(risks) if risks else 'N/A'}")
            print(f"Feasibility Score: {score if score is not None else 'N/A'}")

        return {
            "research_concepts": {
                "markdown": critique_markdown,
                "concepts": concept_blocks,
            },
            "messages": [response],
        }

    return conservative_researcher


def _extract_markdown(section: object) -> str:
    if isinstance(section, dict):
        if "markdown" in section and isinstance(section["markdown"], str):
            return section["markdown"]
        return json.dumps(section, indent=2, default=str)
    if isinstance(section, str):
        return section
    return str(section)


def _split_concept_sections(markdown_text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current_title: str | None = None
    current_lines: list[str] = []

    for line in markdown_text.splitlines():
        heading_match = re.match(r"^##\s+(.*)", line.strip())
        if heading_match:
            if current_title is not None:
                sections[current_title] = "\n".join(current_lines).strip()
            current_title = heading_match.group(1).strip()
            current_lines = []
        elif current_title is not None:
            current_lines.append(line)

    if current_title is not None:
        sections[current_title] = "\n".join(current_lines).strip()

    return sections


def _extract_score(section_text: str) -> int | None:
    cleaned = section_text.replace("**", "")
    match = re.search(r"Feasibility Score\s*[:\-]\s*(\d+)", cleaned, re.IGNORECASE)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return None
    return None


def _extract_bullets(section_text: str, heading: str) -> list[str]:
    pattern = re.compile(rf"###\s*{re.escape(heading)}\s*(.*?)\n(?=###|$)", re.IGNORECASE | re.DOTALL)
    match = pattern.search(section_text)
    if not match:
        return []

    bullets: list[str] = []
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if stripped.startswith("-"):
            bullets.append(stripped[1:].strip())
    return bullets


def system_prompt(concepts_markdown: str, requirements_markdown: str) -> str:
    return f"""
# ROLE
You are a Principal Technology Analyst at a chemical venture capital firm. Your job is to conduct rigorous due diligence on innovative process technologies to assess their investment potential. You are an expert in evaluating technical feasibility, market viability, and operational risk.

# TASK
Critically evaluate each of the provided process concepts. For each one, augment the existing information with a detailed analysis of its risks, a calculated feasibility score, and clear, actionable recommendations. Your analysis must consider the given requirements and constraints. The output must be a Markdown report.

# FORMAT
For each concept, produce a section with the following structure:
```
## <Concept Name>
**Feasibility Score:** <integer 1-10>

### Risks
- Technical Risk: ...
- Economic Risk: ...
- Safety Risk: ...

### Recommendations
- ...
- ...
```
Include exactly the same number of concept sections as provided in the input.

# DATA FOR ANALYSIS
---
**CONCEPTS (Markdown):**
{concepts_markdown}

**REQUIREMENTS / CONSTRAINTS (Markdown):**
{requirements_markdown}

# FINAL MARKDOWN OUTPUT:
"""
