"""
Pydantic schemas for Journal endpoints.
"""
from datetime import datetime
from pydantic import BaseModel, field_validator, ConfigDict
from app.schemas.emotion import EmotionRead


class JournalCreate(BaseModel):
    title: str
    content: str
    mood_score: int | None = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v.strip()

    @field_validator("mood_score")
    @classmethod
    def mood_in_range(cls, v: int | None) -> int | None:
        if v is not None and not (1 <= v <= 10):
            raise ValueError("Mood score must be between 1 and 10")
        return v


class JournalUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    mood_score: int | None = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v

    @field_validator("mood_score")
    @classmethod
    def mood_in_range(cls, v: int | None) -> int | None:
        if v is not None and not (1 <= v <= 10):
            raise ValueError("Mood score must be between 1 and 10")
        return v


class JournalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    mood_score: int | None
    created_at: datetime
    updated_at: datetime
    emotion: EmotionRead | None = None


class JournalListResponse(BaseModel):
    items: list[JournalRead]
    total: int
    page: int
    page_size: int
    total_pages: int
