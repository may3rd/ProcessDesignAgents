# Repository Guidelines

ProcessDesignAgents coordinates specialised agents for conceptual chemical-process design.

## Project Structure & Module Organization
- Core agents live in `processdesignagents/agents/`; graph orchestration and shared state definitions are under `processdesignagents/graph/` and `processdesignagents/utils/`.
- User-facing entry points sit in `main.py` (batch run) and `cli/main.py` (Rich dashboard). Keep new interface code alongside these scripts.
- Documentation belongs in `docs/`; assets that accompany reports or demos live in `assets/` and generated artefacts land in `results/` or `reports/`.
- Sample end-to-end outputs are archived in `examples/` (see `examples/reports/` for representative project bundles).
- Tests currently sit beside modules (see `test_auth.py`); prefer adding new suites under a dedicated `tests/` package that mirrors the source tree.

## Build, Test, and Development Commands
- `python -m venv venv && source venv/bin/activate`: create and activate a virtual environment for isolated dependencies.
- `pip install -r requirements.txt`: install runtime and agent framework dependencies.
- `python main.py`: execute the default end-to-end flow defined in `processdesignagents/default_config.py`.
- `python -m cli.main -p "design ..."`: launch the streaming CLI for live monitoring; pass prompts with `-p`.
- `pytest`: run the automated test suite; add `-k name` to target a subset when iterating quickly.

## Coding Style & Naming Conventions
- Target Python 3.10+ and prefer explicit type hints in new public functions.
- Follow Black-style formatting (4-space indents, double quotes where practical) and group imports with isort-style sections (stdlib, third-party, local).
- Name agents and tools descriptively (e.g., `ProcessRequirementsAnalyst`, `estimate_pump_power`) and keep file names snake_case.
- Document non-obvious orchestration steps with concise comments—especially around state transitions inside `graph/setup.py`.

## Testing Guidelines
- Use `pytest` with the `tests/` prefix (`tests/test_streams.py`, etc.) and organise fixtures in `tests/conftest.py`.
- Mirror agent behaviours with deterministic inputs; mock external LLM calls using lightweight stubs in `processdesignagents/utils`.
- Aim for coverage of new state mutations and tool calculations; include regression tests when adjusting sizing formulae.

## Commit & Pull Request Guidelines
- Keep commits small and imperative (e.g., `refine equipment sizing notes`); the history shows concise summaries, so follow that tone.
- Reference related issues in the body when relevant and note any docs or data updates.
- Pull requests should include: a plain-language summary, verification steps (`pytest`, CLI run), and screenshots or excerpts for CLI/report changes.

## Agent & Configuration Tips
- Store provider keys (e.g., `OPENROUTER_API_KEY`) in your environment or a local `.env` ignored by git.
- Update `processdesignagents/default_config.py` or per-run overrides cautiously; document agent prompt changes in `docs/AGENTS.md` to keep artefact guidance aligned.
