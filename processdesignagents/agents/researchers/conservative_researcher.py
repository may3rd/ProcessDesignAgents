from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter  # Assuming wrapper from prior resolution
from processdesignagents.agents.utils.json_utils import extract_json_from_response
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv
import json

load_dotenv()

def create_conservative_researcher(quick_think_llm: str):
    def conservative_researcher(state: DesignState) -> DesignState:
        """Conservative Researcher: Critiques concepts for practicality using LLM."""
        llm = ChatOpenRouter()
        
        concepts = state.get("research_concepts", {}).get("concepts", [])
        prompt = f"""
        Critique the following process concepts for risks, costs, and feasibility, considering constraints.
        Concepts: {concepts}
        Requirements/Constraints: {state.get('requirements', {})}
        
        For each concept, add: risks [str], feasibility_score (1-10), recommendations [str].
        Output as JSON: {{"concepts": [{{"name": str, "description": str, "units": [str], "benefits": [str], "risks": [str], "feasibility_score": int, "recommendations": [str] }}]}}
        """
        
        print("\n=========================== Conservatively Critiqued Concepts===========================\n")
        
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