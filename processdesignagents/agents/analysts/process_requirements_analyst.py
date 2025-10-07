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
    prompt = system_prompt(state['problem_statement'])
    response = llm.invoke(prompt)
    
    try:
        clean_json = extract_json_from_response(response.content)
        requirements = json.loads(clean_json)
    except (json.JSONDecodeError, ValueError):
        requirements = {"throughput": 1000, "purity": 99, "yield_target": 95, "constraints": ["Environmental compliance"]}

    state["requirements"] = requirements
    print(f"Extracted requirements: {requirements}")
    return state

def system_prompt(problem_statement: str) -> str:
    return f"""
# ROLE:
You are an expert Senior Process Engineer with 20 years of experience in conceptual process design and requirement analysis. Your task is to meticulously analyze a chemical process design problem and extract key parameters.

# TASK:
Your goal is to act as a Process Requirement Analyst. You must read the provided problem statement, identify all critical process parameters, and structure them into a clean, machine-readable JSON object.

# INSTRUCTIONS:
1.  **Analyze Carefully:** Read the entire 'PROBLEM STATEMENT' below. Identify all specified and implied process requirements.
2.  **Think Step-by-Step:** First, identify the main chemical reaction or separation process. Second, list all chemical components and their roles (e.g., reactant, product, solvent). Third, extract quantitative data like throughput, purity, and yield targets. Fourth, identify all operational constraints.
3.  **Handle Missing Information:**
    * If a parameter (e.g., 'yield_target') is not mentioned at all, its value in the JSON MUST be `null`.
    * If a reasonable default can be inferred from standard chemical engineering principles (e.g., assuming atmospheric pressure if not specified), you may use it. However, you MUST add a note about this assumption in the 'constraints' list.
4.  **Format Output:** Your final output MUST be a single, valid JSON object. Do not include any text or explanations before or after the JSON block.

# NEGATIVES:
    * **throughput** MUST have value. Default units is kg/h, if not stated in the problem statement.
    * **yield_target.value** CANNOT be None. Put 100.0 as default.

# JSON SCHEMA:
Your JSON output must conform to this exact structure and data types:
{{
  "throughput": {{
    "value": float,
    "units": "kg/h"
  }},
  "components": [
    {{
      "name": "string",
      "role": "string (e.g., Reactant, Product, Catalyst, Solvent, Inert)"
    }}
  ],
  "purity": {{
    "component": "string (name of the target component)",
    "value": "float (e.g., 99.5 for 99.5%)"
  }},
  "yield_target": {{
    "value": "float (e.g., 95.0 for 95%)",
    "basis": "string (e.g., Based on limiting reactant 'Methanol')"
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
  "throughput": {{
    "value": 1500.0,
    "units": "kg/h"
  }},
  "components": [
    {{
      "name": "Ethanol",
      "role": "Reactant"
    }},
    {{
      "name": "Acetic Acid",
      "role": "Reactant"
    }},
    {{
      "name": "Ethyl Acetate",
      "role": "Product"
    }},
    {{
      "name": "Water",
      "role": "Product"
    }},
    {{
      "name": "Sulfuric Acid",
      "role": "Catalyst"
    }}
  ],
  "purity": {{
    "component": "Ethyl Acetate",
    "value": 99.8
  }},
  "yield_target": {{
    "value": 92.0,
    "basis": "Based on limiting reactant 'Acetic Acid'"
  }},
  "constraints": [
    "Reactor operating temperature must be below 100°C."
  ]
}}
---

# PROBLEM STATEMENT TO ANALYZE:
{problem_statement}

# FINAL JSON OUTPUT:
"""