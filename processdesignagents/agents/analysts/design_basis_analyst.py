from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .static.design_basis_prompts import basic_system_prompt, google_system_prompt
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv

load_dotenv()

def create_design_basis_analyst(llm):
    def design_basis_analyst(state: DesignState) -> DesignState:
        """Design Basis Analyst: Converts requirements into a structured design basis summary."""
        print("\n---\n# Design Basis\n")

        problem_statement = state.get("problem_statement", "")
        requirements_markdown = state.get("requirements", "")
        selected_concept_details = state.get("selected_concept_details", "")
        selected_concept_name = state.get("selected_concept_name", "")
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)
        if not isinstance(selected_concept_details, str):
            selected_concept_details = str(selected_concept_details)
        if not isinstance(selected_concept_name, str):
            selected_concept_name = str(selected_concept_name)

        system_message = google_system_prompt(
            problem_statement,
            requirements_markdown,
            selected_concept_name,
            selected_concept_details,
        )

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a helpful AI Assistant, collaborating with other assistants."
                "\n{system_message}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ])

        chain = prompt.partial(system_message=system_message) | llm
        response = chain.invoke(state.get("messages", []))

        design_basis_markdown = (
            response.content if isinstance(response.content, str) else str(response.content)
        )

        print(design_basis_markdown)

        return {
            "design_basis": design_basis_markdown,
            "messages": [response],
        }

    return design_basis_analyst
