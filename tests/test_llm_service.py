from __future__ import annotations

import pytest

from app.config.settings import settings
from app.services.llm_service import LLMService, MissingOpenAIKeyError


def test_llm_service_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "")

    with pytest.raises(MissingOpenAIKeyError):
        LLMService().build_client()


def test_llm_service_uses_default_model() -> None:
    service = LLMService()
    assert service.model_name == settings.OPENAI_MODEL
