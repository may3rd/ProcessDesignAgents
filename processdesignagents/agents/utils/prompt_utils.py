from __future__ import annotations


def jinja_raw(text: str) -> str:
    """Wrap content in a Jinja2 raw block so literal braces pass through."""
    return "{% raw %}" + text + "{% endraw %}"
