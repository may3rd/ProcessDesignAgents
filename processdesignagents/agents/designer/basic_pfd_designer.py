from __future__ import annotations

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from dotenv import load_dotenv

from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.prompt_utils import jinja_raw, strip_markdown_code_fences

load_dotenv()


def create_basic_pfd_designer(llm):
    def basic_pfd_designer(state: DesignState) -> DesignState:
        """Basic PFD Designer: synthesizes a preliminary process flow diagram consistent with the detailed concept and design basis."""
        print("\n# Basic PFD Design", flush=True)

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

        base_prompt = basic_pfd_prompt(
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
            response = chain.invoke({"messages": list(state.get("messages", []))})
            basic_pfd_markdown = (
                response.content if isinstance(response.content, str) else str(response.content)
            ).strip()
            basic_pfd_markdown = strip_markdown_code_fences(basic_pfd_markdown)
            is_done = len(basic_pfd_markdown) > 100
            try_count += 1
            if try_count > 10:
                print("+ Maximum try is reached.")
                exit(-1)

        print(basic_pfd_markdown, flush=True)
        return {
            "basic_pfd": basic_pfd_markdown,
            "messages": [response],
        }

    return basic_pfd_designer


def basic_pfd_prompt(
    concept_name: str,
    concept_details: str,
    requirements: str,
    design_basis: str,
) -> ChatPromptTemplate:
    system_content = f"""
You are a **Senior Process Design Engineer** with 20 years of experience specializing in creating clear, innovative, and accurate Process Flow Diagrams (PFDs) from conceptual data.

**Context:**

  * You will be provided with vetted project documentation, including a `DESIGN BASIS` and `REQUIREMENTS`.
  * Your task is to translate these documents into a preliminary Process Flow Diagram (PFD), presented in a structured Markdown format.
  * This PFD is a critical deliverable that serves as the backbone for downstream engineering, including stream definition, equipment sizing, safety assessment, and project approval.
  * The project sponsor expects a state-of-the-art flowsheet that showcases advanced integration, modularization, and smart instrumentation where appropriate.

**Instructions:**

  * **Synthesize Inputs:** Extract boundary conditions, operating intent, and critical assumptions from the provided `DESIGN BASIS` and `REQUIREMENTS`.
  * **Map Operations & Connectivity:** Identify all major process units and utility systems. Assign unique IDs (`T-101`, `E-101`, etc., for units; `1001`, `1002`, etc., for streams). Define the connectivity by fully populating the `Units` and `Streams` tables, ensuring every stream has a clear source, destination, and purpose.
  * **Incorporate Innovation:** Where applicable, embed state-of-the-art features (e.g., high-efficiency units, modular skids, digital monitoring). Highlight these in the `Overall Description` or `Notes`.
  * **Provide Narrative:** Write a clear `Overall Description` of the process flow. Use the `Notes` section to clarify key assumptions, highlight innovative elements, or list critical considerations for downstream teams.
  * **Format Adherence:** Your final output must be a PURE Markdown document. Do not wrap it in code blocks or add any text outside the specified template. Ensure all tables are complete and correctly formatted.

-----

  * **REQUIREMENTS:**
    ```
    {{requirements}}
    ```
  * **DESIGN BASIS:**
    ```
    {{design_basis}}
    ```

-----

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

    ```markdown
    ## Flowsheet Summary
    - Concept: Ethanol Cooler Module
    - Objective: Reduce hot ethanol from 80°C to 40°C using plant cooling water in a modular skid.
    - Key Drivers: Maintain storage temperature and ensure high operational reliability.

    ## Units
    | ID    | Name                | Type                       | Description                                    |
    | ----- | ------------------- | -------------------------- | ---------------------------------------------- |
    | E-101 | Ethanol Cooler      | Shell-and-tube exchanger | Transfers heat from ethanol to cooling water.  |
    | P-101 | Product Pump        | Centrifugal pump           | Boosts cooled ethanol pressure for transfer to storage. |
    | U-201 | Cooling Water Loop  | Utility Header             | Provides 25°C cooling water supply and return. |

    ## Streams
    | ID   | Stream             | From             | To           | Description                                    |
    | ---- | ------------------ | ---------------- | ------------ | ---------------------------------------------- |
    | 1001 | Hot Ethanol Feed   | Upstream Blender | E-101        | Process ethanol at 80°C and 1.5 barg.           |
    | 1002 | Cooled Ethanol     | E-101            | P-101        | Product leaving exchanger at 40°C.              |
    | 1003 | Storage Transfer   | P-101            | Storage Tank | Pumped ethanol to atmospheric tank.            |
    | 2001 | CW Supply          | U-201            | E-101        | Cooling water enters at 25°C.                  |
    | 2002 | CW Return          | E-101            | U-201        | Warmed cooling water returns at approx. 35°C.    |

    ## Overall Description
    Hot ethanol from the upstream blending unit (Stream 1001) is fed to the shell side of the Ethanol Cooler (E-101). Heat is exchanged against plant cooling water (Stream 2001) flowing on the tube side. The cooled ethanol (Stream 1002) flows to the Product Pump (P-101), which provides the necessary head to transfer the product to the main storage tank (Stream 1003). Warmed cooling water (Stream 2002) is returned to the utility header.

    ## Notes
    - A bypass line around E-101 should be included for maintenance flexibility.
    - Recommend temperature and pressure transmitters on all process and utility streams for smart monitoring.
    - Design assumes the entire unit (E-101, P-101, and piping) is mounted on a single modular skid.
    ```

-----

**Your Task:** Based on the `REQUIREMENTS` and `DESIGN BASIS` provided, generate ONLY the valid Markdown PFD that precisely follows the structure and rules defined above, **not in code block**.
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
