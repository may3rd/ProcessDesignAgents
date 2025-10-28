from .stream_calculation_tools import (
    calculate_molar_flow_from_mass,
    calculate_mass_flow_from_molar,
    convert_compositions,
    calculate_volume_flow,
    perform_mass_balance_split,
    perform_mass_balance_mix,
    perform_energy_balance_mix,
    calculate_heat_exchanger_outlet_temp,
    calculate_heat_exchanger_duty,
    get_physical_properties, # Now uses CoolProp
    build_stream_object,
    )

__all__ = [
    "calculate_molar_flow_from_mass",
    "calculate_mass_flow_from_molar",
    "convert_compositions",
    "calculate_volume_flow",
    "perform_mass_balance_split",
    "perform_mass_balance_mix",
    "perform_energy_balance_mix",
    "calculate_heat_exchanger_outlet_temp",
    "calculate_heat_exchanger_duty",
    "get_physical_properties",
    "build_stream_object",
]