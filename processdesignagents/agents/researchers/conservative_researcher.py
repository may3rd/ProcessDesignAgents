from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import re

load_dotenv()


def create_conservative_researcher(llm):
    def conservative_researcher(state: DesignState) -> DesignState:
        """Conservative Researcher: Critiques concepts for practicality using LLM."""
        print("\n# Conservatively Critiqued Concepts")

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
        # concept_blocks = _split_concept_sections(critique_markdown)
        
        print(critique_markdown)

        return {
            "research_concepts": critique_markdown,
            "messages": [response],
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
# CONTEXT
From the 'REQUIREMENTS / CONSTRAINTS' and 'CONCEPTS' input, we are going to evaluate the design concept and other information and calculate a feasibily score.

# ROLE
You are a Principal Technology Analyst at a chemical venture capital firm. Your job is to conduct rigorous due diligence on innovative process technologies to assess their investment potential. You are an expert in evaluating technical feasibility, market viability, and operational risk.

# TASK
Critically evaluate each of the provided process concepts. For each one, augment the existing information with a detailed analysis of its risks, a calculated feasibility score, and clear, actionable recommendations. Your analysis must consider the given requirements and constraints. The output must be a Markdown report.

# INSTRUCTIONS
1. Review the REQUIREMENTS / CONSTRAINTS and the source CONCEPTS to understand performance targets, boundary conditions, and any hard show-stoppers.
2. For each concept, test its claims against conservative assumptions: highlight technology maturity limits, scale-up hurdles, regulatory concerns, and hidden cost drivers.
3. Assign a single integer Feasibility Score from 1 (very high risk) to 10 (ready for near-term deployment) based on technical robustness, economic viability, safety, and alignment with requirements.
4. Populate the Risks subsection with at least three bullets covering technical, economic, and safety/operational themes; add more if material gaps exist.
5. Provide actionable Recommendations that mitigate the highlighted risks or outline essential validation steps (pilot programs, vendor vetting, contingency designs).
6. Preserve the section order and formatting exactly as defined in the Markdown template; do not add extra narrative outside the concept sections.

# MARKDOWN TEMPLATE:
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

**EXPECTED MARKDOWN OUTPUT:**
<md_output>
## Concept 1: Ethanol Cooling Exchanger Skid
**Feasibility Score:** 7

### Risks
- Technical Risk: Potential fouling on cooling water side increases approach temperature.
- Economic Risk: Utility cost rises if cooling water demand exceeds base allocation.
- Safety Risk: Tube failure could allow ethanol in cooling water return leading to fire hazard.

### Recommendations
- Implement periodic backflush and water-side chemical treatment.
- Install hydrocarbon detectors on cooling water return header.
</md_output>

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
