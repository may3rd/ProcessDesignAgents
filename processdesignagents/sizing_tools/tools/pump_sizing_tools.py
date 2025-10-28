from __future__ import annotations

from langchain_core.tools import tool
from typing import Annotated, Dict
from processdesignagents.sizing_tools.interface import equipment_sizing

@tool
def size_pump_basic(
    pump_data: Annotated[Dict, {}],
    stream_in: Annotated[Dict, {}],
    stream_out: Annotated[Dict, {}]
) -> str:
    """
    Sizing the basic heat exchanger.
    Agrs:
        pump_data (Dict): the information of pump extracted from equipment list
        stream_in (Dict): process stream in data
        stream_out (Dict): process stream out data
    Returns:
        str: An update equipment sizing in JSON format.
    """
    return equipment_sizing("pump_sizing", pump_data, stream_in, stream_out)
