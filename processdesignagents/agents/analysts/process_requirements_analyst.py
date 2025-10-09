from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from processdesignagents.agents.utils.agent_states import DesignState
from dotenv import load_dotenv

load_dotenv()

def create_process_requiruments_analyst(quick_think_llm: str, llm):
  def process_requirements_analyst(state: DesignState) -> DesignState:
      """Process Requirements Analyst: Extracts key design requirements using LLM."""
      print("\n=========================== Problem ===========================\n")
      # llm = ChatOpenRouter()
      system_message = system_prompt(state['problem_statement'])
      
      prompt = ChatPromptTemplate.from_messages([
        (
          "system",
          "You are a helpful AI Assistant, collabarating with other assistants."
          "\n{system_message}"
        ),
        MessagesPlaceholder(variable_name="messages"),
      ])
      
      prompt = prompt.partial(system_message=system_message)
      
      chain = prompt | llm
      
      response = chain.invoke(state.get("messages", []))
      
      # response = llm.invoke(system_message, model=quick_think_llm, temperature=0.7)
      
      requirements_markdown = response.content if isinstance(response.content, str) else str(response.content)

      print(f"Extracted requirements (markdown).\n{requirements_markdown}")
      
      return {
        "requirements": {"markdown": requirements_markdown},
        "messages": [response]
      }
  return process_requirements_analyst

def system_prompt(problem_statement: str) -> str:
    return f"""
# ROLE:
You are an expert Senior Process Engineer with 20 years of experience in conceptual process design and requirement analysis. Your task is to meticulously analyze a chemical process design problem and extract key parameters.

# TASK:
Your goal is to act as a Process Requirement Analyst. You must read the provided problem statement, identify all critical process parameters, and structure them into a concise Markdown briefing.

# INSTRUCTIONS:
1.  **Analyze Carefully:** Read the entire 'PROBLEM STATEMENT' below. Identify all specified and implied process requirements.
2.  **Think Step-by-Step:** 
    1. Identify the main process objective.
    2. List all chemical components involve in the process.
    3. Extract quantitative data like throughput, purity.
    4. Identify all operational constraints.
3.  **Handle Missing Information:**
    * If a parameter (e.g., 'yield_target') is not mentioned at all, mark it as `Not specified` and include a short note explaining the gap in the final section.
    * If a reasonable default can be inferred from standard chemical engineering principles (e.g., assuming atmospheric pressure if not specified), you may use it but clearly flag the assumption in the Constraints & Assumptions section.
4.  **Format Output:** Your final output MUST be a single Markdown document using the section headers shown below. Do not wrap your answer in JSON or code fences.

# NEGATIVES:
    * **Capacity** row must always include a numeric value; if absent, estimate a reasonable default and note the assumption.
    * **Purity Target** should never be left blank—use `Not specified` and explain why if no data exists.

# MARKDOWN TEMPLATE:
Your Markdown output must follow this structure:
## Objective
- Primary goal: <text>
- Key drivers: <text or `Not specified`>

## Capacity
| Parameter | Value | Units | Basis |
|-----------|-------|-------|-------|
| Throughput | <value or `Not specified`> | kg/h | <basis or `Not specified`> |

## Components
- <Component 1 and role>
- <Component 2 and role>
- ...

## Purity Target
- Component: <name or `Not specified`>
- Value: <percentage or `Not specified`>

## Constraints & Assumptions
- <Constraint or assumption 1>
- <Constraint or assumption 2>
- ...

# EXAMPLE:
---
**PROBLEM STATEMENT:** "We need to design a plant to produce 1500 kg/h of high-purity Ethyl Acetate from the esterification of Ethanol and Acetic Acid using Sulfuric Acid as a catalyst. The target purity for the Ethyl Acetate product is 99.8%. The reaction should achieve at least a 92% yield based on the limiting reactant, which is Acetic Acid. The reactor must operate below 100°C."

**EXPECTED MARKDOWN OUTPUT:**
## Objective
- Primary goal: Produce high-purity Ethyl Acetate via esterification of Ethanol and Acetic Acid
- Key drivers: Maintain catalyst activity (Sulfuric Acid) while maximizing conversion

## Capacity
| Parameter | Value | Units | Basis |
|-----------|-------|-------|-------|
| Throughput | 1500.0 | kg/h | Ethyl Acetate product sent to storage |

## Components
- Ethanol — Reactant
- Acetic Acid — Reactant
- Ethyl Acetate — Product
- Water — Byproduct
- Sulfuric Acid — Catalyst

## Purity Target
- Component: Ethyl Acetate
- Value: 99.8%

## Constraints & Assumptions
- Reactor operating temperature must remain below 100°C.
- Achieve at least 92% yield based on Acetic Acid (limiting reactant).
---
# NEGATIVES:

* ENSURE the the capacity UOM conversion is done correctly.

# PROBLEM STATEMENT TO ANALYZE:
{problem_statement}

# FINAL MARKDOWN OUTPUT:
"""
