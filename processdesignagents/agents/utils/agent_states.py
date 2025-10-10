from typing import Annotated, List, TypedDict, NotRequired
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

class DesignState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    problem_statement: Annotated[str, "problem_statement"]
    requirements: Annotated[str, ""]
    literature_data: Annotated[str, ""]
    research_concepts: Annotated[str, ""]
    selected_concept_details: Annotated[str, ""]
    selected_concept_name: Annotated[str, ""]
    flowsheet: Annotated[str, ""]
    validation_results: Annotated[str, ""]
    approval: Annotated[str, ""]
    design_basis: NotRequired[str]
    design_basis_report: NotRequired[str]
    process_requirements_report: NotRequired[str]
    literature_data_report: NotRequired[str]
    innovative_research_report: NotRequired[str]
    conservative_research_report: NotRequired[str]
    concept_detail_report: NotRequired[str]
    designer_report: NotRequired[str]
    process_simulator_report: NotRequired[str]
    equipment_sizing_report: NotRequired[str]
    safety_risk_analyst_report: NotRequired[str]
    project_manager_report: NotRequired[str]
