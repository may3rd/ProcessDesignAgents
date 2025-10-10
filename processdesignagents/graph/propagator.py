from typing import Dict, Any
from langchain_core.messages import HumanMessage
from processdesignagents.agents.utils.agent_states import DesignState
import uuid

class Propagator:
    """Handle state initialization and propagation through the graph."""
    
    def __init__(self, max_recur_limit: int = 100):
        """Initialize with configuration parameters."""
        self.max_recur_limit = max_recur_limit
        
    def create_initial_state(
        self, problem_statement: str
    ) -> Dict[str, Any]:
        """Create the initial state for the agent graph."""
        return {
            "messages": [HumanMessage(content=problem_statement)],
            "problem_statement": problem_statement,
            "requirements": "",
            "literature_data": "",
            "research_concepts": "",
            "selected_concept_details": "",
            "selected_concept_name": "",
            "flowsheet": "",
            "validation_results": "",
            "approval": ""
        }
        
    def get_graph_args(self) -> Dict[str, Any]:
        """Get arguments for the graph invocation."""
        thread_id = str(uuid.uuid4())
        return {
            "stream_mode": "values",
            "config": {
                "recursion_limit": self.max_recur_limit,
                "configurable": {"thread_id": thread_id},
            },
        }
        
