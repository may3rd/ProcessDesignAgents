from typing import Annotated, Dict, Any, List, TypedDict, NotRequired
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

class DesignState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    problem_statement: str
    requirements: Dict[str, Any]
    literature_data: Dict[str, Any]
    research_concepts: Dict[str, Any]
    flowsheet: Dict[str, Any]
    validation_results: Dict[str, Any]
    approval: Dict[str, Any]
    process_requirements_report: NotRequired[str]
    literature_data_report: NotRequired[str]
    innovative_research_report: NotRequired[str]
    conservative_research_report: NotRequired[str]
    designer_report: NotRequired[str]
    process_simulator_report: NotRequired[str]
    equipment_sizing_report: NotRequired[str]
    safety_risk_analyst_report: NotRequired[str]
    project_manager_report: NotRequired[str]
