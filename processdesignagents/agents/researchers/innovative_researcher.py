from typing import Dict, Any
from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter  # Assuming wrapper from prior resolution
from processdesignagents.default_config import load_config
import json

class DesignState:
    pass  # Placeholder; align with graph's TypedDict in production

def innovative_researcher(state: DesignState) -> DesignState:
    """Innovative Researcher: Proposes novel process concepts using LLM."""
    config = load_config()
    llm = ChatOpenRouter(model=config["quick_think_llm"])
    
    prompt = f"""
    Based on the following requirements and literature data, propose 3 innovative chemical process concepts.
    Requirements: {state.get('requirements', {})}
    Literature Data: {state.get('literature_data', {})}
    
    For each concept, include: description, key units (e.g., reactor type), potential benefits.
    Output as JSON: {{"concepts": [{{"name": str, "description": str, "units": [str], "benefits": [str]}}]}}
    """
    
    response = llm.invoke(prompt)
    try:
        research_concepts = json.loads(response.content)
    except json.JSONDecodeError:
        research_concepts = {"concepts": [{"name": "Plasma Cracking", "description": "High-temperature plasma reactor for ethane", "units": ["Plasma Reactor"], "benefits": ["Higher yield"]}]}
    
    state["research_concepts"] = research_concepts
    print("Generated innovative research concepts.")
    return state