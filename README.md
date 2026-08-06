# ProcessDesignAgents — DEPRECATED

> ⚠️ **This repository is archived.** The active project has moved to the [process-orchestrator-plugin](https://github.com/may3rd/process-orchestrator-plugin) Agent Plugin.

## What Changed

The multi-agent process design workflow has been **repackaged as a portable [Agent Plugins](https://agent-plugins.org) v1.0.0 plugin**. Instead of a Python/LangGraph codebase, the pipeline is now defined as 13 `SKILL.md` files (orchestrator + 12 sub-agents) with a shared state schema, PES MCP integration, and an OpenClaw extension namespace.

### Old Architecture (this repo)
- Python LangGraph state machine
- LangChain prompt templates
- CLI via `python -m cli.main`
- Tied to Python runtime

### New Architecture ([process-orchestrator-plugin](https://github.com/may3rd/process-orchestrator-plugin))
- Portable Agent Plugins format (client-agnostic)
- 13 `SKILL.md` files with YAML frontmatter
- Pipeline defined in `ai.openclaw/config/graph.json`
- PES MCP server for calculations (Streamable HTTP + stdio)
- Works in any conformant client (OpenClaw, Cursor, VS Code, etc.)

## Migration

If you were using this repo, the new plugin is at:

```
https://github.com/may3rd/process-orchestrator-plugin
```

The 12-step pipeline, state schema, and agent responsibilities are preserved. The new format is simpler, more portable, and requires no Python runtime to define the workflow.

## License

MIT License (see [LICENSE](LICENSE) for details).
