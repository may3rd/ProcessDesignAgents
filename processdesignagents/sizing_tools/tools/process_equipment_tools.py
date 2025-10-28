from __future__ import annotations

from langchain_core.tools import tool

from processdesignagents.sizing_tools.interface import equipment_sizing


@tool
def size_reactor_vessel_basic(
    feed_flow_kg_h: float,
    residence_time_minutes: float,
    mixture_density_kg_m3: float,
    reaction_exothermic: bool = False,
    heat_removal_kw: float = 0.0,
    design_pressure_barg: float = 5.0,
    design_temperature_c: float = 60.0,
) -> str:
    """
    Preliminary reactor vessel sizing based on holdup, agitation, and heat removal needs.
    """
    return equipment_sizing(
        "reactor_vessel_sizing",
        feed_flow_kg_h,
        residence_time_minutes,
        mixture_density_kg_m3,
        reaction_exothermic,
        heat_removal_kw,
        design_pressure_barg,
        design_temperature_c,
    )
