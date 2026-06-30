"""
Emotion detector using a fine-tuned transformer model.
Model: j-hartmann/emotion-english-distilroberta-base
Labels: joy, sadness, fear, anger, surprise, disgust, neutral
"""
from functools import lru_cache
from app.config import get_settings


class EmotionDetector:
    """Wraps the HuggingFace text-classification pipeline for emotion detection."""

    def __init__(self, model_name: str):
        self._model_name = model_name
        self._pipeline = None

    def _load(self):
        """Lazy-load the model on first use."""
        if self._pipeline is None:
            from transformers import pipeline
            self._pipeline = pipeline(
                "text-classification",
                model=self._model_name,
                top_k=None,  # Return all label scores
                truncation=True,
                max_length=512,
            )

    def analyze(self, text: str) -> dict[str, float]:
        """
        Analyze text and return a dict of {emotion_label: score}.
        Example: {"joy": 0.85, "sadness": 0.05, ...}
        """
        self._load()

        # Truncate very long text to avoid token overflow
        text = text[:2000] if len(text) > 2000 else text

        results = self._pipeline(text)[0]

        # Normalise label names to lowercase
        scores = {}
        for item in results:
            label = item["label"].lower()
            scores[label] = round(item["score"], 4)

        # Ensure all expected labels are present
        expected = {"joy", "sadness", "fear", "anger", "surprise", "disgust", "neutral"}
        for label in expected:
            scores.setdefault(label, 0.0)

        return scores


@lru_cache(maxsize=1)
def get_emotion_detector() -> EmotionDetector:
    """Return a cached singleton EmotionDetector."""
    settings = get_settings()
    return EmotionDetector(settings.emotion_model)
