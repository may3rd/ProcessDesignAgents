from __future__ import annotations

import json
from json_repair import repair_json
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

from dotenv import load_dotenv

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import jinja_raw, load_prompt
from processdesignagents.agents.utils.json_tools import get_json_str_from_llm, extract_first_json_document


load_dotenv()


def create_conservative_researcher(llm):
    def conservative_researcher(state: DesignState) -> DesignState:
        """Conservative Researcher: Critiques concepts for practicality using LLM."""
        print("\n# Conservatively Critiqued Concepts", flush=True)
        
        # Get problem requirement and research concepts list
        concepts_json = state.get("research_concepts", "")
        requirements_markdown = state.get("process_requirements", "")
        
        # Create system prompt and user prompt
        base_prompt = conservative_researcher_prompt(concepts_json, requirements_markdown)
        prompt_messages = base_prompt.messages # + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        
        try:
            # Call function to execute LLM with expecting JSON in response.content
            response, response_content = get_json_str_from_llm(llm, prompt, state)
            
            response_dict = json.loads(repair_json(response_content))
            
            # Get correct item if return list
            if isinstance(response_dict, list):
                for a in response_dict:
                    if "concepts" in a:
                        response_dict = a
                        break
                print("DEBUG: Fail to create concepts list.")
                exit(-1)
            
            print(convert_concepts_to_markdown(response_dict.get("concepts", "")), flush=True)
        except Exception as e:
            # Handle errors
            print(f"Error: {e}")
            print(response_content)
            exit(-1)
        return {
            "research_rating_results": json.dumps(response_dict),
            "messages": [response],
        }

    return conservative_researcher


def convert_concepts_to_markdown(concepts: list) -> str:
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
        summary = concept.get("summary")
        feasibility_score = concept.get("feasibility_score")
        risks = concept.get("risks")
        recommendations = concept.get("recommendations")

        lines.append("---")
        lines.append(f"## Concept {concept_counter}. {name}")
        if isinstance(summary, str) and summary:
            lines.append(f"**Summary:** {summary}")
        if isinstance(feasibility_score, int):
            lines.append(f"**Feasibility Score:** {feasibility_score}")
        if isinstance(risks, dict):
            lines.append("**Risks:**")
            for key, value in risks.items():
                lines.append(f"- {key}: {value}")
        if isinstance(recommendations, list) and recommendations:
            lines.append("**Recommendations:**")
            for recommendation in recommendations:
                lines.append(f"- {recommendation}")
    if not lines:
        return ""

    return "\n".join(lines)


def conservative_researcher_prompt(
    concepts_json: str,
    requirements_markdown: str,
) -> ChatPromptTemplate:
    system_content = load_prompt("conservative_researcher_system.xml")

    human_content = f"""
# DATA FOR ANALYSIS
---
**Requirements / Constraints (Markdown):**
{requirements_markdown}

**Concepts (JSON):**
{concepts_json}

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
