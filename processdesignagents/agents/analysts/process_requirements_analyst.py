from typing import Dict, Any
from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter
from processdesignagents.agents.utils.json_utils import extract_json_from_response
from processdesignagents.default_config import load_config
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

class DesignState:  # Local type hint; import from graph if centralized
    pass  # Placeholder; use TypedDict from graph in full import

def process_requirements_analyst(state: DesignState) -> DesignState:
    """Process Requirements Analyst: Extracts key design requirements using LLM."""
    config = load_config()
    llm = ChatOpenRouter(model=config["quick_think_llm"], temperature=0.7)
    prompt = f"""
    Analyze the following chemical process design problem and extract structured requirements.
    Problem: {state['problem_statement']}
    Output a JSON object with keys: throughput (kg/h), components, purity (%), yield_target (%), constraints (list of strings).
    Focus on chemical engineering aspects; infer reasonable defaults if unspecified.
    """
    response = llm.invoke(prompt)
    
    try:
        clean_json = extract_json_from_response(response.content)
        requirements = json.loads(clean_json)
    except (json.JSONDecodeError, ValueError):
        requirements = {"throughput": 1000, "purity": 99, "yield_target": 95, "constraints": ["Environmental compliance"]}

    state["requirements"] = requirements
    print(f"Extracted requirements: {requirements}")
    return state