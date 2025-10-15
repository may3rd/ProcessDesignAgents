import argparse
from processdesignagents.graph.process_design_graph import build_graph
from processdesignagents.default_config import load_config, DEFAULT_CONNFIG
from processdesignagents.utils.report_saver import save_final_report
from processdesignagents.utils.design_outputs import generate_hmb, generate_pfd, generate_equipment_list

DEFAULT_PROBLEM = """
design compressed air unit with capacity 300 Nm3/h for plant air and instrument air.
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ProcessDesignAgents workflow with a problem statement.")
    parser.add_argument(
        "-p", "--problem", dest="problem",
        metavar="PROBLEM_STATEMENT",
        type=str,
        help="The chemical process design problem statement.", 
        default=DEFAULT_PROBLEM
        )
    args = parser.parse_args()
    
    config = DEFAULT_CONNFIG.copy()
    graph = build_graph(config)
    input_state = {"problem_statement": args.problem}
    result = graph.invoke(input_state)
    print(result)
    
    # Generate and save design outputs
    basic_pfd = result.get('basic_pfd', '')
    basic_hmb = result.get('basic_hmb_results', '')
    hmb = generate_hmb(basic_pfd, basic_hmb)
    pfd = generate_pfd(basic_pfd, basic_hmb)
    equipment = generate_equipment_list(basic_pfd)
    
    hmb.to_csv('reports/hmb.csv', index=False)
    pfd.render('reports/pfd', format='png', view=False)
    equipment.to_csv('reports/equipment_list.csv', index=False)
    
    print("H&MB Table:\n", hmb.to_markdown())
    print("\nEquipment List:\n", equipment.to_markdown())
    
    # Save final report with session ID based on problem
    session_id = args.problem[:20].replace(" ", "_").lower()  # Truncated for filename
    save_final_report(result, session_id=session_id)
