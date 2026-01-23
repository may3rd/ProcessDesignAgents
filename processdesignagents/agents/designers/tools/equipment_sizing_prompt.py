from __future__ import annotations

from typing import Tuple
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from processdesignagents.agents.utils.prompt_utils import jinja_raw, load_prompt

def equipment_sizing_prompt_with_tools(
    design_basis: str,
    flowsheet_description: str,
    equipment_and_stream_results: str,
) -> Tuple[ChatPromptTemplate, str, str]:
    """
    Create prompt with pre-computed tool results
    """
    
    system_content = load_prompt("equipment_sizing_system.xml")

    human_content = f"""
Based on the design basis, flowsheet description, and equipment and stream data below, use the available sizing tools to calculate and update the equipment list.

**Design Basis**
{design_basis}

**Flowsheet Description**
{flowsheet_description}

**Equipment and Stream Data (JSON):**
{equipment_and_stream_results}

**Output ONLY the final equipment list JSON object (no code fences, no additional text, no tool calls, no XML tags). The output must start directly with `{{` and end with `}}`.**
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

    return ChatPromptTemplate.from_messages(messages), system_content, human_content