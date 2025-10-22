import re
from langchain_core.messages import AIMessage
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


def strip_markdown_code_block(text: str) -> str:
    """Return text without enclosing ```markdown ``` code fences."""
    if not isinstance(text, str):
        return text
    pattern = re.compile(r"```(?:markdown)?\s*([\s\S]*?)```", re.IGNORECASE)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return text


def create_safety_risk_analyst(llm):
    def safety_risk_analyst(state: DesignState) -> DesignState:
        """Safety and Risk Analyst: Performs HAZOP-inspired risk assessment on current concept."""
        print("\n# Safety and Risk Assessment", flush=True)
        requirements_markdown = state.get("requirements", "")
        design_basis_markdown = state.get("design_basis", "")
        basic_pfd_markdown = state.get("basic_pfd", "")
        equipment_and_stream_list = state.get("equipment_and_stream_list", "")

        base_prompt = safety_risk_prompt(
            requirements_markdown,
            design_basis_markdown,
            basic_pfd_markdown,
            equipment_and_stream_list,
        )
        prompt_messages = base_prompt.messages + [MessagesPlaceholder(variable_name="messages")]
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | llm
        is_done = False
        try_count = 0
        while not is_done:
            try_count += 1
            if try_count > 10:
                print("+ Max try count reached.", flush=True)
                exit(-1)
            try:
                # Get the response from LLM
                response = chain.invoke({"messages": list(state.get("messages", []))})
                is_done = True
            except Exception as e:
                print(f"Attemp {try_count} has failed.")
        cleaned_content = strip_markdown_code_block(response.content)
        print(cleaned_content, flush=True)
        ai_message = AIMessage(content=cleaned_content)
        return {
            "safety_risk_analyst_report": cleaned_content,
            "messages": [ai_message],
        }
    return safety_risk_analyst


def safety_risk_prompt(
    process_requirement: str,
    design_basis_markdown: str,
    basic_pfd_markdown: str,
    equipment_and_stream_list: str,
) -> ChatPromptTemplate:
    system_content = """
You are a **Certified Process Safety Professional (CPSP)** with 20 years of experience facilitating Hazard and Operability (HAZOP) studies for the chemical industry.

**Context:**

  * You are given structured `DESIGN_DOCUMENTS` covering the process narrative, stream inventory, and equipment list.
  * Your task is to produce a preliminary HAZOP-style assessment highlighting the most critical hazards.
  * Stakeholders require the results as a markdown code only.

**Instructions:**

  * Review the provided information to map unit operations, stream connectivity, and operating envelopes.
  * Identify at least three and at most five hazards covering credible deviations (e.g., loss of flow, high pressure, contamination, utility failure).
  * For each hazard provide:
      - `title`
      - `severity` (integer 1–5)
      - `likelihood` (integer 1–5)
      - `risk_score` (severity × likelihood)
      - `causes`, `consequences`, `mitigations`, `notes` (arrays of concise statements referencing stream IDs/equipment tags where relevant)
  * Summarize the overall risk posture in `overall_assessment` with `risk_level` (Low | Medium | High) and `compliance_notes` (array of follow-up actions or reminders).
  * Use `"TBD"` where data is genuinely unavailable; otherwise provide reasoned estimates.
  * Return a markdown code only.

**Example Output:**
## Hazards

### 1. Loss of Cooling Water Flow
**Severity:** 3 | **Likelihood:** 3 | **Risk Score:** 9

**Causes:**
- Cooling water control valve XV-201 fails closed
- Utility header pressure drops during maintenance

**Consequences:**
- Ethanol outlet > 50 °C causing vapor in downstream storage
- Potential overpressure at vent system

**Mitigations:**
- Install redundant cooling water pumps with automatic switchover
- Add high-temperature alarm TAH-101 with shutdown logic

**Notes:**
Streams 1001/1002 and equipment E-101 impacted; verify relief design for temperature excursion.

---

## Overall Assessment

**Risk Level:** Medium

**Compliance Notes:**
- Confirm redundancy test for cooling water network before commissioning.
- Finalize corrosion monitoring program for E-101 tubes.

"""
    human_content = f"""
# DATA FOR HAZOP ANALYSIS
---
**REQUIREMENTS / CONSTRAINTS (Markdown):**
{process_requirement}

**DESIGN BASIS (Markdown):**
{design_basis_markdown}

**BASIC PROCESS FLOW DIAGRAM (Markdown):**
{basic_pfd_markdown}

**EQUIPMENT AND STREAMS DATA (JSON):**
{equipment_and_stream_list}
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
