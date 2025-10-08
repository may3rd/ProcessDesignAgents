from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents import *

class GraphSetup:
    """Handle the setup and configuration of the agent graph."""
    
    def __init__(
        self,
        quick_think_llm: str,
        deep_think_llm: str,
    ):
        """Initialize with required components."""
        self.quick_think_llm = quick_think_llm
        self.deep_think_llm = deep_think_llm
        
    def setup_graph(
        self
    ):
        """Set up and complie the agent graph."""
        graph = StateGraph(DesignState)
        
        process_requirements_analyst = create_process_requiruments_analyst(self.quick_think_llm)
        literature_data_analyst = create_literature_data_analyst(self.quick_think_llm)
        innovative_researcher = create_innovative_researcher(self.quick_think_llm)
        conservative_researcher = create_conservative_researcher(self.deep_think_llm)
        
        # Add implemented nodes (expand as agents are developed)
        graph.add_node("process_requirements_analyst", process_requirements_analyst)
        graph.add_node("literature_data_analyst", literature_data_analyst)
        graph.add_node("innovative_researcher", innovative_researcher)
        graph.add_node("conservative_researcher", conservative_researcher)
        # graph.add_node("designer_agent", designer_agent)
        # graph.add_node("process_simulator", process_simulator)
        # graph.add_node("optimizer", optimizer)
        # graph.add_node("safety_risk_analyst", safety_risk_analyst)
        # graph.add_node("project_manager", project_manager)
        
        # Set entry point
        graph.set_entry_point("process_requirements_analyst")
        graph.add_edge("process_requirements_analyst", "literature_data_analyst")
        graph.add_edge("literature_data_analyst", "innovative_researcher")
        graph.add_edge("innovative_researcher", "conservative_researcher")
        # graph.add_edge("conservative_researcher", "designer_agent")
        # graph.add_edge("designer_agent", "process_simulator")
        # graph.add_edge("process_simulator", "optimizer")
        # graph.add_edge("optimizer", "safety_risk_analyst")
        # graph.add_edge("safety_risk_analyst", "project_manager")
        # graph.add_edge("project_manager", END)
        
        graph.add_edge("conservative_researcher", END)
        
        return graph.compile()