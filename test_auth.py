from processdesignagents.agents.utils.chat_openrouter import ChatOpenRouter
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
print(f"Loaded API Key (first 10 chars): {api_key[:10] if api_key else 'None'}")

llm = ChatOpenRouter(model="google/gemini-2.5-flash-lite")

try:
    response = llm.invoke("Test authentication with a simple query.")
    print("Success: Response received.")
    print(response.content[:100])  # Truncate for brevity
except Exception as e:
    print(f"Error: {e}")