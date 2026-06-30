"""
OpenAI chat completion provider.
Uses the official openai Python SDK.
"""
from openai import OpenAI
from app.ai.base import AIProvider
from app.config import get_settings


class OpenAIProvider(AIProvider):
    """Wraps the OpenAI Chat Completions API."""

    def __init__(self):
        settings = get_settings()
        self._client = OpenAI(api_key=settings.openai_api_key)
        self._model = settings.openai_model

    def complete(self, messages: list[dict]) -> str:
        """
        Send messages to OpenAI and return the assistant content string.
        Raises OpenAIError on API failure (let it propagate to the router
        where it will be caught and returned as a 502).
        """
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )
        return response.choices[0].message.content.strip()
