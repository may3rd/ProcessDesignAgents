from __future__ import annotations

from typing import Any, Dict


def prefix_mass_fraction_component_names(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure that any component tracked by mass fraction is prefixed with ``m_``.

    The workflow expects mass-fraction entries to be distinguishable from molar
    fractions, particularly for downstream property calculations. This function
    walks the stream objects in a payload and renames composition keys where the
    unit indicates a mass fraction and the key is missing the ``m_`` prefix.
    """

    if not isinstance(payload, dict):
        return payload

    streams = payload.get("streams")
    if isinstance(streams, list):
        for stream in streams:
            if isinstance(stream, dict):
                _normalize_stream_compositions(stream, "compositions")
                _normalize_stream_compositions(stream, "components")
    return payload


def _normalize_stream_compositions(stream: Dict[str, Any], field: str) -> None:
    compositions = stream.get(field)
    if not isinstance(compositions, dict):
        return

    updated: Dict[str, Any] = {}
    mutated = False

    for name, entry in compositions.items():
        new_name = name
        if (
            isinstance(name, str)
            and isinstance(entry, dict)
            and _is_mass_fraction(entry.get("unit"))
        ):
            new_name = _canonical_mass_fraction_key(name)
            mutated = True
        updated[new_name] = entry

    if mutated:
        stream[field] = updated


def _is_mass_fraction(unit: Any) -> bool:
    if not isinstance(unit, str):
        return False
    unit_lower = unit.lower()
    return "mass" in unit_lower or "wt" in unit_lower


def _canonical_mass_fraction_key(name: str) -> str:
    """
    Normalize a component name so mass-fraction keys strictly follow ``m_<component>``.
    """
    if not isinstance(name, str):
        return name

    base = name.strip()
    if base.startswith("m_"):
        base = base[2:]

    # Remove common descriptive prefixes before the component name
    lower_base = base.lower()
    for prefix in (
        "mass_fraction_",
        "massfraction_",
        "mass_frac_",
        "mass_",
        "wt_fraction_",
        "wt_frac_",
        "wtpercent_",
        "wt%_",
        "wt_",
        "w_",
    ):
        if lower_base.startswith(prefix):
            base = base[len(prefix) :]
            lower_base = base.lower()
            break

    base = base.lstrip("_")
    if not base:
        return "m_component"
    return f"m_{base}"
