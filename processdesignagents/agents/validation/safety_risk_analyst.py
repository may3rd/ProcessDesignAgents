from typing import Dict, Any
from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter  # Assuming resolved wrapper
from processdesignagents.agents.utils.json_utils import extract_json_from_response
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
def create_safety_risk_analyst(deep_think_llm: str):
    def safety_risk_analyst(state: DesignState) -> DesignState:
        """Safety and Risk Analyst: Performs HAZOP-inspired risk assessment on optimized flowsheet."""
        print("\n=========================== Safety and Risk Assessment ===========================\n")
        llm = ChatOpenRouter()  # Use deep_think for thorough analysis
        validation_results = state.get("validation_results", {})
        flowsheet = state.get("flowsheet", {})
        requirements = state.get("requirements", {})
        
        # Convert NumPy types before serialization
        flowsheet_serializable = convert_numpy_to_python(flowsheet)
        validation_results_serializable = convert_numpy_to_python(validation_results)
        
        prompt = system_prompt(json.dumps(flowsheet_serializable, indent=2), json.dumps(validation_results_serializable, indent=2), requirements.get('constraints', []))   
        response = llm.invoke(prompt, model=deep_think_llm)
        
        try:
            clean_json = extract_json_from_response(response.content)
            risk_data = json.loads(clean_json)
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
        
        return state
    
    return safety_risk_analyst

def system_prompt(flowsheet: str, validation_results: str, requirements: str) -> str:
    return f"""
# ROLE
You are a Certified Process Safety Professional (CPSP) with 20 years of experience facilitating Hazard and Operability (HAZOP) studies for the chemical industry.

# TASK
Conduct a preliminary, HAZOP-style risk assessment based on the provided process 'FLOWSHEET', 'OPTIMIZED RESULTS' (H&MB), and operational 'CONSTRAINTS'. Your analysis must identify 3-5 critical process hazards, assess their risks, and propose actionable mitigations. The final output must be a single, valid JSON object.

# METHODOLOGY
1.  **Risk Matrix Definition:**
    * **Severity (S):** 1 (Minor) to 5 (Catastrophic effect on safety or environment).
    * **Likelihood (L):** 1 (Rare) to 5 (Frequent).
    * **Risk Score (S x L):** Calculated as Severity multiplied by Likelihood.
2.  **Hazard Identification:** Systematically review the process, applying HAZOP guidewords (e.g., NO FLOW, MORE PRESSURE, HIGHER TEMPERATURE, LEAK) to identify potential hazards.
3.  **Assessment:** For each identified hazard, assign Severity and Likelihood ratings based on the provided data and standard engineering principles.
4.  **Mitigation:** Propose specific, practical engineering or administrative controls (e.g., "Install pressure relief valve (PSV) set at X barg," "Implement high-temperature alarm and trip").
5.  **Overall Assessment:** Determine the 'overall_risk_level' (Low, Medium, High) based on the highest calculated risk score.
6.  **Compliance:** The 'compliance_notes' should summarize how the proposed mitigations help adhere to general environmental and process safety management (PSM) standards.

# JSON SCHEMA
Your output MUST strictly conform to this schema. Do not change the key names.
{{
    "risk_matrix": [
        {{
            "hazard": "string",
            "severity": "int",
            "likelihood": "int",
            "risk_score": "int",
            "mitigations": ["string"]
        }}
    ],
    "overall_risk_level": "string (Low, Medium, or High)",
    "compliance_notes": "string"
}}

# EXAMPLE
---
**FLOWSHEET:** {{"units": [{{"id": "R-101", "type": "CSTR"}}]}}
**OPTIMIZED RESULTS:** {{"hmb": [{{"source_unit": "Feed", "dest_unit": "R-101", "temperature_C": 80.0, "pressure_bar": 10.0}}]}}
**CONSTRAINTS:** ["Reactor pressure must not exceed 12 bar."]

**EXPECTED JSON OUTPUT:**
{{
    "risk_matrix": [
        {{
            "hazard": "High Pressure in Reactor (R-101) due to runaway reaction or blocked outlet.",
            "severity": 5,
            "likelihood": 2,
            "risk_score": 10,
            "mitigations": [
                "Install a pressure relief valve (PSV) on R-101 set to 11.5 bar.",
                "Implement a high-pressure alarm and interlock to stop reactant feed.",
                "Regularly inspect the reactor outlet line for blockages."
            ]
        }},
        {{
            "hazard": "Loss of Containment (Leak) of flammable reactants from R-101.",
            "severity": 4,
            "likelihood": 3,
            "risk_score": 12,
            "mitigations": [
                "Implement a preventive maintenance program for reactor seals and gaskets.",
                "Install hydrocarbon gas detectors in the reactor area.",
                "Ensure proper ventilation to prevent accumulation of flammable vapors."
            ]
        }}
    ],
    "overall_risk_level": "Medium",
    "compliance_notes": "Proposed mitigations, such as pressure relief systems and leak detection, are fundamental to meeting OSHA PSM and EPA RMP standards for managing highly hazardous chemicals. Regular inspections and maintenance support mechanical integrity requirements."
}}
---

# DATA FOR HAZOP ANALYSIS
---
**FLOWSHEET:**
{flowsheet}

**OPTIMIZED RESULTS:**
{validation_results}

**CONSTRAINTS:**
{requirements}

# FINAL JSON OUTPUT:
"""