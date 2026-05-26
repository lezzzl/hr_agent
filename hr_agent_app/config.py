import os

from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter

load_dotenv(override=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-3-flash-preview")

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "hr_agent")
LANGSMITH_ENDPOINT = os.getenv(
    "LANGSMITH_ENDPOINT",
    "https://eu.api.smith.langchain.com",
)


def setup_langsmith() -> None:
    if not LANGSMITH_API_KEY:
        return

    values = {
        "LANGSMITH_TRACING": "true",
        "LANGSMITH_API_KEY": LANGSMITH_API_KEY,
        "LANGSMITH_PROJECT": LANGSMITH_PROJECT,
        "LANGSMITH_ENDPOINT": LANGSMITH_ENDPOINT,
        "LANGCHAIN_TRACING_V2": "true",
        "LANGCHAIN_API_KEY": LANGSMITH_API_KEY,
        "LANGCHAIN_PROJECT": LANGSMITH_PROJECT,
        "LANGCHAIN_ENDPOINT": LANGSMITH_ENDPOINT,
    }

    for key, value in values.items():
        os.environ[key] = value


def get_llm() -> ChatOpenRouter:
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is missing. Add it to .env.")

    setup_langsmith()

    return ChatOpenRouter(
        model=OPENROUTER_MODEL,
        openrouter_api_key=OPENROUTER_API_KEY,
    )
