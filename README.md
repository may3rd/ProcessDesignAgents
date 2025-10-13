# ProcessDesignAgents

ProcessDesignAgents is a multi-agent workflow for conceptual chemical-process design. Each agent is responsible for a portion of the engineering study—from requirement extraction through stream definition, equipment sizing, safety review, and gate approval. The project is inspired by the multi-agent patterns popularised by the [TradingAgents](https://github.com/TauricResearch/TradingAgents) project and adapts those ideas to process engineering.

## Key Features

- **Graph Orchestrated Agents** – A `langgraph` state machine coordinates requirement analysis, concept detailing, stream definition, simulation, equipment sizing, safety review, and project management.
- **Structured Markdown Outputs** – Intermediate artefacts (requirements, stream tables, equipment lists, H&MB summaries) are expressed as Markdown for quick human review and downstream automation.
- **Tool-Assisted Sizing** – Built‑in sizing tools estimate vessel dimensions, exchanger area, column diameter, reactor volume, pump/compressor power, and more.
- **CLI Visualisation** – The CLI (`cli/main.py`) streams agent status, tool calls, and report sections as they are produced.

## Project Layout

```
ProcessDesignAgents/
├─ README.md
├─ requirements.txt
├─ main.py
├─ processdesignagents/
│  ├─ agents/              # Analyst, researcher, designer, and PM agents
│  ├─ graph/               # Graph wiring and propagator
│  ├─ utils/               # Shared helpers and LLM utilities
│  └─ default_config.py
├─ cli/                    # Rich-based command-line viewer
└─ docs/
   ├─ ARCHITECTURE.md      # High-level architecture & dataflow
   └─ AGENTS.md            # Responsibilities and prompts for each agent
```

Additional documentation is available under `docs/`.

## Getting Started

### Prerequisites

- Python 3.10+
- Recommended: virtual environment (e.g. `python -m venv venv`)

### Installation

```bash
git clone https://github.com/YOUR_ORG/ProcessDesignAgents.git
cd ProcessDesignAgents
pip install -r requirements.txt
```

Set any required API keys for your LLM provider (e.g. `OPENROUTER_API_KEY`) in your environment or `.env`.

## Running the Workflow

### Simple Entry Point

```bash
python main.py
```

Edit the `problem_statement` in `main.py` to explore different design briefs.

### CLI Visualization

```bash
python -m cli.main -p "design the energy recovery from flue gas..."
```

The CLI streams agent progress, tool invocations, and compiled reports using Rich panels.

## Agent Pipeline (Default Graph)

1. **Process Requirements Analyst** – Extracts structured requirements from the problem statement.
2. **Innovative Researcher** – Brainstorms potential process concepts.
3. **Conservative Researcher** – Refines and validates potential process concepts.
4. **Concept Detailer** – Selects the most feasible concept and builds a detailed brief.
5. **Design Basis Analyst** – Writes the design basis referencing the concept detail.
6. **Basic PDF Designer** – Produces the conceptual flowsheet in Markdown.
7. **Stream Data Builder** – Creates a stream summary table with placeholders.
8. **Stream Data Estimator** – Populates stream and H&MB tables with estimated conditions.
9. **Equipment List Builder** – Generates an equipment template table tied to streams.
10. **Equipment Sizing Agent** – Calls sizing tools and fills equipment details & notes.
11. **Safety & Risk Analyst** – Performs a HAZOP-style review.
12. **Project Manager** – Compiles the final approval report.

The graph wiring lives in `processdesignagents/graph/setup.py`. State fields are defined in `processdesignagents/agents/utils/agent_states.py`.

## Tooling & Extensions

The sizing tools are located in `processdesignagents/agents/tools/equipment_tools.py`. They currently cover:

- Heat exchanger area
- Vessel volume, diameter, length, orientation
- Distillation column diameter
- Reactor space-time volume
- Pump power
- Compressor power

Adding new tools only requires defining a `@tool` function and registering it in the equipment sizing agent.

## Development

- **Tests**: Add unit tests under `tests/` (not yet provided) and run with `pytest`.
- **Formatting**: Follow `black`/`isort` style conventions if you add CI.
- **Docs**: Update `docs/` when the graph or agent prompts change.

## Citation

If you use this repository, please cite both ProcessDesignAgents and the inspiration source TradingAgents:

```
ProcessDesignAgents. 2025. https://github.com/YOUR_ORG/ProcessDesignAgents.
TradingAgents. 2025. https://github.com/TauricResearch/TradingAgents.
```

## License

MIT License (see `LICENSE`, if provided).
