from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any

from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
# from langchain_google import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

from processdesignagents.default_config import DEFAULT_CONNFIG
from processdesignagents.agents.utils.agent_states import DesignState

from .setup import GraphSetup
from .propagator import Propagator

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
        # if self.config["llm_provider"].lower() == "openai" or self.config["llm_provider"] == "ollama" or self.config["llm_provider"] == "openrouter":
        #     self.deep_thinking_llm = ChatOpenAI(model=self.config["deep_think_llm"], base_url=self.config["backend_url"])
        #     self.quick_thinking_llm = ChatOpenAI(model=self.config["quick_think_llm"], base_url=self.config["backend_url"], api_key=os.getenv("OPENAI_API_KEY"))
        # elif self.config["llm_provider"].lower() == "anthropic":
        #     self.deep_thinking_llm = ChatAnthropic(model=self.config["deep_think_llm"], base_url=self.config["backend_url"])
        #     self.quick_thinking_llm = ChatAnthropic(model=self.config["quick_think_llm"], base_url=self.config["backend_url"])
        # elif self.config["llm_provider"].lower() == "google":
        #     self.deep_thinking_llm = ChatGoogleGenerativeAI(model=self.config["deep_think_llm"])
        #     self.quick_thinking_llm = ChatGoogleGenerativeAI(model=self.config["quick_think_llm"])
        # else:
        #     raise ValueError(f"Unsupported LLM provider: {self.config['llm_provider']}")

        self.graph_setup = GraphSetup(
            self.config["quick_think_llm"],
            self.config["deep_think_llm"],
        )
        
        self.propagator = Propagator()
        
        # Set up the graph
        self.graph = self.graph_setup.setup_graph()
        
    def proagate(self, problem_statement: str=""):
        self.problem_statement = problem_statement
        
        init_agent_state = self.propagator.create_initial_state(problem_statement)

        args = self.propagator.get_graph_args()
        
        final_state = self.graph.invoke(init_agent_state, **args)
        
        self.curr_state = final_state
        
        return final_state