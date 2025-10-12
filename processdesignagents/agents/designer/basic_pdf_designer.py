from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import re

load_dotenv()

def create_basic_pdf_designer(llm):
    def basic_pdf_designer(state: DesignState) -> DesignState:
        """Basic PDF Designer: Synthesizes preliminary flowsheet consistent with the detailed concept and design basis."""
        print("\n# Basic PDF Design")

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

        system_message = system_prompt(
            selected_concept_name,
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

        basic_pdf_markdown = response.content if isinstance(response.content, str) else str(response.content)

        print(basic_pdf_markdown)

        return {
            "basic_pdf": basic_pdf_markdown,
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
# CONTEXT
You receive vetted concept documentation, design basis, and requirements assembled by upstream teams. The sponsor expects a state-of-the-art flowsheet that showcases advanced integration, modularisation, and smart instrumentation suitable for rapid deployment. Your deliverable seeds downstream stream definition, equipment sizing, safety assessment, and project approval.

# TARGET AUDIENCE
- Stream definition, equipment, and safety agents relying on a consistent flowsheet backbone.
- Project sponsors and gate reviewers evaluating readiness of the selected concept.
- Operations stakeholders needing clear visibility into unit operations and connectivity.

# ROLE
You are a senior process design engineer with 20 years of experience in drafting process flow diagram (PDF) that represent the sequence of process steps of the selected concept. Your task is to create a conceptual process flowsheet based on a selected design concept, technical requirements, and design basis.

# TASK
Synthesize a preliminary process flowsheet using the provided 'REQUIREMENTS' and 'DESIGN BASIS'. The flowsheet must align with the approved design basis and highlight how the concept executes that basis.

# INSTRUCTIONS
1. **Digest inputs:** Extract boundary conditions, operating intent, and critical assumptions from the concept detail, requirements, and design basis.
2. **Promote innovation:** Embed state-of-the-art features (high-efficiency units, modular skids, digital monitoring, heat-integration strategies) wherever they reinforce the concept without contradicting provided data.
3. **Map operations:** Identify all major process units, utility systems, bypasses, and recycles; assign unique IDs consistent with plant conventions.
4. **Define connectivity:** Populate Units and Connections tables fully, ensuring every stream has a clear source, destination, and purpose tied to the advanced concept.
5. **Explain execution:** Use the narrative and notes to highlight innovative elements, automation hooks, and assumptions that downstream teams must honor.
6. **Adhere to template:** Follow the Markdown structure exactly—no extra sections, no missing fields.

# CRITICALS
- **MUST** return the full flowsheet in markdown format.
- Ensure the tables are complete and readable.
- The ID must be followed:
  *  Units ID, e.g. T-101, E-101, C-101, etc.
  *  Connections ID, 1001, 1002, etc.
- Reference any design basis assumptions directly in the summary or notes.

# MARKDOWN TEMPLATE:
Structure your Markdown exactly as follows:
```
## Flowsheet Summary
- Concept: <concept name without 'Concept #' prefix>
- Objective: <one-sentence objective>
- Key Drivers: <one sentence>

## Units
| ID | Name | Type | Description |
|----|------|------|-------------|
| ... | ... | ... | ... |

## Streams
| ID | Stream | From | To | Description |
| --- |--------|------|----|-------------|
| ... | ... | ... | ... | ... |

## Overall Description
<Paragraphs describing the process flow>

## Notes
- <note 1>
- <note 2>
- ...

```

# EXAMPLE
For a simple exchanger that cools ethanol from 80 C to 40 C using cooling water, include a single E-101 heat exchanger unit, show the warm ethanol feed entering and cooled ethanol product leaving, and note the cooling water supply and return connections.

**EXPECTED MARKDOWN OUTPUT:**
<md_output>
## Flowsheet Summary
- Concept: Ethanol Cooler Module
- Objective: Reduce hot ethanol from 80 degC to 40 degC using plant cooling water
- Key Drivers: Maintain storage temperature while minimising cooling water use

## Units
| ID | Name | Type | Description |
|----|------|------|-------------|
| E-101 | Ethanol Cooler | Shell-and-tube exchanger | Transfers heat from ethanol to cooling water |
| P-101 | Product Pump | Centrifugal pump | Boosts cooled ethanol to storage |
| U-201 | Cooling Water Loop | Utility header | Provides 25 degC cooling water supply |

## Connections
| ID | Stream | From | To | Description |
| --- |--------|------|----|-------------|
| 1001 | Hot ethanol feed | Upstream blender | E-101 | Ethanol at 80 degC and 1.5 barg |
| 1002 | Cooled ethanol | E-101 | P-101 | Product leaving exchanger at 40 degC |
| 1003 | Storage transfer | P-101 | Storage tank | Pumped ethanol to atmospheric tank |
| 2001 | CW supply | CW header | E-101 | Cooling water enters at 25 degC |
| 2002 | CW return | E-101 | CW header | Return water at 35 degC |

## Overall Description
Hot ethanol from the blender enters E-101 where heat is exchanged against plant cooling water. The cooled ethanol flows to P-101 for transfer to storage. Cooling water circulates from the utility header through E-101 and back to the return manifold.

## Notes
- Provide strainers on cooling water inlet to limit fouling.
- Include bypass line around E-101 for maintenance.
</md_output>

# DATA FOR ANALYSIS
---
**REQUIREMENTS:**
{requirements}

**DESIGN BASIS:**
{design_basis}

"""
