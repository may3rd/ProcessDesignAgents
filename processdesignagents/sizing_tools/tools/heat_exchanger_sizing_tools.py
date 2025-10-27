from langchain_core.tools import tool
from typing import Annotated, Dict
from processdesignagents.sizing_tools.interface import equipment_sizing

@tool
def size_heat_exchanger_basic(
    heat_exchanger_data: Annotated[Dict, {}],
    hot_stream_in: Annotated[Dict, {}],
    hot_stream_out: Annotated[Dict, {}],
    cold_stream_in: Annotated[Dict, {}],
    cold_stream_out: Annotated[Dict, {}]
) -> str:
    """
    Sizing the basic heat exchanger.
    Agrs:
        basic_heat_exchanger_sizing (Dict): the information of heat exchanger extracted from equipment list
        hot_stream_in (Dict): hot stream in data
        hot_stream_out (Dict): hot stream out data
        cold_stream_in (Dict): cold stream in data
        cold_stream_out (Dict): cold stream out
    Returns:
        str: An update equipment sizing in JSON format.
    """
    return equipment_sizing(
        "basic_heat_exchanger_sizing",
            heat_exchanger_data, hot_stream_in, hot_stream_out,
            cold_stream_in, cold_stream_out
        )

@tool
def size_shell_and_tube_heat_exchanger(
    heat_exchanger_data: Annotated[Dict, {}],
    hot_stream_in: Annotated[Dict, {}],
    hot_stream_out: Annotated[Dict, {}],
    cold_stream_in: Annotated[Dict, {}],
    cold_stream_out: Annotated[Dict, {}]
) -> str:
    """
    Sizing the shell and tube heat exchanger.
    Sizing the basic heat exchanger.
    Agrs:
        basic_heat_exchanger_sizing (Dict): the information of heat exchanger extracted from equipment list
        hot_stream_in (Dict): hot stream in data
        hot_stream_out (Dict): hot stream out data
        cold_stream_in (Dict): cold stream in data
        cold_stream_out (Dict): cold stream out
    Returns:
        str: An update equipment sizing in JSON format.
    """
    return equipment_sizing(
        "shell_and_tubu_heat_exchanger_sizing",
            heat_exchanger_data, hot_stream_in, hot_stream_out,
            cold_stream_in, cold_stream_out
        )
