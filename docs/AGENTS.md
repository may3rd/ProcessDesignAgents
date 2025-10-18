# Agent Responsibilities

Below is a concise reference for each agent, its inputs, outputs, and key prompts. Review the source files for full details.

| Agent | Module | Reads | Writes | Purpose |
|-------|--------|-------|--------|---------|
| Process Requirements Analyst | `agents/analysts/process_requirements_analyst.py` | `problem_statement`, `messages` | `requirements` | Extracts objectives, constraints, components, and assumptions from the raw brief. |
| Innovative Researcher | `agents/researchers/innovative_researcher.py` | `requirements` | `research_concepts` | Proposes multiple process concepts. |
| Conservative Researcher | `agents/researchers/conservative_researcher.py` | `research_concepts`, `requirements` | Refined `research_concepts` (overwrites prior concepts) | Stress-tests concepts and adds feasibility commentary. |
| Concept Detailer | `agents/researchers/concept_detailer.py` | `research_concepts`, `requirements` | `selected_concept_details`, `selected_concept_name` | Selects the best concept and elaborates it for downstream agents (can prompt for manual choice). |
| Design Basis Analyst | `agents/analysts/design_basis_analyst.py` | `problem_statement`, `requirements`, concept detail | `design_basis` | Produces the formal design basis document. |
| Basic PFD Designer | `agents/designer/basic_pfd_designer.py` | `selected_concept_details`, `design_basis`, `requirements` | `basic_pfd` | Generates the conceptual flowsheet narrative. |
| Equipments & Streams List Builder | `agents/designer/equipments_and_streams_list_builder.py` | `basic_pfd`, `design_basis`, `requirements`, `selected_concept_details` | `stream_list_template` | Builds the canonical stream inventory JSON scaffold for downstream estimation. |
| Stream Data Estimator | `agents/designer/stream_data_estimator.py` | `stream_list_template`, `basic_pfd`, `design_basis`, `requirements`, `selected_concept_details` | `stream_list_results` | Estimates temperatures, pressures, flows, and compositions. |
| Equipment List Builder | `agents/designer/equipment_list_builder.py` | `stream_list_results`, `basic_pfd`, `design_basis`, `requirements` | `equipment_list_template` | Lists major equipment as JSON objects ready for sizing. |
| Equipment Sizing Agent | `agents/designer/equipment_sizing_agent.py` | `equipment_list_template`, `stream_list_template`, `stream_list_results`, `requirements`, `design_basis` | `equipment_list_results` | Uses built-in sizing tools to populate duty/size fields and notes. |
| Safety & Risk Analyst | `agents/analysts/safety_risk_analyst.py` | `basic_pfd`, `stream_list_results`, `equipment_list_results`, `requirements` | `safety_risk_analyst_report` | Performs a HAZOP-style hazard assessment (JSON dossier). |
| Project Manager | `agents/project_manager/project_manager.py` | `requirements`, `basic_pfd`, `stream_list_results`, `equipment_list_results`, `safety_risk_analyst_report` | `approval`, `project_manager_report` | Issues the final gate decision and implementation plan. |

## Tool Catalogue

The equipment sizing stage uses Python tools defined in `agents/tools/equipment_tools.py`:

- `heat_exchanger_sizing`
- `vessel_volume_estimate` (returns volume, diameter, length, orientation)
- `distillation_column_diameter`
- `reactor_volume_space_time`
- `pump_power_estimate`
- `compressor_power_estimate`

Each tool returns a dictionary that the LLM references while filling in the equipment table.

## Prompt Conventions

- Intermediate artefacts are shared as Markdown summaries or structured JSON depending on the agent (see table above).
- When JSON values are unknown, emit `null` so downstream agents can detect open items explicitly.
- Agents downstream from the simulator treat stream and equipment payloads as canonical sources, so keep identifiers consistent.

For reference runs, inspect the sample reports in `examples/reports/`.

Referencing source prompts when modifying behaviour is strongly recommended to maintain compatibility across the pipeline.
