from __future__ import annotations

import json
from json_repair import repair_json
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

from processdesignagents.agents.designer.tools import (
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

from processdesignagents.agents.utils.agent_states import DesignState, create_design_state
from processdesignagents.agents.utils.prompt_utils import jinja_raw
from processdesignagents.agents.utils.equipment_stream_markdown import equipments_and_streams_dict_to_markdown

from processdesignagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openrouter"
config["quick_think_llm"] = "openai/gpt-5-nano"
config["deep_think_llm"] = "openai/gpt-5-nano"

# config["quick_think_llm"] = "google/gemini-2.5-flash-lite-preview-09-2025"

config["quick_think_llm"] = "x-ai/grok-4-fast"

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
        equipment_stream_template = temp_data.get("equipment_and_stream_template", "{}")
        equipment_stream_list_str = temp_data.get("equipment_and_stream_list", "{}")
        
        es_template = json.loads(equipment_stream_template)
        stream_template = {"streams": es_template["streams"] if "streams" in es_template else []}
        
        # ---
        # Actual workflow start from here
        # ---

        tools_list = [
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
        ]
        
        # Create tools list to be called by agent
        # The tool map will be used to look up and invoke the correct tool by name.
        tool_map = {tool.name: tool for tool in tools_list}
        
        # Create agent prompt
        _, system_content, human_content = stream_calculation_prompt_with_tools(
            design_basis=design_basis_md,
            basic_pfd_description=basic_pfd_md,
            stream_list_template=json.dumps(stream_template),
        )
        
        # Create agent with tools list
        agent = create_agent(
            model=quick_thinking_llm,
            system_prompt=system_content,
            tools=tools_list,
        )
        
        # --- Agent Invocation Loop ---
        # A ReAct agent works iteratively. We need to manage the conversation
        # by invoking the agent, checking for tool calls, executing them,
        # and feeding the results back until the agent provides a final answer.
        
        # Start the conversation with the initial user prompt
        conversation_history: List[BaseMessage] = [{"role": "user", "content": human_content}]
        
        # Limit iterations to prevent infinite loops
        max_iterations = 15 
        for i in range(max_iterations):
            print(f"\n--- Iteration {i + 1}/{max_iterations} ---", flush=True)
            
            # Invoke the agent with the current conversation history
            result = agent.invoke({"messages": conversation_history})
            
            # The agent's response is the last message in the output
            ai_message: AIMessage = result['messages'][-1]
            
            # Add the AI's response to our history
            conversation_history.append(ai_message)
            
            # Check if the agent made any tool calls
            if not ai_message.tool_calls:
                print("\nAgent finished. Final answer received.", flush=True)
                # If no tool calls, the agent has provided its final answer.
                # Extract the JSON content from the final message.
                final_json_str = repair_json(ai_message.content)
                print("\n--- Final Stream Table (JSON) ---", flush=True)
                print(final_json_str, flush=True)
                
                # Convert to Markdown for display
                final_stream_list = json.loads(final_json_str)
                _, _, streams_md = equipments_and_streams_dict_to_markdown(final_stream_list)
                print("\n--- Final Stream Table (Markdown) ---", flush=True)
                print(streams_md, flush=True)
                break # Exit the loop

            # If there are tool calls, execute them
            print(f"Agent requested {len(ai_message.tool_calls)} tool call(s)...", flush=True)
            for tool_call in ai_message.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                print(f"  - Calling tool: {tool_name} with args: {tool_args}", flush=True)
                
                # Find and run the corresponding tool
                if tool_name in tool_map:
                    tool_result = tool_map[tool_name].invoke(tool_args)
                    # Add the tool's result to the conversation history for the agent's next turn
                    conversation_history.append(ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"]))
        

def stream_calculation_prompt_with_tools(
    design_basis: str,
    basic_pfd_description: str,
    stream_list_template: str,
) -> Tuple[ChatPromptTemplate, str, str]:
    """
    Creates system and human prompts for generating a stream table using calculation tools.

    Args:
        design_basis: Text describing the overall design parameters (feed, products, utilities).
        basic_pfd_description: Text describing the sequence of unit operations.
        stream_list_template: JSON template string for the desired output structure.

    Returns:
        Tuple containing:
            - ChatPromptTemplate object for LangChain.
            - The generated system prompt string.
            - The generated human prompt string.
    """

    # Define the tools based on the stream_tools_coolprop.py file provided
    # Descriptions are derived from the function docstrings
    system_content = f"""
<?xml version="1.0" encoding="UTF-8"?>
<agent>
  <metadata>
    <role>Process Simulation Engineer</role>
    <specialization>Heat and Material Balance Generation</specialization>
    <function>Develop a complete and consistent stream table based on process description and design basis using calculation tools.</function>
    <deliverable>Validated stream table in JSON format adhering strictly to the provided template.</deliverable>
    <project_phase>Conceptual Design / Basic Engineering - H&MB Development Phase</project_phase>
  </metadata>

  <context>
    <tool_environment>Python-based stream property and balance calculation tools (using CoolProp)</tool_environment>
    <available_tools>
      <!-- Property Calculation Tools -->
      <tool name="calculate_molar_flow_from_mass">
        <description>Calculates molar flow (kmol/h) and average MW (kg/kmol) from mass flow (kg/h) and composition (molar or mass fractions).</description>
        <inputs>
          <input name="mass_flow_kg_h" type="float">Mass flow rate in kg/h.</input>
          <input name="compositions" type="dict">Composition dict (molar or mass fractions).</input>
          <input name="composition_type" type="string" default="molar">"molar" or "mass".</input>
        </inputs>
        <outputs>
          <output name="molar_flow_kmol_h" type="float"></output>
          <output name="average_mw_kg_kmol" type="float"></output>
        </outputs>
      </tool>
      <tool name="calculate_mass_flow_from_molar">
        <description>Calculates mass flow (kg/h) and average MW (kg/kmol) from molar flow (kmol/h) and composition (molar or mass fractions).</description>
        <inputs>
          <input name="molar_flow_kmol_h" type="float">Molar flow rate in kmol/h.</input>
          <input name="compositions" type="dict">Composition dict (molar or mass fractions).</input>
          <input name="composition_type" type="string" default="molar">"molar" or "mass".</input>
        </inputs>
        <outputs>
          <output name="mass_flow_kg_h" type="float"></output>
          <output name="average_mw_kg_kmol" type="float"></output>
        </outputs>
      </tool>
      <tool name="convert_compositions">
        <description>Converts between molar and mass fraction dictionaries using CoolProp MWs. Returns a dict containing BOTH original and converted fractions.</description>
        <inputs>
          <input name="compositions" type="dict">Input composition dict.</input>
          <input name="input_type" type="string">"molar" or "mass".</input>
          <input name="output_type" type="string">"molar" or "mass".</input>
        </inputs>
        <outputs>
          <output name="combined_compositions" type="dict">Dict with original and converted fractions.</output>
        </outputs>
      </tool>
      <tool name="calculate_volume_flow">
        <description>Calculates volume flow rate (m³/h) from mass flow rate (kg/h) and density (kg/m³).</description>
        <inputs>
          <input name="mass_flow_kg_h" type="float"></input>
          <input name="density_kg_m3" type="float"></input>
        </inputs>
        <outputs>
          <output name="volume_flow_m3_h" type="float"></output>
        </outputs>
      </tool>
      <tool name="get_physical_properties">
        <description>Looks up physical properties (density, cp, viscosity, phase, molecular_weight) for a mixture using CoolProp.</description>
        <inputs>
          <input name="components" type="list[str]">List of component names (e.g., ["Ethanol", "Water"]).</input>
          <input name="mole_fractions" type="list[float]">List of mole fractions (must sum to 1.0).</input>
          <input name="temperature_c" type="float">Temperature in °C.</input>
          <input name="pressure_barg" type="float">Pressure in barg.</input>
          <input name="properties_needed" type="list[str]">List of properties (e.g., ["density", "cp", "phase", "molecular_weight"]).</input>
        </inputs>
        <outputs>
          <output name="properties" type="dict">Dict of calculated properties with values and units.</output>
          <output name="notes" type="string">Calculation notes, including any errors.</output>
        </outputs>
      </tool>

      <!-- Mass Balance Tools -->
      <tool name="perform_mass_balance_split">
        <description>Calculates outlet mass flows (kg/h) for a stream splitter.</description>
        <inputs>
          <input name="inlet_mass_flow_kg_h" type="float">Inlet mass flow.</input>
          <input name="split_fractions" type="list[float]">List of outlet fractions (summing to 1.0).</input>
          <input name="outlet_stream_ids" type="list[str]">List of corresponding outlet stream IDs.</input>
        </inputs>
        <outputs>
          <output name="outlet_flows" type="dict">Dict mapping outlet_stream_ids to calculated mass flows.</output>
        </outputs>
      </tool>
      <tool name="perform_mass_balance_mix">
        <description>Calculates the outlet mass flow (kg/h) for a stream mixer.</description>
        <inputs>
          <input name="inlet_mass_flows_kg_h" type="dict">Dict mapping inlet stream IDs to mass flows.</input>
        </inputs>
        <outputs>
          <output name="outlet_mass_flow_kg_h" type="float"></output>
        </outputs>
      </tool>

      <!-- Energy Balance Tools -->
      <tool name="perform_energy_balance_mix">
        <description>Calculates the outlet temperature (°C) for an adiabatic mixer, assuming constant Cp.</description>
        <inputs>
          <input name="inlet_flows_temps" type="dict">Dict mapping inlet stream IDs to {{"mass_flow": kg/h, "temp": °C}}.</input>
          <input name="outlet_mass_flow_kg_h" type="float">Total outlet mass flow (kg/h).</input>
          <input name="specific_heat_kj_kg_k" type="float">Average mixture specific heat (kJ/kg-K).</input>
        </inputs>
        <outputs>
          <output name="outlet_temperature_c" type="float"></output>
        </outputs>
      </tool>
      <tool name="calculate_heat_exchanger_outlet_temp">
        <description>Calculates HEX outlet temperature (°C) given duty (kW), flow (kg/h), Cp (kJ/kg-K), and inlet temp (°C). Positive duty heats, negative duty cools.</description>
        <inputs>
          <input name="duty_kw" type="float">Duty (+ for heating, - for cooling).</input>
          <input name="mass_flow_kg_h" type="float"></input>
          <input name="specific_heat_kj_kg_k" type="float"></input>
          <input name="inlet_temp_c" type="float"></input>
        </inputs>
        <outputs>
          <output name="outlet_temperature_c" type="float"></output>
        </outputs>
      </tool>
      <tool name="calculate_heat_exchanger_duty">
        <description>Calculates HEX duty (kW) given flow (kg/h), Cp (kJ/kg-K), inlet temp (°C), and outlet temp (°C). Positive duty for heating, negative for cooling.</description>
        <inputs>
          <input name="mass_flow_kg_h" type="float"></input>
          <input name="specific_heat_kj_kg_k" type="float"></input>
          <input name="inlet_temp_c" type="float"></input>
          <input name="outlet_temp_c" type="float"></input>
        </inputs>
        <outputs>
          <output name="duty_kw" type="float"></output>
        </outputs>
      </tool>

      <!-- Utility Tool -->
      <tool name="build_stream_object">
        <description>Constructs a single stream object dictionary in the correct JSON format, validating inputs.</description>
        <inputs>
            <input name="stream_id" type="str"></input>
            <input name="name" type="str"></input>
            <input name="description" type="str"></input>
            <input name="from_unit" type="str"></input>
            <input name="to_unit" type="str"></input>
            <input name="phase" type="str">"Liquid", "Vapor", "TwoPhase", etc.</input>
            <input name="mass_flow_kg_h" type="float" optional="true"></input>
            <input name="molar_flow_kmol_h" type="float" optional="true"></input>
            <input name="temperature_c" type="float" optional="true"></input>
            <input name="pressure_barg" type="float" optional="true"></input>
            <input name="volume_flow_m3_h" type="float" optional="true"></input>
            <input name="density_kg_m3" type="float" optional="true"></input>
            <input name="compositions" type="dict" optional="true">Should contain both molar and mass fractions.</input>
            <input name="notes" type="str" optional="true"></input>
        </inputs>
        <outputs>
          <output name="stream_json" type="string">JSON string of the single stream object, or JSON with an error key.</output>
        </outputs>
      </tool>
    </available_tools>
    <inputs_to_agent>
      <input name="design_basis" format="text">Overall design parameters (feed, products, utilities).</input>
      <input name="basic_pfd_description" format="text">Sequence of unit operations.</input>
      <input name="stream_list_template" format="json">JSON structure for the final output (contains 'streams' list).</input>
    </inputs_to_agent>
    <purpose>Generate a complete, consistent stream table by calculating unknown stream properties based on known inputs and process flow, using the available tools.</purpose>
    <downstream_users>
      <user>Equipment Sizing Engineers</user>
      <user>Process Control Engineers</user>
      <user>Safety Engineers (for relief calculations)</user>
      <user>Cost Estimation Teams</user>
    </downstream_users>
  </context>

  <instructions>
    <instruction id="1">
      <title>Understand the Process Flow and Design Basis</title>
      <details>
        - Read the `basic_pfd_description` to understand the sequence of equipment (e.g., Feed -> Splitter -> E-101 -> Mixer -> P-101 -> Product).
        - Read the `design_basis` to identify known feed conditions (flow, T, P, composition), product specifications (T, P, composition), utility conditions (e.g., CW T_in, T_out), and key operational targets (e.g., final product temperature).
        - Identify all streams mentioned implicitly or explicitly in the description and design basis. Assign preliminary IDs if needed.
      </details>
    </instruction>

    <instruction id="2">
      <title>Initialize Known Streams</title>
      <details>
        - For each feed stream and utility stream identified in the design basis, gather all known properties (flow, T, P, composition).
        - If composition is given in only one basis (molar or mass), use `convert_compositions` tool to calculate the other basis. Ensure the `compositions` dictionary contains BOTH molar (e.g., "Ethanol") and mass (e.g., "m_Ethanol") fractions.
        - If mass flow and composition are known, use `calculate_molar_flow_from_mass` to find molar flow.
        - If molar flow and composition are known, use `calculate_mass_flow_from_molar` to find mass flow.
        - Use `get_physical_properties` to find density, phase, and Cp at the known T and P. Use ["density", "cp", "phase", "molecular_weight"] as `properties_needed`. Verify the phase reported by CoolProp matches expectations.
        - Once density is known, use `calculate_volume_flow` if mass flow is known.
        - Use the `build_stream_object` tool to create the complete JSON object for each known stream. Add detailed notes explaining the source of the data (e.g., "From Design Basis", "Calculated using CoolProp"). Keep track of these completed stream objects.
      </details>
    </instruction>

    <instruction id="3">
      <title>Calculate Streams Unit by Unit (Iterative Process)</title>
      <details>
        - Follow the equipment sequence from the `basic_pfd_description`.
        - For each unit operation:
          * **Identify Inputs/Outputs:** Determine the ID(s) of the stream(s) entering and leaving the unit.
          * **Gather Known Input Data:** Retrieve the full data for the input stream(s) calculated previously.
          * **Apply Balances & Unit Logic:**
            - **Splitter:** Use `perform_mass_balance_split` with specified fractions (from description or assumed). Outlet T, P, composition, phase are usually identical to inlet. Create outlet streams.
            - **Mixer:** Use `perform_mass_balance_mix`. Outlet composition is a flow-weighted average of inlet compositions (calculate this manually/logically first). Use `get_physical_properties` to estimate outlet Cp. Use `perform_energy_balance_mix` to find outlet T (assume adiabatic). Outlet P is typically the lowest inlet P unless specified otherwise. Create outlet stream.
            - **Pump:** Outlet mass flow and composition = inlet. Outlet P is specified in design basis or downstream requirement. Assume outlet T = inlet T (or add a small rise like 1-2°C if high pressure). Create outlet stream.
            - **Compressor:** Outlet mass flow and composition = inlet. Outlet P is specified. Calculate outlet T using polytropic assumptions (or use a dedicated compressor tool if available, not listed here). Pressure/temp rise affects density/phase. Create outlet stream.
            - **Heat Exchanger:** One stream's T_out or the duty is usually the target.
                - If T_in, T_out known for one stream: Use `get_physical_properties` for its Cp, then `calculate_heat_exchanger_duty`.
                - Apply the negative of this duty to the other stream. Use `get_physical_properties` for the second stream's Cp, then use `calculate_heat_exchanger_outlet_temp` to find its T_out.
                - Assume reasonable pressure drops (e.g., 0.1-0.5 bar) if not given. Create outlet streams.
            - **Reactor/Separator:** Apply specified conversions, yields, or separation factors to calculate outlet flows and compositions from inlet(s). Perform mass and energy balances. Create outlet streams.
          * **Calculate Properties for New Streams:** For each *newly calculated* outlet stream:
            - Ensure composition dict has both molar and mass fractions (use `convert_compositions` if needed).
            - Calculate molar/mass flow using `calculate_molar_flow_from_mass` / `calculate_mass_flow_from_molar`.
            - Use `get_physical_properties` with the calculated T, P, and composition to find density, phase, Cp, etc.
            - Use `calculate_volume_flow`.
          * **Document Calculations:** Add detailed notes to each new stream using `build_stream_object`, explaining how each property was determined (e.g., "Outlet T from E-101 energy balance", "Density from CoolProp at stream T, P", "Mass flow from mixer mass balance", "Composition assumed same as inlet Stream XXX"). State ALL assumptions (e.g., "Assumed Cp = 4.18 kJ/kgK", "Assumed 0.2 bar pressure drop").
          * **Build and Store:** Use `build_stream_object` to format the new stream and store it.
      </details>
    </instruction>

     <instruction id="4">
      <title>Verify Consistency and Iterate if Necessary</title>
      <details>
        - After calculating all streams, perform consistency checks:
          * **Overall Mass Balance:** Does total mass in (feeds + utilities consumed) equal total mass out (products + utilities returned + losses)?
          * **Component Mass Balances:** Does mass balance close for each component across the entire process?
          * **Energy Balance:** Does overall energy balance close (approximately, neglecting minor losses)? Check major heat duties.
          * **Specification Check:** Do the final product stream(s) meet the temperature, pressure, and composition specified in the design basis?
        - If inconsistencies are found or specifications are not met (e.g., final mixed temperature is off target), identify the assumptions or calculation steps that need adjustment (e.g., heat exchanger duty, bypass split fraction).
        - **Iterate:** Go back to the relevant unit operation calculation, adjust the assumption (clearly stating the change in the notes), and recalculate downstream streams. Repeat verification.
      </details>
    </instruction>

    <instruction id="5">
      <title>Final Formatting and Output</title>
      <details>
        - Assemble all the generated stream objects (JSON strings from `build_stream_object`) into a final list.
        - Create the final JSON output object with a single top-level key "streams" containing this list.
        - Ensure the final output strictly adheres to the structure provided in the `stream_list_template`.
        - Make sure all numerical values are represented as floats (e.g., 50.0, not 50).
        - Ensure all strings use double quotes.
        - **Output ONLY the final, validated JSON object. Do not include any explanation, preamble, markdown formatting, or code fences (```).**
      </details>
    </instruction>
  </instructions>

  <output_schema>
    <description>A single JSON object containing a list named "streams". Each item in the list must conform exactly to the structure provided in the input `stream_list_template`.</description>
    <example>
      ```json
      {{
        "streams": [
          {{
            "id": "1001",
            "name": "Hot Feed",
            "description": "...",
            "from": "...",
            "to": "...",
            "phase": "Liquid",
            "properties": {{
              "mass_flow": {{"value": 1000.0, "unit": "kg/h"}},
              "molar_flow": {{"value": 21.7, "unit": "kmol/h"}},
              "temperature": {{"value": 95.0, "unit": "°C"}},
              "pressure": {{"value": 1.2, "unit": "barg"}},
              "volume_flow": {{"value": 1.25, "unit": "m³/h"}},
              "density": {{"value": 800.0, "unit": "kg/m³"}}
            }},
            "compositions": {{
              "Ethanol": {{"value": 0.9, "unit": "molar fraction"}},
              "Water": {{"value": 0.1, "unit": "molar fraction"}},
              "m_Ethanol": {{"value": 0.957, "unit": "mass fraction"}},
              "m_Water": {{"value": 0.043, "unit": "mass fraction"}}
            }},
            "notes": "Feed stream from design basis. Molar flow calculated. Density from CoolProp. Mass fractions calculated."
          }},
          {{ ... more stream objects ... }}
        ]
      }}
      ```
    </example>
    <critical_rules>
        <rule>Output must be a single, valid JSON object starting with `{{` and ending with `}}`.</rule>
        <rule>The root object must have ONLY ONE key: "streams".</rule>
        <rule>The value of "streams" must be a JSON list `[...]`.</rule>
        <rule>Each item in the "streams" list must be a JSON object matching the template structure exactly.</rule>
        <rule>All property and composition values must be numeric (float or int), not strings.</rule>
        <rule>All units must be strings as specified in the template.</rule>
        <rule>Both molar and mass fractions must be present in the `compositions` dict for every stream.</rule>
        <rule>Molar fractions must sum to ~1.0. Mass fractions must sum to ~1.0.</rule>
        <rule>The `notes` field for every stream MUST explain how key properties were calculated and list assumptions.</rule>
        <rule>Do NOT include ```json``` or any other markdown/text outside the main JSON object.</rule>
    </critical_rules>
  </output_schema>
</agent>
"""

    human_content = f"""
Generate the complete stream table in JSON format based on the following information. Use the available tools for calculations and property lookups. Adhere strictly to the provided JSON template and instructions, especially regarding documentation in the 'notes' field and outputting ONLY the final JSON object.

**1. Design Basis:**
```text
{design_basis}
```

**2. Basic PFD Description:**
```text
{basic_pfd_description}
```

**3. Stream List JSON Template (Target Structure):**
```json
{stream_list_template}
```

**Output ONLY the final stream list JSON object (no code fences, no additional text).**
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

    # Create the ChatPromptTemplate
    prompt_template = ChatPromptTemplate.from_messages(messages)

    return prompt_template, system_content, human_content

if __name__ == "__main__":
    main()