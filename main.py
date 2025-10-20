import asyncio
from processdesignagents.graph.process_design_graph import ProcessDesignGraph
from processdesignagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openrouter"
config["quick_think_llm"] = "google/gemini-2.5-flash-preview-09-2025"
config["deep_think_llm"] = "x-ai/grok-4-fast"

# config["deep_think_llm"] = "openai/gpt-oss-120b"

config["quick_think_llm"] = "google/gemini-2.5-flash-lite-preview-09-2025"
config["deep_think_llm"] = "google/gemini-2.5-flash-lite-preview-09-2025"
# config["deep_think_llm"] = "anthropic/claude-sonnet-4.5"
# config["deep_think_llm"] = "z-ai/glm-4.6"

# config["llm_provider"] = "google"
# config["quick_think_llm"] = "gemini-2.5-flash"
# config["deep_think_llm"] = "gemeni-2.5-flash"

# config["llm_provider"] = "ollama"
# config["quick_think_llm"] = "llama3.2"
# config["deep_think_llm"] = "llama3.2"

config["quick_think_temperature"] = 0.5
config["deep_think_temperature"] = 0.5

def main():
    graph = ProcessDesignGraph(debug=False, config=config)

    # problem_statement = "design generic compressed air unit for refinery with capacity 300 Nm3/h for plant air and instrument air."
    # problem_statement = "design carbon capture unit with capacity 100 ton per day of captured carbon product, the feed is flue gas with CO2 around 12.4 wt%."
    # problem_statement = "design MWCNT production, CVD of Methane in Fludized Bed Reactor, feed stock is LNG with 93% mole Methane (do need feed vaporization), the by-product H2 generated will be collected to be blue hydrogen (use PSA for H2 collection). Target capacity is 200 Ton per year of CNT production."
    # problem_statement = f"design the energy recovery from flue gas of LNG burner, 10,000 SCFD, 300°C, 0.1 barg and use it to produce electricity with 30% efficiency."
    problem_statement = "design the carbon capture modular package, the feed to the package can be flue gas from various burner type. The target CO2 purity is 99.5%"
    # problem_statement = "design heat exchanger to cool the ethanol product (99.5% purity molar basis) from 100 C to 40 C. Design flowrate of ethanol feed is 2500 kg/hr."
    
    _ = graph.propagate(
        problem_statement=problem_statement, 
        save_markdown="reports/latest_run.md",
        save_word_doc="reports/latest_run.docx",
        manual_concept_selection=False
        )

if __name__ == "__main__":
    main()
