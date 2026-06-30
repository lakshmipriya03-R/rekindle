from openai import OpenAI
from app.ai.base import AIProvider
from app.config import get_settings


class GroqProvider(AIProvider):
    def __init__(self):
        settings = get_settings()

        self.client = OpenAI(
            api_key=settings.groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )

        self.model = settings.groq_model

    def complete(self, messages: list[dict]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=512,
        )

        return response.choices[0].message.content.strip()