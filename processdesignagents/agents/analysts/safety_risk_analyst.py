from __future__ import annotations

from operator import le
import re
from langchain_core.messages import AIMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from dotenv import load_dotenv
from sympy import continued_fraction_periodic

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import jinja_raw, load_prompt

load_dotenv()


def strip_markdown_code_block(text: str) -> str:
    """Return text without enclosing ```markdown ``` code fences."""
    if not isinstance(text, str):
        return text
    
    # Remove the text outside mardown code
    text = text.strip()
    if not text.startswith("```markdown"):
        return text
    if not text.endswith("```"):
        return text
    
    # use re to capture text inside ``` markdown ```
    pattern = re.compile(r"```(?:markdown)?\s*([\s\S]*?)""", re.IGNORECASE)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return text


def create_safety_risk_analyst(llm):
    def safety_risk_analyst(state: DesignState) -> DesignState:
        """Safety and Risk Analyst: Performs HAZOP-inspired risk assessment on current concept."""
        print("\n# Safety and Risk Assessment", flush=True)
        requirements_markdown = state.get("process_requirements", "")
        design_basis_markdown = state.get("design_basis", "")
        flowsheet_description_markdown = state.get("flowsheet_description", "")
        equipment_and_stream_results = state.get("equipment_and_stream_results", "")

        base_prompt = safety_risk_prompt(
            requirements_markdown,
            design_basis_markdown,
            flowsheet_description_markdown,
            equipment_and_stream_results,
        )
        prompt_messages = base_prompt.messages # + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        
        llm.temperature = 1.0
        
        chain = prompt | llm
        is_done = False
        try_count = 0
        cleaned_content = ""
        while not is_done:
            try_count += 1
            if try_count > 10:
                print("+ Max try count reached.", flush=True)
                exit(-1)
            try:
                # Get the response from LLM
                response = chain.invoke({"messages": list(state.get("messages", []))})
                cleaned_content = strip_markdown_code_block(response.content)
                if not cleaned_content:
                    print(f"Attemp {try_count} - response is empty.")
                    print(response, flush=True)
                    continue
                if len(cleaned_content) > 50:
                    is_done = True
                else:
                    print(f"Attemp {try_count} - response is too short.")
                    print(response, flush=True)
            except Exception as e:
                print(f"Attemp {try_count} has failed.")
        print(cleaned_content, flush=True)
        return {
            "safety_risk_analyst_report": cleaned_content,
            "messages": [response],
        }
    return safety_risk_analyst


def safety_risk_prompt(
    process_requirements_markdown: str,
    design_basis_markdown: str,
    flowsheet_description_markdown: str,
    equipment_and_stream_results: str,
) -> ChatPromptTemplate:
    system_content = load_prompt("safety_risk_analyst_system.xml")
    
    human_content = f"""
# DATA FOR HAZOP ANALYSIS
---
**REQUIREMENTS / CONSTRAINTS (Markdown):**
{process_requirements_markdown}

**DESIGN BASIS (Markdown):**
{design_basis_markdown}

**BASIC PROCESS FLOW DIAGRAM (Markdown):**
{flowsheet_description_markdown}

**EQUIPMENT AND STREAMS DATA (JSON):**
{equipment_and_stream_results}

**You must output only pure markdown format, not code blocks, XML, or JSON.**
---
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

    return ChatPromptTemplate.from_messages(messages)