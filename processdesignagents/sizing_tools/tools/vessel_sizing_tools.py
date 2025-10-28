from __future__ import annotations

from langchain_core.tools import tool
from typing import Annotated, Dict
from processdesignagents.sizing_tools.interface import equipment_sizing

@tool
def size_pressurized_vessel_basic(
    vessel_data: Annotated[Dict, {}],
    stream_in: Annotated[Dict, {}]
) -> str:
    """
    Sizing the basic heat exchanger.
    Agrs:
        vessel_data (Dict): the information of vessel extracted from equipment list
        stream_in (Dict): process stream in data
    Returns:
        str: An update equipment sizing in JSON format.
    """
    return equipment_sizing("pressurized_vessel_sizing", vessel_data, stream_in)
