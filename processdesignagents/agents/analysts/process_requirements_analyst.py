from __future__ import annotations

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

def create_process_requiruments_analyst(llm):
    def process_requirements_analyst(state: DesignState) -> DesignState:
        """Process Requirements Analyst: Extracts key design requirements using LLM."""
        
        # Read problem statemant from agent state
        problem_statement = state.get("problem_statement", "")
        if not isinstance(problem_statement, str):
            problem_statement = str(problem_statement)
        
        print(f"# Problem statement: {problem_statement}", flush=True)
        print("# Process Requirements Analysis", flush=True)
        
        # Create base prompt from problem statement
        base_prompt = process_requirements_prompt(problem_statement=problem_statement)
        prompt_messages = base_prompt.messages # + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | llm
        is_done = False
        try_count = 0
        requirements_summary = ""
        while not is_done:
            try_count += 1
            if try_count > 10:
                print("+ Max try count reached.", flush=True)
                exit(-1)
            try:
                response = chain.invoke({"messages": list(state.get("messages", []))})
                requirements_summary = (
                    response.content if isinstance(response.content, str) else str(response.content)
                ).strip()
                requirements_summary = strip_markdown_code_fences(requirements_summary)
                if len(requirements_summary) > 50:
                    is_done = True
                else:
                    print("DEBUG: The respones message is too short. Try again.")
            except Exception as e:
                print(f"Attemp {try_count} has failed.")
        print(f"{requirements_summary}", flush=True)
        return {
            "process_requirements": requirements_summary,
            "messages": [response],
        }
    return process_requirements_analyst

def process_requirements_prompt(problem_statement: str) -> ChatPromptTemplate:
    system_content = load_prompt("process_requirements_analyst_system.xml")

    human_content = f"""
# PROBLEM STATEMENT TO ANALYZE:
{problem_statement}
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
