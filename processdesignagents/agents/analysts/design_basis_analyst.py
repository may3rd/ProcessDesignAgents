from __future__ import annotations

from dotenv import load_dotenv
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import (
    jinja_raw,
    strip_markdown_code_fences,
    load_prompt,
)

load_dotenv()

def create_design_basis_analyst(llm):
    def design_basis_analyst(state: DesignState) -> DesignState:
        """Design Basis Analyst: Converts requirements into a structured design basis summary."""
        print("\n# Design Basis Analyst", flush=True)

        problem_statement = state.get("problem_statement", "")
        requirements_markdown = state.get("process_requirements", "")
        selected_concept_details = state.get("selected_concept_details", "")
        selected_concept_name = state.get("selected_concept_name", "")
        component_list = state.get("component_list", "")
        
        if not isinstance(problem_statement, str):
            problem_statement = str(problem_statement)
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)
        if not isinstance(selected_concept_details, str):
            selected_concept_details = str(selected_concept_details)
        if not isinstance(selected_concept_name, str):
            selected_concept_name = str(selected_concept_name)
        if not isinstance(component_list, str):
            component_list = str(component_list)
        
        base_prompt = google_prompt_templates(
            problem_statement=problem_statement,
            requirements_markdown=requirements_markdown,
            concept_name=selected_concept_name,
            concept_details_markdown=selected_concept_details,
            component_list=component_list,
        )
        # Combine Based prompt
        prompt = ChatPromptTemplate.from_messages(base_prompt.messages)
        chain = prompt | llm
        is_done = False
        try_count = 0
        while not is_done:
            try_count += 1
            if try_count > 3:
                print("+ Max try count reached.", flush=True)
                exit(-1)
            try:
                response = chain.invoke({"messages": list(state.get("messages", []))})
                design_basis_markdown = (
                    response.content if isinstance(response.content, str) else str(response.content)
                ).strip()
                design_basis_markdown = strip_markdown_code_fences(design_basis_markdown)
                is_done = len(design_basis_markdown) > 100
            except Exception as e:
                print(f"Attemp {try_count}: {e}")
        print(design_basis_markdown, flush=True)
        return {
            "design_basis": design_basis_markdown,
            "messages": [response],
        }

    return design_basis_analyst


def google_prompt_templates(
    problem_statement: str,
    requirements_markdown: str,
    concept_name: str,
    concept_details_markdown: str,
    component_list: str,
) -> ChatPromptTemplate:
    # Static instructions for SystemMessage
    system_content = load_prompt("design_basis_analyst_system.xml")
    
    # User-specific context for HumanMessage
    human_content = f"""
# REFERENCE MATERIAL:
---
**PROBLEM STATEMENT:**
{problem_statement}

**PROCESS REQUIREMENTS SUMMARY:**
{requirements_markdown}

**SELECTED CONCEPT NAME:**
{concept_name or "Not provided"}

**SELECTED CONCEPT DETAIL:**
{concept_details_markdown or "Not provided"}

**COMPONENT LIST:**
{component_list or "Not provided"}
    """
    
    # Construct the template
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
