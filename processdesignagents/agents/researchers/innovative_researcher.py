from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter  # Assuming wrapper from prior resolution
from processdesignagents.agents.utils.json_utils import extract_json_from_response
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import json

load_dotenv()

def create_innovative_researcher(quick_think_llm: str):
    def innovative_researcher(state: DesignState) -> DesignState:
        """Innovative Researcher: Proposes novel process concepts using LLM."""
        print("\n=========================== Innovative Research Concepts ===========================\n")
        llm = ChatOpenRouter()
        prompt = system_prompt(state.get('requirements', {}), state.get('literature_data', {}))
        response = llm.invoke(prompt, model=quick_think_llm)
        
        try:
            clean_json = extract_json_from_response(response.content)
            research_concepts = json.loads(clean_json)
        except json.JSONDecodeError:
            raise ValueError("Failed to extract research concepts from response")
            research_concepts = {"concepts": [{"name": "Plasma Cracking", "description": "High-temperature plasma reactor for ethane", "units": ["Plasma Reactor"], "benefits": ["Higher yield"]}]}
        
        state["research_concepts"] = research_concepts
        print("Generated innovative research concepts.")
        
        # print name of concepts
        print("\n--- Concept Names ---")
        for concept in research_concepts.get("concepts", []):
            print(f"- {concept.get('name', 'Unknown')}")
            
        return state
    return innovative_researcher

def system_prompt(requirements: str, literature: str) -> str:
    return f"""
# ROLE
You are a Senior R&D Process Engineer specializing in conceptual design and process innovation. Your expertise lies in brainstorming novel, sustainable, and efficient chemical processes.

# TASK
Based on the provided 'REQUIREMENTS' and 'LITERATURE DATA', generate exactly 3 distinct and innovative chemical process concepts. Your goal is to propose traditional methods and creative solutions. For each concept, provide a concise name, a clear description, the key unit operations involved, and its primary benefits.

# INSTRUCTIONS
1.  **Synthesize Data:** First, thoroughly analyze the 'REQUIREMENTS' and 'LITERATURE DATA' to understand the core objective, key components, and known science.
2.  **Brainstorm Process Ideas:** Think across process idea vectors such as:
    * **Standard Practice:** The typical process unit that widely used in the industry.
    * **Alternative creative solutions:** The new methods that improve from traditional methods.
3.  **Develop Concepts:** For each of your three ideas, structure it with a descriptive name, a paragraph explaining the concept, a list of the essential unit operations, and a list of its key advantages.
4.  **Format Output:** Your final output must be a single, valid JSON object that strictly adheres to the schema below.

# JSON SCHEMA
{{
    "concepts": [
        {{
            "name": "string",
            "description": "string",
            "units": ["list of strings"],
            "benefits": ["list of strings"]
        }}
    ]
}}

# EXAMPLE
---
**REQUIREMENTS:** {{"components": ["Styrene"], "throughput": {{"value": 100000, "units": "t/a"}}}}
**LITERATURE DATA:** {{"info": "Conventional styrene production is via ethylbenzene dehydrogenation, which is energy-intensive and equilibrium-limited."}}

**EXPECTED JSON OUTPUT:**
{{
    "concepts": [
        {{
            "name": "Oxidative Coupling of Toluene",
            "description": "A novel pathway that uses toluene, a cheaper feedstock, and couples it with methane or methanol in an oxidative reaction to directly synthesize styrene. This avoids the energy-intensive ethylbenzene intermediate.",
            "units": ["Fluidized Bed Reactor", "Catalyst Regeneration System", "Product Separation Train"],
            "benefits": ["Utilizes lower-cost feedstock", "Potentially lower energy consumption", "Avoids equilibrium limitations of dehydrogenation"]
        }},
        {{
            "name": "Biocatalytic Synthesis from Cinnamic Acid",
            "description": "A green chemistry approach using a genetically engineered microorganism or enzyme to convert cinnamic acid to styrene under mild conditions (room temperature and atmospheric pressure). Cinnamic acid can be sourced from biomass.",
            "units": ["Bioreactor (Fermenter)", "Centrifuge/Filtration Unit", "Extraction Column"],
            "benefits": ["Uses renewable feedstocks", "Significantly lower energy footprint", "High selectivity and minimal byproducts", "Operates at mild conditions"]
        }},
        {{
            "name": "Microwave-Assisted Dehydrogenation",
            "description": "This concept enhances the traditional ethylbenzene dehydrogenation process by using microwave heating. Microwaves can selectively heat the catalyst bed, leading to faster reaction rates and potentially shifting the equilibrium favorably.",
            "units": ["Microwave Reactor", "Heat Recovery Exchanger", "Styrene Purification Unit"],
            "benefits": ["Improved energy efficiency through targeted heating", "Higher conversion and selectivity", "Faster start-up and shutdown times"]
        }}
    ]
}}
---

# DATA FOR ANALYSIS
---
**REQUIREMENTS:**
{requirements}

**LITERATURE DATA:**
{literature}

# FINAL JSON OUTPUT:
"""