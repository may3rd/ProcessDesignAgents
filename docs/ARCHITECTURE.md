# Architecture

ProcessDesignAgents uses a `langgraph` state machine to orchestrate a sequence of specialised agents. Each agent reads from and writes to a shared `DesignState` (see `processdesignagents/agents/utils/agent_states.py`). The graph is defined in `processdesignagents/graph/setup.py` and compiled by `ProcessDesignGraph`.

```
Problem Statement → Requirements Analyst → Concept Detailer → Design Basis →
Basic PFD Designer → Equipments & Streams List Builder → Stream Data Estimator → Equipment List →
Equipment Sizing → Safety & Risk → Project Manager
```

## State Fields

| Field | Description | Primary Writer |
|-------|-------------|----------------|
| `requirements` | Markdown summary of objectives, constraints, components | Process Requirements Analyst |
| `selected_concept_details`, `selected_concept_name` | Detailed concept brief and name | Concept Detailer |
| `design_basis` | Markdown design basis for sizing/validation | Design Basis Analyst |
| `basic_pfd` | Conceptual flowsheet narrative | Basic PFD Designer |
| `stream_list_template` | Stream inventory JSON template | Equipments & Streams List Builder |
| `stream_list_results` | Heat & material balance JSON payload | Stream Data Estimator |
| `equipment_list_template` | Equipment catalogue JSON with placeholders | Equipment List Builder |
| `equipment_list_results` | Sized equipment catalogue JSON | Equipment Sizing Agent |
| `safety_risk_analyst_report` | HAZOP-style risk assessment JSON | Safety & Risk Analyst |
| `project_manager_report` | Final gate approval | Project Manager |

## Message Flow

LLM responses are appended to `state["messages"]` so downstream agents can reference prior context when necessary. The CLI visualises these messages, tool calls, and reports.

## Adding Agents

1. Define the agent function factory in `processdesignagents/agents/...`.
2. Update `DesignState` with new fields if needed.
3. Register the factory in `processdesignagents/agents/__init__.py`.
4. Insert the node and edges in `processdesignagents/graph/setup.py`.
5. Add UI hooks (CLI report sections, etc.) when appropriate.

For deeper examples, examine the stream and equipment builder agents—they show how structured artefacts flow through the pipeline and are reused by later stages. Sample end-to-end outputs are available in `examples/reports/` for quick reference.
