import asyncio
from processdesignagents.graph.process_design_graph import ProcessDesignGraph
from processdesignagents.default_config import DEFAULT_CONNFIG

config = DEFAULT_CONNFIG.copy()
config["llm_provider"] = "openrouter"
config["quick_think_llm"] = "google/gemini-2.5-flash"
config["deep_think_llm"] = "x-ai/grok-4-fast"

# config["quick_think_llm"] = "google/gemini-2.5-flash-preview-09-2025"
# config["deep_think_llm"] = "anthropic/claude-sonnet-4.5"
# config["deep_think_llm"] = "z-ai/glm-4.6"

async def main():
    graph = ProcessDesignGraph(debug=False, config=config)

    # problem_statement = "design generic compressed air unit for refinery with capacity 300 Nm3/h for plant air and instrument air."
    # problem_statement = "design carbon capture unit with capacity 100 ton per day of captured carbon product, the feed is flue gas with CO2 around 12.4 wt%."
    # problem_statement = "design MWCNT production, CVD of Methane in Fludized Bed Reactor, feed stock is LNG with 93% mole Methane (do need feed vaporization), the by-product H2 generated will be collected to be blue hydrogen (use PSA for H2 collection). Target capacity is 200 Ton per year of CNT production."
    # problem_statement = f"design the energy recovery from flue gas of LNG burner, 10,000 SCFD, 300°C, 0.1 barg and use it to produce electricity with 30% efficiency."
    problem_statement = "design the carbon capture modular package, the feed to the package can be flue gas from various burner type. The target CO2 purity is 99.5%"

    _ = await graph.propagate(
        problem_statement=problem_statement, 
        save_markdown="reports/latest_run.md",
        manual_concept_selection=False
        )

if __name__ == "__main__":
    asyncio.run(main())
