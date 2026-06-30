from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from app.ai.base import AIProvider
from app.config import get_settings
import torch


class HuggingFaceProvider(AIProvider):

    def __init__(self):
        model_name = get_settings().hf_model

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def complete(self, messages: list[dict]) -> str:
        # Use the latest user message
        prompt = ""

        for m in reversed(messages):
            if m["role"] == "user":
                prompt = m["content"]
                break

        inputs = self.tokenizer(prompt, return_tensors="pt")

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=120,
            do_sample=True,
            temperature=0.7,
        )

        return self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True,
        ).strip()