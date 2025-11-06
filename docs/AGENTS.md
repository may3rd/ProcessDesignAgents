# Agent Responsibilities

`ProcessDesignGraph` wires a sequential LangGraph over the factories exported in `processdesignagents/agents/__init__.py`. Each agent consumes a subset of the shared `DesignState` and produces Markdown or JSON artefacts that drive the next stage. This page supplements `AGENTS.md` with module-level detail and notes on current behaviour.

## Execution Order & Artefacts

| Step | Agent | Module | Reads | Writes | Output Format |
| --- | --- | --- | --- | --- | --- |
| 1 | Process Requirements Analyst | `agents/analysts/process_requirements_analyst.py` | `problem_statement`<br>`messages` | `process_requirements`<br>`messages` | Markdown requirements brief |
| 2 | Innovative Researcher | `agents/researchers/innovative_researcher.py` | `process_requirements`<br>`messages` | `research_concepts`<br>`messages` | JSON `{ "concepts": [...] }` |
| 3 | Conservative Researcher | `agents/researchers/conservative_researcher.py` | `research_concepts`<br>`process_requirements`<br>`messages` | `research_rating_results`<br>`messages` | JSON with feasibility scores + risks |
| 4 | Concept Detailer | `agents/researchers/detail_concept_researcher.py` | `research_rating_results`<br>`process_requirements`<br>`messages` | `selected_concept_name`<br>`selected_concept_details`<br>`selected_concept_evaluation`<br>`messages` | Markdown concept brief + stored JSON |
| 5 | Component List Researcher | `agents/researchers/component_list_researcher.py` | `process_requirements`<br>`selected_concept_details`<br>`selected_concept_name`<br>`design_basis` (fallbacks to empty)<br>`messages` | `component_list`<br>`messages` | Markdown component table |
| 6 | Design Basis Analyst | `agents/analysts/design_basis_analyst.py` | `problem_statement`<br>`process_requirements`<br>`selected_concept_details`<br>`selected_concept_name`<br>`component_list`<br>`messages` | `design_basis`<br>`messages` | Markdown basis-of-design |
| 7 | Flowsheet Design Agent | `agents/designer/flowsheet_design_agent.py` | `process_requirements`<br>`design_basis`<br>`selected_concept_details`<br>`selected_concept_name`<br>`messages` | `flowsheet_description`<br>`messages` | Markdown flowsheet narrative |
| 8 | Equipment & Stream Catalog Agent | `agents/designer/equipment_stream_catalog_agent.py` | `flowsheet_description`<br>`design_basis`<br>`process_requirements`<br>`selected_concept_details`<br>`messages` | `equipment_list_template`<br>`stream_list_template`<br>`messages` | JSON templates with `equipments[]` and `streams[]` placeholders |
| 9 | Stream Property Estimation Agent | `agents/designer/stream_property_estimation_agent.py` | `flowsheet_description`<br>`design_basis`<br>`equipment_list_template`<br>`stream_list_template`<br>`messages` | `stream_list_results`<br>`messages` | JSON stream list with reconciled properties |
| 10 | Equipment Sizing Agent | `agents/designer/equipment_sizing_agent.py` | `design_basis`<br>`flowsheet_description`<br>`equipment_list_results`<br>`equipment_list_template`<br>`stream_list_results`<br>`messages` | `equipment_list_results`<br>`messages` | JSON equipment list with sizing parameters filled |
| 11 | Safety & Risk Analyst | `agents/analysts/safety_risk_analyst.py` | `process_requirements`<br>`design_basis`<br>`flowsheet_description`<br>`equipment_list_results`<br>`stream_list_results`<br>`messages` | `safety_risk_analyst_report`<br>`messages` | Markdown HAZOP-style report |
| 12 | Project Manager | `agents/project_manager/project_manager.py` | `process_requirements`<br>`design_basis`<br>`flowsheet_description`<br>`equipment_list_results`<br>`stream_list_results`<br>`safety_risk_analyst_report`<br>`messages` | `project_manager_report`<br>`project_approval`<br>`messages` | Markdown approval memo |

## Behaviour Notes

### Concept Selection
- By default, the concept detailer selects the option with the highest `feasibility_score`. Passing `manual_concept_selection=True` to `ProcessDesignGraph.propagate(...)` injects a callback that prompts the operator to choose instead.
- The chosen concept's evaluation JSON is stored under `selected_concept_evaluation` for reference even though the typed state does not yet expose that field explicitly.

### Combined Equipment & Stream View
- Equipment and stream artefacts now live in dedicated state fields. When an agent or report needs the merged view, helper `build_equipment_stream_payload` combines the two JSON structures on the fly before passing them to `equipments_and_streams_dict_to_markdown` for rendering.
- This separation keeps state lean while preserving compatibility with existing Markdown and prompt formats that expect a combined payload.

### Tool Access
- The only tool node currently registered is `"equipment_sizing"`, which exposes `size_heat_exchanger_basic` and `size_pump_basic`. Add new sizing helpers by importing them in `processdesignagents/graph/process_design_graph.py` and appending to the `ToolNode` list.
- Sizing helpers live under `processdesignagents/agents/utils/agent_sizing_tools.py` and `processdesignagents/sizing_tools/`.

### Reporting & Logging
- `ProcessDesignGraph.propagate` writes the final state snapshot to `eval_results/ProcessDesignAgents_logs/full_states_log.json`.
- Set `save_markdown` or `save_word_doc` when running `propagate` to export compiled reports. DOCX export assumes Pandoc is installed and uses the template located at `reports/template.docx`.
- The Rich CLI (`python -m cli.main`) streams `messages` alongside the report sections; stream and equipment panels now render the merged Markdown produced from the separate artefacts.
- Resume from the most recent unfinished run is enabled by default. Pass `resume_from_last_run=False` when calling `ProcessDesignGraph.propagate(...)` to force a clean run for the current brief.

When modifying prompts or hand-offs, update both this document and `AGENTS.md` so contributors have an accurate reference.
