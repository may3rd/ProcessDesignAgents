from __future__ import annotations

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


def create_stream_data_estimator(llm):
    def stream_data_estimator(state: DesignState) -> DesignState:
        """Stream Data Estimator: Generates stream and H&MB tables with estimated conditions."""
        print("\n# Stream Data Estimator", flush=True)

        llm.temperature = 0.7
        
        basic_pfd_markdown = state.get("basic_pfd", "")
        requirements_markdown = state.get("requirements", "")
        design_basis_markdown = state.get("design_basis", "")
        concept_details_markdown = state.get("selected_concept_details", "")
        stream_template = state.get("basic_stream_data", "")

        base_prompt = stream_data_estimator_prompt(
            basic_pfd_markdown,
            requirements_markdown,
            design_basis_markdown,
            concept_details_markdown,
            stream_template,
        )
        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | llm
        
        is_done = False
        try_count = 0
        while not is_done:
            response = chain.invoke({"messages": list(state.get("messages", []))})

            markdown_output = (
                response.content if isinstance(response.content, str) else str(response.content)
            ).strip()
            is_done = len(markdown_output) > 100
            try_count += 1
            if not is_done:
                print("- Failed to create stream data, Try again.")
                if try_count > 10:
                    print("+ Max try count reached.", flush=True)
                    exit(-1)

        print(markdown_output, flush=True)
        exit(0)
        return {
            "basic_stream_data": markdown_output,
            "basic_hmb_results": markdown_output,
            "messages": [response],
        }

    return stream_data_estimator


def stream_data_estimator_prompt(
    basic_pfd_markdown: str,
    requirements_markdown: str,
    design_basis_markdown: str,
    concept_details_markdown: str,
    stream_template: str,
) -> ChatPromptTemplate:
    system_content = f"""
You are a **Senior Process Simulation Engineer** specializing in developing first-pass heat and material balances for conceptual designs.

**Context:**

  * You are provided with a `STREAM_TEMPLATE` table containing placeholders, along with supporting `DESIGN_DOCUMENTS` (concept summary, requirements, design basis).
  * Your task is to populate the stream table with realistic, reconciled operating conditions.
  * This completed table is the foundational dataset that enables downstream teams to begin equipment sizing, detailed simulation, and cost estimation.

**Instructions:**

  * **Analyze Inputs:** Review the `STREAM_TEMPLATE` and all supporting `DESIGN_DOCUMENTS` to understand the intended unit operations, performance targets, and constraints.
  * **Perform Balances:** Replace every `<value>` placeholder with a realistic estimate. Your estimates must be consistent and adhere to the principles of heat and material balance across each unit and the overall process.
  * **Enforce Conservation:** Ensure that for any unit operation, the total mass and component flows entering equal the total leaving.
  * **Document Assumptions:** Use the `## Notes` section to clearly and concisely document all key assumptions, calculation methods (e.g., specific heat values used), or correction factors applied to reconcile the balance.
  * **Ensure Completeness:** Confirm that every composition column sums to 100% (mol or mass, as appropriate).
  * **Format Adherence:** Your final output must be a PURE Markdown document. Do not wrap it in code blocks or add any text outside of the specified stream table and notes section format.

-----

**Example:**

  * **DESIGN DOCUMENTS:**

    ```
    "A shell-and-tube heat exchanger (E-101) cools 10,000 kg/h of 93 mol% ethanol from 80°C to 40°C. Plant cooling water is used, entering at 25°C. Assume Cp of ethanol stream is 2.5 kJ/kg-K and water is 4.18 kJ/kg-K."
    ```

  * **STREAM TEMPLATE:**

    ```markdown
    | Attribute          | 1001                 | 1002                       | 2001                   | 2002                   |
    | ------------------ | -------------------- | -------------------------- | ---------------------- | ---------------------- |
    | Name / Description | Hot Ethanol Feed     | Cooled Ethanol Product     | Cooling Water Supply   | Cooling Water Return   |
    | From               | Upstream Blender     | E-101 Outlet               | CW Header              | E-101                  |
    | To                 | E-101 Shell          | Storage Tank via P-101     | E-101 Tubes            | CW Header              |
    | Phase              | Liquid               | Liquid                     | Liquid                 | Liquid                 |
    | Mass Flow [kg/h]   | <value>              | <value>                    | <value>                | <value>                |
    | Temperature [°C]   | <value>              | <value>                    | <value>                | <value>                |
    | Pressure [barg]    | <value>              | <value>                    | <value>                | <value>                |
    | **Key Components** | **(mol %)** | **(mol %)** | **(mol %)** | **(mol %)** |
    | Ethanol (C₂H₆O)    | <value>              | <value>                    | <value>                | <value>                |
    | Water (H₂O)        | <value>              | <value>                    | <value>                | <value>                |
    ```

  * **Response:**

    ```markdown
    | Attribute          | 1001                 | 1002                       | 2001                   | 2002                   |
    | ------------------ | -------------------- | -------------------------- | ---------------------- | ---------------------- |
    | Name / Description | Hot Ethanol Feed     | Cooled Ethanol Product     | Cooling Water Supply   | Cooling Water Return   |
    | From               | Upstream Blender     | E-101 Outlet               | CW Header              | E-101                  |
    | To                 | E-101 Shell          | Storage Tank via P-101     | E-101 Tubes            | CW Header              |
    | Phase              | Liquid               | Liquid                     | Liquid                 | Liquid                 |
    | Mass Flow [kg/h]   | 10000                | 10000                      | 23923                  | 23923                  |
    | Temperature [°C]   | 80                   | 40                         | 25                     | 35                     |
    | Pressure [barg]    | 1.5                  | 1.3                        | 2.5                    | 2.3                    |
    | **Key Components** | **(mol %)** | **(mol %)** | **(mol %)** | **(mol %)** |
    | Ethanol (C₂H₆O)    | 93                   | 93                         | 0                      | 0                      |
    | Water (H₂O)        | 7                    | 7                          | 100                    | 100                    |

    ## Notes
    - Heat Duty Calculation: Ethanol heat removed = 10000 kg/h * (80-40)°C * 2.5 kJ/kg-K = 1,000,000 kJ/h ≈ 0.278 MW.
    - Cooling Water Flow: Required CW flow = (1,000,000 kJ/h) / ((35-25)°C * 4.18 kJ/kg-K) = 23,923 kg/h.
    - Pressure drops are estimated as 0.2 bar across the exchanger for both streams.
    ```

-----

**Your Task:** Based on the provided `DESIGN_DOCUMENTS` and `STREAM_TEMPLATE`, generate ONLY the valid Markdown document containing the completed stream table and a notes section that precisely follows the structure and rules defined above.
"""

    human_content = f"""

# REFERENCE MATERIAL
---
**Requirements Summary (Markdown):**
{requirements_markdown}

**Concept Details (Markdown):**
{concept_details_markdown}

**Design Basis (Markdown):**
{design_basis_markdown}

**Basic Process Flow Diagram (Markdown):**
{basic_pfd_markdown}

# STREAM TEMPLATE
{stream_template}

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
