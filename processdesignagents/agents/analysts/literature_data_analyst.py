from typing import Dict, Any
import pubchempy as pcp
from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter
from processdesignagents.agents.utils.json_utils import extract_json_from_response
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import json

load_dotenv()

def create_literature_data_analyst(quick_think_llm: str):
    def literature_data_analyst(state: DesignState) -> DesignState:
        """Literature and Data Analyst: Extracts components from requirements and fetches PubChem data."""
        print("\n=========================== Component List ===========================\n")
        llm = ChatOpenRouter()
        requirements = state.get("requirements", {})
        prompt = system_prompt(json.dumps(requirements, default=str))
        response = llm.invoke(prompt, model=quick_think_llm)
        
        try:
            clean_json = extract_json_from_response(response.content)
            components_data = json.loads(clean_json)
            components = components_data.get("components", ["ethane"])  # Fallback to default
        except (json.JSONDecodeError, ValueError):
            raise ValueError("Failed to extract components from requirements")
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
    return literature_data_analyst

def system_prompt(requirements: str) -> str:
    return f"""
# ROLE:
You are an expert chemical engineer specializing in process data analysis. Your task is to identify the most critical chemical components from a set of process requirements.

# TASK:
Analyze the provided 'PROCESS REQUIREMENTS' JSON. Extract the 1 to 5 most important chemical components mentioned or implied (e.g., primary reactants and products). Your output MUST be a single, valid JSON object.

# JSON SCHEMA:
{{
    "components": ["list of component names as strings"]
}}

# INSTRUCTIONS:
1.  **Analyze Context:** Carefully read the 'PROCESS REQUIREMENTS' to understand the core chemical process being described.
2.  **Identify Chemicals:** Look for keys like 'components', 'purity', 'yield_target', or descriptions that name chemicals.
3.  **Prioritize:** Select only the primary reactants and the main target product. Ignore catalysts, solvents, or trace impurities unless they are the central focus.
4.  **Infer if Necessary:** If a process is named (e.g., "ammonia synthesis"), infer the primary components (e.g., "Nitrogen", "Hydrogen", "Ammonia").
5.  **Format Output:** List the component names as strings in the "components" list. If no components can be identified, return an empty list: `[]`.

# EXAMPLE:
---
**PROCESS REQUIREMENTS:**
{{
    "throughput": {{"value": 1500.0, "units": "kg/h"}},
    "components": [
        {{"name": "Ethanol", "role": "Reactant"}},
        {{"name": "Acetic Acid", "role": "Reactant"}},
        {{"name": "Ethyl Acetate", "role": "Product"}},
        {{"name": "Water", "role": "Product"}},
        {{"name": "Sulfuric Acid", "role": "Catalyst"}}
    ],
    "purity": {{"component": "Ethyl Acetate", "value": 99.8}},
    "yield_target": {{"value": 92.0, "basis": "Based on limiting reactant 'Acetic Acid'"}},
    "constraints": ["Reactor operating temperature must be below 100°C."]
}}

**EXPECTED JSON OUTPUT:**
{{
    "components": ["Ethyl Acetate", "Ethanol", "Acetic Acid"]
}}
---

# NEGATIVES:
 * DO NOT return comman mixture names, e.g. Air, instead list the common chemical components in it.

# PROCESS REQUIREMENTS TO ANALYZE:
{requirements}

# FINAL JSON OUTPUT:
"""