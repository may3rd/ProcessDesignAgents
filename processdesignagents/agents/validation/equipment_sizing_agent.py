from __future__ import annotations

from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.tools import EQUIPMENT_SIZING_TOOLS
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import json

load_dotenv()


def create_equipment_sizing_agent(llm):
    def equipment_sizing_agent(state: DesignState) -> DesignState:
        """Equipment Sizing Agent: Estimates key equipment dimensions using design heuristics."""
        print("\n=========================== Equipment Sizing ===========================\n")

        flowsheet_markdown = state.get("flowsheet", "")
        requirements_markdown = state.get("requirements", "")
        validation_markdown = state.get("validation_results", "")
        if not isinstance(flowsheet_markdown, str):
            flowsheet_markdown = str(flowsheet_markdown)
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)
        if not isinstance(validation_markdown, str):
            validation_markdown = str(validation_markdown)

        # Step 1: Generate design basis using the base LLM (no tools)
        prior_messages = list(state.get("messages", []))
        basis_prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])
        basis_prompt = basis_prompt.partial(
            system_message=design_basis_prompt(
                requirements_markdown,
                flowsheet_markdown,
                validation_markdown,
            )
        )
        basis_conversation = basis_prompt.format_prompt(messages=prior_messages).to_messages()
        basis_response = llm.invoke(basis_conversation)
        basis_markdown = basis_response.content if isinstance(basis_response.content, str) else str(basis_response.content)
        print("Equipment design basis prepared.")
        print(basis_markdown)

        extended_messages = prior_messages + [basis_response]

        # Step 2: Perform sizing with tool support
        tool_enabled_llm = llm.bind_tools(EQUIPMENT_SIZING_TOOLS)
        system_message = system_prompt(
            requirements_markdown,
            flowsheet_markdown,
            validation_markdown,
            basis_markdown,
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
        ])
        partial_prompt = prompt.partial(system_message=system_message)

        conversation = partial_prompt.format_prompt(messages=extended_messages).to_messages()
        new_messages = [basis_response]

        response = tool_enabled_llm.invoke(conversation)
        conversation.append(response)
        new_messages.append(response)

        iteration_count = 0
        max_iterations = 5

        while getattr(response, "tool_calls", None):
            if iteration_count >= max_iterations:
                guard_message = ToolMessage(
                    content=json.dumps({"error": "Tool iteration limit exceeded."}),
                    tool_call_id="equipment_sizing_guard",
                )
                conversation.append(guard_message)
                new_messages.append(guard_message)
                break

            iteration_count += 1

            for tool_call in response.tool_calls:
                tool = _TOOL_REGISTRY.get(tool_call["name"])
                if tool is None:
                    tool_output = {"error": f"Tool {tool_call['name']} not found."}
                else:
                    try:
                        tool_output = tool.invoke(tool_call["args"])
                    except Exception as exc:  # noqa: BLE001
                        tool_output = {"error": str(exc)}
                tool_message = ToolMessage(
                    content=json.dumps(tool_output),
                    tool_call_id=tool_call["id"],
                )
                conversation.append(tool_message)
                new_messages.append(tool_message)

            response = tool_enabled_llm.invoke(conversation)
            conversation.append(response)
            new_messages.append(response)

        sizing_markdown = response.content if isinstance(response.content, str) else str(response.content)
        missing_sections = [
            section
            for section in ["Equipment Sizing Summary", "Detailed Calculations"]
            if f"## {section}" not in sizing_markdown
        ]
        if "Equipment Sizing Summary" in missing_sections:
            sizing_markdown += (
                "\n\n## Equipment Sizing Summary\n"
                "| Equipment | Key Parameters | Estimated Size | Notes |\n"
                "|-----------|----------------|----------------|-------|\n"
                "| TBD | Not provided | Not provided | Placeholder generated automatically |\n"
            )
        if "Detailed Calculations" in missing_sections:
            sizing_markdown += (
                "\n\n## Detailed Calculations\n"
                "- Detailed calculations were not provided by the sizing step. Placeholder added automatically.\n"
            )
        if missing_sections:
            print(
                f"[!] Equipment sizing report missing sections: {', '.join(missing_sections)}. Added default placeholders."
            )
        existing_validation = state.get("validation_results", "")
        if not isinstance(existing_validation, str):
            existing_validation = str(existing_validation or "")
        validation_segments = []
        if existing_validation.strip():
            validation_segments.append(existing_validation.strip())
        validation_segments.append(basis_markdown.strip())
        validation_segments.append(sizing_markdown.strip())
        updated_validation = "\n\n".join(validation_segments)

        print("\nEquipment sizing report generated.")
        print(sizing_markdown)

        return {
            "validation_results": updated_validation,
            "equipment_sizing_report": sizing_markdown,
            "messages": new_messages,
        }

    return equipment_sizing_agent


def design_basis_prompt(
    requirements_markdown: str,
    flowsheet_markdown: str,
    validation_markdown: str,
) -> str:
    return f"""
# ROLE
You are a process engineer preparing design bases for equipment sizing.

# TASK
Analyze the requirements, flowsheet, and stream data to estimate key design duties and conditions for major equipment. Provide a Markdown table summarizing the duty/conditions that will serve as inputs to sizing calculations.

# OUTPUT FORMAT
```
## Equipment Design Basis
| Equipment | Service | Key Duty/Load | Design Conditions | Notes |
|-----------|---------|---------------|-------------------|-------|
| ... | ... | ... | ... | ... |

## Assumptions
- <assumption 1>
- <assumption 2>
```
Include estimated heat duties (kW), volumetric holdup (m³), or vapor loads (kg/h) where appropriate. Make reasonable engineering assumptions if data is missing, flagging them clearly.

# DATA
---
**REQUIREMENTS SUMMARY (Markdown):**
{requirements_markdown}

**FLOWSHEET SUMMARY (Markdown):**
{flowsheet_markdown}

**STREAM SUMMARY (Markdown):**
{validation_markdown}

# FINAL MARKDOWN OUTPUT:
"""


def system_prompt(
    requirements_markdown: str,
    flowsheet_markdown: str,
    validation_markdown: str,
    basis_markdown: str,
) -> str:
    return f"""
# ROLE
You are a senior process equipment engineer. Your task is to estimate preliminary equipment sizes using design heuristics and the provided sizing tools.

# TASK
Review the requirements, flowsheet, stream data, and the provided design basis. For each major piece of equipment (reactors, columns, heat exchangers, vessels, pump, compressor), propose sizing estimates. Call the provided tools to compute quantitative values where applicable, then summarize the sizing in Markdown.

# OUTPUT FORMAT
Produce Markdown with the structure:
```
## Equipment Sizing Summary
| Equipment | Key Parameters | Estimated Size | Notes |
|-----------|----------------|----------------|-------|
| ... | ... | ... | ... |

## Detailed Calculations
- <equipment>: <brief explanation and reference to tool outputs>
- ...
```
Include references to the tool calculations you performed.

# AVAILABLE TOOLS
- heat_exchanger_sizing(duty_kw, overall_u_kw_m2_k, lmt_delta_t_k)
- vessel_volume_estimate(volumetric_flow_m3_per_hr, residence_time_min, holdup_fraction=0.75)
- distillation_column_diameter(vapor_mass_flow_kg_per_hr, vapor_density_kg_per_m3, design_velocity_m_per_s=1.5)

# DESIGN DATA
---
**REQUIREMENTS SUMMARY (Markdown):**
{requirements_markdown}

**FLOWSHEET SUMMARY (Markdown):**
{flowsheet_markdown}

**STREAM SUMMARY (Markdown):**
{validation_markdown}

**DESIGN BASIS (Markdown):**
{basis_markdown}

# FINAL MARKDOWN OUTPUT:
"""


_TOOL_REGISTRY = {tool.name: tool for tool in EQUIPMENT_SIZING_TOOLS}
