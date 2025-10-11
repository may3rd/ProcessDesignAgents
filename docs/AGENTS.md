# Agent Responsibilities

Below is a concise reference for each agent, its inputs, outputs, and key prompts. Review the source files for full details.

| Agent | Module | Reads | Writes | Purpose |
|-------|--------|-------|--------|---------|
| Process Requirements Analyst | `agents/analysts/process_requirements_analyst.py` | `problem_statement`, `messages` | `requirements`, `process_requirements_report` | Extracts objectives, constraints, components, and assumptions from the raw brief. |
| Innovative Researcher | `agents/researchers/innovative_researcher.py` | `requirements`, `literature_data` (optional) | `research_concepts`, `innovative_research_report` | Proposes multiple process concepts. |
| Conservative Researcher | `agents/researchers/conservative_researcher.py` | `research_concepts`, `requirements` | Refined `research_concepts`, `conservative_research_report` | Stress-tests concepts and adds feasibility commentary. |
| Concept Detailer | `agents/researchers/concept_detailer.py` | `research_concepts`, `requirements` | `selected_concept_details`, `selected_concept_name`, `concept_detail_report` | Selects the best concept and elaborates it for downstream agents. |
| Design Basis Analyst | `agents/analysts/design_basis_analyst.py` | `problem_statement`, `requirements`, concept detail | `design_basis`, `design_basis_report` | Produces the formal design basis document. |
| Basic PDF Designer | `agents/designer/basic_pdf_designer.py` | `selected_concept_details`, `design_basis`, `requirements` | `basic_pdf`, `basic_pdf_report` | Generates the conceptual flowsheet narrative. |
| Stream Data Builder | `agents/validation/stream_data_builder.py` | `basic_pdf`, `design_basis`, `requirements`, concept detail | `basic_stream_data`, `basic_stream_report` | Builds the stream summary template as a markdown table. |
| Process Simulator | `agents/validation/process_simulator.py` | Stream template, `basic_pdf`, `design_basis`, `requirements`, concept detail | Updated stream/H&MB tables (`basic_stream_data`, `basic_hmb_results`) | Estimates temperatures, pressures, flows, and compositions. |
| Equipment List Builder | `agents/validation/equipment_list_builder.py` | Stream table, `basic_pdf`, `design_basis`, `requirements` | `basic_equipment_template`, `basic_equipment_report` | Lists major equipment and placeholders for sizing data. |
| Equipment Sizing Agent | `agents/validation/equipment_sizing_agent.py` | Equipment template, stream table, `basic_hmb_results`, requirements, design basis | Updated equipment table (`basic_equipment_template`, `basic_equipment_report`, `equipment_sizing_report`) | Uses built-in sizing tools to populate duty/size fields and notes. |
| Safety & Risk Analyst | `agents/validation/safety_risk_analyst.py` | `basic_pdf`, `basic_hmb_results`, `basic_equipment_template`, `requirements` | `basic_hmb_results`, `safety_risk_analyst_report` | Performs a HAZOP-style hazard assessment. |
| Project Manager | `agents/project_manager/project_manager.py` | `requirements`, `basic_pdf`, `basic_hmb_results`, `basic_equipment_template`, `safety_risk_analyst_report` | `approval`, `project_manager_report` | Issues the final gate decision and implementation plan. |

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

- All intermediate artefacts are Markdown tables or sections with explicit headings.
- Values not yet known should be marked as `<value>` with units inside the string (e.g., `<value> °C`).
- Agents downstream from the simulator treat stream/equipment tables as canonical sources, so keep identifiers consistent.

Referencing source prompts when modifying behaviour is strongly recommended to maintain compatibility across the pipeline.
