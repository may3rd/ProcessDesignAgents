from typing import Annotated, List, TypedDict, NotRequired
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

class DesignState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    problem_statement: Annotated[str, "problem_statement"]
    requirements: Annotated[str, ""]
    research_concepts: Annotated[str, ""]
    selected_concept_details: Annotated[str, ""]
    selected_concept_name: Annotated[str, ""]
    basic_pfd: Annotated[str, ""]
    basic_hmb_results: Annotated[str, ""]
    basic_equipment_template: Annotated[str, ""]
    basic_stream_data: Annotated[str, ""]
    approval: Annotated[str, ""]
    design_basis: NotRequired[str]
    safety_risk_analyst_report: NotRequired[str]
    project_manager_report: NotRequired[str]
