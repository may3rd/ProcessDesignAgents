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
        quick_thinking_llm: ChatOpenAI,
        deep_thinking_llm: ChatOpenAI,
        checkpointer=None,
    ):
        """Initialize with required components."""
        self.quick_thinking_llm = quick_thinking_llm
        self.deep_thinking_llm = deep_thinking_llm
        self.checkpointer = checkpointer
        
    def setup_graph(
        self
    ):
        """Set up and complie the agent graph."""
        graph = StateGraph(DesignState)
        
        process_requirements_analyst = create_process_requiruments_analyst(self.quick_thinking_llm)
        # literature_data_analyst = create_literature_data_analyst(self.quick_thinking_llm)
        innovative_researcher = create_innovative_researcher(self.quick_thinking_llm)
        conservative_researcher = create_conservative_researcher(self.deep_thinking_llm)
        concept_detailer = create_concept_detailer(self.deep_thinking_llm)
        design_basis_analyst = create_design_basis_analyst(self.quick_thinking_llm)
        basic_pdf_designer = create_basic_pdf_designer(self.quick_thinking_llm)
        process_simulator = create_process_simulator(self.deep_thinking_llm)
        equipment_sizing_agent = create_equipment_sizing_agent(self.deep_thinking_llm)
        # optimizer = create_optimizer(self.quick_thinking_llm)
        safety_risk_analyst = create_safety_risk_analyst(self.deep_thinking_llm)
        project_manager = create_project_manager(self.deep_thinking_llm)
        
        # Add implemented nodes (expand as agents are developed)
        graph.add_node("process_requirements_analyst", process_requirements_analyst)
        graph.add_node("innovative_researcher", innovative_researcher)
        graph.add_node("conservative_researcher", conservative_researcher)
        graph.add_node("concept_detailer", concept_detailer)
        graph.add_node("design_basis_analyst", design_basis_analyst)
        graph.add_node("basic_pdf_designer", basic_pdf_designer)
        graph.add_node("process_simulator", process_simulator)
        graph.add_node("equipment_sizing_agent", equipment_sizing_agent)
        graph.add_node("safety_risk_analyst", safety_risk_analyst)
        graph.add_node("project_manager", project_manager)
        
        # Set entry point
        graph.set_entry_point("process_requirements_analyst")
        graph.add_edge("process_requirements_analyst", "innovative_researcher")
        graph.add_edge("innovative_researcher", "conservative_researcher")
        graph.add_edge("conservative_researcher", "concept_detailer")
        graph.add_edge("concept_detailer", "design_basis_analyst")
        graph.add_edge("design_basis_analyst", "basic_pdf_designer")
        # graph.add_edge("basic_pdf_designer", "process_simulator")
        # graph.add_edge("process_simulator", "equipment_sizing_agent")
        # graph.add_edge("equipment_sizing_agent", "safety_risk_analyst")
        # graph.add_edge("safety_risk_analyst", "project_manager")
        # graph.add_edge("project_manager", END)
        
        graph.add_edge("basic_pdf_designer", END)
        
        if self.checkpointer is not None:
            return graph.compile(checkpointer=self.checkpointer)
        return graph.compile()
