from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.markdown_validators import require_heading_prefix
from dotenv import load_dotenv
import json
import re

load_dotenv()


def create_innovative_researcher(llm):
    def innovative_researcher(state: DesignState) -> DesignState:
        """Innovative Researcher: Proposes novel process concepts using LLM."""
        print("\n=========================== Innovative Research Concepts ===========================\n")

        requirements_summary = _extract_markdown(state.get("requirements", {}))
        literature_summary = _extract_markdown(state.get("literature_data", {}))
        system_message = system_prompt(requirements_summary, literature_summary)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])

        chain = prompt.partial(system_message=system_message) | llm
        response = chain.invoke(state.get("messages", []))

        research_markdown = response.content if isinstance(response.content, str) else str(response.content)
        require_heading_prefix(research_markdown, "Concept", "Innovative concepts report")
        concept_names = _extract_concept_names(research_markdown)
        if len(concept_names) < 3:
            raise ValueError("Innovative concepts report must include at least three concept sections.")

        print("Generated innovative research concepts.")
        print("\n--- Concept Names ---")
        if concept_names:
            for concept_name in concept_names:
                print(f"- {concept_name}")
        else:
            print("- (No concept headings detected)")

        return {
            "research_concepts": {
                "markdown": research_markdown,
                "concept_names": concept_names,
            },
            "innovative_research_report": research_markdown,
            "messages": [response],
        }

    return innovative_researcher


def _extract_markdown(section: object) -> str:
    if isinstance(section, dict):
        if "markdown" in section and isinstance(section["markdown"], str):
            return section["markdown"]
        return json.dumps(section, indent=2, default=str)
    if isinstance(section, str):
        return section
    return str(section)


def _extract_concept_names(markdown_text: str) -> list[str]:
    names: list[str] = []
    for line in markdown_text.splitlines():
        match = re.match(r"^##\s+(.*)", line.strip())
        if match:
            names.append(match.group(1).strip())
    return names


def system_prompt(requirements_markdown: str, literature_markdown: str) -> str:
    return f"""
# ROLE
You are a Senior R&D Process Engineer specializing in conceptual design and process innovation. Your expertise lies in brainstorming novel, sustainable, and efficient chemical processes.

# TASK
Based on the provided 'REQUIREMENTS' and 'LITERATURE DATA' summaries, generate 3 to 5 distinct process concepts. For each concept, provide a concise name, a clear description, the key unit operations involved, and its primary benefits.

The concepts you generate must includes the typical or standard process that widely used in refinery and petrochemical industy, more complex and innovative processes, and state-of-the-art processes.


# INSTRUCTIONS
1.  **Synthesize Data:** First, thoroughly analyze the 'REQUIREMENTS' and 'LITERATURE DATA' summaries to understand the core objective, key components, and known science.
2.  **Brainstorm Process Ideas:** Consider both conventional and unconventional approaches that align with the requirements and literature insights.
3.  **Develop Concepts:** For each of your three ideas, structure it with a descriptive name, a compact paragraph explaining the concept, a list of the essential unit operations, and a list of its key advantages.
4.  **Format Output:** Your final output MUST be Markdown with the following structure repeated for each concept:
    ```
    ## Concept N: <Descriptive Name>
    **Description:** <one paragraph summarizing the idea>
    **Unit Operations:**
    - <unit operation>
    - ...
    **Key Benefits:**
    - <benefit>
    - ...
    ```
    Ensure there are exactly three concept sections (Concept 1, Concept 2, Concept 3).

# DATA FOR ANALYSIS
---
**REQUIREMENTS SUMMARY (Markdown):**
{requirements_markdown}

**LITERATURE DATA SUMMARY (Markdown or JSON):**
{literature_markdown}

# FINAL MARKDOWN OUTPUT:
"""
