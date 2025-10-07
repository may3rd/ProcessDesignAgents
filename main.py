from processdesignagents.graph.design_graph import build_graph
from processdesignagents.default_config import load_config
from processdesignagents.utils.report_saver import save_final_report
from processdesignagents.utils.design_outputs import generate_hmb, generate_pfd, generate_equipment_list

if __name__ == "__main__":
    config = load_config()
    graph = build_graph()
    input_state = {"problem_statement": "Sample process design"}
    result = graph.invoke(input_state)
    print(result)
    
    # Add final report saving
    save_final_report(result, session_id="sample_session_001")  # Optional ID for naming
    
    # ... after result = graph.invoke(input_state) ...
    hmb = generate_hmb(result['flowsheet'], result['validation_results'])
    pfd = generate_pfd(result['flowsheet'], result['validation_results'])  # Updated call
    equipment = generate_equipment_list(result['flowsheet'])

    # Save or print outputs
    hmb.to_csv('reports/hmb.csv', index=False)
    pfd.render('reports/pfd_sample', format='png', view=False)  # Generates PNG
    equipment.to_csv('reports/equipment_list.csv', index=False)

    print("H&MB Table:\n", hmb.to_markdown())
    print("\nPFD DOT Source (render with Graphviz):\n", pfd.source)
    print("\nEquipment List:\n", equipment.to_markdown())