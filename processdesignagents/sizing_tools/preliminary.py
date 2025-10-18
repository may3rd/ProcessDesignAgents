import json
from typing import Annotated, Dict

#
def prelim_basic_heat_exchanger_sizing(
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

def prelim_pump_sizing(flow_kg_hr: str) -> str:
    return_json = {
        "flow_kg_hr": flow_kg_hr,
    }
    
    return_str = json.dumps(return_json)
    return return_str

def prelim_centrifugal_pump_sizing(flow_kg_hr: str) -> str:
    return_json = {
        "flow_kg_hr": flow_kg_hr,
    }
    
    return_str = json.dumps(return_json)
    return return_str