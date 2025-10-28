from __future__ import annotations

from langchain_core.tools import tool

from processdesignagents.sizing_tools.interface import equipment_sizing


@tool
def size_pressure_safety_valve_basic(
    protected_equipment_id: str,
    required_relief_flow_kg_h: float,
    relief_pressure_barg: float,
    back_pressure_barg: float,
    fluid_phase: str = "vapor",
    fluid_density_kg_m3: float | None = None,
) -> str:
    """
    Preliminary PSV sizing returning nozzle, capacity, and valve class recommendations.
    """
    return equipment_sizing(
        "pressure_safety_valve_sizing",
        protected_equipment_id,
        required_relief_flow_kg_h,
        relief_pressure_barg,
        back_pressure_barg,
        fluid_phase,
        fluid_density_kg_m3,
    )


@tool
def size_blowdown_valve_basic(
    protected_equipment_id: str,
    equipment_volume_m3: float,
    blowdown_time_minutes: float,
    initial_pressure_barg: float,
    final_pressure_barg: float = 0.5,
    fluid_type: str = "hydrocarbon",
    fluid_density_kg_m3: float | None = None,
) -> str:
    """
    Preliminary blowdown valve sizing estimating capacities and connection diameters.
    """
    return equipment_sizing(
        "blowdown_valve_sizing",
        protected_equipment_id,
        equipment_volume_m3,
        blowdown_time_minutes,
        initial_pressure_barg,
        final_pressure_barg,
        fluid_type,
        fluid_density_kg_m3,
    )


@tool
def size_vent_valve_basic(
    vessel_id: str,
    vapor_flow_kmol_h: float,
    vapor_molecular_weight: float,
    vapor_density_kg_m3: float,
    relieving_temperature_c: float,
    relieving_pressure_barg: float,
) -> str:
    """
    Preliminary vent valve sizing for atmospheric or low-pressure relief scenarios.
    """
    return equipment_sizing(
        "vent_valve_sizing",
        vessel_id,
        vapor_flow_kmol_h,
        vapor_molecular_weight,
        vapor_density_kg_m3,
        relieving_temperature_c,
        relieving_pressure_barg,
    )
