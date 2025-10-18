from langchain_core.tools import tool
from typing import Annotated, Dict
from processdesignagents.sizing_tools.interface import equipment_sizing

@tool
def size_heat_exchanger_basic(
    heat_exchanger_data: Annotated[Dict, {}],
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
    return equipment_sizing("basic_heat_exchanger_sizing", heat_exchanger_data, hot_stream, cold_stream)
