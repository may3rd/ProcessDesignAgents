# Architecture

ProcessDesignAgents uses a `langgraph` state machine to orchestrate a sequence of specialised agents. Each agent reads from and writes to a shared `DesignState` (see `processdesignagents/agents/utils/agent_states.py`). The graph is defined in `processdesignagents/graph/setup.py` and compiled by `ProcessDesignGraph`.

```
Problem Statement → Requirements Analyst → Innovative Researcher → Conservative Researcher →
Concept Detailer → Design Basis → Basic PFD Designer → Equipments & Streams List Builder →
Stream Data Estimator → Equipment Sizing → Safety & Risk → Project Manager
```

## State Fields

| Field | Description | Primary Writer |
|-------|-------------|----------------|
| `process_requirements` | Markdown summary of objectives, constraints, components | Process Requirements Analyst |
| `selected_concept_details`, `selected_concept_name` | Detailed concept brief and name | Concept Detailer |
| `design_basis` | Markdown design basis for sizing/validation | Design Basis Analyst |
| `flowsheet_description` | Conceptual flowsheet narrative | Basic PFD Designer |
| `equipment_and_stream_results` | Combined equipment/stream JSON that remains the canonical artefact through estimation and sizing | Equipments & Streams List Builder (updated downstream) |
| `stream_list_template` | Stream inventory JSON template | Equipments & Streams List Builder |
| `stream_list_results` | Heat & material balance JSON payload | Stream Data Estimator |
| `equipment_list_template` | Equipment catalogue JSON with placeholders (currently populated by the combined builder) | Equipments & Streams List Builder |
| `equipment_list_results` | Sized equipment catalogue JSON extracted from the combined artefact | Equipment Sizing Agent |
| `safety_risk_analyst_report` | HAZOP-style risk assessment JSON | Safety & Risk Analyst |
| `project_manager_report` | Final gate approval | Project Manager |

## Message Flow

LLM responses are appended to `state["messages"]` so downstream agents can reference prior context when necessary. The CLI visualises these messages, tool calls, and reports. Each run also creates a JSON snapshot at `eval_results/ProcessDesignAgents_logs/full_states_log.json` for offline review.

## Adding Agents

1. Define the agent function factory in `processdesignagents/agents/...`.
2. Update `DesignState` with new fields if needed.
3. Register the factory in `processdesignagents/agents/__init__.py`.
4. Insert the node and edges in `processdesignagents/graph/setup.py` (the combined equipment/stream artefact is the preferred hand-off between units).
5. Add UI hooks (CLI report sections, etc.) when appropriate.

For deeper examples, examine the combined equipment/stream builder and the downstream estimators—they show how structured artefacts flow through the pipeline and are reused by later stages. Sample end-to-end outputs are available in `examples/reports/` for quick reference.
