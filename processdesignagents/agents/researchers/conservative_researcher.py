from typing import Dict, Any
from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter
from processdesignagents.agents.utils.json_utils import extract_json_from_response
from processdesignagents.default_config import load_config
import json

class DesignState:
    pass

def conservative_researcher(state: DesignState) -> DesignState:
    """Conservative Researcher: Critiques concepts for practicality using LLM."""
    config = load_config()
    llm = ChatOpenRouter(model=config["quick_think_llm"])
    
    concepts = state.get("research_concepts", {}).get("concepts", [])
    prompt = f"""
    Critique the following process concepts for risks, costs, and feasibility, considering constraints.
    Concepts: {concepts}
    Requirements/Constraints: {state.get('requirements', {})}
    
    For each concept, add: risks [str], feasibility_score (1-10), recommendations [str].
    Output as JSON: {{"concepts": [{{"name": str, "description": str, "units": [str], "benefits": [str], "risks": [str], "feasibility_score": int, "recommendations": [str] }}]}}
    """
    
    response = llm.invoke(prompt)
    try:
        clean_json = extract_json_from_response(response.content)
        updated_concepts = json.loads(clean_json)
        state["research_concepts"] = updated_concepts
    except json.JSONDecodeError:
        # Fallback: Add simple critiques
        for concept in concepts:
            concept["risks"] = ["High energy use"]
            concept["feasibility_score"] = 7
            concept["recommendations"] = ["Pilot testing required"]
    
    print("Applied conservative critiques to research concepts.")
    return state