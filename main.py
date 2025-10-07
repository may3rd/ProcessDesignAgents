from processdesignagents.graph.design_graph import build_graph
from processdesignagents.default_config import load_config
from processdesignagents.utils.report_saver import save_final_report

if __name__ == "__main__":
    config = load_config()
    graph = build_graph()
    input_state = {"problem_statement": "Sample process design"}
    result = graph.invoke(input_state)
    print(result)
    
    # Add final report saving
    save_final_report(result, session_id="sample_session_001")  # Optional ID for naming