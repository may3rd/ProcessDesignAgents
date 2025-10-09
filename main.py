from processdesignagents.graph.process_design_graph import ProcessDesignGraph
from processdesignagents.default_config import DEFAULT_CONNFIG

config = DEFAULT_CONNFIG.copy()
config["deep_think_llm"] = "x-ai/grok-4-fast"
config["quick_think_llm"] = "google/gemini-2.5-flash"

graph = ProcessDesignGraph(debug=False, config=config)

problem_statement = "design generic compressed air unit for refinery with capacity 300 Nm3/h for plant air and instrument air."
# problem_statement = "design carbon capture unit with capacity 100 ton per day of captured carbon product, the feed is flue gas with CO2 around 12.4 wt%."
# problem_statement = "design MWCNT production, CVD of Methane in Fludized Bed Reactor, feed stock is LNG with 93% mole Methane, the H2 generated will be collected to be blue hydrogen. Target capacity is 37 kg/h of CNT production."
result = graph.proagate(problem_statement=problem_statement)
# print(result)