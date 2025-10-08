from typing import TypedDict, Dict, Any

class DesignState(TypedDict):
    problem_statement: str
    requirements: Dict[str, Any]
    literature_data: Dict[str, Any]
    research_concepts: Dict[str, Any]
    flowsheet: Dict[str, Any]
    validation_results: Dict[str, Any]
    approval: Dict[str, Any]