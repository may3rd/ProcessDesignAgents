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

# EXAMPLE:
For a heat exchanger that cools an ethanol stream from 80 C to 40 C using cooling water, document the inlet and outlet temperatures, define ethanol and cooling water in the component list, and state any assumed flow rates or constraints you impose to close the basis.

# MARKDOWN TEMPLATE:
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

**EXPECTED MARKDOWN OUTPUT:**
<md_output>
## Executive Summary
- Process objective: Cool 95 wt% ethanol feed from 80 degC to 40 degC before storage
- Design strategy: Shell-and-tube exchanger using plant cooling water loop
- Key risks: Thermal shock in downstream storage if duty spikes

## Design Scope
- Battery limits: From pump discharge (hot ethanol) to cooled ethanol storage nozzle
- Operating mode: Continuous
- Design horizon: 15-year service with 30% turndown capability

## Feed Specifications
| Stream | Description | Flow Rate | Composition | Key Conditions |
|--------|-------------|-----------|-------------|----------------|
| F-101 | Hot ethanol feed | 10,000 kg/h | Ethanol 95 wt%, Water 5 wt% | 80 degC, 1.5 barg |

## Product Specifications
| Stream | Description | Production Rate | Quality Targets | Delivery Conditions |
|--------|-------------|-----------------|-----------------|---------------------|
| P-101 | Cooled ethanol product | 10,000 kg/h | Ethanol >=95 wt% | 40 degC, 1.3 barg |

## Components
- Ethanol (C2H6O)
- Water (H2O)
- Cooling water (utility)

## Assumptions & Constraints
- Assume constant ethanol flow rate of 10,000 kg/h from upstream blender.
- Cooling water supply available at 25 degC and max return of 35 degC.
- Maintain minimum 5 degC approach temperature on hot side to avoid ice formation.

## Notes & Data Gaps
- Confirm upstream ethanol composition and any fouling inhibitors.
- Need cooling water availability confirmation during summer design conditions.
</md_output>

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

"""
