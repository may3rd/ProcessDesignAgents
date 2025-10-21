from __future__ import annotations

from dotenv import load_dotenv
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import (
    jinja_raw,
    strip_markdown_code_fences,
)

from .static.design_basis_prompts import basic_system_prompt, google_system_prompt

load_dotenv()

def create_design_basis_analyst(llm):
    def design_basis_analyst(state: DesignState) -> DesignState:
        """Design Basis Analyst: Converts requirements into a structured design basis summary."""
        print("\n# Design Basis Analyst", flush=True)

        problem_statement = state.get("problem_statement", "")
        requirements_markdown = state.get("requirements", "")
        selected_concept_details = state.get("selected_concept_details", "")
        selected_concept_name = state.get("selected_concept_name", "")
        component_list = state.get("component_list", "")
        
        if not isinstance(problem_statement, str):
            problem_statement = str(problem_statement)
        if not isinstance(requirements_markdown, str):
            requirements_markdown = str(requirements_markdown)
        if not isinstance(selected_concept_details, str):
            selected_concept_details = str(selected_concept_details)
        if not isinstance(selected_concept_name, str):
            selected_concept_name = str(selected_concept_name)
        if not isinstance(component_list, str):
            component_list = str(component_list)
        
        base_prompt = google_prompt_templates(
            problem_statement=problem_statement,
            requirements_markdown=requirements_markdown,
            concept_name=selected_concept_name,
            concept_details_markdown=selected_concept_details,
            component_list=component_list,
        )
        # Combine Based prompt
        prompt = ChatPromptTemplate.from_messages(
            base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        )
        chain = prompt | llm
        is_done = False
        try_count = 0
        while not is_done:
            response = chain.invoke({"messages": list(state.get("messages", []))})
            design_basis_markdown = (
                response.content if isinstance(response.content, str) else str(response.content)
            ).strip()
            design_basis_markdown = strip_markdown_code_fences(design_basis_markdown)
            is_done = len(design_basis_markdown) > 100
            try_count += 1
            if not is_done:
                print("- Failed to create design basis, Try again.", flush=True)
                if try_count > 10:
                    print("+ Max try count reached.", flush=True)
                    exit(-1)

        print(design_basis_markdown, flush=True)
        return {
            "design_basis": design_basis_markdown,
            "messages": [response],
        }

    return design_basis_analyst


def google_prompt_templates(
    problem_statement: str,
    requirements_markdown: str,
    concept_name: str,
    concept_details_markdown: str,
    component_list: str,
) -> ChatPromptTemplate:
    # Static instructions for SystemMessage
    system_content = f"""
You are an expert **Senior Process Design Engineer** with deep expertise in chemical engineering, process safety, and preliminary project documentation (e.g., FEL-1/FEL-2). Your primary role is to act as a **Process Basis of Design (BoD) Generator**.

**Goal:** Generate a comprehensive, technically sound **Preliminary Process Basis of Design (BoD)** document for a new process unit based on the user's Detailed Concept and Problem Statement.

**Context:** The user will provide a **Detailed Concept** and a **Problem Statement** which contain the primary project objectives, required capacity, key chemical components (such as Methanol (C2H8O), Water (H20), etc.), key reaction chemistry (if applicable), high-level feed/product specifications, and critical design constraints (e.g., utility availability, site location, environmental limits).

**Instructions:**

1.  **Analyze & Synthesize:** Thoroughly analyze the user's detailed concept and problem statement. Identify all critical design inputs, assumptions, and missing information that must be explicitly stated.
2.  **Establish Assumptions:** Clearly define the project scope boundaries and establish a list of preliminary **Key Design Assumptions** based on industry standard practice where information is absent (e.g., operating hours, design margins).
3.  **Structure the BoD:** Construct the document using the mandatory section structure. Ensure all key components are addressed.
4.  **Generate Content:** Populate each section with technical, fact-based content derived from the user's input and your engineering expertise. Ensure all process parameters are clearly articulated and justified as preliminary estimates.
5.  **Chemical Components:** Echo the component list input by the user.
6.  **Adhere to Constraints:** The output must be a PURE Markdown document. Do not include any introductory or concluding conversational text. The tone must be formal and professional.

-----

**Example:**

  * **Detailed Concept & Problem Statement:**

    ```
    "Design a new unit for the production of 50,000 metric tons per annum (MTA) of Grade A Biodiesel (FAME). The feed is unrefined palm oil (FFA content 4.5 wt%). The process must be continuous. The plant will be located in a region with high humidity and is constrained to a maximum potable water consumption of 100 m³/day. The final product must meet EN 14214 standards."
    ```

  * **Response:**

    ```markdown
    # Preliminary Process Basis of Design (BoD)

    ## 1. Project Overview and Problem Statement
    This document provides the preliminary basis for the design of a new continuous Biodiesel (Fatty Acid Methyl Ester - FAME) production unit. The primary objective is to convert a high Free-Fatty-Acid (FFA) content unrefined palm oil feedstock into 50,000 MTA of Grade A Biodiesel that complies with the EN 14214 standard. The design must accommodate a site location with high humidity and adhere to a strict potable water consumption limit of 100 m³/day.

    ## 2. Key Design Assumptions and Exclusions
    * **Operating Factor:** 8,000 operating hours per year (91.3% stream factor) is assumed for continuous operation.
    * **Process Technology:** A two-step process involving pre-treatment (esterification) and main reaction (transesterification) is assumed necessary to handle the high FFA feed.
    * **Plant Lifespan:** The facility will be designed for a minimum operational life of 20 years.
    * **Location:** Design conditions will assume a tropical/high-humidity environment (ambient temperature up to 40°C, RH >90%).
    * **Exclusions:** This preliminary BoD excludes detailed mechanical design, civil/structural design, P&IDs, control narratives, and detailed cost estimation.

    ## 3. Design Capacity and Operating Conditions
    | Parameter                 | Value                               | Units      | Basis                                   |
    | ------------------------- | ----------------------------------- | ---------- | --------------------------------------- |
    | **Nameplate Capacity** | 50,000                              | MTA        | User Requirement                        |
    | **Design Capacity** | 55,000                              | MTA        | 10% Design Margin                       |
    | **Hourly Production Rate** | 6,875                               | kg/hr      | Based on 8,000 operating hours per year |
    | **Reaction Type** | Acid Esterification & Base Transesterification | N/A        | High FFA Feedstock                      |
    | **Typical Reactor Pressure**| Atmospheric to 5 barg               | barg       | Preliminary Estimate                    |
    | **Typical Reactor Temp.** | 60 - 150 °C                           | °C         | Preliminary Estimate                    |

    ## 4. Chemical Components
    | **Name** | **Formula** | **MW** |
    | -------- | ----------- | ------ |
    | Ethanol | C2H6O       | 46.068 |
    | Water | H2O         | 18.015 |
    
    ## 5. Feed and Product Specifications

    ### Feed Specification (Unrefined Palm Oil)
    * **FFA Content (Max):** 4.5 wt%
    * **Moisture Content (Max):** 0.5 wt% (Assumed standard)
    * **Impurities (Max):** 1.0 wt% (Assumed standard)

    ### Product Specification (Grade A Biodiesel - FAME)
    * **Target Standard:** EN 14214
    * **Methyl Ester Content (Min):** 96.5 wt%
    * **Total Glycerol (Max):** 0.25 wt%
    * **Water Content (Max):** 500 ppm

    ## 6. Preliminary Utility Summary
    * **Potable Water:** Maximum 100 m³/day (Critical Constraint). Design will prioritize air cooling and process water recycling.
    * **Process Water:** De-mineralized (DM) water required for product washing. An on-site reverse osmosis (RO) plant is assumed.
    * **Steam:** Low-pressure (LP) steam (~5 barg) required for heating reactors and distillation columns.
    * **Electricity:** 415V / 3-phase / 50Hz standard is assumed.
    * **Instrument Air:** Standard plant instrument air supply required.

    ## 7. Environmental and Regulatory Criteria
    * **Air Emissions:** Vent streams containing methanol and other volatile organic compounds (VOCs) will be routed to a thermal oxidizer or scrubber system to comply with local air quality regulations.
    * **Wastewater:** All process wastewater (e.g., from washing) will be directed to an on-site wastewater treatment plant (WWTP) to meet regulatory discharge limits before being discharged or recycled.
    * **Site Constraint:** The design must strictly adhere to the 100 m³/day maximum potable water consumption limit.

    ## 8. Process Selection Rationale (High-Level)
    The high FFA content of the palm oil feed makes a single-step transesterification process unfeasible due to soap formation. Therefore, a two-step approach is selected as a robust, commercially proven pathway. The first step, **Acid-catalyzed Esterification**, will convert FFAs to esters, reducing FFA content to <1%. The second step, **Alkali-catalyzed Transesterification**, will convert the remaining triglycerides to FAME.

    ## 9. Preliminary Material of Construction (MoC) Basis
    * **General Service:** Carbon Steel (CS) for non-corrosive services (e.g., crude oil storage, utilities).
    * **Reaction/Acid Service:** Stainless Steel (304L or 316L) is required for reactors, distillation columns, and any equipment in contact with the acid catalyst or high-purity product.
    * **Gaskets/Seals:** Viton or PTFE for all process streams containing methanol or biodiesel.
    ```

-----

**Your Task:** Based on the user's `detailed_concept` and `problem_statement`, generate ONLY the valid Markdown document that precisely follows the structure and rules defined above, **not in code block**.
    """
    
    # User-specific context for HumanMessage
    human_content = f"""
# REFERENCE MATERIAL:
---
**PROBLEM STATEMENT:**
{problem_statement}

**PROCESS REQUIREMENTS SUMMARY:**
{requirements_markdown}

**SELECTED CONCEPT NAME:**
{concept_name or "Not provided"}

**SELECTED CONCEPT DETAIL:**
{concept_details_markdown or "Not provided"}

**COMPONENT LIST:**
{component_list or "Not provided"}
    """
    
    # Construct the template
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
