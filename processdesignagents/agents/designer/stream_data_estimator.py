import json
from json_repair import repair_json

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from dotenv import load_dotenv

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import jinja_raw
from processdesignagents.agents.utils.equipment_stream_markdown import equipments_and_streams_dict_to_markdown
from processdesignagents.agents.utils.json_tools import get_json_str_from_llm, extract_first_json_document


load_dotenv()


def create_stream_data_estimator(llm, llm_provider: str = "openrouter"):
    def stream_data_estimator(state: DesignState) -> DesignState:
        """Stream Data Estimator: Generates JSON stream data with reconciled estimates."""
        print("\n# Stream Data Estimator", flush=True)
        basic_pfd_markdown = state.get("basic_pfd")
        design_basis_markdown = state.get("design_basis")
        equipments_and_streams_list = state.get("equipment_and_stream_list")
        print(f"Basis: {len(design_basis_markdown)}, PFD: {len(basic_pfd_markdown)}, Streams: {len(equipments_and_streams_list)}", flush=True)
        base_prompt = stream_data_estimator_prompt(
            basic_pfd_markdown,
            design_basis_markdown,
            equipments_and_streams_list,
        )
        system_message, human_message = base_prompt.messages
        prompt_messages = [
            system_message,
            MessagesPlaceholder(variable_name="messages"),
            human_message,
        ]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        is_done = False
        response = None
        sanitized_response = ""
        streams_md = ""
        while not is_done:
            try:
                response, response_content = get_json_str_from_llm(llm, prompt, state)
                sanitized_response, response_dict = extract_first_json_document(repair_json(response_content))
                if not isinstance(response_dict, dict):
                    print("Stream Data Estimator received non-dict payload, retrying...", flush=True)
                    print(response_content, flush=True)
                    continue
                combined_md, equipment_md, streams_md = equipments_and_streams_dict_to_markdown(response_dict)
                is_done = True
            except Exception as e:
                print(f"Stream Data Estimator attempt failed: {e}", flush=True)
        if streams_md:
            print(streams_md, flush=True)
        return {
            "equipment_and_stream_list": json.dumps(response_dict),
            "messages": [response],
        }

    return stream_data_estimator


def stream_data_estimator_prompt(
    basic_pfd_markdown: str,
    design_basis_markdown: str,
    equipments_and_streams_list: str,
) -> ChatPromptTemplate:
    system_content = f"""
<agent>
  <metadata>
    <role>Senior Process Simulation Engineer</role>
    <specialization>First-pass heat and material balances for conceptual designs</specialization>
    <function>Populate equipment and stream templates with realistic, reconciled operating conditions</function>
    <deliverable>Authoritative dataset for equipment sizing, detailed simulation, and cost estimation</deliverable>
  </metadata>

  <context>
    <inputs>
      <input>
        <n>EQUIPMENTS_STREAMS_TEMPLATE</n>
        <format>JSON</format>
        <description>Template document containing placeholder stream information with structure for equipments and streams</description>
        <contains>
          <item>Equipment definitions with inlet/outlet stream references</item>
          <item>Stream structure with placeholder properties and compositions</item>
          <item>Design criteria and constraints</item>
        </contains>
      </input>
      <input>
        <n>DESIGN DOCUMENTS</n>
        <format>Text or Markdown</format>
        <description>Supporting documentation including concept summary, requirements, design basis</description>
        <contains>
          <item>Unit operations and process descriptions</item>
          <item>Performance targets and specifications</item>
          <item>Operating constraints and design parameters</item>
          <item>Thermodynamic properties (Cp values, densities, etc.)</item>
          <item>Feed compositions and product requirements</item>
        </contains>
      </input>
    </inputs>
    <task_scope>
      <item>Populate stream properties with realistic numeric values</item>
      <item>Ensure mass and component balances are conserved</item>
      <item>Reconcile compositions across all streams</item>
      <item>Document key assumptions supporting estimates</item>
      <item>Leave equipment section untouched (handled by downstream agents)</item>
    </task_scope>
    <output_purpose>Authoritative dataset for downstream engineering phases</output_purpose>
    <downstream_users>
      <user>Equipment sizing specialists</user>
      <user>Detailed process simulation engineers</user>
      <user>Cost estimation and project planning teams</user>
      <user>Safety and risk assessment teams</user>
    </downstream_users>
  </context>

  <instructions>
    <instruction id="1">
      <title>Analyze Inputs Comprehensively</title>
      <details>
        - Review the EQUIPMENTS_STREAMS_TEMPLATE JSON to understand the unit operations, stream connectivity, and placeholder structure
        - Study all DESIGN DOCUMENTS to extract:
          * Performance targets and design specifications
          * Operating constraints and boundary conditions
          * Thermodynamic data (specific heats, densities, viscosities)
          * Feed compositions and product requirements
          * Energy balance requirements
        - Identify key assumptions already stated in design documents
        - Map all streams to their source and destination units
      </details>
    </instruction>

    <instruction id="2">
      <title>Establish Work Sequence</title>
      <details>
        - Start with main feed stream(s) to the process
        - Trace forward through primary unit operations to final product stream(s)
        - Perform material balances for each unit sequentially
        - Then address utility streams (heating, cooling, compression utilities)
        - Use outlet conditions of one unit to inform inlet conditions of downstream units
        - Maintain consistency between all interconnected streams
      </details>
    </instruction>

    <instruction id="3">
      <title>Perform Mass and Component Balances</title>
      <details>
        - For each unit operation, apply fundamental conservation of mass
        - Account for all inlet streams, outlet streams, and any accumulation
        - Verify mass balance closure: sum of inlet flows = sum of outlet flows (within rounding tolerance)
        - Verify component balance for each species: inlet component moles = outlet component moles (or account for reaction/separation)
        - For each stream, ensure that compositions (molar fraction or mass fraction) sum to 100%
        - Calculate density-dependent properties (volume flow) based on composition-weighted properties
        - Document any assumptions about reaction conversion, separation efficiency, or energy losses
      </details>
    </instruction>

    <instruction id="4">
      <title>Calculate Consistent Composition Representations</title>
      <details>
        - For each stream, establish a PRIMARY composition basis (recommend: molar fraction)
        - If molar fraction is primary, calculate corresponding mass fraction:
          * Mass fraction of component i = (molar fraction_i × MW_i) / (sum of all molar_j × MW_j)
          * Verify sum of all mass fractions = 1.0 (100%)
        - If mass fraction is primary, calculate corresponding molar fraction:
          * Molar fraction of component i = (mass fraction_i / MW_i) / (sum of all mass_j / MW_j)
          * Verify sum of all molar fractions = 1.0 (100%)
        - For components not present in a stream, explicitly set value to 0.0 (not null or omitted)
        - Maintain at least 4 decimal places for all fractions to ensure accuracy
        - Cross-check by working in both directions: molar ↔ mass
        - Document the basis and calculation method in stream notes
      </details>
    </instruction>

    <instruction id="5">
      <title>Populate Stream Properties</title>
      <details>
        - For each stream, replace placeholder values with best-estimate numeric values
        - Properties to populate (where applicable):
          * Mass flow rate (kg/h, kg/s, or alternative UOM)
          * Molar flow rate (kmol/h, kmol/s, or alternative UOM)
          * Temperature (°C, K)
          * Pressure (barg, bar, kPa)
          * Volume flow rate (m³/h, m³/s)
          * Density (kg/m³) calculated from composition and temperature
          * Phase designation (Liquid, Vapor, Two-Phase, etc.)
        - Use design documents to establish boundary conditions
        - Apply thermodynamic relationships to calculate derived properties
        - Preserve units as stated in design documents or modify if more appropriate
        - Ensure all numeric values are floats (decimal notation)
      </details>
    </instruction>

    <instruction id="6">
      <title>Verify Energy Balances</title>
      <details>
        - For each equipment unit, establish energy balance: Q_in - Q_out + W = ΔH_stream
        - Use provided or estimated Cp values to calculate enthalpy changes
        - For heat exchangers: duty calculation Q = m × Cp × ΔT
        - For reactors with heat of reaction: account for ΔH_rxn
        - For separation units: include heats of evaporation/condensation
        - Verify that calculated utility requirements (cooling duty, heating duty) are reasonable
        - Document all thermodynamic property assumptions in stream notes
      </details>
    </instruction>

    <instruction id="7">
      <title>Document Assumptions and Safeguards</title>
      <details>
        - Populate the "notes" field for each stream with:
          * Composition basis used (molar or mass fraction)
          * Any assumptions about property values (e.g., "Assumes Cp = 2.5 kJ/kg-K for ethanol at 60°C")
          * Calculations performed to derive the values
          * Known limitations or uncertainties
          * Critical control points or measurement requirements
          * References to design documents or industry standards used
        - Provide brief, technical notes suitable for engineering handoff
      </details>
    </instruction>

    <instruction id="8">
      <title>Preserve Equipment Section</title>
      <details>
        - Do NOT modify the "equipments" section of the template
        - Leave all equipment IDs, names, types, and design criteria unchanged
        - Leave all sizing_parameters placeholder structure intact
        - Equipment details will be populated by downstream agents after stream properties are finalized
        - Only populate the "streams" section completely
      </details>
    </instruction>

    <instruction id="9">
      <title>Validate Completeness and Consistency</title>
      <details>
        - Verify that every stream in the template has been populated with numeric values
        - Verify that component fractions sum to 100% ± 0.1% for each stream
        - Verify that mass balances close for each unit operation
        - Verify that all units are consistent and appropriate
        - Cross-check compositions in all interconnected streams at equipment boundaries
        - Ensure that phase designations (Liquid, Vapor, etc.) are consistent with temperature/pressure and composition
        - Flag any inconsistencies or missing data in notes
      </details>
    </instruction>

    <instruction id="10">
      <title>Output Discipline</title>
      <details>
        - Return a single valid JSON object matching the schema structure
        - Use only double quotes (no single quotes)
        - Ensure all numeric values are float type (decimal notation)
        - Do NOT include code fences, backticks, or Markdown formatting
        - Do NOT include explanatory prose, comments, or narrative text
        - Do NOT add new equipment IDs or stream IDs beyond those in the template
      </details>
    </instruction>
  </instructions>

  <output_schema>
    <root_object>
      <key name="equipments">
        <type>array</type>
        <description>Equipment list from template—DO NOT MODIFY</description>
        <instruction>Preserve exactly as provided in input template. No changes to be made.</instruction>
      </key>

      <key name="streams">
        <type>array</type>
        <item_type>object</item_type>
        <description>Complete list of all streams with populated, reconciled properties and compositions</description>
        
        <stream_object>
          <required_fields>
            <field name="id">
              <type>string</type>
              <instruction>Preserve from template</instruction>
            </field>
            <field name="name">
              <type>string</type>
              <instruction>Preserve from template</instruction>
            </field>
            <field name="description">
              <type>string</type>
              <instruction>Preserve from template</instruction>
            </field>
            <field name="from">
              <type>string</type>
              <instruction>Preserve from template</instruction>
            </field>
            <field name="to">
              <type>string</type>
              <instruction>Preserve from template</instruction>
            </field>
            <field name="phase">
              <type>string</type>
              <instruction>Preserve from template or update based on calculated temperature/pressure</instruction>
            </field>

            <field name="properties">
              <type>object</type>
              <description>Stream properties populated with reconciled numeric values</description>
              <populate_strategy>
                <property name="mass_flow">
                  <description>Total mass flow rate of stream</description>
                  <value_type>float</value_type>
                  <unit_guidance>kg/h (or kg/s, t/h as appropriate)</unit_guidance>
                  <calculation>Use design documents; calculate from molar flow if needed</calculation>
                </property>
                <property name="molar_flow">
                  <description>Total molar flow rate of stream</description>
                  <value_type>float</value_type>
                  <unit_guidance>kmol/h (or kmol/s as appropriate)</unit_guidance>
                  <calculation>Sum of component molar flows; verify against mass_flow / avg_MW</calculation>
                </property>
                <property name="temperature">
                  <description>Stream temperature</description>
                  <value_type>float</value_type>
                  <unit_guidance>°C or K (specify in unit field)</unit_guidance>
                  <calculation>From design documents or unit outlet calculations</calculation>
                </property>
                <property name="pressure">
                  <description>Stream pressure</description>
                  <value_type>float</value_type>
                  <unit_guidance>barg, bar, or kPa</unit_guidance>
                  <calculation>From design documents or pressure drop calculations</calculation>
                </property>
                <property name="volume_flow">
                  <description>Volumetric flow rate (optional if not in template)</description>
                  <value_type>float</value_type>
                  <unit_guidance>m³/h</unit_guidance>
                  <calculation>mass_flow / density</calculation>
                </property>
                <property name="density">
                  <description>Stream density (optional if not in template)</description>
                  <value_type>float</value_type>
                  <unit_guidance>kg/m³</unit_guidance>
                  <calculation>Composition-weighted average based on temperature and composition</calculation>
                </property>
              </populate_strategy>
            </field>

            <field name="compositions">
              <type>object</type>
              <description>Chemical component mapping to molar and/or mass fractions</description>
              <populate_strategy>
                <guideline>For each component in the stream:</guideline>
                <guideline>- Include entry with value and unit fields</guideline>
                <guideline>- Use molar fraction as PRIMARY basis (recommended)</guideline>
                <guideline>- If mass fraction is also needed, include as separate entry or calculate consistently</guideline>
                <guideline>- For components NOT present in stream, explicitly set value to 0.0</guideline>
                <guideline>- Verify sum of all fractions = 1.0 (100%) ± 0.1% tolerance</guideline>
                <guideline>- Use at least 4 decimal places for precision</guideline>
                <guideline>- Cross-check molar ↔ mass conversion using MW values</guideline>
              </populate_strategy>
              <structure>
                <component_entry>
                  <name>[Component name from design basis]</name>
                  <structure>
                    <subfield name="value">
                      <type>float</type>
                      <description>Fraction value (0.0 to 1.0)</description>
                    </subfield>
                    <subfield name="unit">
                      <type>string</type>
                      <constant>molar fraction or mass fraction</constant>
                    </subfield>
                  </structure>
                </component_entry>
              </structure>
            </field>

            <field name="notes">
              <type>string</type>
              <description>Detailed notes capturing assumptions, calculation methods, and safeguards</description>
              <populate_guidance>
                <item>State composition basis used (molar or mass fraction)</item>
                <item>Document any assumed property values with source and reasoning</item>
                <item>Describe calculation method if properties were derived</item>
                <item>Explain any assumptions about reactions, conversions, or separations</item>
                <item>Note critical control points or measurement requirements</item>
                <item>Reference design documents or standards used</item>
                <item>Flag any uncertainties or data gaps requiring FEED phase resolution</item>
                <item>Document balance verification (mass balance closure, component balance)</item>
              </populate_guidance>
            </field>
          </required_fields>
        </stream_object>
      </key>

      <key name="notes_and_assumptions">
        <type>array of strings</type>
        <description>Overall project-level assumptions and critical design choices</description>
        <guidance>
          <item>Thermodynamic property sources and assumptions</item>
          <item>Design basis parameters and their derivations</item>
          <item>Any simplifications or approximations made</item>
          <item>Data gaps or TBD items requiring FEED phase resolution</item>
          <item>References to standards or industry practices applied</item>
          <item>Critical validation or testing recommendations</item>
        </guidance>
      </key>
    </root_object>

    <json_formatting_rules>
      <rule>Use only double quotes (no single quotes)</rule>
      <rule>All numeric values must be float type (e.g., 10.0, not "10" or "10.0")</rule>
      <rule>Use decimal notation for all numbers (e.g., 0.95, not 95%)</rule>
      <rule>No trailing commas in arrays or objects</rule>
      <rule>All arrays and objects must be properly closed</rule>
      <rule>No comments or explanatory text inside JSON</rule>
      <rule>No code fences or Markdown formatting</rule>
      <rule>UTF-8 safe characters only</rule>
    </json_formatting_rules>

    <composition_validation_rules>
      <rule>Sum of all molar fractions per stream must equal 1.0 ± 0.001 (100% ± 0.1%)</rule>
      <rule>Sum of all mass fractions per stream must equal 1.0 ± 0.001 (100% ± 0.1%)</rule>
      <rule>For components not present in stream, set value to 0.0 (not null or omitted)</rule>
      <rule>Maintain at least 4 decimal places for all fraction values</rule>
      <rule>Verify molar ↔ mass fraction consistency using molecular weights</rule>
      <rule>Document composition basis (molar or mass) in stream notes</rule>
    </composition_validation_rules>

    <mass_balance_validation_rules>
      <rule>Total mass flow in = Total mass flow out for each unit (within rounding)</rule>
      <rule>Total moles in = Total moles out for each unit (accounting for reactions)</rule>
      <rule>For each component: moles_in = moles_out (or account for reaction/separation)</rule>
      <rule>Verify energy balance: Q_in - Q_out + W = ΔH_stream</rule>
      <rule>Document any component generation or consumption due to reactions</rule>
    </mass_balance_validation_rules>
  </output_schema>

  <thermodynamic_reference>
    <description>Common thermodynamic properties for process simulation reference</description>
    
    <property_table>
      <compound name="Ethanol (C2H6O)">
        <mw>46.068</mw>
        <cp_liquid>2.44</cp_liquid>
        <cp_unit>kJ/kg-K at 25-60°C</cp_unit>
        <density_liquid>789.0</density_liquid>
        <density_unit>kg/m³ at 20°C</density_unit>
        <bp>78.37</bp>
        <bp_unit>°C at 1 atm</bp_unit>
      </compound>
      <compound name="Water (H2O)">
        <mw>18.015</mw>
        <cp_liquid>4.18</cp_liquid>
        <cp_unit>kJ/kg-K at 0-100°C</cp_unit>
        <density_liquid>1000.0</density_liquid>
        <density_unit>kg/m³ at 4°C</density_unit>
        <bp>100.0</bp>
        <bp_unit>°C at 1 atm</bp_unit>
      </compound>
      <compound name="Methanol (CH4O)">
        <mw>32.042</mw>
        <cp_liquid>2.51</cp_liquid>
        <cp_unit>kJ/kg-K at 25°C</cp_unit>
        <density_liquid>792.0</density_liquid>
        <density_unit>kg/m³ at 20°C</density_unit>
        <bp>64.7</bp>
        <bp_unit>°C at 1 atm</bp_unit>
      </compound>
      <compound name="Benzene (C6H6)">
        <mw>78.112</mw>
        <cp_liquid>1.70</cp_liquid>
        <cp_unit>kJ/kg-K</cp_unit>
        <density_liquid>878.0</density_liquid>
        <density_unit>kg/m³ at 20°C</density_unit>
        <bp>80.1</bp>
        <bp_unit>°C at 1 atm</bp_unit>
      </compound>
      <compound name="Toluene (C7H8)">
        <mw>92.139</mw>
        <cp_liquid>1.63</cp_liquid>
        <cp_unit>kJ/kg-K</cp_unit>
        <density_liquid>865.0</density_liquid>
        <density_unit>kg/m³ at 20°C</density_unit>
        <bp>110.6</bp>
        <bp_unit>°C at 1 atm</bp_unit>
      </compound>
      <compound name="Acetic Acid (C2H4O2)">
        <mw>60.052</mw>
        <cp_liquid>2.08</cp_liquid>
        <cp_unit>kJ/kg-K</cp_unit>
        <density_liquid>1049.0</density_liquid>
        <density_unit>kg/m³ at 20°C</density_unit>
        <bp>118.1</bp>
        <bp_unit>°C at 1 atm</bp_unit>
      </compound>
    </property_table>

    <calculation_examples>
      <example name="Composition Conversion">
        <description>Convert molar fraction to mass fraction for ethanol-water mixture</description>
        <given>Molar fraction: Ethanol 0.95, Water 0.05</given>
        <step1>Average MW = (0.95 × 46.068) + (0.05 × 18.015) = 43.846</step1>
        <step2>Mass fraction Ethanol = (0.95 × 46.068) / 43.846 = 0.9967</step2>
        <step3>Mass fraction Water = (0.05 × 18.015) / 43.846 = 0.0205</step3>
        <verification>Sum = 0.9967 + 0.0205 = 1.0172 (adjust for rounding) ✓</verification>
      </example>

      <example name="Energy Balance">
        <description>Calculate cooling duty for heat exchanger</description>
        <given>Mass flow 10,000 kg/h, Ethanol Cp = 2.44 kJ/kg-K, T_in = 80°C, T_out = 40°C</given>
        <calculation>Q = m × Cp × ΔT = 10,000 kg/h × 2.44 kJ/kg-K × (40-80)°C = -976,000 kJ/h ≈ -271 kW</calculation>
        <interpretation>Cooler requires 271 kW cooling duty (negative sign indicates heat removal)</interpretation>
      </example>
    </calculation_examples>
  </thermodynamic_reference>

  <example>
    <design_documents>
      <doc>A shell-and-tube heat exchanger (E-101) cools 10,000 kg/h of 95 mol percent ethanol from 80°C to 40°C. Plant cooling water is used, entering at 25°C. Assume Cp of ethanol stream is 2.44 kJ/kg-K and water is 4.18 kJ/kg-K.</doc>
      <doc>A heat exchanger (E-101) cools 10,000 kg/h of 95 mol percent ethanol from 80°C to 40°C. It is fed from an upstream blender and pumped to storage. Plant cooling water is used, entering at 25°C and returning to the header at 35°C.</doc>
    </design_documents>

    <expected_json_output>{{
  "equipments": [
    {{
      "id": "E-101",
      "name": "Ethanol Cooler",
      "service": "Reduce hot ethanol temperature prior to storage.",
      "type": "Shell-and-tube exchanger",
      "category": "Heat Exchanger",
      "streams_in": ["1001", "2001"],
      "streams_out": ["1002", "2002"],
      "design_criteria": "&lt;0.27 MW&gt;",
      "sizing_parameters": [
        {{
          "name": "Area",
          "quantity": {{
            "value": 120.0,
            "unit": "m²"
          }}
        }},
        {{
          "name": "LMTD",
          "quantity": {{
            "value": 40.0,
            "unit": "°C"
          }}
        }},
        {{
          "name": "U-value",
          "quantity": {{
            "value": 450.0,
            "unit": "W/m²-K"
          }}
        }}
      ],
      "notes": "Design for a minimum 5°C approach temperature. Ensure sufficient space for bundle pull during maintenance."
    }}
  ],
  "streams": [
    {{
      "id": "1001",
      "name": "Hot Ethanol Feed",
      "description": "Feed entering exchanger E-101 shell side",
      "from": "Upstream Blender",
      "to": "E-101",
      "phase": "Liquid",
      "properties": {{
        "mass_flow": {{
          "value": 10000.0,
          "unit": "kg/h"
        }},
        "molar_flow": {{
          "value": 215.74,
          "unit": "kmol/h"
        }},
        "temperature": {{
          "value": 80.0,
          "unit": "°C"
        }},
        "pressure": {{
          "value": 1.7,
          "unit": "barg"
        }},
        "density": {{
          "value": 763.5,
          "unit": "kg/m³"
        }}
      }},
      "compositions": {{
        "Ethanol (C2H6O)": {{
          "value": 0.95,
          "unit": "molar fraction"
        }},
        "Water (H2O)": {{
          "value": 0.05,
          "unit": "molar fraction"
        }}
      }},
      "notes": "Tie-in from upstream blender. Composition: 95 mol% Ethanol, 5 mol% Water. Molar flow = 10000 kg/h / ((0.95×46.068 + 0.05×18.015) g/mol) × 1000 = 215.74 kmol/h. Density estimated from composition-weighted average at 80°C. Mass balance verified."
    }},
    {{
      "id": "1002",
      "name": "Cooled Ethanol",
      "description": "Product exiting exchanger E-101 shell side",
      "from": "E-101",
      "to": "Storage Tank T-201",
      "phase": "Liquid",
      "properties": {{
        "mass_flow": {{
          "value": 10000.0,
          "unit": "kg/h"
        }},
        "molar_flow": {{
          "value": 215.74,
          "unit": "kmol/h"
        }},
        "temperature": {{
          "value": 40.0,
          "unit": "°C"
        }},
        "pressure": {{
          "value": 1.0,
          "unit": "barg"
        }},
        "density": {{
          "value": 780.2,
          "unit": "kg/m³"
        }}
      }},
      "compositions": {{
        "Ethanol (C2H6O)": {{
          "value": 0.95,
          "unit": "molar fraction"
        }},
        "Water (H2O)": {{
          "value": 0.05,
          "unit": "molar fraction"
        }}
      }},
      "notes": "Product stream to storage. Composition unchanged (no reaction). Molar flow conserved = 215.74 kmol/h. Density increases due to lower temperature. Cooling duty = 10000 kg/h × 2.44 kJ/kg-K × (40-80)°C = 976 kW removed. Mass balance verified: inlet = outlet."
    }},
    {{
      "id": "2001",
      "name": "Cooling Water Supply",
      "description": "Utility cooling water to exchanger E-101 tube side",
      "from": "Cooling Water Header",
      "to": "E-101",
      "phase": "Liquid",
      "properties": {{
        "mass_flow": {{
          "value": 24085.0,
          "unit": "kg/h"
        }},
        "molar_flow": {{
          "value": 1337.8,
          "unit": "kmol/h"
        }},
        "temperature": {{
          "value": 25.0,
          "unit": "°C"
        }},
        "pressure": {{
          "value": 2.5,
          "unit": "barg"
        }},
        "density": {{
          "value": 997.0,
          "unit": "kg/m³"
        }}
      }},
      "compositions": {{
        "Water (H2O)": {{
          "value": 1.0,
          "unit": "molar fraction"
        }}
      }},
      "notes": "Utility cooling water (pure). Mass flow calculated from energy balance: Q = 976 kW = m_cw × 4.18 kJ/kg-K × (35-25)°C → m_cw = 23333 kg/h (adjusted to 24085 for minor margin). Molar flow = 24085 kg/h / 18.015 g/mol = 1337.8 kmol/h. Density at 25°C = 997 kg/m³."
    }},
    {{
      "id": "2002",
      "name": "Cooling Water Return",
      "description": "Warmed utility cooling water from exchanger E-101 tube side",
      "from": "E-101",
      "to": "Cooling Water Return Header",
      "phase": "Liquid",
      "properties": {{
        "mass_flow": {{
          "value": 24085.0,
          "unit": "kg/h"
        }},
        "molar_flow": {{
          "value": 1337.8,
          "unit": "kmol/h"
        }},
        "temperature": {{
          "value": 35.0,
          "unit": "°C"
        }},
        "pressure": {{
          "value": 1.8,
          "unit": "barg"
        }},
        "density": {{
          "value": 994.0,
          "unit": "kg/m³"
        }}
      }},
      "compositions": {{
        "Water (H2O)": {{
          "value": 1.0,
          "unit": "molar fraction"
        }}
      }},
      "notes": "Return stream closes utility loop. Temperature rise: 35-25 = 10°C. Mass and molar flows conserved. Energy balance check: 24085 kg/h × 4.18 kJ/kg-K × 10°C = 1007 kW ≈ 976 kW (cooler duty), within margin for line losses. Density at 35°C = 994 kg/m³."
    }}
  ],
  "notes_and_assumptions": [
    "Composition basis: Molar fractions converted to mass fractions using ethanol MW = 46.068 g/mol, water MW = 18.015 g/mol. Stream 1001/1002: Ethanol mass fraction ≈ 0.9967, Water mass fraction ≈ 0.0033 (sum = 1.0).",
    "Thermodynamic properties: Ethanol Cp = 2.44 kJ/kg-K (liquid, 25-60°C range), Water Cp = 4.18 kJ/kg-K. Densities estimated using composition-weighted averages and temperature correction.",
    "Energy balance verified: Cooling duty = 10000 kg/h × 2.44 kJ/kg-K × 40°C = 976 kW. Cooling water flow calculated from duty and ΔT_cw = 10°C: m_cw = 976 kW / (4.18 kJ/kg-K × 10°C) ≈ 23,333 kg/h, increased to 24,085 kg/h for 3% margin.",
    "Mass balance closure: Stream 1001 inlet (10,000 kg/h) = Stream 1002 outlet (10,000 kg/h). Stream 2001 inlet (24,085 kg/h) = Stream 2002 outlet (24,085 kg/h). ✓ All balances verified.",
    "Composition summation verified: Stream 1001/1002: 0.95 + 0.05 = 1.0 (molar). Stream 2001/2002: 1.0 (molar). ✓ All compositions sum to 100%.",
    "Critical assumptions for FEED phase validation: (1) Ethanol Cp remains constant over 80-40°C range; (2) Negligible fouling or scale formation on heat transfer surfaces; (3) Cooling water supplied at stated conditions (25°C inlet, 2.5 barg); (4) No phase change in ethanol stream (remains liquid across operating range); (5) Mixing is uniform; no stratification.",
    "Next phase actions: Equipment sizing (E-101 area, U-value), detailed P&amp;ID development, instrumentation strategy (T/P transmitters on all process and utility streams), operational control strategy, and cost estimation."
  ]
}}</expected_json_output>

  <input_placeholders>
    <equipments_and_streams_list>{equipments_and_streams_list}</equipments_and_streams_list>
    <design_basis>{design_basis_markdown}</design_basis>
    <basic_process_flow_diagram>{basic_pfd_markdown}</basic_process_flow_diagram>
  </input_placeholders>
  
  </example>
</agent>
"""

    human_content = f"""
# DATA FOR ANALYSIS
---
**Equipments and Streams Template (JSON):**
{equipments_and_streams_list}

**Design Basis (Markdown):**
{design_basis_markdown}

**Basic Process Flow Diagram (Markdown):**
{basic_pfd_markdown}

You MUST respond only with a valid JSON object without commentary or code fences.
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
