from typing import Annotated, List, TypedDict, Optional, Sequence

try:  # Python <3.11 fallback
    from typing import NotRequired  # type: ignore
except ImportError:  # pragma: no cover
    from typing_extensions import NotRequired  # type: ignore
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

class DesignState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    problem_statement: Annotated[str, "problem_statement"]
    requirements: Annotated[str, ""]
    research_concepts: Annotated[str, ""]
    research_rateing_results: Annotated[str, ""]
    selected_concept_details: Annotated[str, ""]
    selected_concept_name: Annotated[str, ""]
    basic_pfd: Annotated[str, ""]
    stream_list_results: Annotated[str, ""]
    equipment_list_template: Annotated[str, ""]
    equipment_list_results: Annotated[str, ""]
    stream_list_template: Annotated[str, ""]
    approval: Annotated[str, ""]
    design_basis: NotRequired[str]
    safety_risk_analyst_report: NotRequired[str]
    project_manager_report: NotRequired[str]


def create_design_state(
    *,
    messages: Optional[Sequence[BaseMessage]] = None,
    problem_statement: str = "",
    requirements: str = "",
    research_concepts: str = "",
    research_rateing_results: str = "",
    selected_concept_details: str = "",
    selected_concept_name: str = "",
    basic_pfd: str = "",
    stream_list_results: str = "",
    equipment_list_template: str = "",
    equipment_list_results: str = "",
    stream_list_template: str = "",
    approval: str = "",
    design_basis: Optional[str] = None,
    safety_risk_analyst_report: Optional[str] = None,
    project_manager_report: Optional[str] = None,
) -> DesignState:
    """Factory to create a DesignState with sensible defaults."""

    state: DesignState = {
        "messages": list(messages) if messages is not None else [],
        "problem_statement": problem_statement,
        "requirements": requirements,
        "research_concepts": research_concepts,
        "research_rateing_results": research_rateing_results,
        "selected_concept_details": selected_concept_details,
        "selected_concept_name": selected_concept_name,
        "basic_pfd": basic_pfd,
        "stream_list_results": stream_list_results,
        "equipment_list_template": equipment_list_template,
        "equipment_list_results": equipment_list_results,
        "stream_list_template": stream_list_template,
        "approval": approval,
    }

    if design_basis is not None:
        state["design_basis"] = design_basis
    if safety_risk_analyst_report is not None:
        state["safety_risk_analyst_report"] = safety_risk_analyst_report
    if project_manager_report is not None:
        state["project_manager_report"] = project_manager_report

    return state
