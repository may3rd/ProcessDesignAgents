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


def create_stream_data_builder(llm):
    def stream_data_builder(state: DesignState) -> DesignState:
        """Stream Data Builder: Produces a transposed markdown table template for process streams."""
        print("\n# Stream Data Template", flush=True)
        
        llm.temperature = 0.7

        basic_pfd_markdown = state.get("basic_pfd", "")
        design_basis_markdown = state.get("design_basis", "")
        requirements_markdown = state.get("requirements", "")
        concept_details_markdown = state.get("selected_concept_details", "")

        base_prompt = stream_data_prompt(
            basic_pfd_markdown,
            design_basis_markdown,
            requirements_markdown,
            concept_details_markdown,
        )
        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | llm
        
        is_done = False
        try_count = 0
        while not is_done:
            response = chain.invoke({"messages": list(state.get("messages", []))})
            table_markdown = (
                response.content if isinstance(response.content, str) else str(response.content)
            ).strip()
            is_done = len(table_markdown) > 100
            try_count += 1
            if try_count > 10:
                print("+ Maximum try is reach.")
                exit(-1)

        print(table_markdown, flush=True)
        return {
            "basic_stream_data": table_markdown,
            "messages": [response],
        }

    return stream_data_builder


def stream_data_prompt(
    basic_pfd_markdown: str,
    design_basis_markdown: str,
    requirements_markdown: str,
    concept_details_markdown: str,
) -> ChatPromptTemplate:
    system_content = f"""
You are a **Process Data Engineer** responsible for establishing the foundational stream data for a new project as it moves from conceptual design to process simulation.

**Context:**

  * You are provided with the approved conceptual design documents (PFD, Design Basis, Requirements).
  * Your task is to create the canonical stream summary. This document is critical as it serves as the single source of truth for downstream teams who will perform detailed simulations, size equipment, and verify the process flow paths.
  * Every process, utility, recycle, bypass, and vent stream must be captured to ensure a complete and accurate basis for the next project phase.

**Instructions:**

  * **Synthesize Inputs:** Review the provided `DESIGN_DOCUMENTS` to identify and extract every stream mentioned or implied by the process flow.
  * **Assign IDs:** Preserve any existing stream identifiers. For streams without an ID, assign a new sequential number (e.g., 1001, 1002 for process; 2001, 2002 for utilities).
  * **Populate Table:** Create a single, transposed Markdown table where columns represent individual streams and rows represent their attributes.
  * **Use Placeholders:** For all numeric data that will be determined later by simulation (e.g., flow rates, compositions), use the format `<value>` but be sure to include the units (e.g., `<8500 kg/h>`). For known design values (e.g., temperatures from the design basis), enter the number directly.
  * **Format Adherence:** Your final output must be a PURE Markdown document containing only the stream table. Do not add any introductory text, concluding remarks, or formatting (like code blocks) that is not part of the specified template.

-----

**Example:**

  * **DESIGN DOCUMENTS:**

    ```
    "A heat exchanger (E-101) cools 10,000 kg/h of 95 mol% ethanol from 80°C to 40°C. It is fed from an upstream blender and pumped to storage. Plant cooling water is used, entering at 25°C and returning to the header at 35°C."
    ```

  * **Response:**

    ```markdown
    | Attribute          | 1001                    | 1002                       | 2001                   | 2002                   |
    | ------------------ | ----------------------- | -------------------------- | ---------------------- | ---------------------- |
    | Name / Description | Hot Ethanol Feed        | Cooled Ethanol Product     | Cooling Water Supply   | Cooling Water Return   |
    | From               | Upstream Blender        | E-101 Outlet               | Cooling Water Header   | E-101                  |
    | To                 | E-101 Shell Inlet       | Storage Tank via P-101     | E-101 Tube Inlet       | Cooling Water Header   |
    | Phase              | Liquid                  | Liquid                     | Liquid                 | Liquid                 |
    | Mass Flow [kg/h]   | 10000                   | 10000                      | <24000>                | <24000>                |
    | Temperature [°C]   | 80                      | 40                         | 25                     | 35                     |
    | Pressure [barg]    | <1.5>                   | <1.3>                      | <2.5>                  | <2.3>                  |
    | **Key Components** | **(mol %)** | **(mol %)** | **(mol %)** | **(mol %)** |
    | Ethanol (C₂H₆O)    | 95                      | 95                         | 0                      | 0                      |
    | Water (H₂O)        | 5                       | 5                          | 100                    | 100                    |
    | Notes              | Tie-in from upstream    | To fixed-roof storage tank | From utility system    | Return to utility system |
    ```

-----

**Your Task:** Based on the provided `DESIGN_DOCUMENTS`, generate ONLY the valid Markdown stream table that precisely follows the structure and rules defined above, **not in code block**.
"""

    human_content = f"""
# DATA FOR ANALYSIS
---
**Basic PFD Description (Markdown):**
{basic_pfd_markdown}

**Design Basis (Markdown):**
{design_basis_markdown}

**Requirements Summary (Markdown):**
{requirements_markdown}

**Concept Details (Markdown):**
{concept_details_markdown}

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
