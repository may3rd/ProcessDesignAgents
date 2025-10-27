import json
import os
from typing import Annotated, Dict, Any, List, Optional, Union, Tuple

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage

# Using create_agent in langchain 1.0
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware

# Import equipment sizing tools
from processdesignagents.agents.utils.agent_sizing_tools import (
    size_heat_exchanger_basic,
    size_pump_basic
)

from processdesignagents.agents.utils.agent_states import DesignState, create_design_state
from processdesignagents.agents.utils.prompt_utils import jinja_raw
from processdesignagents.agents.utils.json_tools import (
    extract_first_json_document,
)
from processdesignagents.agents.utils.equipment_stream_markdown import equipments_and_streams_dict_to_markdown

from processdesignagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openrouter"
config["quick_think_llm"] = "openai/gpt-5-nano"
config["deep_think_llm"] = "openai/gpt-5-nano"

config["quick_think_llm"] = "google/gemini-2.5-flash-lite-preview-09-2025"

def main():
    if config["llm_provider"].lower() == "openrouter":
        base_url = "https://openrouter.ai/api/v1"
        api_key = os.getenv("OPENROUTER_API_KEY")
        deep_thinking_llm = ChatOpenAI(model=config["deep_think_llm"], base_url=base_url, api_key=api_key)
        quick_thinking_llm = ChatOpenAI(model=config["quick_think_llm"], base_url=base_url, api_key=api_key)

        quick_thinking_llm.temperature = 0.5
        deep_thinking_llm.temperature = 0.5
        
        # Load example data
        with open("eval_results/ProcessDesignAgents_logs/full_states_log.json", "r") as f:
            temp_data = json.load(f)
        
        # temp_data: Dict[str, Any]= json.load("eval_results/ProcessDesignAgents_logs/full_states_log.json")
        requirement_md = temp_data.get("requirements", "")
        design_basis_md = temp_data.get("design_basis", "")
        basic_pfd_md = temp_data.get("basic_pfd", "")
        equipment_stream_list_str = temp_data.get("equipment_and_stream_list", "")
        
        # Adapt agent_state
        state = create_design_state(
            requirements=requirement_md,
            design_basis=design_basis_md,
            basic_pfd=basic_pfd_md,
            equipment_and_stream_list=equipment_stream_list_str,
        )
        
        # Todo: implement below logit to agents/designers/equipment_sizing_agent.py
        equipment_category_set = set()  # define as set
        equipment_stream_list_dict = json.loads(equipment_stream_list_str)
        
        if "equipments" in equipment_stream_list_dict:
            # Get the equipment list from master dict
            equipment_list = equipment_stream_list_dict["equipments"]
            
            # Loop throught equipment list
            for eq in equipment_list:
                equipment_category_set.add(eq.get("category", ""))
                
            equipment_category_names = list(equipment_category_set)
            
            print(equipment_category_names)
            
            equipment_category = [
                {
                    "name": name,
                    "ids": [eq.get("id", "") for eq in equipment_list if eq.get("category", "") == name]
                }
                for name in equipment_category_names
            ]
            
            for cat in equipment_category:
                print(cat)
        else:
            raise ValueError("Equipments not found")
        
        # Tools
        tools_list = [
            size_heat_exchanger_basic,
            size_pump_basic,
        ]
        
        _, system_content, human_content = equipment_sizing_prompt_with_tools(
            equipment_and_stream_list=equipment_stream_list_str,
        )
        
        agent = create_agent(
            model=quick_thinking_llm,
            system_prompt=system_content,
            tools=tools_list,
        )
        
        results = agent.invoke({"messages" : [{"role": "user", "content": human_content}]})
        
        ai_message = results['messages'][-1]
        print(ai_message.content)
        
        combined_md, equipment_md, streams_md = equipments_and_streams_dict_to_markdown(json.loads(ai_message.content))
        print(equipment_md)
        

def equipment_sizing_prompt_with_tools(
    equipment_and_stream_list: str,
) -> ChatPromptTemplate:
    """Create prompt with pre-computed tool results"""
    
    system_content = f"""
You are a **Lead Equipment Sizing Engineer** responsible for finalizing equipment specifications using automated sizing tools.

**Context:**

  * You have access to sizing calculations tools (heat exchangers, pumps, vessels, compressors).
  * Your task is to use these tools to fill in the missing values in the final equipment specification JSON, adding engineering judgment and filling gaps where tools could not be applied.
  * I want the equipment list with the upadte sizing_parameter of the equipment provided from user.
  
**Tool Available:** `size_heat_exchanger_basic`, `size_pump_basic`, `size_vessel_basic`, `size_compressor_basic`.

**Instructions:**

  1. **Use Sizing Tool:** to calculate the equipment specification values.
  
  2. **Populate Sizing Parameters:** Use tool results to fill the `sizing_parameters` array. For example:
     - Heat Exchanger: ["Area: <area_m2> m²", "LMTD: <lmtd_C> °C", "U: <U_design_W_m2K> W/m²·K"]
     - Pump: ["Flow: <flow_m3_hr> m³/h", "Head: <total_head_m> m", "Power: <motor_rating_kW> kW"]
     - Vessel: ["Diameter: <diameter_mm> mm", "Length: <length_mm> mm", "Thickness: <shell_thickness_mm> mm"]
     - Compressor: ["Stages: <number_of_stages>", "Power: <driver_rating_kW> kW", "Discharge Temp: <discharge_temperature_C> °C"]
  
  3. **Update Duty/Load Field:** Replace placeholder values with calculated duties (e.g., "21.7 MW" for heat exchanger, "45 kW" for pump motor).
  
  4. **Document in Notes:** Reference the tool used and key assumptions. Example: "Sized using heat_exchanger_sizing tool with LMTD method. U-value estimated at 850 W/m²·K for hydrocarbon/water service."
  
  5. **Handle Missing Tool Results:** For equipment without tool results (columns, special equipment), use engineering judgment and the stream data to provide reasonable estimates or mark as "TBD".
  
  6. **Update Assumptions:** Add any new global assumptions to `metadata.assumptions`, such as "All pump efficiencies assumed at 75% unless specified."

  7. **Maintain JSON Structure:** Output ONLY a valid JSON object matching the equipment template schema. Do NOT use code fences.
  
  8. **Update the Equipment List:** Use the results from the tool to update the equipment list.

**Critical Rules:**

  - All numeric values must have units
  - Round to appropriate precision (areas to 0.1 m², power to nearest kW)
  - Reference tool usage in notes for traceability
  - If tool result contains "error", note the issue and provide manual estimate or "TBD"
  - **Output ONLY the final equipment list JSON object (no code fences, no additional text).**
"""

    human_content = f"""
Based on the equipment and stream list below, using tools provided to calculate and update the equipment list.

**Output ONLY the final equipment list with updated sizing parameters (JSON): object (no code fences, no additional text).**

**Equipment and Stream Data (JSON):**
{equipment_and_stream_list}
"""

    messages = [
        SystemMessagePromptTemplate.from_template(
            jinja_raw(system_content),
            template_format="jinja2",
        ),
        HumanMessagePromptTemplate.from_template(
            jinja_raw(human_content),
            template_format="jinja2",
        ),
    ]

    return ChatPromptTemplate.from_messages(messages), system_content, human_content


if __name__ == "__main__":
    main()
