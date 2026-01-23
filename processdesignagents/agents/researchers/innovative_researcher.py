from __future__ import annotations

import json
from json_repair import repair_json
from langchain_core.messages import AIMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

from dotenv import load_dotenv

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import jinja_raw, load_prompt
from processdesignagents.agents.utils.json_tools import get_json_str_from_llm

load_dotenv()

def create_innovative_researcher(llm):
    def innovative_researcher(state: DesignState) -> DesignState:
        """Innovative Researcher: Proposes novel process concepts using LLM."""
        print("\n# Innovative Research Concepts", flush=True)

        # Get the requirement summary from state
        requirements_summary = state.get("process_requirements", "")
        if not isinstance(requirements_summary, str):
            requirements_summary = str(requirements_summary)
            
        # Create system prompt and user prompt
        base_prompt = innovative_researcher_prompt(requirements_summary)
        prompt_messages = base_prompt.messages # + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        
        try:
            # Call function to execute LLM with expecting JSON in response.content
            response, response_content = get_json_str_from_llm(llm, prompt, state)
            
            # print(f"DEBUG: {response_content}", flush=True)
            
            # Convert str to dict
            response_dict = json.loads(repair_json(response_content))
            
            # Get correct item if return list
            if isinstance(response_dict, list):
                for a in response_dict:
                    print(a)
                    if "concepts" in a:
                        response_dict = a
                        break
                print("DEBUG: Fail to create concepts list.")
                exit(-1)

            # Display the generated concepts
            print(convert_concepts_list_to_markdown(response_dict.get("concepts", [])), flush=True)
        except Exception as e:
            # Handle errors
            print(f"Error: {e}")
            print(response_dict)
            exit(-1)

        # Update the current states.
        return {
            "research_concepts": json.dumps(response_dict),
            "messages": [response]
        }

    return innovative_researcher


def convert_concepts_list_to_markdown(concepts: list) -> str:
    """Convert list of concept output into a readable Markdown summary."""
    if not isinstance(concepts, list):
        return ""

    lines: list[str] = []
    concept_counter = 0
    for concept in concepts:
        if not isinstance(concept, dict):
            continue

        concept_counter += 1
        name = concept.get("name", "Untitled Concept")
        maturity = concept.get("maturity", "unknown")
        description = concept.get("description", "unknown")
        unit_operations = concept.get("unit_operations", [])
        key_benefits = concept.get("key_benefits", [])

        lines.append("---")
        lines.append(f"## Concept {concept_counter}. {name}")
        if isinstance(maturity, str) and maturity:
            normalized_maturity = maturity.replace("_", " ").title()
            lines.append(f"**Maturity:** {normalized_maturity}")
        if isinstance(description, str) and description:
            lines.append(f"**Description:** {description}")

        if isinstance(unit_operations, list) and unit_operations:
            lines.append("**Unit Operations:**")
            for unit in unit_operations:
                lines.append(f"- {unit}")

        if isinstance(key_benefits, list) and key_benefits:
            lines.append("**Key Benefits:**")
            for benefit in key_benefits:
                lines.append(f"- {benefit}")

    if not lines:
        return ""

    return "\n".join(lines)


def innovative_researcher_prompt(requirements_markdown: str) -> ChatPromptTemplate:
    system_content = load_prompt("innovative_researcher_system.xml")

    human_content = f"""
# DATA FOR ANALYSIS:
---
**REQUIREMENTS:**
{requirements_markdown}

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
