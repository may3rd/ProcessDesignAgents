# Sizing Tool Architecture

This document explains how the equipment sizing helpers in ProcessDesignAgents are organised, how agents call them, and what you need to touch when adding new sizing capabilities.

## Overview

- All sizing helpers live under `processdesignagents/sizing_tools/`.
- LangChain-compatible tool wrappers are defined in `processdesignagents/sizing_tools/tools/…` and each one forwards to the central dispatcher in `processdesignagents/sizing_tools/interface.py`.
- The dispatcher loads configuration from `processdesignagents/sizing_tools/config.py`, routes the request to the relevant implementation (currently the preliminary sizing layer), and returns a JSON string result.
- Agent-facing modules import the wrappers through `processdesignagents/agents/utils/agent_sizing_tools.py`, which exposes a stable list for the Equipment Sizing Agent.

## Package Layout

- `sizing_tools/tools/`: LangChain `@tool` wrappers grouped by equipment family (heat transfer, fluid handling, separation, storage, relief, specialised).
- `sizing_tools/interface.py`: Category registry, configuration lookup, and the `equipment_sizing()` router that fans out to specific implementations.
- `sizing_tools/preliminary.py`: Reference implementations for each tool. Functions return JSON-formatted strings with the calculated sizing data or error messages.
- `sizing_tools/advanced.py`: Placeholder for more detailed sizing routines; not currently wired into the dispatcher but available for future expansion.
- `sizing_tools/config.py`: Loads defaults from `processdesignagents/default_config.py` and offers setters for overriding category-level behaviour.
- `agents/utils/agent_sizing_tools.py`: Re-exports the LangChain tool callables so agents can import a single module without depending on individual tool files.

## Call Flow

1. The Equipment Sizing Agent builds a `tools_list` from the exports in `agent_sizing_tools.py` and passes it to `run_agent_with_tools`.
2. When the LLM selects a tool, the LangChain wrapper (for example `size_heat_exchanger_basic`) calls `equipment_sizing("basic_heat_exchanger_sizing", …)`.
3. `equipment_sizing()`:
   - Determines the tool category via `SIZING_TOOLS_BY_CATEGORIES`.
   - Reads configuration (category- or tool-level) from `config.get_config()`.
   - Attempts the configured implementation (currently the preliminary layer) and falls back to any other registered implementations if the primary raises.
   - Aggregates the JSON string results and returns them to the agent.
4. The agent merges the JSON payload back into the shared design state and logs the tool output for reporting.

## Tool Catalogue

The dispatcher uses two registries in `interface.py`:

- `SIZING_TOOLS_BY_CATEGORIES`: human-readable description plus the tool identifiers exposed in prompts.
- `SIZING_TOOL_METHODS`: maps each identifier (e.g. `"pump_sizing"`) to one or more implementation callables (`prelim_pump_sizing`, etc.).

Each implementation returns a JSON string that contains the primary sizing outputs and any warning notes. The Equipment Sizing Agent expects the JSON to include, at minimum, the fields described in that tool’s prompt examples (see `processdesignagents/agents/designers/tools/equipment_sizing_prompt.py`).

## Configuration & Fallbacks

- Defaults reside in `processdesignagents/default_config.py` under the `category_level_methods` and `sizing_tool_methods` keys.
- `config.initialize_config()` loads those defaults; call `config.set_config({...})` early in your application to override behaviour.
- Category-level settings apply to every tool in the group, while tool-level settings take precedence for specific identifiers.
- Multiple implementations can be chained by separating values with commas (e.g. `"basic_heat_exchanger_sizing": "advanced, preliminary"`). The router will try each method in order until one succeeds.

## Adding a New Tool

1. Implement the sizing logic in the appropriate module (or create a new one) under `sizing_tools/tools/`. Wrap the function with `@tool` and forward the call to `equipment_sizing("<identifier>", …)`.
2. Add a preliminary (or advanced) implementation in `sizing_tools/preliminary.py` (or another implementation module) that returns a JSON string.
3. Register the identifier in `SIZING_TOOLS_BY_CATEGORIES` and `SIZING_TOOL_METHODS` within `interface.py`, pointing to your implementation function.
4. Re-export the wrapper in `agents/utils/agent_sizing_tools.py` so agents can import it.
5. Update `processdesignagents/agents/designers/equipment_sizing_agent.py` to include the new callable in the `tools_list`.
6. Extend prompt examples (`agents/designers/tools/equipment_sizing_prompt.py`) and tests (`tests/test_equipment_sizing.py`) so the LLM understands how to invoke the tool and downstream validations stay aligned.

### Skeleton Example

```python
# processdesignagents/sizing_tools/tools/cooling_equipment_tools.py
from __future__ import annotations

from langchain_core.tools import tool

from processdesignagents.sizing_tools.interface import equipment_sizing


@tool
def size_cooling_tower_basic(
    duty_kw: float,
    water_inlet_c: float,
    water_outlet_c: float,
    wet_bulb_c: float,
    approach_c: float,
) -> str:
    """Preliminary sizing for a mechanical draft cooling tower."""
    return equipment_sizing(
        "cooling_tower_sizing",
        duty_kw,
        water_inlet_c,
        water_outlet_c,
        wet_bulb_c,
        approach_c,
    )
```

```python
# processdesignagents/sizing_tools/preliminary.py
def prelim_cooling_tower_sizing(
    duty_kw: float,
    water_inlet_c: float,
    water_outlet_c: float,
    wet_bulb_c: float,
    approach_c: float,
) -> str:
    results = {
        "fill_volume_m3": 42.0,
        "fan_power_kw": 18.0,
        "circulation_rate_m3_h": 320.0,
        "notes": "Assumes mechanical draft tower with counter-flow fill; validate with vendor.",
    }
    return json.dumps(results, indent=4)
```

```python
# processdesignagents/sizing_tools/interface.py
SIZING_TOOLS_BY_CATEGORIES["cooling_tower"] = {
    "description": "Size a cooling tower.",
    "tools": ["cooling_tower_sizing"],
}

SIZING_TOOL_METHODS["cooling_tower_sizing"] = {
    "preliminary": prelim_cooling_tower_sizing,
}
```

```python
# processdesignagents/agents/utils/agent_sizing_tools.py
from processdesignagents.sizing_tools.tools.cooling_equipment_tools import (
    size_cooling_tower_basic,
)

__all__.append("size_cooling_tower_basic")
```

```python
# processdesignagents/agents/designers/equipment_sizing_agent.py
tools_list = [
    # existing entries ...
    size_cooling_tower_basic,
]
```

## Debugging Tips

- The dispatcher prints `DEBUG` lines whenever it calls an implementation or encounters an error. Run the CLI with logging enabled to trace the tool selection order.
- Each preliminary function emits JSON strings even on validation errors; parse the result and surface the `error` field in agent notes to keep operators informed.
- If a tool is not appearing in the prompt, ensure it is included in both the agent’s `tools_list` and the XML tool specification inside `equipment_sizing_prompt_with_tools`.
