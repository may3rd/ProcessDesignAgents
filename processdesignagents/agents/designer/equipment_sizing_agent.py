from __future__ import annotations

import json
import re
from typing import Dict, List, Any, Optional

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_core.tools import tool

from dotenv import load_dotenv

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import jinja_raw
from processdesignagents.agents.utils.json_tools import (
    convert_streams_json_to_markdown,
    convert_equipment_json_to_markdown,
    extract_first_json_document,
)

load_dotenv()


# ============================================================================
# TOOL DEFINITIONS (Based on Your Sizing Prompts)
# ============================================================================

@tool
def size_heat_exchanger(
    duty_kW: float,
    hot_inlet_temp_C: float,
    hot_outlet_temp_C: float,
    cold_inlet_temp_C: float,
    cold_outlet_temp_C: float,
    hot_fluid: str = "process fluid",
    cold_fluid: str = "cooling water",
    flow_arrangement: str = "countercurrent",
    fouling_allowance: float = 0.0002
) -> Dict[str, Any]:
    """
    Size a shell-and-tube heat exchanger using LMTD method.
    
    Args:
        duty_kW: Heat duty in kW
        hot_inlet_temp_C: Hot side inlet temperature (°C)
        hot_outlet_temp_C: Hot side outlet temperature (°C)
        cold_inlet_temp_C: Cold side inlet temperature (°C)
        cold_outlet_temp_C: Cold side outlet temperature (°C)
        hot_fluid: Type of hot fluid (for U estimation)
        cold_fluid: Type of cold fluid (for U estimation)
        flow_arrangement: "countercurrent" or "cocurrent" or "1-2"
        fouling_allowance: Fouling factor (m²·K/W)
    
    Returns:
        Dictionary with area, LMTD, U_clean, U_design
    """
    # LMTD Calculation
    dt1 = hot_inlet_temp_C - cold_outlet_temp_C
    dt2 = hot_outlet_temp_C - cold_inlet_temp_C
    
    if dt1 <= 0 or dt2 <= 0:
        return {"error": "Temperature cross detected - invalid configuration"}
    
    if abs(dt1 - dt2) < 0.1:
        lmtd = (dt1 + dt2) / 2
    else:
        lmtd = (dt1 - dt2) / (abs(dt1 / dt2) if dt2 != 0 else 1e-6)
        lmtd = abs(lmtd) if lmtd > 0 else 1.0
    
    # Correction factor for 1-2 shell-and-tube
    F_correction = 0.95 if flow_arrangement == "1-2" else 1.0
    lmtd_corrected = lmtd * F_correction
    
    # Estimate U (W/m²·K) based on fluid types
    U_clean = estimate_U_value(hot_fluid, cold_fluid)
    U_design = 1 / (1/U_clean + fouling_allowance * 1000)  # Convert to W/m²·K
    
    # Area calculation
    duty_W = duty_kW * 1000
    area_m2 = duty_W / (U_design * lmtd_corrected)
    
    return {
        "area_m2": round(area_m2, 1),
        "area_ft2": round(area_m2 * 10.764, 1),
        "lmtd_C": round(lmtd, 1),
        "lmtd_corrected_C": round(lmtd_corrected, 1),
        "U_clean_W_m2K": U_clean,
        "U_design_W_m2K": round(U_design, 0),
        "F_correction": F_correction
    }


@tool
def size_pump(
    flow_kg_hr: float,
    density_kg_m3: float,
    suction_pressure_bara: float,
    discharge_pressure_bara: float,
    static_head_m: float = 0,
    efficiency: float = 0.75
) -> Dict[str, Any]:
    """
    Size a centrifugal pump.
    
    Args:
        flow_kg_hr: Mass flow rate (kg/hr)
        density_kg_m3: Fluid density (kg/m³)
        suction_pressure_bara: Suction pressure (bara)
        discharge_pressure_bara: Discharge pressure (bara)
        static_head_m: Elevation difference (m)
        efficiency: Pump efficiency (0-1)
    
    Returns:
        Dictionary with power, head, flow_m3hr
    """
    # Convert to volumetric flow
    flow_m3_hr = flow_kg_hr / density_kg_m3
    flow_m3_s = flow_m3_hr / 3600
    
    # Calculate differential head
    pressure_head_m = ((discharge_pressure_bara - suction_pressure_bara) * 1e5) / (density_kg_m3 * 9.81)
    total_head_m = pressure_head_m + static_head_m
    
    # Brake power
    brake_power_kW = (flow_m3_s * density_kg_m3 * 9.81 * total_head_m) / (efficiency * 1000)
    
    # Motor sizing with service factor
    service_factor = 1.15
    motor_power_kW = brake_power_kW * service_factor
    
    # Round to standard motor sizes
    standard_sizes = [0.75, 1.1, 1.5, 2.2, 3, 4, 5.5, 7.5, 11, 15, 18.5, 22, 30, 37, 45, 55, 75, 90, 110, 132, 160, 200]
    motor_rating_kW = min([s for s in standard_sizes if s >= motor_power_kW], default=motor_power_kW)
    
    return {
        "flow_m3_hr": round(flow_m3_hr, 1),
        "total_head_m": round(total_head_m, 1),
        "brake_power_kW": round(brake_power_kW, 2),
        "motor_rating_kW": motor_rating_kW,
        "motor_rating_HP": round(motor_rating_kW * 1.341, 1),
        "efficiency_percent": efficiency * 100
    }


@tool
def size_vessel(
    volume_m3: float,
    design_pressure_bara: float,
    design_temperature_C: float,
    orientation: str = "vertical",
    L_D_ratio: float = 3.0,
    corrosion_allowance_mm: float = 3.0,
    material: str = "carbon steel"
) -> Dict[str, Any]:
    """
    Size a pressure vessel per ASME Section VIII.
    
    Args:
        volume_m3: Required volume (m³)
        design_pressure_bara: Design pressure (bara)
        design_temperature_C: Design temperature (°C)
        orientation: "vertical" or "horizontal"
        L_D_ratio: Length to diameter ratio
        corrosion_allowance_mm: Corrosion allowance (mm)
        material: Vessel material
    
    Returns:
        Dictionary with dimensions, thickness, weight
    """
    import math
    
    # Material allowable stress (simplified)
    S_MPa = 138 if design_temperature_C < 200 else 120
    E = 0.85  # Joint efficiency (spot RT)
    
    # Calculate diameter
    # Volume = π/4 × D² × L (for cylindrical section)
    # Assume 2:1 elliptical heads add ~15% volume
    effective_volume = volume_m3 / 1.15
    D_m = (4 * effective_volume / (math.pi * L_D_ratio)) ** (1/3)
    L_m = L_D_ratio * D_m
    
    # Shell thickness (ASME UG-27)
    P_MPa = (design_pressure_bara - 1.01325) * 0.1  # Convert to MPa gauge
    R_m = D_m / 2
    t_mm = (P_MPa * R_m * 1000) / (S_MPa * E - 0.6 * P_MPa) + corrosion_allowance_mm
    
    # Minimum thickness check
    t_min_mm = 6 if D_m < 0.9 else (8 if D_m < 1.5 else 10)
    t_mm = max(t_mm, t_min_mm)
    
    # Weight estimation (rough)
    shell_weight_kg = math.pi * D_m * L_m * (t_mm / 1000) * 7850
    head_weight_kg = 2 * 0.5 * math.pi * (D_m ** 2) * (t_mm / 1000) * 7850
    total_weight_kg = (shell_weight_kg + head_weight_kg) * 1.15  # Add 15% for nozzles
    
    return {
        "diameter_mm": round(D_m * 1000, 0),
        "diameter_inches": round(D_m * 39.37, 1),
        "length_mm": round(L_m * 1000, 0),
        "shell_thickness_mm": round(t_mm, 1),
        "empty_weight_kg": round(total_weight_kg, 0),
        "L_D_ratio": round(L_D_ratio, 1)
    }


@tool
def size_compressor(
    mass_flow_kg_hr: float,
    suction_pressure_bara: float,
    discharge_pressure_bara: float,
    suction_temp_C: float,
    molecular_weight: float,
    k_ratio: float = 1.4,
    polytropic_efficiency: float = 0.78
) -> Dict[str, Any]:
    """
    Size a centrifugal compressor.
    
    Args:
        mass_flow_kg_hr: Mass flow rate (kg/hr)
        suction_pressure_bara: Suction pressure (bara)
        discharge_pressure_bara: Discharge pressure (bara)
        suction_temp_C: Suction temperature (°C)
        molecular_weight: Gas molecular weight (kg/kmol)
        k_ratio: Cp/Cv ratio
        polytropic_efficiency: Polytropic efficiency (0-1)
    
    Returns:
        Dictionary with power, stages, discharge temperature
    """
    import math
    
    # Pressure ratio
    r_p = discharge_pressure_bara / suction_pressure_bara
    
    # Estimate stages (limit per-stage ratio to 3.5)
    stages = max(1, math.ceil(math.log(r_p) / math.log(3.5)))
    r_stage = r_p ** (1 / stages)
    
    # Polytropic exponent
    n = k_ratio / ((k_ratio - 1) / polytropic_efficiency + 1)
    
    # Discharge temperature
    T_suction_K = suction_temp_C + 273.15
    T_discharge_K = T_suction_K * (r_p ** ((n - 1) / n))
    T_discharge_C = T_discharge_K - 273.15
    
    # Polytropic head (J/kg)
    R = 8314 / molecular_weight  # Gas constant
    Z_avg = 0.95  # Simplified compressibility
    H_poly = (Z_avg * R * T_suction_K * n / (n - 1)) * ((r_p ** ((n - 1) / n)) - 1)
    
    # Power calculation
    mass_flow_kg_s = mass_flow_kg_hr / 3600
    P_poly_kW = (mass_flow_kg_s * H_poly) / (polytropic_efficiency * 1000)
    
    # Shaft power with mechanical losses
    eta_mech = 0.98
    P_shaft_kW = P_poly_kW / eta_mech
    
    # Driver power with service factor
    service_factor = 1.15
    P_driver_kW = P_shaft_kW * service_factor
    
    return {
        "pressure_ratio": round(r_p, 2),
        "number_of_stages": stages,
        "pressure_ratio_per_stage": round(r_stage, 2),
        "discharge_temperature_C": round(T_discharge_C, 1),
        "polytropic_power_kW": round(P_poly_kW, 0),
        "shaft_power_kW": round(P_shaft_kW, 0),
        "driver_rating_kW": round(P_driver_kW, 0),
        "driver_rating_HP": round(P_driver_kW * 1.341, 0),
        "polytropic_efficiency_percent": polytropic_efficiency * 100
    }


def estimate_U_value(hot_fluid: str, cold_fluid: str) -> float:
    """Estimate overall heat transfer coefficient (W/m²·K)"""
    U_map = {
        ("water", "water"): 1200,
        ("steam", "water"): 1500,
        ("process fluid", "water"): 850,
        ("process fluid", "cooling water"): 850,
        ("hydrocarbon", "water"): 800,
        ("gas", "water"): 300,
        ("condensing vapor", "water"): 1000,
    }
    
    key = (hot_fluid.lower(), cold_fluid.lower())
    return U_map.get(key, 500)  # Default conservative value


# ============================================================================
# TOOL INPUT PREPARATION
# ============================================================================

def prepare_heat_exchanger_inputs(
    equipment: Dict[str, Any],
    stream_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Extract parameters for heat exchanger sizing from equipment spec and streams"""
    
    streams_in = equipment.get("streams_in", [])
    streams_out = equipment.get("streams_out", [])
    
    if len(streams_in) != 2 or len(streams_out) != 2:
        return None
    
    # Find hot and cold streams
    stream_dict = {s["id"]: s for s in stream_data.get("streams", [])}
    
    in_streams = [stream_dict.get(sid) for sid in streams_in if sid in stream_dict]
    out_streams = [stream_dict.get(sid) for sid in streams_out if sid in stream_dict]
    
    if len(in_streams) != 2 or len(out_streams) != 2:
        return None
    
    # Determine hot and cold sides by temperature
    hot_in = max(in_streams, key=lambda s: float(s["properties"]["temperature"]))
    cold_in = min(in_streams, key=lambda s: float(s["properties"]["temperature"]))
    
    hot_out = [s for s in out_streams if s["from"] == hot_in["from"]][0]
    cold_out = [s for s in out_streams if s["from"] == cold_in["from"]][0]
    
    # Extract duty from equipment spec
    duty_str = equipment.get("duty_or_load", "0")
    duty_kW = parse_duty(duty_str)
    
    return {
        "duty_kW": duty_kW,
        "hot_inlet_temp_C": float(hot_in["properties"]["temperature"]),
        "hot_outlet_temp_C": float(hot_out["properties"]["temperature"]),
        "cold_inlet_temp_C": float(cold_in["properties"]["temperature"]),
        "cold_outlet_temp_C": float(cold_out["properties"]["temperature"]),
        "hot_fluid": identify_fluid_type(hot_in),
        "cold_fluid": identify_fluid_type(cold_in),
    }


def prepare_pump_inputs(
    equipment: Dict[str, Any],
    stream_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Extract parameters for pump sizing"""
    
    streams_in = equipment.get("streams_in", [])
    
    if not streams_in:
        return None
    
    stream_dict = {s["id"]: s for s in stream_data.get("streams", [])}
    inlet_stream = stream_dict.get(streams_in[0])
    
    if not inlet_stream:
        return None
    
    # Extract flow and density from stream
    mass_flow = parse_flow(inlet_stream["properties"].get("mass_flow", "0"))
    
    # Estimate density from phase and composition
    density = estimate_density(inlet_stream)
    
    # Extract pressures from key_parameters if available
    params_str = " ".join(equipment.get("key_parameters", []))
    differential_head = extract_number(params_str, r"Differential Head:\s*([\d.]+)\s*bar")
    
    if differential_head is None:
        return None
    
    suction_pressure = float(inlet_stream["properties"]["pressure"])
    discharge_pressure = suction_pressure + differential_head
    
    return {
        "flow_kg_hr": mass_flow,
        "density_kg_m3": density,
        "suction_pressure_bara": suction_pressure,
        "discharge_pressure_bara": discharge_pressure,
        "static_head_m": 0,  # Could be extracted from notes
    }


def prepare_vessel_inputs(
    equipment: Dict[str, Any],
    stream_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Extract parameters for vessel sizing"""
    
    # Extract volume from duty_or_load field
    volume_str = equipment.get("duty_or_load", "")
    volume_m3 = parse_volume(volume_str)
    
    if volume_m3 is None or volume_m3 <= 0:
        return None
    
    # Extract operating pressure from key_parameters
    params_str = " ".join(equipment.get("key_parameters", []))
    operating_pressure = extract_number(params_str, r"Operating Pressure:\s*([\d.]+)\s*bara")
    
    if operating_pressure is None:
        operating_pressure = 2.0  # Default assumption
    
    design_pressure = operating_pressure * 1.1 + 1.0  # Design margin
    
    # Determine orientation from name/type
    orientation = "vertical" if "vertical" in equipment.get("name", "").lower() else "horizontal"
    
    return {
        "volume_m3": volume_m3,
        "design_pressure_bara": design_pressure,
        "design_temperature_C": 120,  # Could be extracted from service description
        "orientation": orientation,
        "L_D_ratio": 3.0 if orientation == "vertical" else 3.5,
    }


def prepare_compressor_inputs(
    equipment: Dict[str, Any],
    stream_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Extract parameters for compressor sizing"""
    
    streams_in = equipment.get("streams_in", [])
    
    if not streams_in:
        return None
    
    stream_dict = {s["id"]: s for s in stream_data.get("streams", [])}
    inlet_stream = stream_dict.get(streams_in[0])
    
    if not inlet_stream:
        return None
    
    mass_flow = parse_flow(inlet_stream["properties"].get("mass_flow", "0"))
    suction_pressure = float(inlet_stream["properties"]["pressure"])
    suction_temp = float(inlet_stream["properties"]["temperature"])
    
    # Extract discharge pressure from key_parameters
    params_str = " ".join(equipment.get("key_parameters", []))
    discharge_pressure = extract_number(params_str, r"Outlet Pressure:\s*([\d.]+)\s*bara")
    
    if discharge_pressure is None:
        return None
    
    # Estimate molecular weight from composition
    molecular_weight = estimate_molecular_weight(inlet_stream)
    
    return {
        "mass_flow_kg_hr": mass_flow,
        "suction_pressure_bara": suction_pressure,
        "discharge_pressure_bara": discharge_pressure,
        "suction_temp_C": suction_temp,
        "molecular_weight": molecular_weight,
        "k_ratio": 1.3,  # Default for hydrocarbons/CO2
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_duty(duty_str: str) -> float:
    """Parse duty from string like '21.7 MW' or 'Cooling Duty: 10.9 MW'"""
    match = re.search(r'([\d.]+)\s*(MW|kW|GJ/h)', duty_str, re.IGNORECASE)
    if match:
        value = float(match.group(1))
        unit = match.group(2).upper()
        if unit == "MW":
            return value * 1000
        elif unit == "GJ/H":
            return value * 277.78
        return value
    return 0


def parse_flow(flow_str: str) -> float:
    """Parse flow from string like '70597 kg/h'"""
    match = re.search(r'([\d.]+)', str(flow_str))
    return float(match.group(1)) if match else 0


def parse_volume(volume_str: str) -> Optional[float]:
    """Parse volume from string like 'Volume: 1.2 m³'"""
    match = re.search(r'([\d.]+)\s*m[³3]', volume_str)
    return float(match.group(1)) if match else None


def extract_number(text: str, pattern: str) -> Optional[float]:
    """Extract number using regex pattern"""
    match = re.search(pattern, text, re.IGNORECASE)
    return float(match.group(1)) if match else None


def identify_fluid_type(stream: Dict[str, Any]) -> str:
    """Identify fluid type from stream composition"""
    components = stream.get("components", {})
    
    if components.get("H2O", 0) > 90:
        return "water"
    elif components.get("CO2", 0) > 50:
        return "CO2"
    elif stream.get("phase") == "Vapor":
        return "gas"
    return "process fluid"


def estimate_density(stream: Dict[str, Any]) -> float:
    """Estimate density from stream data"""
    phase = stream.get("phase", "Liquid")
    components = stream.get("components", {})
    
    if phase == "Liquid":
        if components.get("H2O", 0) > 50:
            return 1000
        elif components.get("Amine Solvent", 0) > 5:
            return 1050
        return 850  # Hydrocarbon default
    else:
        # Ideal gas at 1 bara, 25°C
        return 1.2


def estimate_molecular_weight(stream: Dict[str, Any]) -> float:
    """Estimate molecular weight from composition"""
    components = stream.get("components", {})
    
    MW_map = {"CO2": 44, "N2": 28, "O2": 32, "H2O": 18, "CH4": 16}
    
    total_mw = 0
    total_fraction = 0
    
    for comp, fraction_str in components.items():
        if comp in MW_map:
            fraction = float(fraction_str) / 100
            total_mw += MW_map[comp] * fraction
            total_fraction += fraction
    
    return total_mw / total_fraction if total_fraction > 0 else 29  # Air default


# ============================================================================
# ENHANCED AGENT
# ============================================================================

def create_equipment_sizing_agent(llm):
    """Create enhanced equipment sizing agent with tool integration"""
    
    # Bind tools to LLM
    tools = [size_heat_exchanger, size_pump, size_vessel, size_compressor]
    llm.temperature = 0.7
    llm_with_tools = llm.bind_tools(tools)
    
    def equipment_sizing_agent(state: DesignState) -> DesignState:
        """Equipment Sizing Agent with automatic tool calling"""
        print("\n# Equipment Sizing with Tool Integration", flush=True)
        
        # Extract state data
        requirements_markdown = state.get("requirements", "")
        design_basis_markdown = state.get("design_basis", "")
        basic_pfd_markdown = state.get("basic_pfd", "")
        basic_hmb_json = state.get("basic_hmb_results", "")
        stream_table = state.get("basic_hmb_results", "")
        equipment_table_template = state.get("basic_equipment_template", "")
        
        if not equipment_table_template.strip():
            raise ValueError("Equipment template is missing.")
        
        # Parse JSONs
        _, stream_payload = extract_first_json_document(stream_table)
        _, equipment_payload = extract_first_json_document(equipment_table_template)
        _, hmb_payload = extract_first_json_document(basic_hmb_json)
        
        if not all([stream_payload, equipment_payload, hmb_payload]):
            raise ValueError("Required JSON data is missing.")
        
        # Format for prompt
        stream_json_formatted = json.dumps(stream_payload, indent=2)
        equipment_template_formatted = json.dumps(equipment_payload, indent=2)
        hmb_json_formatted = json.dumps(hmb_payload, indent=2)
        stream_table_markdown = convert_streams_json_to_markdown(json.dumps(stream_payload))
        
        # Prepare tool inputs for each equipment item
        equipment_list = equipment_payload.get("equipment", [])
        tool_results = {}
        
        for eq in equipment_list:
            eq_id = eq.get("id")
            eq_type = eq.get("type", "").lower()
            
            print(f"- Processing {eq_id}: {eq.get('name')}...", flush=True)
            
            # Determine which tool to use and prepare inputs
            tool_inputs = None
            tool_name = None
            
            if "exchanger" in eq_type or "cooler" in eq_type or "heater" in eq_type:
                tool_inputs = prepare_heat_exchanger_inputs(eq, stream_payload)
                tool_name = "size_heat_exchanger"
            elif "pump" in eq_type:
                tool_inputs = prepare_pump_inputs(eq, stream_payload)
                tool_name = "size_pump"
            elif "vessel" in eq_type or "drum" in eq_type or "separator" in eq_type:
                tool_inputs = prepare_vessel_inputs(eq, stream_payload)
                tool_name = "size_vessel"
            elif "compressor" in eq_type:
                tool_inputs = prepare_compressor_inputs(eq, stream_payload)
                tool_name = "size_compressor"
            
            # Call tool if inputs are available
            if tool_inputs and tool_name:
                try:
                    if tool_name == "size_heat_exchanger":
                        result = size_heat_exchanger.invoke(tool_inputs)
                    elif tool_name == "size_pump":
                        result = size_pump.invoke(tool_inputs)
                    elif tool_name == "size_vessel":
                        result = size_vessel.invoke(tool_inputs)
                    elif tool_name == "size_compressor":
                        result = size_compressor.invoke(tool_inputs)
                    else:
                        result = {"error": "Unknown tool"}
                    
                    tool_results[eq_id] = result
                    print(f"  ✓ Tool result: {result}", flush=True)
                except Exception as e:
                    print(f"  ✗ Tool error: {str(e)}", flush=True)
                    tool_results[eq_id] = {"error": str(e)}
            else:
                print(f"  - No tool applicable or insufficient data", flush=True)
        
        # Create enhanced prompt with tool results
        base_prompt = equipment_sizing_prompt_with_tools(
            requirements_markdown,
            design_basis_markdown,
            basic_pfd_markdown,
            hmb_json_formatted,
            stream_json_formatted,
            stream_table_markdown,
            equipment_template_formatted,
            tool_results
        )
        
        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | llm_with_tools
        
        # Invoke with retry logic
        is_done = False
        try_count = 0
        sanitized_output = ""
        response = None
        
        while not is_done and try_count < 10:
            response = chain.invoke({"messages": list(state.get("messages", []))})
            raw_output = (
                response.content if isinstance(response.content, str) else str(response.content)
            ).strip()
            
            sanitized_output, payload = extract_first_json_document(raw_output)
            sized_entries = payload.get("equipment") if isinstance(payload, dict) else payload
            
            is_done = isinstance(sized_entries, list) and len(sized_entries) > 0
            try_count += 1
            
            if not is_done:
                print("- Retrying equipment sizing...", flush=True)
        
        if not is_done:
            print("+ Max retry count reached.", flush=True)
            raise ValueError("Failed to generate sized equipment data.")
        
        equipment_markdown = convert_equipment_json_to_markdown(sanitized_output)
        print(sanitized_output, flush=True)
        exit(0)
        return {
            "basic_equipment_template": sanitized_output,
            "messages": [response] if response else [],
        }
    
    return equipment_sizing_agent


def equipment_sizing_prompt_with_tools(
    requirements_markdown: str,
    design_basis_markdown: str,
    basic_pfd_markdown: str,
    basic_hmb_json: str,
    stream_data_json: str,
    stream_data_markdown: str,
    equipment_template_json: str,
    tool_results: Dict[str, Dict[str, Any]]
) -> ChatPromptTemplate:
    """Create prompt with pre-computed tool results"""
    
    # Format tool results for inclusion in prompt
    tool_results_formatted = json.dumps(tool_results, indent=2)
    
    system_content = f"""
You are a **Lead Equipment Sizing Engineer** responsible for finalizing equipment specifications using automated sizing tools.

**Context:**

  * You have access to preliminary sizing calculations performed by specialized tools (heat exchangers, pumps, vessels, compressors).
  * Your task is to integrate these tool results into the final equipment specification JSON, adding engineering judgment and filling gaps where tools could not be applied.

**Tool Results Available:**

The following equipment items have been pre-sized using specialized tools:

```json
{tool_results_formatted}
```

**Instructions:**

  1. **Review Tool Results:** For each equipment item with tool results, incorporate the calculated values (area, power, dimensions, etc.) into the corresponding fields in the equipment JSON.
  
  2. **Populate Key Parameters:** Use tool results to fill the `key_parameters` array. For example:
     - Heat Exchanger: ["Area: <area_m2> m²", "LMTD: <lmtd_C> °C", "U: <U_design_W_m2K> W/m²·K"]
     - Pump: ["Flow: <flow_m3_hr> m³/h", "Head: <total_head_m> m", "Power: <motor_rating_kW> kW"]
     - Vessel: ["Diameter: <diameter_mm> mm", "Length: <length_mm> mm", "Thickness: <shell_thickness_mm> mm"]
     - Compressor: ["Stages: <number_of_stages>", "Power: <driver_rating_kW> kW", "Discharge Temp: <discharge_temperature_C> °C"]
  
  3. **Update Duty/Load Field:** Replace placeholder values with calculated duties (e.g., "21.7 MW" for heat exchanger, "45 kW" for pump motor).
  
  4. **Document in Notes:** Reference the tool used and key assumptions. Example: "Sized using heat_exchanger_sizing tool with LMTD method. U-value estimated at 850 W/m²·K for hydrocarbon/water service."
  
  5. **Handle Missing Tool Results:** For equipment without tool results (columns, special equipment), use engineering judgment and the stream data to provide reasonable estimates or mark as "TBD".
  
  6. **Update Assumptions:** Add any new global assumptions to `metadata.assumptions`, such as "All pump efficiencies assumed at 75% unless specified."

  7. **Maintain JSON Structure:** Output ONLY a valid JSON object matching the equipment template schema. Do NOT use code fences.

**Example Integration:**

If tool result for E-101 is:
```json
{{
  "area_m2": 120.5,
  "lmtd_C": 25.3,
  "U_design_W_m2K": 850
}}
```

Then update the equipment entry:
```json
{{
  "id": "E-101",
  "name": "Amine Absorber Cooler",
  "duty_or_load": "10.9 MW",
  "key_parameters": [
    "Area: 120.5 m²",
    "LMTD: 25.3 °C",
    "U (Design): 850 W/m²·K"
  ],
  "notes": "Sized using heat_exchanger_sizing tool. Duty calculated from cooling flue gas. Fouling factor 0.0002 m²·K/W applied."
}}
```

**Critical Rules:**

  - All numeric values must have units
  - Round to appropriate precision (areas to 0.1 m², power to nearest kW)
  - Reference tool usage in notes for traceability
  - If tool result contains "error", note the issue and provide manual estimate or "TBD"
"""

    human_content = f"""
# DATA FOR ANALYSIS:

**Design Basis:**
{design_basis_markdown}

**Process Flow Diagram:**
{basic_pfd_markdown}

**Heat & Material Balance:**
{basic_hmb_json}

**Stream Data (JSON):**
{stream_data_json}

**Equipment Template (JSON):**
{equipment_template_json}

**Tool Results (Pre-computed):**
{tool_results_formatted}

---

# YOUR TASK:

Integrate the tool results into the equipment JSON. For each equipment item:

1. If tool results exist, populate `duty_or_load` and `key_parameters` with calculated values
2. Update `notes` to reference the tool and document assumptions
3. For items without tool results, provide engineering estimates or mark "TBD"
4. Ensure all equipment entries are complete and consistent

Output ONLY the final equipment JSON object (no code fences, no additional text).
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

    return ChatPromptTemplate.from_messages(messages)