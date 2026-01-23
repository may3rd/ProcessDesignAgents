from __future__ import annotations

import re

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from dotenv import load_dotenv

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import jinja_raw, strip_markdown_code_fences, load_prompt

load_dotenv()


def create_project_manager(llm):
    def project_manager(state: DesignState) -> DesignState:
        """Project Manager: Reviews design for approval and generates implementation plan."""
        print("\n# Project Review", flush=True)

        requirements_markdown = state.get("process_requirements", "")
        design_basis = state.get("design_basis", "")
        flowsheet_description_markdown = state.get("flowsheet_description", "")
        equipment_and_stream_results = state.get("equipment_and_stream_results", "")
        safety_report = state.get("safety_risk_analyst_report", "")
        base_prompt = project_manager_prompt(
            requirements_markdown,
            design_basis,
            flowsheet_description_markdown,
            equipment_and_stream_results,
            safety_report
        )

        prompt_messages = base_prompt.messages # + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        
        is_done = False
        try_conut = 0
        approval_markdown = ""
        while not is_done:
            try_conut += 1
            if try_conut > 3:
                print("Maximum try count reached. Exiting...", flush=True)
                raise Exception("Maximum try count reached. Exiting...")
            try:
                chain = prompt | llm
                response = chain.invoke({"messages": list(state.get("messages", []))})

                approval_markdown = (
                    response.content if isinstance(response.content, str) else str(response.content)
                ).strip()
                approval_markdown = strip_markdown_code_fences(approval_markdown)
                if len(approval_markdown) > 50:
                    is_done = True
            except Exception as e:
                continue
        approval_status = _extract_status(approval_markdown)

        print(f"Project review completed. Status: **{approval_status or 'Unknown'}**\n", flush=True)
        print(approval_markdown, flush=True)

        return {
            "project_approval": approval_status or "",
            "project_manager_report": approval_markdown,
            "messages": [response],
        }

    return project_manager


def _extract_status(markdown_text: str) -> str | None:
    match = re.search(r"Approval Status\s*[:\-]\s*([A-Za-z ]+)", markdown_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def project_manager_prompt(
    process_requirements_markdown: str,
    design_basis: str,
    flowsheet_description_markdown: str,
    equipment_and_stream_results: str,
    safety_and_risk_json: str,
) -> ChatPromptTemplate:
    system_content = load_prompt("project_manager_system.xml")

    human_content = f"""
Create a project summary based on the following data:

**Requirements Summary:**
{process_requirements_markdown}

**Design Basis:**
{design_basis}

**Basic Process Flow Diagram:**
{flowsheet_description_markdown}

**Equipments and Streams Data:**
{equipment_and_stream_results}

**Safety & Risk Assessments:**
{safety_and_risk_json}
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