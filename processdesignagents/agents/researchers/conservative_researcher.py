from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter  # Assuming wrapper from prior resolution
from processdesignagents.agents.utils.json_utils import extract_json_from_response
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import json

load_dotenv()

def create_conservative_researcher(quick_think_llm: str):
    def conservative_researcher(state: DesignState) -> DesignState:
        """Conservative Researcher: Critiques concepts for practicality using LLM."""
        print("\n=========================== Conservatively Critiqued Concepts===========================\n")
        llm = ChatOpenRouter()
        concepts = state.get("research_concepts", {}).get("concepts", [])
        prompt = system_prompt(concepts, state.get('requirements', {}))
        response = llm.invoke(prompt, model=quick_think_llm)
        
        try:
            clean_json = extract_json_from_response(response.content)
            updated_concepts = json.loads(clean_json)
            state["research_concepts"] = updated_concepts
        except json.JSONDecodeError:
            # Fallback: Add simple critiques
            for concept in concepts:
                concept["risks"] = ["High energy use"]
                concept["feasibility_score"] = 7
                concept["recommendations"] = ["Pilot testing required"]
        
        print("Applied conservative critiques to research concepts.")
        for concept in updated_concepts.get("concepts", []):
            print(f"---\nConcept: {concept.get('name', 'Unknown')}")
            print(f"Risks: {', '.join(concept.get('risks', []))}")
            print(f"Feasibility Score: {concept.get('feasibility_score', 'N/A')}")
        return state
    return conservative_researcher

def system_prompt(concepts: str, requirements: str) -> str:
    return f"""
# ROLE
You are a Principal Technology Analyst at a chemical venture capital firm. Your job is to conduct rigorous due diligence on innovative process technologies to assess their investment potential. You are an expert in evaluating technical feasibility, market viability, and operational risk.

# TASK
Critically evaluate each of the provided process 'CONCEPTS'. For each one, you must augment the existing information with a detailed analysis of its risks, a calculated feasibility score, and clear, actionable recommendations. Your analysis must consider the given 'REQUIREMENTS/CONSTRAINTS'. The output must be a single JSON object containing the updated list of concepts.

# METHODOLOGY
1.  **Review Concept:** For each concept, analyze its description, units, and benefits in the context of the project requirements.
2.  **Risk Analysis:** Identify 2-3 significant risks for each concept, categorizing them as:
    * **Technical Risks:** (e.g., unproven technology, catalyst stability, complex separations).
    * **Economic Risks:** (e.g., high capital expenditure (CAPEX), feedstock price volatility, market acceptance).
    * **Safety/EHS Risks:** (e.g., hazardous materials, extreme operating conditions, difficult-to-handle byproducts).
3.  **Feasibility Scoring (1-10):** The score should be a weighted average of the following criteria. **Briefly justify your scoring in the recommendations.**
    * **Technical Readiness (40%):** How mature is the technology? (1=Purely theoretical, 10=Commercially proven).
    * **Economic Viability (40%):** How strong is the business case? (1=Very weak, 10=Very strong).
    * **Safety & Simplicity (20%):** How manageable are the risks and complexity? (1=Extremely complex/hazardous, 10=Simple/Inherently safe).
4.  **Recommendations:** Provide a clear, forward-looking recommendation for each concept. Examples: "Recommend for preliminary techno-economic analysis," "Suggest lab-scale pilot to de-risk key technology," or "Not recommended due to low TRL and high CAPEX."

# JSON SCHEMA
Your output MUST be a JSON object containing the original list of concepts, with each concept object updated to include the 'risks', 'feasibility_score', and 'recommendations' fields. **Do not alter the existing data for each concept.**
{{
    "concepts": [
        {{
            "name": "string",
            "description": "string",
            "units": ["string"],
            "benefits": ["string"],
            "risks": ["string"],
            "feasibility_score": "int",
            "recommendations": ["string"]
        }}
    ]
}}

# EXAMPLE
---
**CONCEPTS:** [{{
    "name": "Biocatalytic Synthesis from Cinnamic Acid",
    "description": "A green chemistry approach using an enzyme to convert cinnamic acid to styrene under mild conditions. Cinnamic acid can be sourced from biomass.",
    "units": ["Bioreactor (Fermenter)", "Centrifuge/Filtration Unit", "Extraction Column"],
    "benefits": ["Uses renewable feedstocks", "Significantly lower energy footprint", "High selectivity", "Operates at mild conditions"]
}}]
**REQUIREMENTS/CONSTRAINTS:** {{"components": ["Styrene"], "throughput": {{"value": 100000, "units": "t/a"}}}}

**EXPECTED JSON OUTPUT:**
{{
    "concepts": [
        {{
            "name": "Biocatalytic Synthesis from Cinnamic Acid",
            "description": "A green chemistry approach using an enzyme to convert cinnamic acid to styrene under mild conditions. Cinnamic acid can be sourced from biomass.",
            "units": ["Bioreactor (Fermenter)", "Centrifuge/Filtration Unit", "Extraction Column"],
            "benefits": ["Uses renewable feedstocks", "Significantly lower energy footprint", "High selectivity", "Operates at mild conditions"],
            "risks": [
                "Technical Risk: Low Technology Readiness Level (TRL); enzyme stability and productivity at industrial scale are unproven.",
                "Economic Risk: High cost and limited availability of cinnamic acid feedstock compared to traditional petrochemicals.",
                "Technical Risk: Product separation from a dilute aqueous solution can be energy-intensive and costly."
            ],
            "feasibility_score": 4,
            "recommendations": [
                "Feasibility Score Justification: The concept scores low on TRL (2/10) and Economic Viability (3/10) due to feedstock cost and scale-up uncertainty, despite a high Safety score (9/10).",
                "Recommendation: Not recommended for immediate large-scale consideration. Suggest a small-scale R&D project to investigate enzyme engineering for improved productivity and stability before any further investment."
            ]
        }}
    ]
}}
---

# DATA FOR ANALYSIS
---
**CONCEPTS:**
{concepts}

**REQUIREMENTS/CONSTRAINTS:**
{requirements}

# FINAL JSON OUTPUT:
"""