from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import re

load_dotenv()


def create_innovative_researcher(llm):
    def innovative_researcher(state: DesignState) -> DesignState:
        """Innovative Researcher: Proposes novel process concepts using LLM."""
        print("\n---\n# Innovative Research Concepts")

        requirements_summary = state.get("requirements", "")
        if not isinstance(requirements_summary, str):
            requirements_summary = str(requirements_summary)
        system_message = system_prompt(requirements_summary)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])

        chain = prompt.partial(system_message=system_message) | llm
        response = chain.invoke(state.get("messages", []))

        research_markdown = response.content if isinstance(response.content, str) else str(response.content)
        # concept_names = _extract_concept_names(research_markdown)
        # if len(concept_names) < 3:
        #     raise ValueError("Innovative concepts report must include at least three concept sections.")

        # print("Generated innovative research concepts.")
        # print("\n--- Concept Names ---")
        # if concept_names:
        #     for concept_name in concept_names:
        #         print(f"- {concept_name}")
        # else:
        #     print("- (No concept headings detected)")

        print(research_markdown)

        return {
            "research_concepts": research_markdown,
            "messages": [response],
        }

    return innovative_researcher


def _extract_concept_names(markdown_text: str) -> list[str]:
    names: list[str] = []
    for line in markdown_text.splitlines():
        match = re.match(r"^##\s+(.*)", line.strip())
        if match:
            names.append(match.group(1).strip())
    return names


def system_prompt(requirements_markdown: str) -> str:
    return f"""
# CONTEXT
We are going to create a list of conceptual design of process unit. Each concopt includes the name, short description, list of unit operations, and key benefits. These concepts will be next criticize by other personal to weight the feasibilty of the concept that will be selected for further design.

# ROLE
You are a Senior R&D Process Engineer specializing in conceptual design and process innovation. Your expertise lies in brainstorming novel, sustainable, and efficient chemical processes.

# TASK
Based on the provided 'REQUIREMENTS' generating 3 to 6 distinct process concepts. For each concept, provide a concise name, a clear description, the key unit operations involved, and its primary benefits.

The concepts you generate must includes the typical or standard process that widely used in refinery and petrochemical industy, more complex and innovative processes, and state-of-the-art processes.

# INSTRUCTIONS
1.  **Synthesize Data:** First, thoroughly analyze the 'REQUIREMENTS', summaries to understand the core objective, key components, and known science.
2.  **Brainstorm Process Ideas:** Consider both conventional and unconventional approaches that align with the requirements insights.
3.  **Develop Concepts:** For each of your three ideas, structure it with a descriptive name, a compact paragraph explaining the concept, a list of the essential unit operations, and a list of its key advantages.
4.  **MARKDOWN TEMPLATE:** Your final output MUST be Markdown with the following structure repeated for each concept:
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
Ensure there are at least three concept sections.

# TARGET AUDIENCE
The target audince of this prompt is an agentic llm that will critically evaluate each of the provided process concepts.
---

**EXPECTED MARKDOWN OUTPUT:**
<md_output>
## Concept 1: Shell-and-Tube Ethanol Cooler
**Description:** Standard shell-and-tube exchanger cools hot ethanol from 80 degC to 40 degC using existing cooling water loop.
**Unit Operations:**
- Feed/product pumps
- Shell-and-tube heat exchanger
**Key Benefits:**
- Proven design with low execution risk
- Minimal footprint and easy maintenance

---

## Concept 2: Plate-and-Frame Modular Cooler
**Description:** Skid-mounted plate heat exchanger with staged plates to boost heat transfer and enable quick cleaning.
**Unit Operations:**
- Modular plate exchanger
- Bypass and isolation valves
**Key Benefits:**
- High heat-transfer coefficients reduce cooling water flow
- Plates can be cleaned offline without long downtime

---

## Concept 3: Heat Pump Assisted Cooling
**Description:** Vapor-compression chiller recovers heat from ethanol stream and rejects it to cooling tower, enabling sub-ambient product temperatures.
**Unit Operations:**
- Heat pump evaporator/condenser
- Chilled-water loop heat exchanger
- Cooling tower interface
**Key Benefits:**
- Reduces cooling water consumption in summer peaks
- Provides flexibility for future lower product temperature requirements
</md_output>

# DATA FOR ANALYSIS
---
**REQUIREMENTS SUMMARY (Markdown):**
{requirements_markdown}

"""
