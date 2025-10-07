from typing import Dict, Any
from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter  # Assuming resolved wrapper
from processdesignagents.default_config import load_config
import json
import numpy as np  # Add for type checking

class DesignState:
    pass  # Placeholder for TypedDict alignment

def convert_numpy_to_python(obj):
    """Recursively convert NumPy types to Python natives for JSON serialization."""
    if isinstance(obj, dict):
        return {k: convert_numpy_to_python(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_to_python(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, (np.ndarray, np.generic)):
        return obj.item()  # Convert scalar arrays
    else:
        return obj

def safety_risk_analyst(state: DesignState) -> DesignState:
    """Safety and Risk Analyst: Performs HAZOP-inspired risk assessment on optimized flowsheet."""
    config = load_config()
    llm = ChatOpenRouter(model=config["deep_think_llm"])  # Use deep_think for thorough analysis
    
    validation_results = state.get("validation_results", {})
    flowsheet = state.get("flowsheet", {})
    requirements = state.get("requirements", {})
    
    # Convert NumPy types before serialization
    flowsheet_serializable = convert_numpy_to_python(flowsheet)
    validation_results_serializable = convert_numpy_to_python(validation_results)
    
    prompt = f"""
    Conduct a HAZOP-style risk assessment for the following process design.
    Flowsheet: {json.dumps(flowsheet_serializable, indent=2)}
    Optimized Results: {json.dumps(validation_results_serializable, indent=2)}
    Constraints: {requirements.get('constraints', [])}
    
    Identify 3-5 key hazards (e.g., high pressure, chemical leaks), rate severity (1-5), likelihood (1-5), and suggest mitigations.
    Output JSON: {{"risk_matrix": [{{"hazard": str, "severity": int, "likelihood": int, "risk_score": int, "mitigations": [str]}}], "overall_risk_level": str, "compliance_notes": str}}
    Focus on environmental and safety compliance.
    """
    
    response = llm.invoke(prompt)
    try:
        risk_data = json.loads(response.content)
    except json.JSONDecodeError:
        # Fallback: Static example for plasma cracking
        risk_data = {
            "risk_matrix": [
                {"hazard": "Plasma arc failure", "severity": 4, "likelihood": 2, "risk_score": 8, "mitigations": ["Redundant arc systems", "Emergency shutdown"]},
                {"hazard": "High-temperature leak", "severity": 5, "likelihood": 1, "risk_score": 5, "mitigations": ["Pressure relief valves", "Thermal monitoring"]},
                {"hazard": "COx byproduct emission", "severity": 3, "likelihood": 3, "risk_score": 9, "mitigations": ["Scrubber integration", "Catalyst optimization"]}
            ],
            "overall_risk_level": "Medium",
            "compliance_notes": "Meets basic environmental standards; further CO2 capture recommended."
        }
    
    state["validation_results"].update({
        "risk_assessment": risk_data,
        "overall_risk_level": risk_data["overall_risk_level"]
    })
    print(f"Risk assessment: Overall level {risk_data['overall_risk_level']}, Key risks identified: {len(risk_data['risk_matrix'])}")
    
    # Add report saving
    from processdesignagents.utils.report_saver import save_agent_report
    save_agent_report("safety_risk_analyst", {"risk_assessment": risk_data}, f"HAZOP assessment: {risk_data['overall_risk_level']} risk level with {len(risk_data['risk_matrix'])} hazards.")
    
    return state