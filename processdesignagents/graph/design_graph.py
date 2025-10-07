from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any
from langchain_openai import ChatOpenAI
from processdesignagents.default_config import load_config
import os
import json
from dotenv import load_dotenv
import pubchempy as pcp

# Load environment variables (e.g., for API keys)
load_dotenv()

class DesignState(TypedDict):
    problem_statement: str
    requirements: Dict[str, Any]  # New field for analyst outputs
    literature_data: Dict[str, Any]
    flowsheet: Dict[str, Any]
    validation_results: Dict[str, Any]

def analyst_node(state: DesignState) -> DesignState:
    """Process Requirements Analyst: Extracts key design requirements using LLM."""
    config = load_config()
    llm = ChatOpenAI(
        model=config["quick_think_llm"],
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
    )
    
    prompt = f"""
    Analyze the following chemical process design problem and extract structured requirements.
    Problem: {state['problem_statement']}
    
    Output a JSON object with keys: throughput (kg/h), purity (%), yield_target (%), constraints (list of strings).
    Focus on chemical engineering aspects; infer reasonable defaults if unspecified.
    """
    
    response = llm.invoke(prompt)
    # Parse response as JSON (in production, add robust parsing)
    try:
        requirements = json.loads(response.content)
        # requirements = val(response.content)  # Simplified; use json.loads in full implementation
    except:
        requirements = {"throughput": 1000, "purity": 99, "yield_target": 95, "constraints": ["Environmental compliance"]}
    
    
    state["requirements"] = requirements
    print(f"Extracted requirements: {requirements}")
    return state

def literature_analyst_node(state: DesignState) -> DesignState:
    """Literature and Data Analyst: Fetches background data from PubChem based on requirements."""
    # Infer primary compound from problem statement (LLM-assisted in full version)
    primary_compound = "ethane"  # Placeholder; use LLM to extract dynamically (e.g., from state['problem_statement'])
    
    try:
        compounds = pcp.get_compounds(primary_compound, 'name')
        if compounds:
            compound = compounds[0]
            literature_data = {
                "compound_name": compound.iupac_name,
                "molecular_weight": compound.molecular_weight,
                "boiling_point": compound.boiling_point if hasattr(compound, 'boiling_point') else None,
                "sources": ["PubChem"]
            }
            print(f"Fetched literature data for {primary_compound}: {literature_data}")
        else:
            literature_data = {"error": f"No data found for {primary_compound}"}
    except Exception as e:
        literature_data = {"error": f"PubChem query failed: {str(e)}"}
    
    state["literature_data"] = literature_data
    return state

def build_graph():
    graph = StateGraph(DesignState)
    
    # Add nodes
    graph.add_node("analyst", analyst_node)
    graph.add_node("literature_analyst", literature_analyst_node)
    
    # Set entry point
    graph.set_entry_point("analyst")
    
    # Define edges: Analyst -> Literature Analyst -> END
    graph.add_edge("analyst", "literature_analyst")
    graph.add_edge("literature_analyst", END)
    
    return graph.compile()