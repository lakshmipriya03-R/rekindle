"""
Abstract AI provider interface.
Concrete implementations: OpenAIProvider, HuggingFaceProvider, GroqProvider.
"""

from abc import ABC, abstractmethod
from functools import lru_cache
from app.config import get_settings


class AIProvider(ABC):
    @abstractmethod
    def complete(self, messages: list[dict]) -> str:
        pass


@lru_cache(maxsize=1)
def get_ai_provider() -> AIProvider:
    settings = get_settings()

    if settings.ai_provider.lower() == "groq":
        from app.ai.groq_provider import GroqProvider
        return GroqProvider()

    elif settings.ai_provider.lower() == "huggingface":
        from app.ai.huggingface_provider import HuggingFaceProvider
        return HuggingFaceProvider()

    else:
        from app.ai.openai_provider import OpenAIProvider
        return OpenAIProvider()