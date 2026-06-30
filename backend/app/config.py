"""
Application configuration loaded from environment variables.
Uses pydantic-settings for type-safe env parsing.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "Rekindle"
    app_env: str = "development"
    debug: bool = False
    secret_key: str

    # Database
    database_url: str = "sqlite:///./rekindle.db"

    # JWT
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    algorithm: str = "HS256"

    # AI
    ai_provider: str = "groq"

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Groq
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    # HuggingFace
    hf_model: str = "facebook/blenderbot-400M-distill"

    # Emotion Detection
    emotion_model: str = "j-hartmann/emotion-english-distilroberta-base"

    # CORS
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — reads .env once per process."""
    return Settings()