import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def get_model_name() -> str:
    """Return the configured OpenAI model name."""
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    if not model_name:
        raise ValueError("OPENAI_MODEL is not configured.")
    return model_name


def require_api_key() -> str:
    """Return the configured API key or raise a helpful error."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add your API key."
        )
    return api_key
