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
        design_basis_markdown = state.get("design_basis", "")
        
        if not isinstance(concept_details_markdown, str):
            concept_details_markdown = str(concept_details_markdown)
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)
        if not isinstance(selected_concept_name, str):
            selected_concept_name = str(selected_concept_name)
        if not isinstance(design_basis_markdown, str):
            design_basis_markdown = str(design_basis_markdown)

        base_prompt = component_list_researcher_prompt(
            selected_concept_name,
            concept_details_markdown,
            requirements_markdown,
            design_basis_markdown,
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
    design_basis: str,
) -> ChatPromptTemplate:
    system_content = f"""
You are a **Senior Process Design Engineer** with 20 years of experience specializing in conceptual design and system data extraction.

**Context:**

  * You will be provided with vetted project documentation, including a `DESIGN BASIS` and `REQUIREMENTS`.
  * Your task is to translate these documents into a component list that has the details all chemical components that will be involved in the process.
  * This component list is a critical deliverable that serves as the backbone for downstream engineering, including stream definition, equipment sizing, safety assessment, and project approval.

**Instructions:**

  * **Synthesize Inputs:** Extract operating intent, and critical assumptions from the provided `DESIGN BASIS` and `REQUIREMENTS`.
  * **List the component list:** List of the possible distinct major components that be involved in the process, including name, chemical formula, and molecular weight.
  * Use provided `Components List (CSV)` as a reference.
  * **Format Adherence:** Your final output must be a PURE Markdown document. Do not wrap it in code blocks or add any text outside the specified template. Ensure all tables are complete and correctly formatted.
  * If possible the table is sorted by boiling point of the component. Low boiling to high boiling.
  * Keep the list as minimum as possible. For general process the main components is less than 10.
  
**Example:**

  * **REQUIREMENTS:**

    ```
    "The system must cool an ethanol stream from 80°C to 40°C. It should be a modular skid design to minimize site installation time. Reliability is key."
    ```

  * **DESIGN BASIS:**

    ```
    "Capacity: 10,000 kg/h ethanol. Utility: Plant cooling water is available at 25°C. The cooled ethanol will be pumped to an existing atmospheric storage tank."
    ```

  * **Response:**
  
  | **Name** | **Formula** | **MW** |
  |----------|-------------|--------|
  | Ethanol | C2H6O | 46.07 |
  | Water | H2O | 18.015 |

-----

"""
    human_content = f"""
# DESIGN INPUTS

**Requirements (Markdown):**
{requirements}

**Selected Concept Name:**
{concept_name or "Not provided"}

**Concept Details (Markdown):**
{concept_details}

**Design Basis (Markdown):**
{design_basis}

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
