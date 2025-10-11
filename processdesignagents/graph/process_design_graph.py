from pathlib import Path
import json

from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any

from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
# from langchain_google import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

from processdesignagents.default_config import DEFAULT_CONNFIG
from .setup import GraphSetup
from .propagator import Propagator
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

class ProcessDesignGraph:
    """Main class that orchestractes the process design workflow."""
    
    def __init__(
        self,
        debug=False,
        config: Dict[str, Any]=None,
    ):
        """Initialize the process design agents graph and component.
        Args:
            debug: Whether to run in debug mode
            config: Configuration dictionary
        """
        self.debug = debug
        self.config = config or DEFAULT_CONNFIG

        # Initialize LLMs
        if self.config["llm_provider"].lower() == "openai" or self.config["llm_provider"] == "ollama" or self.config["llm_provider"] == "openrouter":
            if self.config["llm_provider"] == "openrouter":
                base_url = "https://openrouter.ai/api/v1"
                api_key = os.getenv("OPENROUTER_API_KEY")
            self.deep_thinking_llm = ChatOpenAI(model=self.config["deep_think_llm"], base_url=base_url, api_key=api_key)
            self.quick_thinking_llm = ChatOpenAI(model=self.config["quick_think_llm"], base_url=base_url, api_key=api_key)
        # elif self.config["llm_provider"].lower() == "anthropic":
        #     self.deep_thinking_llm = ChatAnthropic(model=self.config["deep_think_llm"], base_url=self.config["backend_url"])
        #     self.quick_thinking_llm = ChatAnthropic(model=self.config["quick_think_llm"], base_url=self.config["backend_url"])
        # elif self.config["llm_provider"].lower() == "google":
        #     self.deep_thinking_llm = ChatGoogleGenerativeAI(model=self.config["deep_think_llm"])
        #     self.quick_thinking_llm = ChatGoogleGenerativeAI(model=self.config["quick_think_llm"])
        else:
            raise ValueError(f"Unsupported LLM provider: {self.config['llm_provider']}")

        self.checkpointer = MemorySaver()

        self.graph_setup = GraphSetup(
            self.quick_thinking_llm,
            self.deep_thinking_llm,
            checkpointer=self.checkpointer,
        )
        
        self.propagator = Propagator()
        self.problem_statement = None
        self.log_state_dict = {}
        
        # Set up the graph
        self.graph = self.graph_setup.setup_graph()
        
    def proagate(self, problem_statement: str=""):
        self.problem_statement = problem_statement
        
        init_agent_state = self.propagator.create_initial_state(problem_statement)

        args = self.propagator.get_graph_args()
        
        if self.debug:
            # Debug mode with tracing
            trace = []
            for chunk in self.graph.stream(init_agent_state, **args):
                if len(chunk["messages"]) == 0:
                    pass
                else:
                    chunk["messages"][-1].pretty_print()
                    trace.append(chunk)
                    
            final_state = trace[-1]
        else:
            # Run the graph
            final_state = self.graph.invoke(init_agent_state, **args)
            print(f"\n=========================== Finish Line ===========================")
        
        # Store current state for reflection
        self.curr_state = final_state
        
        # Log state
        self._log_state(final_state)
        
        # Return
        return final_state
    
    def _log_state(self, final_state):
        """Log the final state to a JSON file."""
        self.log_state_dict = {
            "problem_statement": final_state.get("problem_statement", ""),
            "requirements": final_state.get("requirements", ""),
            "design_basis": final_state.get("design_basis", ""),
            "literature_data": final_state.get("literature_data", ""),
            "research_concepts": final_state.get("research_concepts", ""),
            "selected_concept_details": final_state.get("selected_concept_details", ""),
            "selected_concept_name": final_state.get("selected_concept_name", ""),
            "basic_pdf": final_state.get("basic_pdf", ""),
            "basic_hmb_results": final_state.get("basic_hmb_results", ""),
            "basic_equipment_template": final_state.get("basic_equipment_template", ""),
            "basic_stream_data": final_state.get("basic_stream_data", ""),
            "approval": final_state.get("approval", ""),
        }
        
        # Save to file
        directory = Path(f"eval_results/ProcessDesignAgents_logs/")
        directory.mkdir(parents=True, exist_ok=True)
        
        with open(
            f"eval_results/ProcessDesignAgents_logs/full_states_log.json", "w"
        ) as f:
            json.dump(self.log_state_dict, f, indent=4)
        
