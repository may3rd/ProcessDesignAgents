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
from processdesignagents.agents.utils.json_utils import extract_json_from_response

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
                output_json = (
                    response.content if isinstance(response.content, str) else str(response.content)
                ).strip()
                is_done = True
            except Exception as e:
                print(f"Attemp {try_count}: {e}")

        print(output_json, flush=True)
        return {
            "component_list": output_json,
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
  * Your task is to translate these documents into a **structured JSON object** that details all chemical components that will be involved in the process.
  * This component list is a critical deliverable that serves as the backbone for downstream engineering, including stream definition, equipment sizing, safety assessment, and project approval.

**Instructions:**

  * **Synthesize Inputs:** Extract boundary conditions, operating intent, and critical assumptions from the provided `DESIGN BASIS` and `REQUIREMENTS`.
  * **List the component list:** List of the possible major components that be involved in the process, including name, chemical formula, and molecular weight.
  * **Format Adherence:** Your final output must be a PURE Markdown document. Do not wrap it in code blocks or add any text outside the specified template. Ensure all tables are complete and correctly formatted.

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
    {{
        "components": [
            {{
                "name": "Ethanol",
                "formula": "C2H6O",
                "MW": 46.068
            }},
            {{
                "name": "Water",
                "formula": "H2O",
                "MW": 18.015
            }}
        ],
        "notes": [
            "**Ethanal:** Target Product",
            "**Water:** Cooling water"
        ]
    }}

-----

**Output ONLY a valid JSON object matching the schema described above. Do not wrap the JSON in a code block. Do not add any comment text.**
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
