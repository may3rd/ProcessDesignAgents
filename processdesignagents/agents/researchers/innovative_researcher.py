from __future__ import annotations

import re

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from dotenv import load_dotenv

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import jinja_raw

load_dotenv()


def create_innovative_researcher(llm):
    def innovative_researcher(state: DesignState) -> DesignState:
        """Innovative Researcher: Proposes novel process concepts using LLM."""
        print("\n# Innovative Research Concepts", flush=True)

        requirements_summary = state.get("requirements", "")
        if not isinstance(requirements_summary, str):
            requirements_summary = str(requirements_summary)
        base_prompt = innovative_researcher_prompt(requirements_summary)

        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)

        chain = prompt | llm
        response = chain.invoke({"messages": list(state.get("messages", []))})

        research_markdown = (
            response.content if isinstance(response.content, str) else str(response.content)
        ).strip()
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
        if len(research_markdown) < 10:
            print(f"The response is too short, exit(-1)")
            exit(-1)
        print(research_markdown, flush=True)

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


def innovative_researcher_prompt(requirements_markdown: str) -> ChatPromptTemplate:
    system_content = f"""
You are a Senior R&D Process Engineer specializing in conceptual design and process innovation. Your expertise lies in brainstorming novel, sustainable, and efficient chemical processes to solve a given problem.

**Context:**

  * You will be provided with a set of `REQUIREMENTS` for a new or modified chemical process.
  * Your task is to generate multiple distinct process concepts that fulfill these requirements.
  * The concepts you generate will be evaluated by a critique agent to determine the most feasible option for further design.
  * The concepts must span a range of technological maturity, including conventional industry standards, innovative improvements, and state-of-the-art approaches.

**Instructions:**

  * Analyze the provided `REQUIREMENTS` to fully understand the core objective, key components, and constraints.
  * Generate between 3 and 6 distinct process concepts that meet the requirements.
  * Structure each concept with a descriptive name, a concise paragraph explaining the idea, a bulleted list of essential unit operations, and a bulleted list of its key benefits.
  * Ensure the range of concepts includes at least one conventional/standard process, one innovative/complex process, and one state-of-the-art process.
  * Your final output must be a PURE Markdown document. Do not add any introductory text, concluding remarks, or formatting (like code blocks) that is not part of the specified template.

-----

  * **REQUIREMENTS:**
    ```
    {{requirements}}
    ```

-----

**Example:**

  * **REQUIREMENTS:**

    ```
    "We need a process to cool a hot ethanol stream from 80°C to 40°C. The primary cooling utility available is the plant's standard cooling water loop."
    ```

  * **Response:**

    ```markdown
    ---
    ## Concept 1: Shell-and-Tube Ethanol Cooler
    **Description:** A standard shell-and-tube heat exchanger is used to cool the hot ethanol stream from 80°C down to 40°C. The process fluid (ethanol) flows on one side while utility cooling water from the existing plant loop flows on the other side to remove the heat. This represents the most common and straightforward industry approach.
    **Unit Operations:**
    - Feed/Product Pumps
    - Shell-and-Tube Heat Exchanger
    **Key Benefits:**
    - Proven, reliable technology with low operational and capital cost.
    - Simple to design, operate, and maintain with readily available parts.

    ---
    ## Concept 2: Plate-and-Frame Modular Cooler
    **Description:** This concept uses a compact plate-and-frame heat exchanger, potentially on a pre-fabricated skid, for higher thermal efficiency. The modular design allows for staged plates to optimize heat transfer and enables quick disassembly for cleaning or capacity expansion, offering an improvement over traditional designs.
    **Unit Operations:**
    - Modular Plate-and-Frame Exchanger
    - Bypass and Isolation Valving
    **Key Benefits:**
    - Higher heat-transfer coefficients reduce the required surface area and footprint.
    - Plates can be easily added, removed, or cleaned offline, minimizing downtime.

    ---
    ## Concept 3: Heat Pump Assisted Cooling
    **Description:** A state-of-the-art approach using a vapor-compression refrigeration cycle (heat pump) to recover low-grade heat from the ethanol stream. This heat is then upgraded and rejected elsewhere, allowing the ethanol to be cooled to sub-ambient temperatures if needed. This decouples the process from the limitations of the cooling water temperature.
    **Unit Operations:**
    - Heat Pump Evaporator/Condenser
    - Chilled-Water Loop Heat Exchanger
    - Cooling Tower Interface
    **Key Benefits:**
    - Achieves product temperatures below the cooling water temperature.
    - Reduces load on the main cooling tower, especially during summer peaks.
    ```

-----

**Your Task:** Output ONLY a valid Markdown document, **not in code block**, containing 3 to 7 distinct process concepts based on the provided `REQUIREMENTS`. Each concept must precisely follow the structure defined above, with each concept separated by a horizontal rule (`---`).
"""

    human_content = f"""
# DATA FOR ANALYSIS:
---
**REQUIREMENTS:**
{requirements_markdown}

"""

    messages = [
        SystemMessagePromptTemplate.from_template(
            jinja_raw(system_content),
            template_format="jinja2",
        ),
        HumanMessagePromptTemplate.from_template(
            jinja_raw(human_content),
            template_format="jinja2",
        ),
    ]

    return ChatPromptTemplate.from_messages(messages)
