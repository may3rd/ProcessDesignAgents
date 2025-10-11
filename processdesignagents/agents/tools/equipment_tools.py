from __future__ import annotations

from langchain_core.tools import tool
import math

GRAVITY = 9.80665  # m/s^2
BAR_TO_PA = 1e5



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
    orientation: str = "vertical",
    slender_ratio: float = 3.0,
) -> dict:
    """Estimate required vessel volume and nominal dimensions based on residence time."""
    if volumetric_flow_m3_per_hr < 0:
        raise ValueError("volumetric_flow_m3_per_hr must be non-negative.")
    if residence_time_min <= 0:
        raise ValueError("residence_time_min must be positive.")
    if not (0 < holdup_fraction <= 1):
        raise ValueError("holdup_fraction must be in (0, 1].")
    if slender_ratio <= 0:
        raise ValueError("slender_ratio must be positive.")
    required_volume = volumetric_flow_m3_per_hr * residence_time_min / 60.0
    design_volume = required_volume / holdup_fraction

    normalized_orientation = orientation.lower().strip()
    if normalized_orientation not in {"vertical", "horizontal"}:
        normalized_orientation = "vertical"

    # Assume cylindrical vessel with length = slender_ratio * diameter
    diameter_m = (4.0 * design_volume / (math.pi * slender_ratio)) ** (1.0 / 3.0)
    length_m = slender_ratio * diameter_m

    return {
        "flow_m3_per_hr": volumetric_flow_m3_per_hr,
        "residence_time_min": residence_time_min,
        "holdup_fraction": holdup_fraction,
        "required_volume_m3": round(required_volume, 3),
        "design_volume_m3": round(design_volume, 3),
        "orientation": normalized_orientation,
        "slender_ratio": slender_ratio,
        "diameter_m": round(diameter_m, 3),
        "length_m": round(length_m, 3),
        "notes": "Cylindrical vessel with length = slender_ratio * diameter; volume set by residence time and holdup.",
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


@tool
def reactor_volume_space_time(
    feed_mass_flow_kg_per_hr: float,
    space_time_hr: float,
    mixture_density_kg_per_m3: float = 1000.0,
) -> dict:
    """Estimate reactor volume from space time (τ)."""
    if feed_mass_flow_kg_per_hr <= 0:
        raise ValueError("feed_mass_flow_kg_per_hr must be positive.")
    if space_time_hr <= 0:
        raise ValueError("space_time_hr must be positive.")
    if mixture_density_kg_per_m3 <= 0:
        raise ValueError("mixture_density_kg_per_m3 must be positive.")
    volumetric_flow_m3_per_hr = feed_mass_flow_kg_per_hr / mixture_density_kg_per_m3
    required_volume_m3 = volumetric_flow_m3_per_hr * space_time_hr
    return {
        "feed_mass_flow_kg_per_hr": feed_mass_flow_kg_per_hr,
        "space_time_hr": space_time_hr,
        "mixture_density_kg_per_m3": mixture_density_kg_per_m3,
        "reactor_volume_m3": round(required_volume_m3, 3),
        "notes": "Volume = volumetric flow * space time.",
    }


@tool
def pump_power_estimate(
    flow_m3_per_hr: float,
    head_m: float,
    efficiency: float = 0.7,
    fluid_density_kg_per_m3: float = 1000.0,
) -> dict:
    """Estimate pump shaft power based on hydraulic duty."""
    if flow_m3_per_hr < 0:
        raise ValueError("flow_m3_per_hr must be non-negative.")
    if head_m <= 0:
        raise ValueError("head_m must be positive.")
    if not (0 < efficiency <= 1):
        raise ValueError("efficiency must be between 0 and 1.")
    if fluid_density_kg_per_m3 <= 0:
        raise ValueError("fluid_density_kg_per_m3 must be positive.")
    flow_m3_per_s = flow_m3_per_hr / 3600.0
    hydraulic_power_kw = fluid_density_kg_per_m3 * GRAVITY * head_m * flow_m3_per_s / 1000.0
    shaft_power_kw = hydraulic_power_kw / efficiency
    return {
        "flow_m3_per_hr": flow_m3_per_hr,
        "head_m": head_m,
        "efficiency": efficiency,
        "fluid_density_kg_per_m3": fluid_density_kg_per_m3,
        "hydraulic_power_kw": round(hydraulic_power_kw, 3),
        "shaft_power_kw": round(shaft_power_kw, 3),
        "notes": "Hydraulic power = ρ g Q H; shaft power accounts for pump efficiency.",
    }


@tool
def compressor_power_estimate(
    suction_flow_m3_per_hr: float,
    suction_pressure_bar: float,
    discharge_pressure_bar: float,
    suction_temperature_c: float = 25.0,
    k: float = 1.4,
    efficiency: float = 0.75,
) -> dict:
    """Estimate compressor power using ideal-gas adiabatic relations."""
    if suction_flow_m3_per_hr <= 0:
        raise ValueError("suction_flow_m3_per_hr must be positive.")
    if suction_pressure_bar <= 0 or discharge_pressure_bar <= 0:
        raise ValueError("pressures must be positive.")
    if discharge_pressure_bar <= suction_pressure_bar:
        raise ValueError("discharge_pressure_bar must exceed suction_pressure_bar.")
    if not (0 < efficiency <= 1):
        raise ValueError("efficiency must be between 0 and 1.")
    if k <= 1:
        raise ValueError("k must be greater than 1.")

    suction_pressure_pa = suction_pressure_bar * BAR_TO_PA
    discharge_pressure_pa = discharge_pressure_bar * BAR_TO_PA
    flow_m3_per_s = suction_flow_m3_per_hr / 3600.0
    temperature_k = suction_temperature_c + 273.15

    pressure_ratio = discharge_pressure_pa / suction_pressure_pa
    power_kw = (
        (k / (k - 1))
        * suction_pressure_pa
        * flow_m3_per_s
        * (pressure_ratio ** ((k - 1) / k) - 1)
        / efficiency
        / 1000.0
    )
    return {
        "suction_flow_m3_per_hr": suction_flow_m3_per_hr,
        "suction_pressure_bar": suction_pressure_bar,
        "discharge_pressure_bar": discharge_pressure_bar,
        "suction_temperature_c": suction_temperature_c,
        "polytropic_exponent": k,
        "efficiency": efficiency,
        "estimated_power_kw": round(power_kw, 3),
        "notes": "Power from adiabatic compression of ideal gas.",
    }


EQUIPMENT_SIZING_TOOLS = [
    heat_exchanger_sizing,
    vessel_volume_estimate,
    distillation_column_diameter,
    reactor_volume_space_time,
    pump_power_estimate,
    compressor_power_estimate,
]
