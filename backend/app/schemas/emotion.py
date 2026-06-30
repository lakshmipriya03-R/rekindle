"""
Pydantic schemas for Emotion endpoints.
"""
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.emotion import EmotionLabel, SourceType


class EmotionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dominant_emotion: EmotionLabel
    confidence: float
    joy_score: float
    sadness_score: float
    fear_score: float
    anger_score: float
    surprise_score: float
    disgust_score: float
    neutral_score: float
    source_type: SourceType
    analyzed_at: datetime


class EmotionSearchResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dominant_emotion: EmotionLabel
    confidence: float
    source_type: SourceType
    journal_id: int | None
    chat_message_id: int | None
    analyzed_at: datetime


class EmotionStats(BaseModel):
    total_entries: int
    emotion_distribution: dict[str, int]
    dominant_overall: str | None
    average_joy: float
    average_sadness: float
    average_fear: float
    average_anger: float
    average_neutral: float


class EmotionTrend(BaseModel):
    date: str
    dominant_emotion: str
    count: int
