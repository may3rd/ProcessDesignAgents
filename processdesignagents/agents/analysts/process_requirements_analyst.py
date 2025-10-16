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

def create_process_requiruments_analyst(llm):
    def process_requirements_analyst(state: DesignState) -> DesignState:
        """Process Requirements Analyst: Extracts key design requirements using LLM."""
        print("\n# Process Requirements Analysis", flush=True)
        base_prompt = process_requirements_prompt(state["problem_statement"])
        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | llm
        response = chain.invoke({"messages": list(state.get("messages", []))})
        requirements_markdown = (
            response.content if isinstance(response.content, str) else str(response.content)
        ).strip()
        print(f"{requirements_markdown}", flush=True)
        return {
            "requirements": requirements_markdown,
            "messages": [response],
        }
    return process_requirements_analyst

def process_requirements_prompt(problem_statement: str) -> ChatPromptTemplate:
    system_content = """
# ROLE:
You are an expert Senior Process Engineer with 20 years of experience in conceptual process design and requirement analysis. Your task is to meticulously analyze a chemical process design problem and extract key parameters.

# TASK:
Your goal is to act as a Process Requirements Analyst. You must read the provided problem statement, identify all critical process parameters enough for technology researcher team to understand and find the best possible pross design and requirement, and structure them into a concise Markdown briefing.

# INSTRUCTIONS:
1.  **Analyze Carefully:** Read the entire 'PROBLEM STATEMENT' below. Identify all specified and implied process requirements.
2.  **Think Step-by-Step:** 
    1. Identify the main process objective.
    2. List all chemical components involve in the process.
    3. Extract or estimate any quantitative data like feed rates or production rates, (optional) product purity.
    4. Identify all operational assumptions and constraints.
3.  **Handle Missing Information:**
    * If a parameter (e.g., 'yield_target') is not mentioned at all, mark it as `Not specified` and include a short note explaining the gap in the final section.
    * If a reasonable default can be inferred from standard chemical engineering principles (e.g., assuming atmospheric pressure if not specified), you may use it but clearly flag the assumption in the Constraints & Assumptions section.
4.  **Format Output:** Your final output MUST be a single Markdown document using the section headers shown below. Do not wrap your answer in JSON or code fences.

# NEGATIVES:
    * **Components** do not output the compound name, e.g. Air, instead report the chemical compostion names, e.g. Hydrogen, Oxygen, Carbon Dioxide, etc.
    * **Plant/Unit Capacity** try to determine a reasonable capacity/throughput of the process unit.
    * **Output ONLY a valid markdown formatting text. Do not use code block.**
    * Enuser that the capacity UOM conversion is done correctly.
    
# MARKDOWN TEMPLATE:
Your Markdown output must follow this structure:
```
## Objective
- Primary goal: <text>
- Key drivers: <text or `Not specified`>

## Capacity
The design capacity of <process unit> is <value with UOM or `Not specified`> <basis>.

## Components
The chemical components involved in the process are:
- <Component 1>
- <Component 2>
- ...

## Purity Target <Optional>
- Component: <name or `Not specified`>
- Value: <percentage or `Not specified`>

## Constraints & Assumptions
- <Constraint or assumption 1>
- <Constraint or assumption 2>
- ...
```

# EXAMPLE:
---
**PROBLEM STATEMENT:** "We need to design a plant to produce 1500 kg/h of high-purity Ethyl Acetate from the esterification of Ethanol and Acetic Acid using Sulfuric Acid as a catalyst. The target purity for the Ethyl Acetate product is 99.8%. The reaction should achieve at least a 92% yield based on the limiting reactant, which is Acetic Acid. The reactor must operate below 100°C."

**EXPECTED MARKDOWN OUTPUT:**
```
## Objective
- Primary goal: Produce high-purity Ethyl Acetate via esterification of Ethanol and Acetic Acid
- Key drivers: Maintain catalyst activity (Sulfuric Acid) while maximizing conversion

## Capacity
The design capacity of high-purity Ethyl Acetate plant is 1500.0 kg/h based on EA product to storage tank.

## Components
The chemical components involved in the process are:
- Ethanol
- Acetic Acid
- Ethyl Acetate
- Water
- Sulfuric Acid

## Purity Target
- Component: Ethyl Acetate
- Value: 99.8%

## Constraints & Assumptions
- Reactor operating temperature must remain below 100°C.
- Achieve at least 92% yield based on Acetic Acid (limiting reactant).
```

---
# PROBLEM STATEMENT TO ANALYZE:
"""
    human_content = f"""
# PROBLEM STATEMENT TO ANALYZE:
{problem_statement}

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
