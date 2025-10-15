import pandas as pd
import graphviz
from typing import Any


def _safe_get_numeric(source: Any, key: str, default: float) -> float:
    if isinstance(source, dict):
        value = source.get(key)
        if isinstance(value, (int, float)):
            return float(value)
    return float(default)


def generate_hmb(basic_pfd: Any, basic_hmb_results: Any) -> pd.DataFrame:
    """Generate a simple Heat and Material Balance table from markdown inputs."""
    optimized_yield = _safe_get_numeric(basic_hmb_results, "optimized_yield", 90.8)

    hmb_data = {
        "Stream": [
            "Feed Stream",
            "Process Outlet",
            "Target Product",
            "Byproducts",
        ],
        "Mass Flow (kg/h)": [1000.0, 1000.0, round(optimized_yield, 1), 1000.0 - round(optimized_yield, 1)],
        "Temperature (°C)": [25.0, 200.0, 35.0, 120.0],
        "Pressure (bar)": [1.1, 5.0, 3.0, 1.5],
    }

    return pd.DataFrame(hmb_data)


def generate_pfd(basic_pfd: Any, basic_hmb_results: Any) -> graphviz.Digraph:
    """Generate a placeholder PFD graph using available markdown descriptions."""
    dot = graphviz.Digraph(comment="Preliminary PFD")
    dot.node("Feed", "Feed Stream\n1000 kg/h")
    dot.node("Process", "Process Block\nDerived from Basic PFD")
    yield_percent = _safe_get_numeric(basic_hmb_results, "optimized_yield", 90.8)
    dot.node("Product", f"Product Stream\nYield {yield_percent:.1f}%")
    dot.node("Waste", "Byproducts")
    dot.edge("Feed", "Process")
    dot.edge("Process", "Product")
    dot.edge("Process", "Waste")
    return dot


def generate_equipment_list(basic_pfd: Any) -> pd.DataFrame:
    """Generate a simple equipment list placeholder."""
    equipment = [
        {"Unit": "Unit-100", "Type": "Placeholder", "Specs": "Derived from basic PFD description."}
    ]
    return pd.DataFrame(equipment)
