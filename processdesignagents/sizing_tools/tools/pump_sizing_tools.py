from langchain_core.tools import tool
from typing import Annotated, Dict
from processdesignagents.sizing_tools.interface import equipment_sizing

@tool
def size_pump_basic(
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
    return equipment_sizing("pump_sizing", pump_data, process_stream)
