from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv

load_dotenv()


def create_stream_data_estimator(llm):
    def stream_data_estimator(state: DesignState) -> DesignState:
        """Stream Data Estimator: Generates stream and H&MB tables with estimated conditions."""
        print("\n# Stream Data Estimator\n")

        llm.temperature = 0.7
        
        basic_pfd_markdown = state.get("basic_pfd", "")
        requirements_markdown = state.get("requirements", "")
        design_basis_markdown = state.get("design_basis", "")
        concept_details_markdown = state.get("selected_concept_details", "")
        stream_template = state.get("basic_stream_data", "")

        system_message = system_prompt(
            basic_pfd_markdown,
            requirements_markdown,
            design_basis_markdown,
            concept_details_markdown,
            stream_template,
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])
        response = (prompt.partial(system_message=system_message) | llm).invoke(state.get("messages", []))

        markdown_output = response.content if isinstance(response.content, str) else str(response.content)

        print(markdown_output)

        return {
            "basic_stream_data": markdown_output,
            "basic_hmb_results": markdown_output,
            "messages": [response],
        }

    return stream_data_estimator


def system_prompt(
    basic_pfd_markdown: str,
    requirements_markdown: str,
    design_basis_markdown: str,
    concept_details_markdown: str,
    stream_template: str,
) -> str:
    return f"""
# CONTEXT
You receive the templated stream inventory, concept summary, and governing requirements from earlier design stages. The project needs first-pass operating conditions and reconciled balances so downstream sizing and analysis teams can proceed with credible data.

# TARGET AUDIENCE
- Equipment sizing agent deriving preliminary dimensions and duties.
- Process simulation specialists building detailed steady-state models.
- Concept reviewers validating feasibility and identifying data gaps.

# ROLE
You are a Senior Process Simulation Engineer. Generate estimated operating conditions for every process stream and summarize the overall heat and material balance.

# TASK
Using the provided information and the 'STREAM TEMPLATE', replace `<value>` placeholders with realistic estimates (include units). Highlight assumptions in notes. Present results strictly as Markdown.

# EXAMPLE
When refining a heat exchanger that cools ethanol from 80 C to 40 C with cooling water, estimate consistent temperatures and flow rates for the ethanol and cooling water streams, ensuring the heat removed from ethanol matches the heat absorbed by the utility and documenting any assumed specific heat values.

# INSTRUCTIONS
1. Review the STREAM TEMPLATE alongside the process description, requirements, and design basis to understand intended unit operations, utilities, and performance targets.
2. Replace every `<value>` placeholder with realistic estimates (include units) derived from energy and material balance reasoning; adjust temperatures, pressures, and flows so each unit operation is internally consistent.
3. Enforce conservation: total mass and key component rates entering any unit must equal the totals leaving unless a justified accumulation/consumption is documented in the Notes.
4. Cross-check the entire flowsheet so overall inputs equal overall outputs; when reconciling gaps, note the assumptions, calculation methods, or correction factors in the Notes and reference affected stream IDs.
5. Ensure each stream retains its identifier, name, and intent from the template; expand the table with additional property rows or component rows if the scenario requires them.
6. Confirm every composition row sums to 100 mol% (or 100 mass% if applicable) and highlight the chosen basis in the Notes when needed.
7. Return the completed Markdown exactly in the required format, including the `## Notes` section with concise bullet entries.

# CRITICALS
- **MUST** return the full stream data table in markdown format.

# MARKDOWN TEMPLATE:
Your Markdown output must follow this structure:
|          | 1001 | 1002 | 1003 | ... | <only show stream ID>
| Description | ------ | ------ | ------ | ----- |
| ---------- | ------ | ------ | ------ | ----- |
| Temperature (°C) | ... | ... | ... | ... |
| Pressure (barg) | ... | ... | ... | ... |
| Mass Flow (kg/h) | ... | ... | ... | ... |
| Key Component | (mol %) | (mol %) | (mol %) | ... |
| Component A | ... | ... | ... | ... | ... |
| Component B | ... | ... | ... | ... | ... |
| Component C | ... | ... | ... | ... | ... |

## Notes
- <note 1>
- <note 2>
- ...

---

**EXPECTED MARKDOWN OUTPUT:**
<md_output>
# Stream Data Table
|          | 1001 | 1002 | 2001 | 2002 |
| Description | Hot ethanol feed | Cooled ethanol product | Cooling water supply | Cooling water return |
| ---------- | ------ | ------ | ------ | ------ |
| Temperature (degC) | 80 | 40 | 25 | 35 |
| Pressure (barg) | 1.5 | 1.3 | 2.5 | 2.3 |
| Mass Flow (kg/h) | 10,000 | 10,000 | 24,000 | 24,000 |
| Key Component | (mol %) | (mol %) | (mol %) | (mol %) |
| Ethanol (C2H6O) | 93 | 93 | 0 | 0 |
| Water (H2O) | 7 | 7 | 100 | 100 |

## Notes
- Cooling water duty balances ethanol heat removal at approx. 0.28 MW.
- Monitoring differential pressure across E-101 ensures early fouling detection.
</md_output>

# STREAM TEMPLATE
{stream_template}

# REFERENCE MATERIAL
---
**BASIC PROCESS FLOW DIAGRAM:**
{basic_pfd_markdown}

**DESIGN BASIS:**
{design_basis_markdown}

**REQUIREMENTS SUMMARY:**
{requirements_markdown}

"""
