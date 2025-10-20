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

def create_process_requiruments_analyst(llm):
    def process_requirements_analyst(state: DesignState) -> DesignState:
        """Process Requirements Analyst: Extracts key design requirements using LLM."""
        print(f"# Problem statement: {state['problem_statement']}", flush=True)
        print("# Process Requirements Analysis", flush=True)
        base_prompt = process_requirements_prompt(state["problem_statement"])
        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | llm
        response = chain.invoke({"messages": list(state.get("messages", []))})
        requirements_markdown = (
            response.content if isinstance(response.content, str) else str(response.content)
        ).strip()
        requirements_markdown = strip_markdown_code_fences(requirements_markdown)
        if len(requirements_markdown) < 10:
            print(f"The response is too short, exit(-1)")
            exit(-1)
        print(f"{requirements_markdown}", flush=True)
        return {
            "requirements": requirements_markdown,
            "messages": [response],
        }
    return process_requirements_analyst

def process_requirements_prompt(problem_statement: str) -> ChatPromptTemplate:
    system_content = f"""
You are an expert Senior Process Engineer with 20 years of experience specializing in conceptual design and requirements analysis. Your function is to meticulously dissect a chemical process problem statement and distill it into a structured set of key parameters for a technology research team.

**Context:**

  * You will be provided with a high-level problem statement describing a chemical process.
  * Your output, a concise Markdown briefing, is the foundational document for the technology research team to begin their design and selection process.
  * Accuracy and clarity are paramount. The team depends on your analysis to define the scope of their work.

**Instructions:**

  * **Analyze the `PROBLEM STATEMENT`:** Read the entire text to identify all specified and implied process requirements.
  * **Extract Key Parameters:** Systematically identify the process objective, key drivers <Energy Conservation, Emission Reduction, High Productivity, etc.>, all chemical components, capacity/throughput, purity targets, and operational constraints or assumptions.
  * **Component Specificity:** When listing components, break down mixtures into their individual chemical species (e.g., instead of "Air," list "Nitrogen," "Oxygen," etc.).
  * **Handle Missing Information:** If a parameter is not mentioned, you must use the text `Not specified`. If you infer a value based on standard engineering principles (e.g., assuming atmospheric pressure), you must explicitly state this in the "Constraints & Assumptions" section.
  * **Capacity Calculation:** Determine a reasonable design capacity for the main process unit. Ensure all unit of measure (UOM) conversions are performed correctly and the basis for the capacity is stated.
  * **Format Adherence:** Your output must be a single, PURE Markdown document. Do not add any introductory text, concluding remarks, or formatting (like code blocks) that is not part of the specified template.

-----

  * **Problem Statement:**
    ```
    {{problem_statement}}
    ```

-----

**Example:**

  * **Problem Statement:**

    ```
    "We need to design a plant to produce 1500 kg/h of high-purity Ethyl Acetate from the esterification of Ethanol and Acetic Acid using Sulfuric Acid as a catalyst. The target purity for the Ethyl Acetate product is 99.8%. The reaction should achieve at least a 92% yield based on the limiting reactant, which is Acetic Acid. The reactor must operate below 100°C."
    ```

  * **Response:**

    ```markdown
    ## Objective
    - Primary goal: Produce high-purity Ethyl Acetate via esterification of Ethanol and Acetic Acid
    - Key drivers: High Energy Optimization (or `Not specified`)

    ## Capacity
    The design capacity of the Ethyl Acetate production unit is 1500.0 kg/h, based on the final product rate.

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
    - The reactor operating temperature must be below 100°C.
    - A minimum yield of 92% must be achieved, based on Acetic Acid as the limiting reactant.
    ```

-----

**Your Task:**
Based on the `problem_statement` provided, generate ONLY the valid Markdown document that precisely follows the structure and rules defined above, **not in code block**.
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
