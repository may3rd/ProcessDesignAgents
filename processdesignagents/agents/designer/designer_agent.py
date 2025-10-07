from typing import Dict, Any
from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter  # Assuming resolved wrapper
from processdesignagents.agents.utils.json_utils import extract_json_from_response
from processdesignagents.default_config import load_config
import json

class DesignState:
    pass  # Placeholder for TypedDict alignment

def designer_agent(state: DesignState) -> DesignState:
    """Designer Agent: Synthesizes preliminary flowsheet from research concepts."""
    config = load_config()
    llm = ChatOpenRouter(model=config["quick_think_llm"])
    
    concepts = state.get("research_concepts", {}).get("concepts", [{}])
    selected_concept = max(concepts, key=lambda c: c.get("feasibility_score", 0))  # Select highest feasibility
    
    prompt = f"""
Synthesize a preliminary process flowsheet for the selected concept: {selected_concept}.
Incorporate requirements: {state.get('requirements', {})} and literature: {state.get('literature_data', {})}.
Output JSON: {{"flowsheet": {{"units": [{{ "name": str, "type": str, "specs": {{}}}} ], "connections": [{{ "from": str, "to": str }} ], "overall_description": str }}}}
Focus on key unit operations (e.g., reactor, separator) with basic specifications.
"""
    
    response = llm.invoke(prompt)
    try:
        clean_json = extract_json_from_response(response.content)
        flowsheet_data = json.loads(clean_json)["flowsheet"]
    except (json.JSONDecodeError, KeyError):
        # Fallback: Static example for ethane cracking
        flowsheet_data = {
            "units": [
                {"name": "Cracker", "type": "Plasma Reactor", "specs": {"temperature": 1000, "pressure": 1}},
                {"name": "Separator", "type": "Distillation Column", "specs": {"stages": 20}}
            ],
            "connections": [{"from": "Cracker", "to": "Separator"}],
            "overall_description": "Integrated cracking and separation for ethane-to-ethylene conversion."
        }
    
    state["flowsheet"] = flowsheet_data
    print(f"Synthesized flowsheet for {selected_concept.get('name', 'concept')}: {flowsheet_data['overall_description']}")
    return state