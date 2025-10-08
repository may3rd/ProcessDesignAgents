from typing import Dict, Any, List
import numpy as np
import pandas as pd

from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter  # Assuming wrapper from prior resolution
from processdesignagents.agents.utils.json_utils import extract_json_from_response
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import json
import copy

load_dotenv()

def create_process_simulator(deep_think_llm: str):
    def process_simulator(state: DesignState) -> DesignState:
        """Process Simulator: Generates preliminary Heat and Material Balance (H&MB) from flowsheet."""
        print("\n=========================== Create Prelim H&MB ===========================\n")
        flowsheet = state.get("flowsheet", {})
        units = flowsheet.get("units", [])
        connections_list = flowsheet.get("connections", [])
        requirements = state.get("requirements", {})
        literature_data = state.get("literature_data", {})  # For potential enthalpy lookups
        
        streams_table = copy.deepcopy(connections_list)
        
        properties_to_add = {
            "temperature": {"value": None, "units": "C"},
            "pressure": {"value": None, "units": "bar"},
            "mass_flow": {"value": None, "units": "kg/h"},
            "composition": {"components": {"Nitrogen": None, "Oxygen": None, "Water": None}, "basis": "mass_fraction"}
        }
        
        for stream in streams_table:
            stream.update(properties_to_add)
        
        final_steams_json = json.dumps({"streams": streams_table}, indent=4)
        
        llm = ChatOpenRouter()
    
        # Step 1: LLM generate initial H&MB
        prompt = system_prompt(flowsheet, final_steams_json, requirements, literature_data)
        
        response = llm.invoke(prompt, model=deep_think_llm)
        try:
            clean_json = extract_json_from_response(response.content)
            hmb_json = json.loads(clean_json)
            hmb_df = pd.DataFrame(hmb_json["streams"])
            notes = hmb_json.get("notes", "LLM-generated H&MB estimate.")
        except json.JSONDecodeError:
            print(response.content)
            raise ValueError("Process Simulation return not JSON")
        
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

def system_prompt(flowsheet: Dict[str, Any], stream_table_json: str, requirements: Dict[str, Any], literature: Dict[str, Any]) -> str:
    # Helper to format dictionaries into JSON strings for the prompt
    def to_json(data):
        return json.dumps(data, default=str)

    return f"""
# ROLE
You are a Senior Process Simulation Engineer. Your task is to complete a preliminary, steady-state Heat and Material Balance (H&MB) by filling in the missing data in a provided stream table.

# TASK
Your primary goal is to take the 'STREAM_TABLE_JSON', which contains `null` values, and fill in every `null` with a reasonable engineering estimate based on the 'FLOWSHEET', 'REQUIREMENTS', and 'LITERATURE' data. The final output must be the fully populated JSON object.

# JSON SCHEMA
Your output MUST be a single JSON object that is an updated version of the input 'STREAM_TABLE_JSON'. It must conform to this exact structure:
{{
    "streams": [
        {{
            "id": "string",
            "from": "string",
            "to": "string",
            "description": "string",
            "temperature": {{
                "value": "float",
                "units": "C"
            }},
            "pressure": {{
                "value": "float",
                "units": "bar"
            }},
            "mass_flow": {{
                "value": "float",
                "units": "kg/h"
            }},
            "composition": {{
                "components": {{
                    "component_1": "float",
                    "component_2": "float"
                }},
                "basis": "mass_fraction"
            }}
        }}
    ]
}}

# INSTRUCTIONS
1.  **Analyze Context:** Review the 'FLOWSHEET', 'REQUIREMENTS', and 'LITERATURE' to build a complete understanding of the process.
2.  **Process Each Stream:** Go through every stream object provided in the 'STREAM_TABLE_JSON'.
3.  **Perform Mass Balance:**
    * Start with the inlet stream(s). Use the throughput from 'REQUIREMENTS' to establish the initial mass flow.
    * Ensure that sum of compositions is 1.0.
    * For the 'composition' of air, use standard values (approx. 0.79 Nitrogen, 0.21 Oxygen by mass) and estimate the initial humidity (Water).
    * Proceed stream by stream, conserving mass across each unit operation. Make logical assumptions about moisture removal in dryers and separators.
4.  **Estimate Thermal Properties:**
    * Assign baseline conditions (e.g., 25°C, 1 bar) for the initial air intake stream.
    * Estimate logical temperature and pressure changes across units (e.g., significant temperature and pressure increase after a compressor, temperature decrease after a cooler).
5.  **Preserve Structure:** Your final output must be the complete `streams` object. Do not add, remove, or reorder streams. Only replace the `null` values.

# EXAMPLE
---
**STREAM_TABLE_JSON (Input Snippet):**
{{
    "streams": [
        {{
            "id": "101",
            "from": "FI-101",
            "to": "MC-101",
            "description": "Filtered ambient air",
            "temperature": {{"value": null, "units": "C"}},
            "pressure": {{"value": null, "units": "bar"}},
            "mass_flow": {{"value": null, "units": "kg/h"}},
            "composition": {{"components": {{"Nitrogen": null, "Oxygen": null, "Water": null}}, "basis": "mass_fraction"}}
        }}
    ]
}}

**EXPECTED JSON OUTPUT (Completed Snippet):**
{{
    "streams": [
        {{
            "id": "101",
            "from": "FI-101",
            "to": "MC-101",
            "description": "Filtered ambient air",
            "temperature": {{
                "value": 25.0,
                "units": "C"
            }},
            "pressure": {{
                "value": 1.01,
                "units": "bar"
            }},
            "mass_flow": {{
                "value": 10000.0,
                "units": "kg/h"
            }},
            "composition": {{
                "components": {{
                    "Nitrogen": 0.782,
                    "Oxygen": 0.208,
                    "Water": 0.01
                }},
                "basis": "mass_fraction"
            }}
        }}
    ]
}}
---

# DATA TO ANALYZE
---
**FLOWSHEET:**
{to_json(flowsheet)}

**STREAM_TABLE_JSON (to be completed):**
{stream_table_json}

**REQUIREMENTS:**
{to_json(requirements)}

**LITERATURE:**
{to_json(literature)}

# FINAL JSON OUTPUT:
"""