from pydantic import BaseModel, Field
from typing import Optional, Tuple
import re
# Define Concepts Schema as Pydantic Models


class risk_base(BaseModel):
    technical: str = Field(..., description="Technical risk description.")
    economic: str = Field(..., description="Economic risk description.")
    safety_operational: str = Field(..., description="Safety/Operational risk description.")

class recommendations_list(BaseModel):
    recommendations: list[str] = Field(..., description="List of recommendations.")

class Concept(BaseModel):
    name: str = Field(..., description="Descriptive name of the process concept.")
    maturity: str = Field(
        ...,
        description="Classification of the technology's maturity (conventional, innovative, state_of_the_art).",
    )
    description: str = Field(
        ..., description="A concise paragraph explaining the process concept."
    )
    unit_operations: list[str] = Field(
        ..., description="List of essential unit operations involved in the concept."
    )
    key_benefits: list[str] = Field(
        ..., description="List of key benefits or advantages of the concept."
    )
    summary: Optional[str] = Field(
        None, description="A concise synopsis of the evaluation."
    )
    feasibility_score: Optional[int] = Field(
        None, description="Feasibility scroce of this concept"
    )
    risk: Optional[risk_base] = Field(
        None, description="Risk evaluation of this concept."
    )
    recommendations: Optional[list[str]] = Field(
        None, description="The recommendation for this concept."
    )

class ConceptsList(BaseModel):
    concepts: list[Concept] = Field(
        ..., description="A list of distinct process concepts."
    )

# Define Equipment and Stream Schema as Pydantic Models

class Quantity(BaseModel):
    value: float = Field(..., description="Value of the quantity.")
    unit: str = Field(..., description="Unit of the quantity (e.g., 'kg/h', '°C', 'barg').")

class Component(BaseModel):
    name: str = Field(..., description="Descriptive name of the component.")
    mole_frac: Optional[Quantity] = Field(None, description="Mole fraction of the component.")
    mass_frac: Optional[Quantity] = Field(None, description="Mass fraction of the component.")

class Properties(BaseModel):
    mass_flow: Optional[Quantity] = Field(None, description="Mass flow rate of the stream.")
    mole_flow: Optional[Quantity] = Field(None, description="Mole flow rate of the stream.")
    volume_flow: Optional[Quantity] = Field(None, description="Volume flow rate of the stream.")
    temperature: Quantity = Field(..., description="Temperature of the stream.")
    pressure: Quantity = Field(..., description="Pressure of the stream.")

class Stream(BaseModel):
    id: str = Field(..., description="Unique identifier for the stream.")
    name: str = Field(..., description="Descriptive name of the stream.")
    description: str = Field(..., description="A concise paragraph describing the stream.")
    from_unit: str = Field(..., description="Unit that this stream coming from.")
    to_unit: str = Field(..., description="Unit that this stream going to.")
    phase: str = Field(..., description="Phase of the stream.")
    properties: Properties = Field(..., description="Properties of the stream.")
    compositions: list[Component] = Field(..., description="Compositions of the stream.")
    notes: str = Field(..., description="Notes about the stream.")

class DesignParameter(BaseModel):
    name: str = Field(..., description="Descriptive name of the design parameter.")
    quantity: Quantity = Field(..., description="Quantity of the design parameter.")
    notes: Optional[str] = Field(None, description="Notes about the design parameter.")

class Equipment(BaseModel):
    id: str = Field(..., description="Unique identifier for the equipment.")
    name: str = Field(..., description="Descriptive name of the equipment.")
    service: str = Field(..., description="Service provided by the equipment.")
    type: str = Field(..., description="Type of the equipment.")
    streams_in: list[str] = Field(..., description="List of streams connected to this equipment.")
    streams_out: list[str] = Field(..., description="List of streams connected to this equipment.")
    design_criteria: str = Field(..., description="Design criteria for the equipment.")
    sizing_parameters: list[DesignParameter] = Field(..., description="Sizing parameters for the equipment.")
    notes: str = Field(..., description="Notes about the equipment.")

class StreamList(BaseModel):
    streams: list[Stream] = Field(..., description="List of streams.")

class EquipmentList(BaseModel):
    equipments: list[Equipment] = Field(..., description="List of equipments.")

class EquipmentsAndStreamsListBuilder(BaseModel):
    equipments: list[Equipment] = Field(..., description="List of equipments.")
    streams: list[Stream] = Field(..., description="List of streams.")

# Define Hazards for sefety and risk analysis

class Hazard(BaseModel):
    hazard_type: str = Field(..., description="Type of hazard (e.g., Chemical, Physical, Biological, Ergonomic).")
    description: str = Field(..., description="Detailed description of the hazard.")
    causes: list[str] = Field(..., description="Potential causes of the hazard.")
    consequences: list[str] = Field(..., description="Potential consequences if the hazard is realized.")
    likelihood: int = Field(..., description="Likelihood of the hazard occurring (e.g., Low, Medium, High).")
    severity: int = Field(..., description="Severity of the consequences (e.g., Minor, Moderate, Major, Catastrophic).")
    risk_level: int = Field(..., description="Overall risk level (e.g., Low, Medium, High, Extreme).")
    mitigation_measures: list[str] = Field(..., description="List of measures to mitigate the hazard.")
    notes: list[str] = Field(..., description="List of notes related to the hazard.")
    
class SafetyRiskReport(BaseModel):
    overall_assessment: str = Field(..., description="Overall assessment of the safety and risks of the process design.")
    identified_hazards: list[Hazard] = Field(..., description="A list of identified hazards, their consequences, likelihood, severity, risk level, and mitigation measures.")
    recommendations: list[str] = Field(..., description="Recommendations for further safety improvements or studies.")

# --- 2. Helper Function to Format Quantities ---

def format_quantity(q: Optional[Quantity]) -> str:
    """Converts a Quantity object to 'value unit' or 'N/A' if None."""
    if q is None:
        return "N/A"
    return f"{q.value} {q.unit}"

def format_compositions(comps: list[Component], frac_type: str) -> str:
    """Formats component fractions into a single string with line breaks."""
    parts = []
    for comp in comps:
        frac_to_check = comp.mass_frac if frac_type == 'mass' else comp.mole_frac
        if frac_to_check:
            # Use <br> for a line break in a markdown table cell
            parts.append(f"{comp.name}: {format_quantity(frac_to_check)}")
    return "<br>".join(parts) if parts else "N/A"

# --- 3. Function to Format Equipment List ---

def format_equipment_to_markdown(equipments: list[Equipment]) -> str:
    """Converts a list of Equipment objects into a markdown table and details."""
    
    md_parts = []
    
    # --- Equipment Summary Table ---
    md_parts.append("## 1. Equipment List Summary")
    md_parts.append(
        "| ID | Name | Type | Service | Streams In | Streams Out |"
    )
    md_parts.append(
        "|:---|:---|:---|:---|:---|:---|"
    )
    
    for eq in equipments:
        streams_in_str = ", ".join(eq.streams_in)
        streams_out_str = ", ".join(eq.streams_out)
        md_parts.append(
            f"| {eq.id} | {eq.name} | {eq.type} | {eq.service} | {streams_in_str} | {streams_out_str} |"
        )
        
    md_parts.append("\n" + ("-"*40) + "\n")

    # --- Equipment Details Section ---
    md_parts.append("## 2. Equipment Details")
    count_id = 0
    for eq in equipments:
        md_parts.append(f"\n### 2.{count_id+1}. {eq.id} - {eq.name}")
        md_parts.append(f"**Type:** {eq.type}")
        md_parts.append(f"**Service:** {eq.service}")
        md_parts.append(f"**Design Criteria:** {eq.design_criteria}")

        # Sizing Parameters Sub-Table
        md_parts.append("\n**Sizing Parameters:**")
        md_parts.append("| Parameter | Value | Notes |")
        md_parts.append("|:---|:---|:---|")
        for param in eq.sizing_parameters:
            md_parts.append(
                f"| {param.name} | {format_quantity(param.quantity)} | {param.notes or ''} |"
            )
        
        # Notes (if any)
        if eq.notes:
            md_parts.append(f"**Notes:** {eq.notes}")
        count_id += 1
    return "\n".join(md_parts).strip()

# --- 4. Function to Format Stream List ---

def format_streams_to_markdown(streams: list[Stream], streams_per_table: int = 10) -> str:
    """
    Converts a list of Stream objects into a transposed, paginated markdown table.
    Streams are columns, attributes are rows. compositions are broken out.
    """
    
    md_parts = []
    md_parts.append("## 3. Stream Details")
    
    if not streams:
        md_parts.append("No stream data provided.")
        return "\n".join(md_parts)

    # Define the static attributes (rows)
    # We will add component rows dynamically
    static_attributes = [
        "ID", "Name", "Description", "From", "To", "Phase", 
        "Temperature", "Pressure", "Mass Flow", "Mole Flow", "Volume Flow"
    ]

    # Collect the ordered list of components that appear across all streams
    component_order: list[str] = []
    for stream in streams:
        for component in stream.compositions:
            if component.name not in component_order:
                component_order.append(component.name)

    # Paginate streams into chunks
    for i in range(0, len(streams), streams_per_table):
        chunk_streams = streams[i : i + streams_per_table]

        # --- Build Header Row ---
        header_cells = ["**Attribute**"] + [f"**{s.id}**" for s in chunk_streams]
        md_parts.append("| " + " | ".join(header_cells) + " |")
        
        # --- Build Separator Row ---
        separator_cells = [":---"] + [":---" for _ in chunk_streams]
        md_parts.append("| " + " | ".join(separator_cells) + " |")
        
        # --- Pre-process data for easy lookup ---
        stream_data_map = {}

        for s in chunk_streams:
            # Store static properties
            props = {
                "ID": s.id,
                "Name": s.name,
                "Description": s.description,
                "From": s.from_unit,
                "To": s.to_unit,
                "Phase": s.phase,
                "Temperature": format_quantity(s.properties.temperature),
                "Pressure": format_quantity(s.properties.pressure),
                "Mass Flow": format_quantity(s.properties.mass_flow),
                "Mole Flow": format_quantity(s.properties.mole_flow),
                "Volume Flow": format_quantity(s.properties.volume_flow),
                "Notes": s.notes or ""
            }
            
            # Store component data and collect names
            props['mass_fracs'] = {}
            props['mole_fracs'] = {}
            for comp in s.compositions:
                if comp.mass_frac:
                    props['mass_fracs'][comp.name] = f"{comp.mass_frac.value:0.4f}"
                if comp.mole_frac:
                    props['mole_fracs'][comp.name] = f"{comp.mole_frac.value:0.4f}"

            stream_data_map[s.id] = props

        # --- Build Static Attribute Rows ---
        for attr in static_attributes:
            row_cells = [f"**{attr}**"]  # First cell is the attribute name
            for s in chunk_streams:
                row_cells.append(stream_data_map[s.id][attr].replace("N/A ", "")) # Clean up units for N/A

            md_parts.append("| " + " | ".join(row_cells) + " |")

        if component_order:
            # --- Build Mass Fraction Component Rows ---
            md_parts.append("| **Mass Fraction** | " + " | ".join(["--" for _ in chunk_streams]) + " |")
            for comp_name in component_order:
                row_cells = [f" {comp_name} "]
                for s in chunk_streams:
                    frac_val = stream_data_map[s.id]['mass_fracs'].get(comp_name, "0.0")
                    row_cells.append(frac_val)
                md_parts.append("| " + " | ".join(row_cells) + " |")

            # --- Build Mole Fraction Component Rows ---
            md_parts.append("| **Mole Fraction** | " + " | ".join(["--" for _ in chunk_streams]) + " |")
            for comp_name in component_order:
                row_cells = [f" {comp_name} "]
                for s in chunk_streams:
                    frac_val = stream_data_map[s.id]['mole_fracs'].get(comp_name, "0.0")
                    row_cells.append(frac_val)
                md_parts.append("| " + " | ".join(row_cells) + " |")

        # --- Build Notes Row ---
        row_cells = [f"**Notes**"]
        for s in chunk_streams:
            row_cells.append(stream_data_map[s.id]["Notes"])
        md_parts.append("| " + " | ".join(row_cells) + " |")

        md_parts.append("\n")  # Add space before the next table (if any)

    return "\n".join(md_parts).strip()

# --- 5. UPDATED Main Conversion Function ---

def convert_to_markdown(data: EquipmentsAndStreamsListBuilder, streams_per_table: int = 10) -> Tuple[str, str, str]:
    """
    Converts the full list of equipment and streams into a single
    markdown document.
    
    Args:
        data: The Pydantic object from the LLM.
        streams_per_table: Max number of streams per table before paginating.
    """
    
    # Generate markdown for equipment
    equipment_md = format_equipment_to_markdown(data.equipments)
    
    
    # Generate markdown for streams, passing the pagination parameter
    streams_md = format_streams_to_markdown(data.streams, streams_per_table)
    
    # Combine them with a clear separator
    return f"# Process Design Document\n\n{equipment_md}\n\n{'-'*80}\n\n{streams_md}", equipment_md, streams_md


# Define a function to extract JSON from markdown
def extract_json_from_markdown(text: str) -> str:
    """Extracts the first JSON object found inside a markdown code block."""
    
    # Use regex to find content between ```json and ```
    match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL | re.MULTILINE)
    
    if match:
        return match.group(1)
    
    # If no markdown block, assume the whole string is JSON (or partial JSON)
    # This helps find JSON even without the backticks
    match = re.search(r'(\{.*?\})', text, re.DOTALL | re.MULTILINE)
    if match:
        return match.group(1)
        
    # If still no match, return the original text and let Pydantic try
    return text.strip()

# Import tools from separate utility files
from processdesignagents.agents.utils.heat_exchanger_sizing_tools import (
    size_heat_exchanger_basic
)

from processdesignagents.agents.utils.pump_sizing_tools import (
    size_pump_basic
)
