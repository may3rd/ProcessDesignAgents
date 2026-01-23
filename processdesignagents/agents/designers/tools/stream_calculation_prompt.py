from __future__ import annotations

from typing import Tuple
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from processdesignagents.agents.utils.prompt_utils import jinja_raw, load_prompt

def stream_calculation_prompt_with_tools(
    design_basis: str,
    flowsheet_description: str,
    stream_list_template: str,
) -> Tuple[ChatPromptTemplate, str, str]:
    """
    Creates system and human prompts for generating a stream table using calculation tools.

    Args:
        design_basis: Text describing the overall design parameters (feed, products, utilities).
        flowsheet_description: Text describing the sequence of unit operations.
        stream_list_template: JSON template string for the desired output structure.

    Returns:
        Tuple containing:
            - ChatPromptTemplate object for LangChain.
            - The generated system prompt string.
            - The generated human prompt string.
    """

    # Define the tools based on the stream_tools_coolprop.py file provided
    # Descriptions are derived from the function docstrings
    system_content = load_prompt("stream_calculation_system.xml")

    human_content = f"""
Generate the **complete stream table** in JSON format based on the following information. Use the available tools for calculations and property lookups. Adhere strictly to the provided JSON template and instructions, especially regarding documentation in the 'notes' field and outputting ONLY the final JSON object.

**1. Design Basis:**
```text
{design_basis}
```

**2. Flowsheet Description:**
```text
{flowsheet_description}
```

**3. Stream List JSON Template (Target Structure):**
```json
{stream_list_template}
```

**Output ONLY the final stream list JSON object (no code fences, no additional text, no tool calls, no XML tags). The output must start directly with `{{` and end with `}}`.**
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

    # Create the ChatPromptTemplate
    prompt_template = ChatPromptTemplate.from_messages(messages)

    return prompt_template, system_content, human_content