import os

def load_config():
    return {
        "deep_think_llm": "google/gemini-2.5-flash-lite",  # Retain for future; requires OpenAI
        "quick_think_llm": "google/gemini-2.5-flash-lite",
        "save_dir": "./reports",
        "max_debate_rounds": 3,
        "property_data_source": "pubchem",
        "simulator": "dwsim"
    }
    
DEFAULT_CONNFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("RESULTS_DIR", "./results"),
    "data_dir": "/Users/yluo/Documents/Code/ScAI/FR1-data",
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings
    "llm_provider": "openrouter",
    "deep_think_llm": "google/gemini-2.5-flash-lite",
    "quick_think_llm": "google/gemini-2.5-flash-lite",
    "backend_url": "https://openrouter.ai/api/v1",
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Tool settings
    "online_tools": True,
    "property_data_source": "pubchem",
    "simulator": "dwsim"
}