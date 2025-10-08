from processdesignagents.graph.process_design_graph import ProcessDesignGraph
from processdesignagents.default_config import DEFAULT_CONNFIG

config = DEFAULT_CONNFIG.copy()

graph = ProcessDesignGraph(debug=True, config=config)

print("\n=========================== Problem ===========================\n")
result = graph.proagate("design compressed air unit with capacity 300 Nm3/h for plant air and instrument air.")
print("\n=========================== Results ===========================\n")
# print(result)
print("Multi-agent workflow completed.")