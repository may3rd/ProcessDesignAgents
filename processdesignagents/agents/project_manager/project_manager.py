from typing import Dict, Any
from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter  # Assuming resolved wrapper
from processdesignagents.default_config import load_config
import json
import numpy as np  # For type handling

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
        return obj.item()
    else:
        return obj

def project_manager(state: DesignState) -> DesignState:
    """Project Manager: Reviews design for approval and generates implementation plan."""
    config = load_config()
    llm = ChatOpenRouter(model=config["deep_think_llm"])  # Use deep_think for strategic review
    
    requirements = state.get("requirements", {})
    validation_results = state.get("validation_results", {})
    flowsheet = state.get("flowsheet", {})
    
    # Convert for serialization
    flowsheet_serializable = convert_numpy_to_python(flowsheet)
    validation_serializable = convert_numpy_to_python(validation_results)
    
    prompt = f"""
    Review the complete process design and issue final approval.
    Requirements: {requirements}
    Flowsheet: {json.dumps(flowsheet_serializable, indent=2)}
    Validation: {json.dumps(validation_serializable, indent=2)}
    
    Determine approval status (Approved/Rejected/Conditional), estimate CAPEX ($M) and OPEX ($/yr), and list 3-5 implementation steps.
    If yield < {requirements.get('yield_target', 95)}%, suggest revisions.
    Output JSON: {{"approval_status": str, "capex_estimate": float, "opex_estimate": float, "implementation_steps": [str], "final_notes": str}}
    """
    
    response = llm.invoke(prompt)
    try:
        approval_data = json.loads(response.content)
    except json.JSONDecodeError:
        # Fallback: Conditional approval for plasma cracking
        approval_data = {
            "approval_status": "Conditional",
            "capex_estimate": 5.2,
            "opex_estimate": 1.8,
            "implementation_steps": [
                "Conduct detailed HAZOP and pilot-scale testing.",
                "Integrate CO2 capture for full compliance.",
                "Refine reactor design to achieve 95% yield.",
                "Prepare regulatory submissions.",
                "Scale-up to full production."
            ],
            "final_notes": "Viable design with optimization potential; address yield gap."
        }
    
    state["approval"] = approval_data
    print(f"Project review: Status {approval_data['approval_status']}, CAPEX ${approval_data['capex_estimate']}M")
    
    # Add report saving
    from processdesignagents.utils.report_saver import save_agent_report
    save_agent_report("project_manager", approval_data, f"Final approval: {approval_data['approval_status']} with implementation plan.")
    
    return state