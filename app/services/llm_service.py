from __future__ import annotations

from openai import OpenAI

from app.config.settings import settings


class MissingOpenAIKeyError(RuntimeError):
    """Raised when the OpenAI API key is missing."""


class LLMService:
    """Minimal abstraction to centralize OpenAI configuration."""

    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name or settings.OPENAI_MODEL

    def build_client(self) -> OpenAI:
        if not settings.OPENAI_API_KEY:
            raise MissingOpenAIKeyError("OPENAI_API_KEY is not configured.")

        return OpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=settings.DEFAULT_TIMEOUT_SECONDS,
        )

    def get_model_name(self) -> str:
        return self.model_name
