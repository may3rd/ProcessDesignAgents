from __future__ import annotations

from typing import Tuple
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from processdesignagents.agents.utils.prompt_utils import jinja_raw, load_prompt


def component_list_researcher_prompt_with_tools(
    concept_name: str,
    concept_details: str,
    requirements: str,
) -> Tuple[ChatPromptTemplate, str, str]:
    system_content = load_prompt("component_list_researcher_system.xml")
    human_content = f"""
Create a components list based on the following data:

# DESIGN INPUTS

**Requirements (Markdown):**
{requirements}

**Selected Concept Name:**
{concept_name or "Not provided"}

**Concept Details (Markdown):**
{concept_details}

**Physical Properties Tool Instructions:**
Use the `get_physical_properties` tool whenever you need molecular weight or any physical property for a candidate component. Call it with:
- `components`: ["ComponentName"]
- `mole_fractions`: [1.0] for a pure component
- `temperature_c`: 25.0 (adjust if project documentation specifies otherwise)
- `pressure_barg`: 0.0
- `properties_needed`: ["molecular_weight", "phase"]

The tool returns molecular weight in kg/kmol (numerically equivalent to g/mol). Reflect the value in the Markdown table and capture any relevant notes in your reasoning. If the tool reports an error for a component, record the issue and cite the reference you use for a fallback estimate.

When compiling the table, include four columns in this order: Name, Formula, MW, Normal Boiling Point (°C). Report normal boiling points at 1 atm; if you must estimate, add "(approx.)" after the numeric value.

Return only the Markdown header and table as defined in your instructions.
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
