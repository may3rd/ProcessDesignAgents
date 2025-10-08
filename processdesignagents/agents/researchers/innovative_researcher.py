from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter  # Assuming wrapper from prior resolution
from processdesignagents.agents.utils.json_utils import extract_json_from_response
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import json

load_dotenv()

def create_innovative_researcher(quick_think_llm: str):
    def innovative_researcher(state: DesignState) -> DesignState:
        """Innovative Researcher: Proposes novel process concepts using LLM."""
        llm = ChatOpenRouter()
        
        prompt = f"""
        Based on the following requirements and literature data, propose 3 innovative chemical process concepts.
        Requirements: {state.get('requirements', {})}
        Literature Data: {state.get('literature_data', {})}
        
        For each concept, include: description, key units (e.g., reactor type), potential benefits.
        Output as JSON: {{"concepts": [{{"name": str, "description": str, "units": [str], "benefits": [str]}}]}}
        """
        
        response = llm.invoke(prompt, model=quick_think_llm)
        try:
            clean_json = extract_json_from_response(response.content)
            research_concepts = json.loads(clean_json)
        except json.JSONDecodeError:
            raise ValueError("Failed to extract research concepts from response")
            research_concepts = {"concepts": [{"name": "Plasma Cracking", "description": "High-temperature plasma reactor for ethane", "units": ["Plasma Reactor"], "benefits": ["Higher yield"]}]}
        
        print("\n=========================== Innovative Research Concepts ===========================\n")
        
        state["research_concepts"] = research_concepts
        print("Generated innovative research concepts.")
        
        # print name of concepts
        print("\n--- Concept Names ---")
        for concept in research_concepts.get("concepts", []):
            print(f"- {concept.get('name', 'Unknown')}")
            
        return state
    return innovative_researcher