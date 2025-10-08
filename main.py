from processdesignagents.graph.process_design_graph import ProcessDesignGraph
from processdesignagents.default_config import DEFAULT_CONNFIG

config = DEFAULT_CONNFIG.copy()

graph = ProcessDesignGraph(debug=True, config=config)

problem_statement = "design compressed air unit with capacity 300 Nm3/h for plant air and instrument air."
# problem_statement = "design carbon capture unit with capacity 100 T/day of captured carbon, the feed is flue gas with CO2 around 12.4 wt%."

print("\n=========================== Problem ===========================\n")
result = graph.proagate(problem_statement=problem_statement)
print("\n=========================== Results ===========================\n")
# print(result)
print("Multi-agent workflow completed.")