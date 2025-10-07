from typing import Dict, Any
import pubchempy as pcp
from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter
from processdesignagents.agents.utils.json_utils import extract_json_from_response
from processdesignagents.default_config import load_config
import json

class DesignState:
    pass  # Placeholder for TypedDict alignment

def literature_data_analyst(state: DesignState) -> DesignState:
    """Literature and Data Analyst: Extracts components from requirements and fetches PubChem data."""
    config = load_config()
    llm = ChatOpenRouter(model=config["quick_think_llm"])
    
    requirements = state.get("requirements", {})
    
    # LLM extraction of key components from requirements
    prompt = f"""
    From the following process requirements, extract 1-3 primary chemical components (e.g., reactants, products).
    Requirements: {json.dumps(requirements, default=str)}
    
    Output JSON: {{"components": ["component1", "component2"]}}
    Focus on chemical names; infer from context if needed (e.g., 'ethane' for ethylene production).
    """
    
    response = llm.invoke(prompt)
    try:
        clean_json = extract_json_from_response(response.content)
        components_data = json.loads(clean_json)
        components = components_data.get("components", ["ethane"])  # Fallback to default
    except (json.JSONDecodeError, ValueError):
        components = ["ethane"]  # Simple fallback
    
    literature_data = {}
    for component in components[:3]:  # Limit to 3 for efficiency
        try:
            compounds = pcp.get_compounds(component, 'name')
            if compounds:
                compound = compounds[0]
                literature_data[component] = {
                    "compound_name": compound.iupac_name,
                    "molecular_weight": compound.molecular_weight,
                    "boiling_point": getattr(compound, 'boiling_point', None),
                    "sources": ["PubChem"]
                }
                print(f"Fetched literature data for {component}: {literature_data[component]}")
            else:
                literature_data[component] = {"error": f"No data found for {component}"}
        except Exception as e:
            literature_data[component] = {"error": f"PubChem query failed: {str(e)}"}
    
    state["literature_data"] = literature_data
    return state