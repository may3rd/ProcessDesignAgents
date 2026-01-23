from __future__ import annotations

import re
from pathlib import Path


_FENCE_PATTERN = re.compile(r"^\s*```(?:\w+)?\s*(.*?)\s*```\s*$", re.DOTALL)


def jinja_raw(text: str) -> str:
    """Wrap content in a Jinja2 raw block so literal braces pass through."""
    return "{% raw %}" + text + "{% endraw %}"


def strip_markdown_code_fences(text: str | None) -> str | None:
    """Remove leading/trailing triple-backtick fences from LLM output."""
    if text is None:
        return None
    match = _FENCE_PATTERN.match(text)
    if match:
        return match.group(1).strip()
    return text


def load_prompt(file_name: str) -> str:
    """
    Loads a prompt from the 'prompts/' directory in the project root.

    Args:
        file_name: The name of the file to load (e.g., 'designer_agent_system.md').

    Returns:
        The content of the prompt file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    # Assuming the project root is 3 directories up from this file's location:
    # processdesignagents/agents/utils/prompt_utils.py
    current_dir = Path(__file__).parent
    # project_root is calculated relative to this file
    # processdesignagents/agents/utils -> processdesignagents/agents -> processdesignagents -> root
    project_root = current_dir.parent.parent.parent
    prompts_dir = project_root / "prompts"

    file_path = prompts_dir / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
