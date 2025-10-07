import os
from typing import Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import Field, SecretStr
from langchain_core.utils.utils import secret_from_env

load_dotenv()

class ChatOpenRouter(ChatOpenAI):
    """Custom ChatOpenAI wrapper for OpenRouter compatibility."""
    openai_api_key: Optional[SecretStr] = Field(
        alias="api_key",
        default_factory=secret_from_env("OPENROUTER_API_KEY", default=None),
    )

    @property
    def lc_secrets(self) -> dict[str, str]:
        return {"openai_api_key": "OPENROUTER_API_KEY"}

    def __init__(self, **kwargs):
        api_key = kwargs.pop("openai_api_key", None) or os.getenv("OPENROUTER_API_KEY")
        super().__init__(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,  # Use modern 'api_key' parameter
            **kwargs
        )