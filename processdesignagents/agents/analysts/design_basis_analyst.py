from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv

load_dotenv()


def create_design_basis_analyst(llm):
    def design_basis_analyst(state: DesignState) -> DesignState:
        """Design Basis Analyst: Converts requirements into a structured design basis summary."""
        print("\n# Design Basis\n")

        problem_statement = state.get("problem_statement", "")
        requirements_markdown = state.get("requirements", "")
        selected_concept_details = state.get("selected_concept_details", "")
        selected_concept_name = state.get("selected_concept_name", "")
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)
        if not isinstance(selected_concept_details, str):
            selected_concept_details = str(selected_concept_details)
        if not isinstance(selected_concept_name, str):
            selected_concept_name = str(selected_concept_name)

        system_message = system_prompt(
            problem_statement,
            requirements_markdown,
            selected_concept_name,
            selected_concept_details,
        )

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

        design_basis_markdown = (
            response.content if isinstance(response.content, str) else str(response.content)
        )

        print(design_basis_markdown)

        return {
            "design_basis": design_basis_markdown,
            "messages": [response],
        }

    return design_basis_analyst


def system_prompt(
    problem_statement: str,
    requirements_markdown: str,
    concept_name: str,
    concept_details_markdown: str,
) -> str:
    return f"""
# ROLE:
You are a senior process engineer with 20 years of experience in writing process design basis of various process unit and plant. Your role is translating high-level requirements and process concepts into an actionable design basis.

# TASK:
Prepare a concise design basis that can guide downstream process simulation and equipment sizing work. Reflect the original problem statement, the extracted process requirements, and the selected concept briefing provided by upstream analysts.

# INSTRUCTIONS:
1. **Synthesize Context:** Combine explicit data from the requirements with engineering judgement to fill gaps. Flag every assumption.
2. **Quantify Carefully:** Provide units (SI preferred) and operating modes (continuous, batch, campaign, etc.) whenever flow rates or conditions are mentioned.
3. **Highlight Constraints:** Separate contractual/mandatory constraints from working assumptions.
4. **Mark Unknowns:** If information is missing, state `Not specified` and explain how it affects the design.
5. **Leverage Concept Brief:** Use the supplied concept detail to anchor feed/product definitions, major process steps, and design scope. Do not contradict the chosen concept unless the requirements force an adjustment—if they do, state the conflict in Notes & Data Gaps.
6. **Extract Components:** List the chemical components than involve in the process, e.g. Hydrogen (H2), Oxygen (O2), Carbon Dioxide (CO2), etc.

# OUTPUT FORMAT:
Your Markdown must follow this exact structure:
```
## Executive Summary
- Process objective: <text>
- Design strategy: <text or `Not specified`>
- Key risks: <text or `Not specified`>

## Design Scope
- Battery limits: <description or `Not specified`>
- Operating mode: <continuous/batch/etc. or `Not specified`>
- Design horizon: <lifetime, turndown, or `Not specified`>

## Feed Specifications
| Stream | Description | Flow Rate | Composition | Key Conditions |
|--------|-------------|-----------|-------------|----------------|
| ... | ... | ... | ... | ... |

## Product Specifications
| Stream | Description | Production Rate | Quality Targets | Delivery Conditions |
|--------|-------------|-----------------|-----------------|---------------------|
| ... | ... | ... | ... | ... |

## Components
- <Component 1>
- <Component 2>
- ...

## Assumptions & Constraints
- <Assumption or constraint 1>
- <Assumption or constraint 2>

## Notes & Data Gaps
- <Outstanding questions or data needs>
```
# NEGATIVES
* Try your best to estimate the missing information, such as the quantity of feed or product specifications.

# REFERENCE MATERIAL:
---
**PROBLEM STATEMENT:**
{problem_statement}

**PROCESS REQUIREMENTS SUMMARY (Markdown):**
{requirements_markdown}

**SELECTED CONCEPT NAME:**
{concept_name or "Not provided"}

**SELECTED CONCEPT DETAIL (Markdown):**
{concept_details_markdown or "Not provided"}

# FINAL MARKDOWN OUTPUT:
"""
