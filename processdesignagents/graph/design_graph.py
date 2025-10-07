from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any

# Import agents
from processdesignagents.agents.analysts.process_requirements_analyst import process_requirements_analyst
from processdesignagents.agents.analysts.literature_data_analyst import literature_data_analyst
# Placeholder imports for expansion
from processdesignagents.agents.researchers.innovative_researcher import innovative_researcher
from processdesignagents.agents.researchers.conservative_researcher import conservative_researcher
from processdesignagents.agents.designer.designer_agent import designer_agent
from processdesignagents.agents.validation.process_simulator import process_simulator
from processdesignagents.agents.validation.optimizer import optimizer
from processdesignagents.agents.validation.safety_risk_analyst import safety_risk_analyst
from processdesignagents.agents.project_manager.project_manager import project_manager

class DesignState(TypedDict):
    problem_statement: str
    requirements: Dict[str, Any]
    literature_data: Dict[str, Any]
    research_concepts: Dict[str, Any]
    flowsheet: Dict[str, Any]
    validation_results: Dict[str, Any]
    approval: Dict[str, Any]

def build_graph():
    graph = StateGraph(DesignState)
    
    # Add implemented nodes (expand as agents are developed)
    graph.add_node("process_requirements_analyst", process_requirements_analyst)
    graph.add_node("literature_data_analyst", literature_data_analyst)
    
    # Placeholder nodes (comment out until implemented)
    graph.add_node("innovative_researcher", innovative_researcher)
    graph.add_node("conservative_researcher", conservative_researcher)
    # graph.add_node("designer_agent", designer_agent)
    # graph.add_node("process_simulator", process_simulator)
    # graph.add_node("optimizer", optimizer)
    # graph.add_node("safety_risk_analyst", safety_risk_analyst)
    # graph.add_node("project_manager", project_manager)
    
    # Set entry point
    graph.set_entry_point("process_requirements_analyst")
    
    # Define edges for current flow
    graph.add_edge("process_requirements_analyst", "literature_data_analyst")
    #graph.add_edge("literature_data_analyst", END)
    
    # Placeholder edges (uncomment as needed)
    graph.add_edge("literature_data_analyst", "innovative_researcher")
    graph.add_edge("innovative_researcher", "conservative_researcher")
    graph.add_edge("conservative_researcher", END)
    # graph.add_edge("conservative_researcher", "designer_agent")
    # graph.add_edge("designer_agent", "process_simulator")
    # graph.add_edge("process_simulator", "optimizer")
    # graph.add_edge("optimizer", "safety_risk_analyst")
    # graph.add_edge("safety_risk_analyst", "project_manager")
    # graph.add_edge("project_manager", END)
    
    return graph.compile()