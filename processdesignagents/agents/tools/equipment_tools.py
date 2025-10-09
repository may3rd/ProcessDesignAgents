from __future__ import annotations

from langchain_core.tools import tool
import math


@tool
def heat_exchanger_sizing(
    duty_kw: float,
    overall_u_kw_m2_k: float,
    lmt_delta_t_k: float,
) -> dict:
    """Estimate required heat-transfer area for a shell-and-tube exchanger."""
    if overall_u_kw_m2_k <= 0:
        raise ValueError("overall_u_kw_m2_k must be positive.")
    if lmt_delta_t_k <= 0:
        raise ValueError("lmt_delta_t_k must be positive.")
    area_m2 = duty_kw / (overall_u_kw_m2_k * lmt_delta_t_k)
    return {
        "duty_kw": duty_kw,
        "overall_u_kw_m2_k": overall_u_kw_m2_k,
        "lmt_delta_t_k": lmt_delta_t_k,
        "area_m2": round(area_m2, 3),
        "notes": "Area calculated using Q = U * A * ΔT_lm.",
    }


@tool
def vessel_volume_estimate(
    volumetric_flow_m3_per_hr: float,
    residence_time_min: float,
    holdup_fraction: float = 0.75,
) -> dict:
    """Estimate required vessel volume based on residence time."""
    if volumetric_flow_m3_per_hr < 0:
        raise ValueError("volumetric_flow_m3_per_hr must be non-negative.")
    if residence_time_min <= 0:
        raise ValueError("residence_time_min must be positive.")
    if not (0 < holdup_fraction <= 1):
        raise ValueError("holdup_fraction must be in (0, 1].")
    required_volume = volumetric_flow_m3_per_hr * residence_time_min / 60.0
    design_volume = required_volume / holdup_fraction
    return {
        "flow_m3_per_hr": volumetric_flow_m3_per_hr,
        "residence_time_min": residence_time_min,
        "holdup_fraction": holdup_fraction,
        "required_volume_m3": round(required_volume, 3),
        "design_volume_m3": round(design_volume, 3),
        "notes": "Assumes vertical vessel with specified liquid holdup fraction.",
    }


@tool
def distillation_column_diameter(
    vapor_mass_flow_kg_per_hr: float,
    vapor_density_kg_per_m3: float,
    design_velocity_m_per_s: float = 1.5,
) -> dict:
    """Estimate distillation column diameter using superficial vapor velocity."""
    if vapor_mass_flow_kg_per_hr <= 0:
        raise ValueError("vapor_mass_flow_kg_per_hr must be positive.")
    if vapor_density_kg_per_m3 <= 0:
        raise ValueError("vapor_density_kg_per_m3 must be positive.")
    if design_velocity_m_per_s <= 0:
        raise ValueError("design_velocity_m_per_s must be positive.")
    volumetric_flow_m3_per_s = vapor_mass_flow_kg_per_hr / 3600.0 / vapor_density_kg_per_m3
    cross_sectional_area = volumetric_flow_m3_per_s / design_velocity_m_per_s
    diameter_m = math.sqrt(4.0 * cross_sectional_area / math.pi)
    return {
        "vapor_mass_flow_kg_per_hr": vapor_mass_flow_kg_per_hr,
        "vapor_density_kg_per_m3": vapor_density_kg_per_m3,
        "design_velocity_m_per_s": design_velocity_m_per_s,
        "diameter_m": round(diameter_m, 3),
        "notes": "Diameter estimated from volumetric flow and superficial vapor velocity.",
    }


EQUIPMENT_SIZING_TOOLS = [
    heat_exchanger_sizing,
    vessel_volume_estimate,
    distillation_column_diameter,
]
