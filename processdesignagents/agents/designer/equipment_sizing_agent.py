from __future__ import annotations

import json

from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from processdesignagents.agents.tools import EQUIPMENT_SIZING_TOOLS
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv

load_dotenv()


def create_equipment_sizing_agent(llm):
    def equipment_sizing_agent(state: DesignState) -> DesignState:
        """Equipment Sizing Agent: populates the equipment table using tool-assisted estimates."""
        print("\n# Equipment Sizing\n")

        llm.temperature = 0.7

        requirements_markdown = state.get("requirements", "")
        design_basis_markdown = state.get("design_basis", "")
        basic_pdf_markdown = state.get("basic_pdf", "")
        basic_hmb_markdown = state.get("basic_hmb_results", "")
        stream_table = state.get("basic_stream_data", "")
        equipment_table_template = state.get("basic_equipment_template", "")

        if not equipment_table_template.strip():
            raise ValueError("Equipment template is missing. Run the equipment list builder before sizing.")

        system_message = equipment_sizing_prompt(
            requirements_markdown,
            design_basis_markdown,
            basic_pdf_markdown,
            basic_hmb_markdown,
            stream_table,
            equipment_table_template,
        )

        # tool_enabled_llm = llm.bind_tools(EQUIPMENT_SIZING_TOOLS)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])
        conversation = prompt.partial(system_message=system_message).format_prompt(
            messages=list(state.get("messages", []))
        ).to_messages()

        new_messages: list = []
        # response = tool_enabled_llm.invoke(conversation)
        
        response = llm.invoke(conversation)
        
        # conversation.append(response)
        # new_messages.append(response)

        # iteration_count = 0
        # max_iterations = 8

        # while getattr(response, "tool_calls", None):
        #     if iteration_count >= max_iterations:
        #         guard_message = ToolMessage(
        #             content=json.dumps({"error": "Tool iteration limit exceeded."}),
        #             tool_call_id="equipment_sizing_guard",
        #         )
        #         conversation.append(guard_message)
        #         new_messages.append(guard_message)
        #         break

        #     iteration_count += 1

        #     for tool_call in response.tool_calls:
        #         tool = _TOOL_REGISTRY.get(tool_call["name"])
        #         if tool is None:
        #             tool_output = {"error": f"Tool {tool_call['name']} not found."}
        #         else:
        #             try:
        #                 tool_output = tool.invoke(tool_call["args"])
        #             except Exception as exc:  # noqa: BLE001
        #                 tool_output = {"error": str(exc)}
        #         tool_message = ToolMessage(
        #             content=json.dumps(tool_output),
        #             tool_call_id=tool_call["id"],
        #         )
        #         conversation.append(tool_message)
        #         new_messages.append(tool_message)

        #     response = tool_enabled_llm.invoke(conversation)
        #     conversation.append(response)
        #     new_messages.append(response)

        markdown_output = response.content if isinstance(response.content, str) else str(response.content)

        print(markdown_output)

        return {
            "basic_equipment_template": markdown_output,
            "messages": new_messages,
        }

    return equipment_sizing_agent


def equipment_sizing_prompt(
    requirements_markdown: str,
    design_basis_markdown: str,
    basic_pdf_markdown: str,
    basic_hmb_markdown: str,
    stream_table: str,
    equipment_table_template: str,
) -> str:
    return f"""
# ROLE
You are the lead equipment engineer completing preliminary sizing calculations for a conceptual design.

# TASK
Update the equipment table with quantitative estimates. When helpful, call the available sizing tools. Capture key parameters (e.g., heat-transfer area, vessel diameter/length/orientation, pump/compressor power). Present the final results as a MARKDOWN TABLE plus brief notes.

# INSTRUCTIONS
- For each equipment entry, verify the flowsheet context (streams, duty expectations) using the stream table, H&MB results, and design basis before sizing.
- Estimate the equipment sizing.
- Replace every `<value>` placeholder in the template with a numeric estimate and unit; note any assumptions or calculation shortcuts directly in the Notes column.
- Group equipment by type (e.g., reactors, exchangers, vessels, rotating equipment) so related items appear together.

# CRITICALS
- **MUST** return the full equipment table in markdown format.

# MARKDOWN TEMPLATE:
Your Markdown output must follow this structure:
```
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Detailed Notes
- E-101: Referenced heat_exchanger_sizing – heat duty = ... kW, heat transfer area = ... m²; assumptions ...
- V-101: Used vessel_volume_estimate – diameter = ... m; length = ... m; orientation = ...
```

# REFERENCE DATA
---
**REQUIREMENTS SUMMARY:**
{requirements_markdown}

**DESIGN BASIS:**
{design_basis_markdown}

**BASIC PROCESS DESCRIPTION:**
{basic_pdf_markdown}

**STREAM TABLE:**
{stream_table}

**PRELIMINARY H&MB:**
{basic_hmb_markdown}

**EQUIPMENT TABLE TEMPLATE:**
{equipment_table_template}
---
# FINAL MARKDOWN OUTPUT:

# EXAMPLE
For a single exchanger that cools ethanol from 80 C to 40 C with cooling water, estimate the duty from the heat balance, size the heat transfer area using the heat_exchanger_sizing tool, and record cooling water inlet/outlet temperatures along with any approach temperature assumptions in the notes.

**EXPECTED MARKDOWN OUTPUT:**
<md_output>
## Equipment Table

### Heat Exchanger
| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| E-101 | Ethanol Cooler | Reduce ethanol temperature | Shell-and-tube exchanger | 1001, 2001 | 1002, 2002 | 0.28 MW | U=450 W/m2-K; Area=120 m2; LMTD=25 degC | Sized via heat_exchanger_sizing; 1-2 pass configuration |

## Pumps

| Equipment ID | Name | Service | Type | Streams In | Streams Out | Duty / Load | Key Parameters | Notes |
|--------------|------|---------|------|------------|-------------|-------------|----------------|-------|
| P-101 | Product Pump | Transfer cooled ethanol | Centrifugal pump | 1002 | 1003 | 45 kW | Flow=10,000 kg/h; Head=18 m; Eff=0.7 | Pump_sizing assumed density 820 kg/m3 |

## Detailed Notes
- E-101: heat_exchanger_sizing(duty=2.8e5 W, U=450 W/m2-K, LMTD=25 degC) -> area 24.9 m2; conservatively rounded to 30 m2 bundle with fouling factor.
- P-101: pump_sizing(flow=10,000 kg/h, head=18 m) -> brake power 42 kW, rounded to 45 kW with 10% contingency.
</md_output>

"""


_TOOL_REGISTRY = {tool.name: tool for tool in EQUIPMENT_SIZING_TOOLS}
