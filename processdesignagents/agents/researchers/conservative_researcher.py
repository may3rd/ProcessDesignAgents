from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import re

load_dotenv()


def create_conservative_researcher(llm):
    def conservative_researcher(state: DesignState) -> DesignState:
        """Conservative Researcher: Critiques concepts for practicality using LLM."""
        print("\n=========================== Conservatively Critiqued Concepts ===========================\n")

        concepts_markdown = state.get("research_concepts", "")
        requirements_markdown = state.get("requirements", "")
        if not isinstance(concepts_markdown, str):
            concepts_markdown = str(concepts_markdown)
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)
        system_message = system_prompt(concepts_markdown, requirements_markdown)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])
        chain = prompt.partial(system_message=system_message) | llm
        response = chain.invoke(state.get("messages", []))

        critique_markdown = response.content if isinstance(response.content, str) else str(response.content)
        concept_blocks = _split_concept_sections(critique_markdown)
        if not concept_blocks:
            raise ValueError("Conservative critique report must include at least one concept section.")

        print("Applied conservative critiques to research concepts.")
        if not concept_blocks:
            print("- No concept sections detected")
        for title, block in concept_blocks.items():
            normalized_block = block
            missing_sections = []
            no_risk = False
            no_recommendation = False
            if "### Risks" not in normalized_block:
                no_risk = True
            if "### Recommendations" not in normalized_block:
                no_recommendation = True
            if no_risk and no_recommendation:
                continue
            if no_risk:
                missing_sections.append("Risks")
                normalized_block += "\n\n### Risks\n- Not provided by conservative reviewer.\n"
            if no_recommendation:
                missing_sections.append("Recommendations")
                normalized_block += "\n\n### Recommendations\n- Not provided by conservative reviewer.\n"
            if missing_sections:
                print(
                    f"[!] Concept '{title}' missing sections: {', '.join(missing_sections)}. Added default placeholders."
                )
                concept_blocks[title] = normalized_block
            score = _extract_score(normalized_block)
            risks = _extract_bullets(normalized_block, heading="Risks")
            print(f"---\n{title}")
            print(f"Risks: {', '.join(risks) if risks else 'N/A'}")
            print(f"Feasibility Score: {score if score is not None else 'N/A'}")

        return {
            "research_concepts": critique_markdown,
            "conservative_research_report": critique_markdown,
            "messages": ["Conservative Researcher - Completed"],
        }

    return conservative_researcher

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

# NEGATIVES

* DO NOT output any other section, only evaluation report

# DATA FOR ANALYSIS
---
**CONCEPTS (Markdown):**
{concepts_markdown}

**REQUIREMENTS / CONSTRAINTS (Markdown):**
{requirements_markdown}

# FINAL MARKDOWN OUTPUT:
"""
