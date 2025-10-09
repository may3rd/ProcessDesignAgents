from __future__ import annotations

import re
from typing import Sequence, Union

HeaderSpec = Union[str, Sequence[str]]


def require_sections(markdown: str, sections: list[str], context: str) -> None:
    """Ensure each section heading appears in the markdown."""
    missing = [section for section in sections if f"## {section}" not in markdown]
    if missing:
        raise ValueError(f"{context} missing required sections: {', '.join(missing)}")


def require_table_headers(markdown: str, headers: Sequence[HeaderSpec], context: str) -> None:
    """Ensure a table contains all specified header columns.

    Each header may be a string or a sequence of alternative strings.
    """
    for header in headers:
        options = [header] if isinstance(header, str) else list(header)
        if not options:
            continue
        if any(
            re.search(rf"\|[^\n]*{re.escape(option)}[^\n]*\|", markdown)
            for option in options
        ):
            continue
        joined = " / ".join(options)
        raise ValueError(f"{context} table missing column '{joined}'.")


def require_heading_prefix(markdown: str, prefix: str, context: str) -> None:
    """Ensure at least one heading with the given prefix exists."""
    if re.search(rf"^##\s+{re.escape(prefix)}", markdown, re.MULTILINE):
        return
    if re.search(rf"^##\s+{re.escape(prefix)}\b", markdown, re.MULTILINE):
        return
    if re.search(rf"^##\s+{re.escape(prefix)}\s*\d", markdown, re.MULTILINE):
        return
    pattern = rf"^##\s+{re.escape(prefix)}"
    if not re.search(pattern, markdown, re.IGNORECASE | re.MULTILINE):
        raise ValueError(f"{context} missing any heading starting with '{prefix}'.")
