"""
EmotionAnalysis ORM model.
Stores detected emotions for both journal entries and chat messages.
"""
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import String, Float, DateTime, ForeignKey, Enum as SAEnum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base


class EmotionLabel(str, Enum):
    joy = "joy"
    sadness = "sadness"
    fear = "fear"
    anger = "anger"
    surprise = "surprise"
    disgust = "disgust"
    neutral = "neutral"


class SourceType(str, Enum):
    journal = "journal"
    chat = "chat"


class EmotionAnalysis(Base):
    __tablename__ = "emotion_analyses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    journal_id: Mapped[int | None] = mapped_column(
        ForeignKey("journals.id", ondelete="CASCADE"), nullable=True, index=True
    )
    chat_message_id: Mapped[int | None] = mapped_column(
        ForeignKey("chat_messages.id", ondelete="CASCADE"), nullable=True, index=True
    )
    source_type: Mapped[SourceType] = mapped_column(SAEnum(SourceType))
    dominant_emotion: Mapped[EmotionLabel] = mapped_column(SAEnum(EmotionLabel), index=True)
    confidence: Mapped[float] = mapped_column(Float)
    # Store all scores as individual columns for query efficiency
    joy_score: Mapped[float] = mapped_column(Float, default=0.0)
    sadness_score: Mapped[float] = mapped_column(Float, default=0.0)
    fear_score: Mapped[float] = mapped_column(Float, default=0.0)
    anger_score: Mapped[float] = mapped_column(Float, default=0.0)
    surprise_score: Mapped[float] = mapped_column(Float, default=0.0)
    disgust_score: Mapped[float] = mapped_column(Float, default=0.0)
    neutral_score: Mapped[float] = mapped_column(Float, default=0.0)
    analyzed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="emotion_analyses")  # noqa: F821
    journal: Mapped["Journal | None"] = relationship(  # noqa: F821
        "Journal", back_populates="emotion_analyses"
    )
    chat_message: Mapped["ChatMessage | None"] = relationship(  # noqa: F821
        "ChatMessage", back_populates="emotion_analysis"
    )
