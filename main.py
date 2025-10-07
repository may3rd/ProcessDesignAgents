import argparse
from processdesignagents.graph.design_graph import build_graph
from processdesignagents.default_config import load_config
from processdesignagents.utils.report_saver import save_final_report
from processdesignagents.utils.design_outputs import generate_hmb, generate_pfd, generate_equipment_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ProcessDesignAgents workflow with a problem statement.")
    parser.add_argument("problem", type=str, help="The chemical process design problem statement.")
    args = parser.parse_args()
    
    config = load_config()
    graph = build_graph()
    input_state = {"problem_statement": args.problem}
    result = graph.invoke(input_state)
    print(result)
    
    # Generate and save design outputs
    hmb = generate_hmb(result['flowsheet'], result['validation_results'])
    pfd = generate_pfd(result['flowsheet'], result['validation_results'])
    equipment = generate_equipment_list(result['flowsheet'])
    
    hmb.to_csv('reports/hmb.csv', index=False)
    pfd.render('reports/pfd', format='png', view=False)
    equipment.to_csv('reports/equipment_list.csv', index=False)
    
    print("H&MB Table:\n", hmb.to_markdown())
    print("\nEquipment List:\n", equipment.to_markdown())
    
    # Save final report with session ID based on problem
    session_id = args.problem[:20].replace(" ", "_").lower()  # Truncated for filename
    save_final_report(result, session_id=session_id)