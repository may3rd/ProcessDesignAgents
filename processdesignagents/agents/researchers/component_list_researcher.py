from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from dotenv import load_dotenv

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import jinja_raw

load_dotenv()


def create_component_list_researcher(llm):
    def component_list_researcher(state: DesignState) -> DesignState:
        """Component List Researcher: Syntensis the problem requirement, concept details, and design basis for component list generation."""
        print("\n# Component List Researcher:", flush=True)

        requirements_markdown = state.get("requirements", "")
        selected_concept_name = state.get("selected_concept_name", "")
        concept_details_markdown = state.get("selected_concept_details", "")
        
        if not isinstance(concept_details_markdown, str):
            concept_details_markdown = str(concept_details_markdown)
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)
        if not isinstance(selected_concept_name, str):
            selected_concept_name = str(selected_concept_name)

        base_prompt = component_list_researcher_prompt(
            selected_concept_name,
            concept_details_markdown,
            requirements_markdown,
        )

        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | llm
        is_done = False
        try_count = 0
        while not is_done:
            try_count += 1
            if try_count > 3:
                print("+ Max try count reached.", flush=True)
                exit(-1)
            try:
                # Get the response from LLM
                response = chain.invoke({"messages": list(state.get("messages", []))})
                if len(response.content) < 20:
                    continue
                is_done = True
            except Exception as e:
                print(f"Attemp {try_count}: {e}")
        print(response.content, flush=True)
        return {
            "component_list": response.content,
            "messages": [response],
        }

    return component_list_researcher


def component_list_researcher_prompt(
    concept_name: str,
    concept_details: str,
    requirements: str,
) -> ChatPromptTemplate:
    system_content = f"""
<?xml version="1.0" encoding="UTF-8"?>
<agent>
  <metadata>
    <role>Senior Process Design Engineer</role>
    <experience>20 years specializing in conceptual design and system data extraction</experience>
    <function>Extract and compile chemical component lists from design documentation</function>
  </metadata>

  <context>
    <inputs>
      <input>
        <n>REQUIREMENTS</n>
        <format>Markdown or text</format>
        <description>Project requirements including objectives, design constraints, and critical specifications</description>
      </input>
      <input>
        <n>SELECTED CONCEPT NAME</n>
        <format>Markdown or text</format>
        <description>The selected concept of design name</description>
      </input>
      <input>
        <n>CONCEPT DETAILS</n>
        <format>Markdown or text</format>
        <description>The selected concept of design details</description>
      </input>
      <input>
        <n>COMPONENTS LIST (CSV)</n>
        <format>CSV (optional reference)</format>
        <description>Optional reference file containing known chemical components with formulas and molecular weights</description>
      </input>
    </inputs>
    <purpose>Translate design documentation into a curated component list that serves as the backbone for downstream engineering</purpose>
    <downstream_applications>
      <application>Stream definition and mass balance</application>
      <application>Equipment sizing and design</application>
      <application>Safety assessment and hazard analysis</application>
      <application>Project approval and documentation</application>
    </downstream_applications>
  </context>

  <instructions>
    <instruction id="1">
      <title>Synthesize Inputs</title>
      <details>Extract operating intent, process flow logic, and critical assumptions from the provided DESIGN BASIS and REQUIREMENTS. Identify the primary feedstocks, products, intermediates, catalysts, solvents, and byproducts involved in the process.</details>
    </instruction>

    <instruction id="2">
      <title>Identify Major Components</title>
      <details>Compile a list of the distinct major chemical components that will be involved in the process. Include:
        - Primary feedstocks
        - Main products
        - Key reactants or catalysts
        - Important intermediate or byproduct streams
        - Solvents or process aids (if significant)
        
        Exclude utility streams that do not participate in the reaction (e.g., general cooling water, steam, nitrogen blanketing gas used only as inert cover).
      </details>
    </instruction>

    <instruction id="3">
      <title>Reference External Data</title>
      <details>Use the provided COMPONENTS LIST (CSV) as a reference source. Cross-check component names, chemical formulas, and molecular weights against this reference to ensure accuracy and consistency.</details>
    </instruction>

    <instruction id="4">
      <title>Sort by Boiling Point</title>
      <details>Arrange the component list in ascending order of boiling point (low boiling to high boiling). This ordering is useful for separation process planning and equipment design downstream. If boiling point data is not readily available, provide a reasonable estimate based on chemical structure or industry standard references.</details>
    </instruction>

    <instruction id="5">
      <title>Minimize Component Count</title>
      <details>Keep the list as minimal as possible. Focus on components that are materially significant to the process. For general chemical processes, the main component list should include no more than 10 distinct species. Exclude trace impurities or minor byproducts unless they are critical for safety, environmental, or quality reasons.</details>
    </instruction>

    <instruction id="6">
      <title>Ensure Accuracy</title>
      <details>Verify all chemical formulas and molecular weights. Use standard chemical nomenclature and correct IUPAC names where applicable. Ensure molecular weight values are calculated or sourced from reliable chemical databases (e.g., PubChem, ChemSpider, or standard chemical engineering references).</details>
    </instruction>

    <instruction id="7">
      <title>Format Adherence</title>
      <details>Your final output must be a PURE Markdown document. Do not wrap content in code blocks or add any explanatory text outside the table. The table must be complete, correctly formatted, and ready for immediate downstream use. Include a brief header identifying the component list.</details>
    </instruction>
  </instructions>

  <output_schema>
    <document_type>Markdown</document_type>
    <structure>
      <header>
        <markdown_heading>## Chemical Components List</markdown_heading>
        <description>Optional brief descriptive line indicating the process or project scope (e.g., "Ethanol Cooling System" or "Biodiesel Production Unit")</description>
      </header>

      <table>
        <markdown_syntax>Markdown table format</markdown_syntax>
        <required_columns>
          <column name="Name">
            <type>string</type>
            <description>IUPAC or common chemical name</description>
          </column>
          <column name="Formula">
            <type>string</type>
            <description>Chemical formula (e.g., C2H6O, H2O, CH3OH)</description>
          </column>
          <column name="MW">
            <type>numeric</type>
            <description>Molecular weight (in g/mol, e.g., 46.07)</description>
          </column>
        </required_columns>
        <table_format>
| **Name** | **Formula** | **MW** |
|----------|-------------|--------|
| [Component 1] | [Formula] | [MW] |
| [Component 2] | [Formula] | [MW] |
        </table_format>
        <sorting_order>Ascending by boiling point (low to high)</sorting_order>
        <minimum_components>2</minimum_components>
        <maximum_components>10</maximum_components>
      </table>
    </structure>

    <formatting_rules>
      <rule>Use Markdown table syntax with pipe delimiters (|)</rule>
      <rule>Use ## for the section header</rule>
      <rule>Bold column headers using **Name**, **Formula**, **MW**</rule>
      <rule>Do NOT use code blocks or backticks</rule>
      <rule>Do NOT add introductory or explanatory text outside the header and table</rule>
      <rule>Do NOT include footer comments or notes</rule>
      <rule>Ensure all rows are complete and all columns are populated</rule>
      <rule>Output ONLY the Markdown table content—no wrapping or additional commentary</rule>
    </formatting_rules>

    <content_quality_guidelines>
      <guideline>Use correct chemical nomenclature and avoid ambiguous or colloquial names</guideline>
      <guideline>Ensure molecular weight values are consistent (typically 2–3 decimal places is appropriate precision)</guideline>
      <guideline>Include only components that are materially significant to the process</guideline>
      <guideline>Exclude utility streams that do not participate in reactions (e.g., cooling water used only for heat transfer, nitrogen used only as inert blanket)</guideline>
      <guideline>If a component appears in multiple roles (e.g., both solvent and reactant), list it only once</guideline>
      <guideline>Verify boiling point ordering; if exact data is unavailable, group components by chemical family or provide a reasonable estimate</guideline>
    </content_quality_guidelines>
    <content_guardrails>
      <guardrail>Do not output the referencing components list</guardrail>
      <guardrail>Ensure that the components list is sorted by boiling point (low to high)</guardrail>
      <guardrail>Assume that cooling water is pure water (H2O)</guardrail>
    </content_guardrails>
  </output_schema>

  <boiling_point_reference>
    <description>Common boiling points for reference in refinery, petrochemical, olefin, and chemical plants (°C at 1 atm)</description>
    <compounds>
      <!-- Cryogenic and Gas Components -->
      <compound name="Nitrogen" formula="N2" mw="28.014" bp="-196.0"/>
      <compound name="Hydrogen" formula="H2" mw="2.016" bp="-252.9"/>
      <compound name="Methane" formula="CH4" mw="16.043" bp="-161.5"/>
      <compound name="Ethane" formula="C2H6" mw="30.070" bp="-88.6"/>
      <compound name="Ethylene" formula="C2H4" mw="28.054" bp="-103.7"/>
      <compound name="Propane" formula="C3H8" mw="44.097" bp="-42.1"/>
      <compound name="Propylene" formula="C3H6" mw="42.081" bp="-47.6"/>
      <compound name="Butane (n-Butane)" formula="C4H10" mw="58.123" bp="-0.5"/>
      <compound name="Isobutane (2-Methylpropane)" formula="C4H10" mw="58.123" bp="-11.7"/>
      <compound name="Butene (1-Butene)" formula="C4H8" mw="56.107" bp="-6.3"/>
      
      <!-- Light Liquids -->
      <compound name="Acetone" formula="C3H6O" mw="58.080" bp="56.1"/>
      <compound name="Methanol" formula="CH4O" mw="32.042" bp="64.7"/>
      <compound name="Ethanol" formula="C2H6O" mw="46.068" bp="78.4"/>
      <compound name="Benzene" formula="C6H6" mw="78.112" bp="80.1"/>
      <compound name="Acetic Acid" formula="C2H4O2" mw="60.052" bp="118.1"/>
      <compound name="Toluene (Methylbenzene)" formula="C7H8" mw="92.139" bp="110.6"/>
      <compound name="Xylene (Dimethylbenzene)" formula="C8H10" mw="106.165" bp="137-145"/>
      
      <!-- Refinery and Petrochemical Products -->
      <compound name="Pentane (n-Pentane)" formula="C5H12" mw="72.150" bp="36.1"/>
      <compound name="Isopentane" formula="C5H12" mw="72.150" bp="27.9"/>
      <compound name="Hexane (n-Hexane)" formula="C6H14" mw="86.177" bp="68.7"/>
      <compound name="Heptane (n-Heptane)" formula="C7H16" mw="100.204" bp="98.4"/>
      <compound name="Octane (n-Octane)" formula="C8H18" mw="114.231" bp="125.7"/>
      <compound name="Nonane (n-Nonane)" formula="C9H20" mw="128.258" bp="150.8"/>
      <compound name="Decane (n-Decane)" formula="C10H22" mw="142.285" bp="174.2"/>
      <compound name="Gasoline" formula="C4-C12 mixture" mw="100-110" bp="40-200"/>
      <compound name="Naphtha (Light)" formula="C5-C8 mixture" mw="70-100" bp="40-200"/>
      <compound name="Kerosene" formula="C10-C14 mixture" mw="140-170" bp="200-310"/>
      <compound name="Diesel" formula="C10-C20 mixture" mw="150-200" bp="200-380"/>
      <compound name="Fuel Oil (Heavy)" formula="C15-C50 mixture" mw="200-600" bp="300-600"/>
      <compound name="Bitumen" formula="C50+ mixture" mw="500+" bp="&gt;400"/>
      
      <!-- Olefins and Intermediates -->
      <compound name="Isoprene (2-Methyl-1,3-butadiene)" formula="C5H8" mw="68.119" bp="34.1"/>
      <compound name="Butadiene (1,3-Butadiene)" formula="C4H6" mw="54.091" bp="-4.4"/>
      <compound name="Styrene (Ethenylbenzene)" formula="C8H8" mw="104.150" bp="145.2"/>
      <compound name="Acetylene (Ethyne)" formula="C2H2" mw="26.037" bp="-84.0"/>
      <compound name="Cumene (Isopropylbenzene)" formula="C9H12" mw="120.192" bp="152.4"/>
      <compound name="Phenol" formula="C6H6O" mw="94.111" bp="181.7"/>
      
      <!-- Chemical Plant Products and Intermediates -->
      <compound name="Formaldehyde" formula="CH2O" mw="30.026" bp="-19.0"/>
      <compound name="Acetaldehyde (Ethanal)" formula="C2H4O" mw="44.052" bp="20.1"/>
      <compound name="Formic Acid" formula="CH2O2" mw="46.026" bp="100.8"/>
      <compound name="Propionic Acid" formula="C3H6O2" mw="74.079" bp="141.1"/>
      <compound name="Butanoic Acid (Butyric Acid)" formula="C4H8O2" mw="88.106" bp="163.3"/>
      <compound name="Acrylic Acid" formula="C3H4O2" mw="72.063" bp="141.6"/>
      <compound name="Methyl Acrylate" formula="C4H6O2" mw="86.089" bp="80.3"/>
      <compound name="Ethyl Acrylate" formula="C5H8O2" mw="100.116" bp="99.0"/>
      <compound name="Methyl Methacrylate" formula="C5H8O2" mw="100.116" bp="100.6"/>
      
      <!-- Amines and Nitrogen Compounds -->
      <compound name="Ammonia" formula="NH3" mw="17.031" bp="-33.3"/>
      <compound name="Methylamine" formula="CH5N" mw="31.057" bp="-6.3"/>
      <compound name="Dimethylamine" formula="C2H7N" mw="45.084" bp="2.8"/>
      <compound name="Aniline" formula="C6H7N" mw="93.128" bp="184.1"/>
      
      <!-- Alcohols and Glycols -->
      <compound name="Isopropanol (2-Propanol)" formula="C3H8O" mw="60.096" bp="82.6"/>
      <compound name="n-Propanol" formula="C3H8O" mw="60.096" bp="97.2"/>
      <compound name="n-Butanol" formula="C4H10O" mw="74.123" bp="117.7"/>
      <compound name="Isobutanol" formula="C4H10O" mw="74.123" bp="108.0"/>
      <compound name="Ethylene Glycol" formula="C2H6O2" mw="62.068" bp="197.3"/>
      <compound name="Propylene Glycol" formula="C3H8O2" mw="76.095" bp="187.6"/>
      <compound name="Glycerin (Glycerol)" formula="C3H8O3" mw="92.094" bp="290"/>
      
      <!-- Inorganic and Utility Compounds -->
      <compound name="Water" formula="H2O" mw="18.015" bp="100.0"/>
      <compound name="Sulfuric Acid" formula="H2SO4" mw="98.079" bp="337"/>
      <compound name="Phosphoric Acid" formula="H3PO4" mw="98.000" bp="213"/>
      <compound name="Hydrochloric Acid" formula="HCl" bp="-85"/>
      <compound name="Sodium Hydroxide" formula="NaOH" mw="40.005" bp="1388"/>
      <compound name="Potassium Hydroxide" formula="KOH" mw="56.106" bp="1327"/>
      <compound name="Sodium Chloride" formula="NaCl" mw="58.443" bp="1465"/>
      <compound name="Calcium Carbonate" formula="CaCO3" mw="100.087" bp="N/A"/>
      <compound name="Carbon Dioxide" formula="CO2" mw="44.009" bp="-78.5"/>
      <compound name="Carbon Monoxide" formula="CO" mw="28.010" bp="-191.5"/>
      <compound name="Oxygen" formula="O2" mw="31.999" bp="-183.0"/>
      <compound name="Hydrogen Sulfide" formula="H2S" mw="34.080" bp="-60.3"/>
      <compound name="Sulfur Dioxide" formula="SO2" mw="64.066" bp="-10.0"/>
      
      <!-- Additives and Specialty Chemicals -->
      <compound name="Dimethyl Sulfoxide (DMSO)" formula="C2H6OS" mw="78.133" bp="189"/>
      <compound name="Tetrahydrofuran (THF)" formula="C4H8O" mw="72.106" bp="66"/>
      <compound name="N,N-Dimethylformamide (DMF)" formula="C3H7NO" mw="73.094" bp="153"/>
      <compound name="Dimethyl Carbonate" formula="C3H6O3" mw="106.079" bp="90.3"/>
      <compound name="Ethylene Oxide" formula="C2H4O" mw="44.052" bp="10.7"/>
      <compound name="Propylene Oxide" formula="C3H6O" mw="58.080" bp="34.3"/>
    </compounds>
  </boiling_point_reference>

  <example>
    <requirements>The system must cool an ethanol stream from 80°C to 40°C. It should be a modular skid design to minimize site installation time. Reliability is key.</requirements>

    <design_basis>Capacity: 10,000 kg/h ethanol. Utility: Plant cooling water is available at 25°C. The cooled ethanol will be pumped to an existing atmospheric storage tank.</design_basis>

    <expected_markdown_output>## Chemical Components List

| **Name** | **Formula** | **MW** | **Boiling Point** |
|----------|-------------|--------|-------------------|
| Ethanol | C2H6O | 46.07 | 78.4°C |
| Water | H2O | 18.015 | 100°C |</expected_markdown_output>

    <explanation>
      <point>Two components identified: Water (cooling utility and contamination in ethanol) and Ethanol (main process stream).</point>
      <point>Note: This ordering choice reflects practical separation considerations; typically low boilers are listed first. Adjust order based on actual boiling points.</point>
    </explanation>
  </example>

</agent>
"""
    human_content = f"""
Create a components list based on the following data:

# DESIGN INPUTS

**Requirements (Markdown):**
{requirements}

**Selected Concept Name:**
{concept_name or "Not provided"}

**Concept Details (Markdown):**
{concept_details}

**Component List (CSV):**
Name,Formula,MW (g/mol)
1-Butene,C4H8,56.107
Acetone,C3H6O,58.08
Air,Mixture,28.96
Ammonia,NH3,17.031
Argon,Ar,39.948
Benzene,C6H6,78.11
CarbonDioxide,CO2,44.01
CarbonMonoxide,CO,28.01
CarbonylSulfide,COS,60.07
CycloHexane,C6H12,84.16
CycloPropane,C3H6,42.08
Cyclopentane,C5H10,70.13
D4,C8H24O4Si4,296.62
D5,C10H30O5Si5,370.77
D6,C12H36O6Si6,444.92
Deuterium,D2,4.028
Dichloroethane,C2H4Cl2,98.96
DiethylEther,C4H10O,74.12
DimethylCarbonate,C3H6O3,90.08
DimethylEther,C2H6O,46.07
Ethane,C2H6,30.07
Ethanol,C2H5OH,46.07
EthylBenzene,C8H10,106.17
Ethylene,C2H4,28.05
EthyleneOxide,C2H4O,44.05
Fluorine,F2,37.996
HFE143m,C2H3F3O,100.04
HeavyWater,D2O,20.028
Helium,He,4.0026
Hydrogen,H2,2.016
HydrogenChloride,HCl,36.46
HydrogenSulfide,H2S,34.08
IsoButane,C4H10,58.12
IsoButene,C4H8,56.107
Isohexane,C6H14,86.18
Isopentane,C5H12,72.15
Krypton,Kr,83.798
MD2M,C12H36O4Si5,384.84
MD3M,C13H39O5Si6,458.99
MD4M,C14H42O5Si6,458.99
MDM,C8H24O2Si3,236.53
MM,C6H18OSi2,162.38
Methane,CH4,16.04
Methanol,CH3OH,32.04
MethylLinoleate,C19H34O2,294.47
MethylLinolenate,C19H32O2,292.46
MethylOleate,C19H36O2,296.49
MethylPalmitate,C17H34O2,270.45
MethylStearate,C19H38O2,298.51
Neon,Ne,20.18
Neopentane,C5H12,72.15
Nitrogen,N2,28.014
NitrousOxide,N2O,44.013
Novec649,C6F12O,316.05
OrthoDeuterium,D2,4.028
OrthoHydrogen,H2,2.016
Oxygen,O2,31.998
ParaDeuterium,D2,4.028
ParaHydrogen,H2,2.016
Propylene,C3H6,42.08
Propyne,C3H4,40.06
R11,CCl3F,137.37
R113,C2Cl3F3,187.38
R114,C2Cl2F4,170.92
R115,C2ClF5,154.47
R116,C2F6,138.01
R12,CCl2F2,120.91
R123,C2HCl2F3,152.93
R1233zd(E),C3H2ClF3,130.5
R1234yf,C3H2F4,114.04
R1234ze(E),C3H2F4,114.04
R1234ze(Z),C3H2F4,114.04
R124,C2HClF4,136.48
R1243zf,C3H3F3,96.05
R125,C2HF5,120.02
R13,CClF3,104.46
R1336mzz(E),C4H2F6,164.05
R134a,C2H2F4,102.03
R13I1,CF3I,195.91
R14,CF4,88.005
R141b,C2H3Cl2F,116.95
R142b,C2H3ClF2,100.5
R143a,C2H3F3,84.04
R152A,C2H4F2,66.05
R161,C2H5F,48.06
R21,CHCl2F,102.92
R218,C3F8,188.02
R22,CHClF2,86.47
R227EA,C3HF7,170.03
R23,CHF3,70.014
R236EA,C3H2F6,152.04
R236FA,C3H2F6,152.04
R245ca,C3H3F5,134.05
R245fa,C3H3F5,134.05
R32,CH2F2,52.02
R365MFC,C4H5F5,148.07
R40,CH3Cl,50.49
R404A,Mixture,97.6
R407C,Mixture,86.2
R41,CH3F,34.03
R410A,Mixture,72.59
R507A,Mixture,98.86
RC318,C4F8,200.03
SES36,C2F6O,154.01
SulfurDioxide,SO2,64.06
SulfurHexafluoride,SF6,146.05
Toluene,C7H8,92.14
Water,H2O,18.015
Xenon,Xe,131.29
cis-2-Butene,C4H8,56.107
m-Xylene,C8H10,106.17
n-Butane,C4H10,58.12
n-Decane,C10H22,142.28
n-Dodecane,C12H26,170.33
n-Heptane,C7H16,100.2
n-Hexane,C6H14,86.18
n-Nonane,C9H20,128.25
n-Octane,C8H18,114.23
n-Pentane,C5H12,72.15
n-Propane,C3H8,44.09
n-Undecane,C11H24,156.31
o-Xylene,C8H10,106.17
p-Xylene,C8H10,106.17
trans-2-Butene,C4H8,56.107
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
