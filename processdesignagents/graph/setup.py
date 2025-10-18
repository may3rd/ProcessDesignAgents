from typing import Dict, Any
import time
from functools import wraps
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
        tool_nodes: Dict[str, ToolNode],
        checkpointer=None,
        delay_time: float = 0.5,
    ):
        """Initialize with required components."""
        self.quick_thinking_llm = quick_thinking_llm
        self.deep_thinking_llm = deep_thinking_llm
        self.tool_nodes = tool_nodes
        self.checkpointer = checkpointer
        self.concept_selection_provider = None
        self.delay_time = delay_time

    def _wrap_with_delay(self, agent_fn):
        """Ensure each agent pauses briefly before yielding control."""
        @wraps(agent_fn)
        def wrapper(state: DesignState) -> DesignState:
            result = agent_fn(state)
            time.sleep(self.delay_time)
            return result
        return wrapper
        
    def setup_graph(
        self
    ):
        """Set up and complie the agent graph."""
        graph = StateGraph(DesignState)
        
        process_requirements_analyst = self._wrap_with_delay(create_process_requiruments_analyst(self.quick_thinking_llm))
        innovative_researcher = self._wrap_with_delay(create_innovative_researcher(self.quick_thinking_llm))
        conservative_researcher = self._wrap_with_delay(create_conservative_researcher(self.quick_thinking_llm))
        concept_detailer = self._wrap_with_delay(create_concept_detailer(self.quick_thinking_llm))
        design_basis_analyst = self._wrap_with_delay(create_design_basis_analyst(self.quick_thinking_llm))
        basic_pfd_designer = self._wrap_with_delay(create_basic_pfd_designer(self.quick_thinking_llm))
        equipments_and_streams_list_builder = self._wrap_with_delay(create_equipments_and_streams_list_builder(self.quick_thinking_llm))
        equipment_list_builder = self._wrap_with_delay(create_equipment_list_builder(self.quick_thinking_llm))
        stream_data_estimator = self._wrap_with_delay(create_stream_data_estimator(self.deep_thinking_llm))
        equipment_sizing_agent = self._wrap_with_delay(create_equipment_sizing_agent(self.deep_thinking_llm))
        safety_risk_analyst = self._wrap_with_delay(create_safety_risk_analyst(self.deep_thinking_llm))
        project_manager = self._wrap_with_delay(create_project_manager(self.deep_thinking_llm))
        
        # Add implemented nodes (expand as agents are developed)
        graph.add_node("process_requirements_analyst", process_requirements_analyst)
        graph.add_node("innovative_researcher", innovative_researcher)
        graph.add_node("conservative_researcher", conservative_researcher)
        graph.add_node("concept_detailer", concept_detailer)
        graph.add_node("design_basis_analyst", design_basis_analyst)
        graph.add_node("basic_pfd_designer", basic_pfd_designer)
        graph.add_node("equipments_and_streams_list_builder", equipments_and_streams_list_builder)
        graph.add_node("equipment_list_builder", equipment_list_builder)
        graph.add_node("stream_data_estimator", stream_data_estimator)
        graph.add_node("equipment_sizing_agent", equipment_sizing_agent)
        graph.add_node("safety_risk_analyst", safety_risk_analyst)
        graph.add_node("project_manager", project_manager)
        
        # Set entry point
        graph.set_entry_point("process_requirements_analyst")
        graph.add_edge("process_requirements_analyst", "innovative_researcher")
        graph.add_edge("innovative_researcher", "conservative_researcher")
        graph.add_edge("conservative_researcher", "concept_detailer")
        graph.add_edge("concept_detailer", "design_basis_analyst")
        graph.add_edge("design_basis_analyst", "basic_pfd_designer")
        graph.add_edge("basic_pfd_designer", "equipments_and_streams_list_builder")
        graph.add_edge("equipments_and_streams_list_builder", "stream_data_estimator")
        graph.add_edge("stream_data_estimator", "equipment_list_builder")
        graph.add_edge("equipment_list_builder", "equipment_sizing_agent")
        graph.add_edge("equipment_sizing_agent", "safety_risk_analyst")
        graph.add_edge("safety_risk_analyst", "project_manager")
        graph.add_edge("project_manager", END)
        
        # graph.add_edge("design_basis_analyst", END)
        # graph.add_edge("equipment_sizing_agent", END)
        
        if self.checkpointer is not None:
            return graph.compile(checkpointer=self.checkpointer)
        return graph.compile()
