from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import pubchempy as pcp
from processdesignagents.agents.utils.agent_states import DesignState
from processdesignagents.agents.utils.markdown_validators import require_sections
from dotenv import load_dotenv
import json
import re

load_dotenv()


def create_literature_data_analyst(llm):
    def literature_data_analyst(state: DesignState) -> DesignState:
        """Literature and Data Analyst: Extracts components from markdown requirements and fetches PubChem data."""
        print("\n=========================== Component List ===========================\n")

        requirements = state.get("requirements", {})
        if isinstance(requirements, dict) and "markdown" in requirements:
            requirements_markdown = requirements.get("markdown", "")
        else:
            requirements_markdown = json.dumps(requirements, default=str)

        system_message = system_prompt(requirements_markdown)

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a helpful AI Assistant, collaborating with other assistants."
                "\n{system_message}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ])

        chain = prompt.partial(system_message=system_message) | llm

        response = chain.invoke(state.get("messages", []))
        response_markdown = response.content if isinstance(response.content, str) else str(response.content)
        require_sections(response_markdown, ["Components", "Rationale"], "Literature component summary")

        components = _extract_components_from_markdown(response_markdown)
        if not components:
            raise ValueError("Failed to extract components from markdown response.")

        literature_data: dict[str, dict[str, object]] = {}
        for component in components[:3]:  # Limit to 3 for efficiency
            try:
                compounds = pcp.get_compounds(component, "name")
                if compounds:
                    compound = compounds[0]
                    literature_data[component] = {
                        "compound_name": compound.iupac_name,
                        "molecular_weight": compound.molecular_weight,
                        "boiling_point": getattr(compound, "boiling_point", None),
                        "sources": ["PubChem"],
                    }
                    print(f"Fetched literature data for {component}: {literature_data[component]}")
                else:
                    literature_data[component] = {"error": f"No data found for {component}"}
            except Exception as exc:
                literature_data[component] = {"error": f"PubChem query failed: {exc}"}

        literature_payload = {
            "components": components,
            "component_data": literature_data,
            "markdown": response_markdown,
        }

        return {
            "literature_data": literature_payload,
            "literature_data_report": response_markdown,
            "messages": [response],
        }

    return literature_data_analyst


def _extract_components_from_markdown(markdown_text: str) -> list[str]:
    components: list[str] = []
    lines = markdown_text.splitlines()
    capture = False

    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith("## components"):
            capture = True
            continue

        if capture:
            if stripped.startswith("## ") and not stripped.lower().startswith("## components"):
                break
            if stripped.startswith("-"):
                item = stripped[1:].strip()
                if not item:
                    continue
                name_part = re.split(r"\(|—|-", item)[0].strip()
                if name_part:
                    components.append(name_part)

    return components


def system_prompt(requirements_markdown: str) -> str:
    return f"""
# ROLE:
You are an expert chemical engineer specializing in process data analysis. Your task is to identify the most critical chemical components from a set of process requirements.

# TASK:
Analyze the provided 'PROCESS REQUIREMENTS' Markdown summary. Extract the 1 to 5 most important chemical components mentioned or implied (e.g., primary reactants and products). Present your findings as a concise Markdown report.

# OUTPUT FORMAT:
Your Markdown must follow this structure exactly:
## Components
- <Component name> — <role or note>
- ...

## Rationale
- <Brief justification for component selection>
- ...

# INSTRUCTIONS:
1.  **Analyze Context:** Carefully read the 'PROCESS REQUIREMENTS' to understand the core chemical process being described.
2.  **Identify Chemicals:** Look for explicit bullet items, purity targets, or descriptions that name chemicals.
3.  **Prioritize:** Select only the primary reactants, products, and essential catalysts. Ignore solvents or trace impurities unless they are central to the process objective.
4.  **Infer if Necessary:** If a process is named (e.g., "ammonia synthesis"), infer the primary components (e.g., "Nitrogen", "Hydrogen", "Ammonia").
5.  **Format Output:** Use the Markdown structure above. List each component with a concise role descriptor (e.g., Product, Reactant, Catalyst).

# EXAMPLE:
---
**PROCESS REQUIREMENTS (Markdown Summary):**
## Components
- Ethanol — Reactant
- Acetic Acid — Reactant
- Ethyl Acetate — Product
- Sulfuric Acid — Catalyst

## Purity Target
- Component: Ethyl Acetate
- Value: 99.8%

**EXPECTED MARKDOWN OUTPUT:**
## Components
- Ethyl Acetate — Product
- Ethanol — Reactant
- Acetic Acid — Reactant
- Sulfuric Acid — Catalyst

## Rationale
- Ethyl Acetate is the specified product with stringent purity requirements.
- Ethanol and Acetic Acid are the primary reactants enabling esterification.
- Sulfuric Acid acts as the catalyst driving the reaction.
---

# NEGATIVES:
* DO NOT return common mixture names (e.g., "Air"). Instead, decompose them into constituent chemicals when relevant.

# PROCESS REQUIREMENTS TO ANALYZE:
{requirements_markdown}

# FINAL MARKDOWN OUTPUT:
"""
