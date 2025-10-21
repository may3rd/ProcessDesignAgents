import json
from typing import Annotated, Dict

#
def prelim_basic_heat_exchanger_sizing(
    basic_heat_exchanger: Annotated[Dict, {}],
    hot_stream: Annotated[Dict, {}],
    cold_stream: Annotated[Dict, {}]
) -> str:
    """
    Sizing the basic heat exchanger.
    Agrs:
        basic_heat_exchanger_sizing (Dict): the information of heat exchanger extracted from equipment list
        hot_stream (Dict): hot stream data
        cold_stream (Dict): cold stream data
    Returns:
        str: An update equipment sizing in JSON format.
    """
    
    return_json = {
        "area_m2": 100,
        "lmtd_C": 100,
        "U_design_W_m2K": 850
    }
    
    return_str = json.dumps(return_json)
    print(f"DEBUG: prelim_basic_heat_exchanger_sizing: {return_str}")
    
    return return_str

def prelim_shell_and_tube_heat_exchanger_sizing(
    basic_heat_exchanger_sizing: Annotated[Dict, {}],
    hot_stream: Annotated[Dict, {}],
    cold_stream: Annotated[Dict, {}]
) -> str:
    duty_kW = basic_heat_exchanger_sizing.get("duty_kW", 0)
    
    return_json = {
        "duty_kW": duty_kW,
    }
    
    return_str = json.dumps(return_json)
    return return_str

def prelim_pressurized_vessel_sizing(volume: str) -> str:
    return_json = {
        "volume": volume,
    }
    
    return_str = json.dumps(return_json)
    return return_str

def prelim_vertical_pressurized_vessel_sizing(volume: str) -> str:
    return_json = {
        "volume": volume,
    }
    
    return_str = json.dumps(return_json)
    return return_str

def prelim_horizontal_pressurized_vessel_sizing(volume: str) -> str:
    return_json = {
        "volume": volume,
    }
    
    return_str = json.dumps(return_json)
    return return_str

def prelim_tank_sizing(volume: str) -> str:
    return_json = {
        "volume": volume,
    }
    
    return_str = json.dumps(return_json)
    return return_str

def prelim_pump_sizing(
    pump_data: Annotated[Dict, {}],
    process_stream: Annotated[Dict, {}],
) -> str:
    """
    Sizing the basic heat exchanger.
    Agrs:
        pump_data (Dict): the information of pump extracted from equipment list
        process_stream (Dict): process stream data
    Returns:
        str: An update equipment sizing in JSON format.
    """
    
    return_json = {
        "flow_kg_hr": 99.0,
        "power_kW": 100.0,
    }
    
    return_str = json.dumps(return_json)
    return return_str

def prelim_centrifugal_pump_sizing(flow_kg_hr: str) -> str:
    return_json = {
        "flow_kg_hr": flow_kg_hr,
    }
    
    return_str = json.dumps(return_json)
    return return_str
