from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter  # Assuming wrapper from prior resolution
from processdesignagents.agents.utils.json_utils import extract_json_from_response
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import json

load_dotenv()

def create_designer_agent(quick_think_llm: str):
    def designer_agent(state: DesignState) -> DesignState:
        """Designer Agent: Synthesizes preliminary flowsheet from research concepts."""
        print("\n=========================== Selected Concept ===========================\n")
        llm = ChatOpenRouter()
        concepts = state.get("research_concepts", {}).get("concepts", [{}])
        selected_concept = max(concepts, key=lambda c: c.get("feasibility_score", 0))  # Select highest feasibility
        prompt = system_prompt(selected_concept, state)
        response = llm.invoke(prompt, model=quick_think_llm)
        
        try:
            clean_json = extract_json_from_response(response.content)
            flowsheet_data = json.loads(clean_json)["flowsheet"]
        except (json.JSONDecodeError, KeyError):
            raise ValueError("Failed to extract flowsheet from response")
            # Fallback: Static example for ethane cracking
            flowsheet_data = {
                "units": [
                    {"id": "R-001", "name": "Cracker", "type": "Plasma Reactor", "specs": {"temperature": 1000, "pressure": 1}},
                    {"id": "S-001", "name": "Separator", "type": "Distillation Column", "specs": {"stages": 20}}
                ],
                "connections": [{"id": "101", "from": "Cracker", "to": "Separator"}],
                "overall_description": "Integrated cracking and separation for ethane-to-ethylene conversion."
            }
        
        state["flowsheet"] = flowsheet_data
        print(f"Synthesized flowsheet for {selected_concept.get('name', 'concept')}: {flowsheet_data['overall_description']}")
        
        # Print units in flowsheet
        print("\n=========================== Flowsheet Units ===========================\n")
        for unit in flowsheet_data["units"]:
            print(f"Unit ID: {unit['id']}, Name: {unit['name']}, Type: {unit['type']}")
        
        # Print connections in flowsheet
        print("\n=========================== Flowsheet Connections ===========================\n")
        for connection in flowsheet_data["connections"]:
            print(f"Connection ID: {connection['id']}, From: {connection['from']}, To: {connection['to']}")
            
        return state
    return designer_agent

def system_prompt(selected_concept: str, state: DesignState) -> str:
    return f"""
# ROLE
You are a senior process design engineer. Your task is to create a conceptual process flowsheet based on a selected design concept, technical requirements, and supporting literature.

# TASK
Synthesize a preliminary process flowsheet for the selected concept: '{selected_concept}'.
Incorporate requirements from: '{state.get('requirements', {})}' and literature insights from: '{state.get('literature_data', {})}'.
Your output must be a single, valid JSON object representing the flowsheet.

# JSON SCHEMA:
Your JSON output must conform to this exact structure and data types. Ensure all 'id' fields are unique strings (e.g., "R-101", "C-101", "S-101").
{{
    "flowsheet": {{
        "units": [
            {{
                "id": "string",
                "name": "string",
                "type": "string",
                "specs": {{
                    "description": "string"
                }}
            }}
        ],
        "connections": [
            {{
                "id": "string (e.g., '101', '102', '201', '202') format: XXX or XXXX",
                "description": "string (e.g., 'Reactant Feed', 'Crude Product')",
                "from": "string (must match a unit id)",
                "to": "string (must match a unit id)",
                "notes:": "string (optional)"
            }}
        ],
        "overall_description": "string"
    }}
}}

# INSTRUCTIONS:
1.  **Deconstruct the Process:** Analyze the 'SELECTED CONCEPT' and break it down into the main logical steps (e.g., Feed Storage / source, Feed Preparation, Reaction, Separation, Purification, Product Storage).
2.  **Identify Unit Operations:** For each process step, assign a primary unit operation. Use standard names like 'Mix Tank', 'Reactor', 'Distillation Column', 'Heat Exchanger', 'Pump', 'Surge Tank', 'Storage Tank'.
3.  **Define Material Flow:** Create a logical sequence of connections showing how material flows from one unit to the next, from raw material feed from tank or external source to final product storage.
4.  **Add Basic Specifications:** For each unit, write a brief, one-sentence `description` in the `specs` object explaining its purpose (e.g., "Reacts A and B to form C", "Separates light component D from heavy product E", "Cools the compressor outlet", "Preheat Feed prior feed to reactor").
5.  **Summarize:** Write a concise `overall_description` that explains the complete process flow from start to finish.
6.  **Assemble JSON:** Construct the final JSON object strictly following the schema. Do not include any text before or after the JSON.

# EXAMPLE:
---
**SELECTED CONCEPT:** "Production of Ethyl Acetate via Catalytic Esterification in a CSTR followed by distillation."
**REQUIREMENTS:** {{'components': [{{'name': 'Ethanol', 'role': 'Reactant'}}, {{'name': 'Acetic Acid', 'role': 'Reactant'}}, {{'name': 'Ethyl Acetate', 'role': 'Product'}}], 'purity': {{'component': 'Ethyl Acetate', 'value': 99.5}}}}
**LITERATURE:** "The reaction is equilibrium-limited. Water is a byproduct and must be removed to drive the reaction forward. Ethyl Acetate and Water form a minimum-boiling azeotrope."

**EXPECTED JSON OUTPUT:**
{{
    "flowsheet": {{
        "units": [
            {{
                "id": "TK-101",
                "name": "Reactant Feed Tank",
                "type": "Storage Tank",
                "specs": {{
                    "description": "Stores and mixes liquid Ethanol and Acetic Acid reactants."
                }}
            }},
            {{
                "id": "P-101",
                "name": "Feed Pump",
                "type": "Pump",
                "specs": {{
                    "description": "Transfers reactants from the feed tank to the reactor."
                }}
            }},
            {{
                "id": "R-101",
                "name": "Esterification Reactor",
                "type": "CSTR",
                "specs": {{
                    "description": "Continuously reacts Ethanol and Acetic Acid with a catalyst to produce Ethyl Acetate and Water."
                }}
            }},
            {{
                "id": "C-101",
                "name": "Purification Column",
                "type": "Distillation Column",
                "specs": {{
                    "description": "Separates the crude product stream, removing unreacted reactants and water byproduct to achieve 99.5% Ethyl Acetate purity."
                }}
            }},
            {{
                "id": "TK-102",
                "name": "Product Storage Tank",
                "type": "Storage Tank",
                "specs": {{
                    "description": "Stores the final high-purity Ethyl Acetate product."
                }}
            }}
        ],
        "connections": [
            {{
                "id": "101",
                "from": "TK-101",
                "to": "P-101",
                "description": "Reactant feed",
                "notes": "Ambient Conitions from Tank",
            }},
            {{
                "id": "102",
                "from": "P-101",
                "to": "R-101",
                "description": "Pressurized reactant feed",
                "notes": "Pressure increased via pump",
            }},
            {{
                "id": "103",
                "from": "R-101",
                "to": "C-101",
                "description": "Crude product mixture",
                "notes": "Composition changed in reactor",
            }},
            {{
                "id": "104",
                "from": "C-101",
                "to": "TK-102",
                "description": "Final Ethyl Acetate product",
                "notes": "The final product to storage, Ethyl Acetate purity 99.5%",
            }}
        ],
        "overall_description": "Ethanol and Acetic Acid are fed from a tank to a CSTR for reaction. The resulting crude mixture is sent to a distillation column to remove impurities and byproducts, yielding a high-purity Ethyl Acetate product which is sent to final storage."
    }}
}}
---
# NEGATIVES:

* NEVER miss the feed from outside, environment, or storage.
* Consider pressure and temperature profile in the system at each equipment carefully.
* Add equipment for pressure changes (e.g. pump, compressor, etc.) and temperature changes (e.g. heat exchanger, etc.) properly.

---

# PROBLEM TO SOLVE
---
**SELECTED CONCEPT:**
{selected_concept}

**REQUIREMENTS:**
{state.get('requirements', {})}

**LITERATURE:**
{state.get('literature_data', {})}

# FINAL JSON OUTPUT:
"""