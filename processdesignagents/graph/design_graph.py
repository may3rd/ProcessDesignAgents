from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any
from langchain_openai import ChatOpenAI
from processdesignagents.default_config import load_config
from openai import AuthenticationError
import ast
import json
import os
from dotenv import load_dotenv

# Load environment variables (e.g., for API keys)
load_dotenv()

class DesignState(TypedDict):
    problem_statement: str
    requirements: Dict[str, Any]  # New field for analyst outputs
    flowsheet: Dict[str, Any]
    validation_results: Dict[str, Any]

def _fallback_requirements(problem_statement: str) -> Dict[str, Any]:
    """Generate deterministic requirements when the LLM path is unavailable."""
    return {
        "throughput": 1000,
        "purity": 98,
        "yield_target": 95,
        "constraints": [
            "Meet environmental regulations",
            "Keep operating costs reasonable",
            f"Address key concern mentioned in problem: {problem_statement[:60]}...",
        ],
    }


def _response_content_to_str(response: Any) -> str:
    """Best-effort conversion of LangChain responses to raw text."""
    content = getattr(response, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                texts.append(item.get("text") or "")
            elif hasattr(item, "text"):
                texts.append(getattr(item, "text") or "")
        return "".join(texts)
    return str(content)


def analyst_node(state: DesignState) -> DesignState:
    """Process Requirements Analyst: Extracts key design requirements using LLM."""
    config = load_config()
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("OPENROUTER_API_KEY is not set; falling back to heuristic requirements.")
        state["requirements"] = _fallback_requirements(state["problem_statement"])
        return state

    llm = ChatOpenAI(
        model=config["quick_think_llm"],
        api_key="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",
        base_url="https://openrouter.ai/api/v1",
        # Optional: Add for request tracking (recommended by OpenRouter for debugging)
        default_headers={
            "HTTP-Referer": "https://github.com/may3rd/ProcessDesignAgents",  # Replace with your repo URL
            "X-Title": "ProcessDesignAgents",
        },
    )

    prompt = (
        "Analyze the following chemical process design problem and extract "
        "structured requirements.\n"
        f"Problem: {state['problem_statement']}\n\n"
        "Output a JSON object with keys: throughput (kg/h), purity (%), "
        "yield_target (%), constraints (list of strings). Focus on chemical "
        "engineering aspects; infer reasonable defaults if unspecified."
    )

    messages = [
        ("system", "You are a helpful assistant."),
        ("human", prompt),
    ]

    try:
        response = llm.invoke(messages)
        content = _response_content_to_str(response)
        requirements = json.loads(content)
    except AuthenticationError as auth_err:
        raise RuntimeError(
            "Authentication with OpenRouter failed. Double-check that your "
            "OPENROUTER_API_KEY is valid and active."
        ) from auth_err
    except json.JSONDecodeError:
        # Handle relaxed JSON outputs coming from certain models
        try:
            requirements = ast.literal_eval(content)
        except (ValueError, SyntaxError):
            requirements = _fallback_requirements(state["problem_statement"])
    except Exception as exc:  # Broad catch to keep pipeline usable offline
        print(f"LLM call failed ({exc}); using heuristic requirements instead.")
        requirements = _fallback_requirements(state["problem_statement"])

    if not isinstance(requirements, dict):
        requirements = _fallback_requirements(state["problem_statement"])

    state["requirements"] = requirements
    print(f"Extracted requirements: {requirements}")
    return state

def build_graph():
    graph = StateGraph(DesignState)
    
    # Add nodes
    graph.add_node("analyst", analyst_node)
    
    # Set entry point
    graph.set_entry_point("analyst")
    
    # Direct flow to END
    graph.add_edge("analyst", END)
    
    return graph.compile()
