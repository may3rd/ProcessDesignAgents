from typing import Annotated, Dict, Any, List, TypedDict
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
