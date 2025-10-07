def load_config():
    return {
        "deep_think_llm": "google/gemini-2.5-flash-lite",  # Retain for future; requires OpenAI
        "quick_think_llm": "google/gemini-2.5-flash-lite",
        "max_debate_rounds": 3,
        "property_data_source": "pubchem",
        "simulator": "dwsim"
    }