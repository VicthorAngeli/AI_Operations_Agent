from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "AI OPERATIONS AGENT")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "true").lower() == "true"

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ai_operations_agent.db")
    DEFAULT_TIMEOUT_SECONDS: int = int(os.getenv("DEFAULT_TIMEOUT_SECONDS", "30"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "2"))

    FASTAPI_HOST: str = os.getenv("FASTAPI_HOST", "0.0.0.0")
    FASTAPI_PORT: int = int(os.getenv("FASTAPI_PORT", "8000"))

    STREAMLIT_HOST: str = os.getenv("STREAMLIT_HOST", "0.0.0.0")
    STREAMLIT_PORT: int = int(os.getenv("STREAMLIT_PORT", "8501"))
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    API_AUTH_TOKEN: str = os.getenv("API_AUTH_TOKEN", "")
    API_ALLOWED_ORIGINS: str = os.getenv("API_ALLOWED_ORIGINS", "http://localhost:8501")
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "30"))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))


settings = Settings()
