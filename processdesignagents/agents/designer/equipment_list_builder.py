from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv

load_dotenv()


def create_equipment_list_builder(llm):
    def equipment_list_builder(state: DesignState) -> DesignState:
        """Equipment List Builder: Produces a markdown equipment template with sizing placeholders."""
        print("\n# Equipment List Template\n", flush=True)

        llm.temperature = 0.7

        basic_pfd_markdown = state.get("basic_pfd", "")
        design_basis_markdown = state.get("design_basis", "")
        requirements_markdown = state.get("requirements", "")
        stream_table = state.get("basic_stream_data", "")

        system_message = system_prompt(
            basic_pfd_markdown,
            design_basis_markdown,
            requirements_markdown,
            stream_table,
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])

        response = (prompt.partial(system_message=system_message) | llm).invoke(
            {"messages": list(state.get("messages", []))}
        )
        table_output = response.content if isinstance(response.content, str) else str(response.content)

        print(table_output, flush=True)

        return {
            "basic_equipment_template": table_output,
            "messages": [response],
        }

    return equipment_list_builder


def system_prompt(
    basic_pfd_markdown: str,
    design_basis_markdown: str,
    requirements_markdown: str,
    stream_table: str,
) -> str:
    return f"""
# CONTEXT
The conceptual flowsheet, requirements, and preliminary stream map are complete. Downstream teams now need a master list of equipment placeholders so sizing, costing, and safety reviews can proceed in parallel.

# TARGET AUDIENCE
- Equipment sizing agent who will replace placeholders with calculated values.
- Cost estimation and procurement teams seeking an initial scope of supply.
- Process safety reviewers checking that critical equipment is accounted for.

# ROLE
You are a process equipment engineer compiling the master equipment list for a preliminary design package. Create an EQUIPMENT SUMMARY in MARKDOWN TABLE form.

# TASK
Use the process description, design basis, requirements, and stream summary to list every major unit (vessels, reactors, exchangers, towers, pumps, compressors, etc.). Provide clear placeholders for sizing data that will be filled in later.

# INSTRUCTIONS
- Read through the process description, design basis, and requirement summary to note every major operation or utility.
- Map stream IDs from the provided stream table to determine inlet/outlet connectivity for each unit.
- Group equipment by type (e.g., reactors, exchangers, vessels, rotating equipment) so related items appear together.
- Populate each row with the best known identifiers and leave `<value>` placeholders for any data not yet available; include units in the placeholder string.
- Capture any assumptions, open questions, or dependencies in the Notes column to guide the sizing step.

# CRITICALS
- **MUST** return the full equipment table in markdown format.

# MARKDOWN TEMPLATE:
Your Markdown output must follow this structure:
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| V-101 | Feed Surge Drum | Buffer upstream of pump | Vessel (Vertical) | 1001 | 1002 | <value> kW | Holdup: <value> m³; Orientation: Vertical | <assumptions or TBD items> |

# INPUT DATA
---
**BASIC PROCESS FLOW DIAGRAM:**
{basic_pfd_markdown}

**DESIGN BASIS:**
{design_basis_markdown}

**REQUIREMENTS SUMMARY:**
{requirements_markdown}

**STREAM TABLE (Markdown):**
{stream_table}

# FINAL MARKDOWN OUTPUT:
---
# EXAMPLE INPUT:
For a cooler that drops ethanol from 80 C to 40 C using cooling water, list E-101 with ethanol feed and product stream IDs, cooling water in/out streams, a duty placeholder, and notes about assumed approach temperatures.

# EXPECTED MARKDOWN OUTPUT:
## Equipment Table

### Heat Exchangers
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| E-101 | Ethanol Cooler | Reduce ethanol temperature | Shell-and-tube exchanger | 1001, 2001 | 1002, 2002 | 0.28 MW | Area: <120 m2>; U: <450 W/m2-K>; Shell pass: 1 | Design for 5 degC approach; allow bundle pull |

### Pumps
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| P-101 | Product Pump | Transfer cooled ethanol to storage | Centrifugal pump | 1002 | 1003 | 45 kW | Flow: 10,000 kg/h; Head: 18 m | Include VFD for turndown control |

"""
