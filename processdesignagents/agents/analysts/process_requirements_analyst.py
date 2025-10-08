from typing import Dict, Any
from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter
from processdesignagents.agents.utils.json_utils import extract_json_from_response
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import json

load_dotenv()

def create_process_requiruments_analyst(quick_think_llm: str):
  def process_requirements_analyst(state: DesignState) -> DesignState:
      """Process Requirements Analyst: Extracts key design requirements using LLM."""
      llm = ChatOpenRouter()
      prompt = system_prompt(state['problem_statement'])
      response = llm.invoke(prompt, model=quick_think_llm, temperature=0.7)
      
      try:
          clean_json = extract_json_from_response(response.content)
          requirements = json.loads(clean_json)
      except (json.JSONDecodeError, ValueError):
          raise ValueError("Failed to extract requirements from response")
          requirements = {"throughput": 1000, "purity": 99, "yield_target": 95, "constraints": ["Environmental compliance"]}

      state["requirements"] = requirements
      print(f"Extracted requirements: {requirements}")
      
      return state
  return process_requirements_analyst

def system_prompt(problem_statement: str) -> str:
    return f"""
# ROLE:
You are an expert Senior Process Engineer with 20 years of experience in conceptual process design and requirement analysis. Your task is to meticulously analyze a chemical process design problem and extract key parameters.

# TASK:
Your goal is to act as a Process Requirement Analyst. You must read the provided problem statement, identify all critical process parameters, and structure them into a clean, machine-readable JSON object.

# INSTRUCTIONS:
1.  **Analyze Carefully:** Read the entire 'PROBLEM STATEMENT' below. Identify all specified and implied process requirements.
2.  **Think Step-by-Step:** 
    1. Identify the main process objective.
    2. List all chemical components involve in the process.
    3. Extract quantitative data like throughput, purity.
    4. Identify all operational constraints.
3.  **Handle Missing Information:**
    * If a parameter (e.g., 'yield_target') is not mentioned at all, its value in the JSON MUST be `null`.
    * If a reasonable default can be inferred from standard chemical engineering principles (e.g., assuming atmospheric pressure if not specified), you may use it. However, you MUST add a note about this assumption in the 'constraints' list.
4.  **Format Output:** Your final output MUST be a single, valid JSON object. Do not include any text or explanations before or after the JSON block.

# NEGATIVES:
    * **capacity** MUST have value. Default units is kg/h, if not stated in the problem statement.
    * **yield_target.value** CANNOT be None. Give value = 80.0 and basis = `default` as default.

# JSON SCHEMA:
Your JSON output must conform to this exact structure and data types:
{{
  "objective": "string",
  "capacity": {{
    "value": float,
    "units": "kg/h",
    "basis": "string"
  }},
  "components": [
    {{
      "name": "string"
    }}
  ],
  "purity": {{
    "component": "string (name of the target component)",
    "value": "float (e.g., 99.5 for 99.5%)"
  }},
  "constraints": [
    "string"
  ]
}}

# EXAMPLE:
---
**PROBLEM STATEMENT:** "We need to design a plant to produce 1500 kg/h of high-purity Ethyl Acetate from the esterification of Ethanol and Acetic Acid using Sulfuric Acid as a catalyst. The target purity for the Ethyl Acetate product is 99.8%. The reaction should achieve at least a 92% yield based on the limiting reactant, which is Acetic Acid. The reactor must operate below 100°C."

**EXPECTED JSON OUTPUT:**
{{
  "objective": "Production of Ethyl Acetate from Ethanol from the esterification of Ethanol and Acetic Acid using Sulfuric Acid as a catalyst",
  "capacity": {{
    "value": 1500.0,
    "units": "kg/h",
    "basis": "Based on total Ethyl Acetate product go to storage tank"
  }},
  "components": [
    {{
      "name": "Ethanol"
    }},
    {{
      "name": "Acetic Acid"
    }},
    {{
      "name": "Ethyl Acetate"
    }},
    {{
      "name": "Water"
    }},
    {{
      "name": "Sulfuric Acid"
    }}
  ],
  "purity": {{
    "component": "Ethyl Acetate",
    "value": 99.8
  }},
  "constraints": [
    "Reactor operating temperature must be below 100°C."
  ]
}}
---
# NEGATIVES:

* ENSURE the the capacity UOM conversion is done correctly.

# PROBLEM STATEMENT TO ANALYZE:
{problem_statement}

# FINAL JSON OUTPUT:
"""