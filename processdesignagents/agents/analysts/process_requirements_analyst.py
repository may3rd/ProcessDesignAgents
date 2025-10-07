from typing import Dict, Any
from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter
from processdesignagents.default_config import load_config
import os
from dotenv import load_dotenv
import json

load_dotenv()

class DesignState:  # Local type hint; import from graph if centralized
    pass  # Placeholder; use TypedDict from graph in full import

def process_requirements_analyst(state: DesignState) -> DesignState:
    """Process Requirements Analyst: Extracts key design requirements using LLM."""
    config = load_config()
    llm = ChatOpenRouter(model=config["quick_think_llm"])
    prompt = f"""
    Analyze the following chemical process design problem and extract structured requirements.
    Problem: {state['problem_statement']}
    Output a JSON object with keys: throughput (kg/h), purity (%), yield_target (%), constraints (list of strings).
    Focus on chemical engineering aspects; infer reasonable defaults if unspecified.
    """
    response = llm.invoke(prompt)
    try:
        requirements = json.loads(response.content)
    except json.JSONDecodeError:
        requirements = {"throughput": 1000, "purity": 99, "yield_target": 95, "constraints": ["Environmental compliance"]}
    state["requirements"] = requirements
    print(f"Extracted requirements: {requirements}")
    return state