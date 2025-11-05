# Architecture

ProcessDesignAgents uses a `langgraph` state machine to orchestrate a sequence of specialised agents. Each agent reads from and writes to a shared `DesignState` (see `processdesignagents/agents/utils/agent_states.py`). The graph is defined in `processdesignagents/graph/setup.py` and compiled by `ProcessDesignGraph`.

```
Problem Statement → Process Requirements Analyst → Innovative Researcher → Conservative Researcher →
Concept Detailer → Component List Researcher → Design Basis Analyst → Flowsheet Design Agent →
Equipment & Stream Catalog Agent → Stream Property Estimation Agent → Equipment Sizing Agent →
Safety & Risk Analyst → Project Manager
```

## State Fields

| Field | Description | Primary Writer |
|-------|-------------|----------------|
| `problem_statement` | Original brief captured from the first human message. | Propagator |
| `process_requirements` | Markdown summary of objectives, constraints, and feed/product details. | Process Requirements Analyst |
| `research_concepts` | JSON list of candidate concepts with maturity tags. | Innovative Researcher |
| `research_rateing_results` | JSON replay providing feasibility scores, risks, and recommendations. | Conservative Researcher |
| `selected_concept_name` | Identifier for the winning concept. | Concept Detailer |
| `selected_concept_details` | Markdown brief describing the chosen concept. | Concept Detailer |
| `selected_concept_evaluation` | JSON payload storing the evaluation data for the chosen concept. | Concept Detailer |
| `component_list` | Markdown inventory (formula and molecular weight) for key components. | Component List Researcher |
| `design_basis` | Markdown basis-of-design that collects the upstream artefacts. | Design Basis Analyst |
| `flowsheet_description` | Markdown flowsheet narrative with preliminary equipment/stream tables. | Flowsheet Design Agent |
| `equipment_list_template` | JSON equipment template seeded with placeholders. | Equipment & Stream Catalog Agent |
| `equipment_list_results` | Sized equipment catalogue JSON. | Equipment Sizing Agent |
| `stream_list_template` | JSON stream template seeded with placeholders. | Equipment & Stream Catalog Agent |
| `stream_list_results` | Heat & material balance JSON payload. | Stream Property Estimation Agent |
| `safety_risk_analyst_report` | Markdown HAZOP-style hazard review. | Safety & Risk Analyst |
| `project_manager_report` | Final gate approval memo. | Project Manager |
| `project_approval` | Extracted approval status (`Approved`, `Conditional`, etc.). | Project Manager |
| `messages` | Running transcript of LLM calls shared across the workflow. | All agents |

The combined view is generated on demand via `build_equipment_stream_payload`, which merges the equipment and stream JSON before rendering or passing to prompts. No dedicated `equipment_and_stream_*` fields remain in the state.

## Message Flow

LLM responses are appended to `state["messages"]` so downstream agents can reference prior context when necessary. The CLI visualises these messages, tool calls, and reports. Each run also creates a JSON snapshot at `eval_results/ProcessDesignAgents_logs/full_states_log.json` for offline review.

## Tool Nodes

`ProcessDesignGraph._create_tool_nodes()` registers the equipment sizing tool node, exposing `size_heat_exchanger_basic` and `size_pump_basic` from `processdesignagents/agents/utils/agent_sizing_tools.py`. Extend the dictionary to surface additional sizing helpers (e.g., compressors or columns) to the Equipment Sizing Agent.

## Adding Agents

1. Define the agent function factory in `processdesignagents/agents/...`.
2. Update `DesignState` with new fields if needed.
3. Register the factory in `processdesignagents/agents/__init__.py`.
4. Insert the node and edges in `processdesignagents/graph/setup.py` (merge equipment and stream data on demand if a new agent expects the combined view).
5. Add UI hooks (CLI report sections, etc.) when appropriate.

For deeper examples, examine the equipment/stream catalog builder and the downstream estimators—they show how the split artefacts flow through the pipeline and are recombined when needed. Sample end-to-end outputs are available in `examples/reports/` for quick reference.
