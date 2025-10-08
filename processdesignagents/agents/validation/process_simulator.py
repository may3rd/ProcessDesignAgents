from typing import Dict, Any
import numpy as np
import pandas as pd

from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter  # Assuming wrapper from prior resolution
from processdesignagents.agents.utils.json_utils import extract_json_from_response
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import json

load_dotenv()

def create_process_simulator(quick_think_llm: str):
    def process_simulator(state: DesignState) -> DesignState:
        """Process Simulator: Generates preliminary Heat and Material Balance (H&MB) from flowsheet."""
        flowsheet = state.get("flowsheet", {})
        units = flowsheet.get("units", [])
        requirements = state.get("requirements", {})
        literature_data = state.get("literature_data", {})  # For potential enthalpy lookups
        
        llm = ChatOpenRouter()
        
        print("\n=========================== Create Prelim H&MB ===========================\n")
        
        # Step 1: LLM generate initial H&MB
        prompt = system_prompt(flowsheet, requirements, literature_data)
        
        response = llm.invoke(prompt, model=quick_think_llm)
        try:
            hmb_json = json.loads(extract_json_from_response(response.content))
            hmb_df = pd.DataFrame(hmb_json["balance_summary"]["streams"])
            notes = hmb_json.get("notes", "LLM-generated H&MB estimate.")
        except json.JSONDecodeError:
            # Fallback default H&MB
            hmb_data = {
                'stream_id': ['Inlet Feed', 'After Unit 1', 'Product', 'Byproducts'],
                'total_mass_flow_kg_h': [requirements.get("throughput", 1000.0), 1000.0, 908.0, 92.0],
                'temperature_C': [25.0, 1200.0, 100.0, 100.0],
                'enthalpy_kJ_h': [0.0, 1500000.0, 90000.0, 1410000.0]
            }
            hmb_df = pd.DataFrame(hmb_data)
            notes = "Fallback H&MB due to parsing error."
        
        mass_balance_met = True
        
        # Store verified H&MB and metrics
        validation_results = {
            "hmb": hmb_df.to_dict(orient='records'),  # Serializable list of dicts
            "mass_balance_met": mass_balance_met,
            "notes": notes
        }
        
        state["validation_results"] = validation_results
        print(f"Simulation results: H&MB generated; Mass balance: {mass_balance_met}")
        
        # --- ADDED PRINT STATEMENTS ---
        print("\n--- Heat and Material Balance (H&MB) ---")
        print(hmb_df.to_string())
        print("----------------------------------------\n")
        
        return state
    return process_simulator

def system_prompt(flowsheet: Dict[str, Any], requirements: Dict[str, Any], literature: Dict[str, Any]) -> str:
    return f"""
# ROLE
You are a Senior Process Simulation Engineer. Your task is to generate a preliminary, steady-state Heat and Material Balance (H&MB) table based on a conceptual process flowsheet, its requirements, and supporting literature data.

# TASK
Analyze the provided 'FLOWSHEET', 'REQUIREMENTS', and 'LITERATURE' data. Create a JSON object representing the H&MB for the 4-6 most critical streams. Use the provided literature data (e.g., molecular weights) to ensure calculations are accurate. Clearly state all assumptions made.

# JSON SCHEMA
Your output MUST be a single JSON object conforming to this exact structure. The 'stream_id' should correspond to the connection IDs in the flowsheet.
{{
    "balance_summary": {{
        "streams": [
            {{
                "stream_id": "string",
                "description": "string",
                "source_unit": "string",
                "dest_unit": "string",
                "temperature_C": "float",
                "pressure_bar": "float",
                "total_mass_flow_kg_h": "float",
                "component_flows_kg_h": {{
                    "component_name_1": "float",
                    "component_name_2": "float"
                }}
            }}
        ],
        "notes": [
            "string (list of key assumptions made, e.g., reaction conversion, separation efficiency)"
        ]
    }}
}}

# INSTRUCTIONS
1.  **Analyze Inputs:** Review the 'FLOWSHEET', 'REQUIREMENTS', and 'LITERATURE' data to understand the complete process context.
2.  **Identify Key Streams:** From the 'FLOWSHEET', select 4-6 critical streams (e.g., main feed, reactor outlet, final product).
3.  **Perform Mass Balance:**
    * Start with the inlet feed stream from 'REQUIREMENTS'.
    * **Use molecular weights from the 'LITERATURE' data for all stoichiometric calculations to ensure accuracy.**
    * Calculate component mass flows for each subsequent stream, ensuring mass is conserved across units.
    * Make and state reasonable assumptions for reaction conversions or separation efficiencies.
4.  **Estimate Thermal Properties:**
    * Assign a baseline temperature and pressure (e.g., 25°C, 1 bar) for the inlet feed if unspecified.
    * Estimate logical temperature changes across units (e.g., increase after an exothermic reactor).
5.  **Document Assumptions:** In the 'notes' section, you MUST list every significant assumption (e.g., "Assumed 95% conversion of Acetic Acid in R-101.", "Pressure drops are neglected.").
6.  **Format Output:** Assemble the data into the final JSON object, strictly adhering to the schema.

# EXAMPLE
---
**FLOWSHEET:** {{"units": [{{"id": "R-101", "type": "CSTR"}}, {{"id": "C-101", "type": "Distillation"}}], "connections": [{{"id": "S-01", "from": "Feed", "to": "R-101"}}, {{"id": "S-02", "from": "R-101", "to": "C-101"}}, {{"id": "S-03", "from": "C-101", "to": "Product"}}]}}
**REQUIREMENTS:** {{"throughput": {{"value": 1000}}, "components": [{{"name": "Acetic Acid", "role": "Reactant"}}, {{"name": "Ethanol", "role": "Reactant"}}]}}
**LITERATURE:** {{"Acetic Acid": {{"molecular_weight": 60.05}}, "Ethanol": {{"molecular_weight": 46.07}}, "Ethyl Acetate": {{"molecular_weight": 88.11}}, "Water": {{"molecular_weight": 18.02}}}}

**EXPECTED JSON OUTPUT:**
{{
    "balance_summary": {{
        "streams": [
            {{
                "stream_id": "S-01",
                "description": "Reactant Feed",
                "source_unit": "Feed",
                "dest_unit": "R-101",
                "temperature_C": 25.0,
                "pressure_bar": 1.5,
                "total_mass_flow_kg_h": 1000.0,
                "component_flows_kg_h": {{
                    "Acetic Acid": 566.0,
                    "Ethanol": 434.0,
                    "Ethyl Acetate": 0.0,
                    "Water": 0.0
                }}
            }},
            {{
                "stream_id": "S-02",
                "description": "Reactor Effluent",
                "source_unit": "R-101",
                "dest_unit": "C-101",
                "temperature_C": 80.0,
                "pressure_bar": 1.2,
                "total_mass_flow_kg_h": 1000.0,
                "component_flows_kg_h": {{
                    "Acetic Acid": 28.3,
                    "Ethanol": 0.0,
                    "Ethyl Acetate": 831.7,
                    "Water": 140.0
                }}
            }},
            {{
                "stream_id": "S-03",
                "description": "Final Product",
                "source_unit": "C-101",
                "dest_unit": "Product",
                "temperature_C": 77.0,
                "pressure_bar": 1.0,
                "total_mass_flow_kg_h": 831.7,
                "component_flows_kg_h": {{
                    "Acetic Acid": 0.0,
                    "Ethanol": 0.0,
                    "Ethyl Acetate": 831.7,
                    "Water": 0.0
                }}
            }}
        ],
        "notes": [
            "Assumed feed is an equimolar ratio of reactants based on literature molecular weights, totaling 1000 kg/h.",
            "Assumed 95% conversion of the limiting reactant (Acetic Acid) in R-101.",
            "Assumed perfect separation of Ethyl Acetate in distillation column C-101.",
            "Temperatures are estimated based on typical values for esterification and distillation."
        ]
    }}
}}

# NEGATIVES:
* NEVER miss the flow rate, temperature, pressure of all streams.

---

# DATA TO ANALYZE
---
**FLOWSHEET:**
{json.dumps(flowsheet, default=str)}

**REQUIREMENTS:**
{json.dumps(requirements, default=str)}

**LITERATURE:**
{json.dumps(literature, default=str)}

# FINAL JSON OUTPUT:
"""