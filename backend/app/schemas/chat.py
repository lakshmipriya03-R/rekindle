"""
Pydantic schemas for Chat endpoints.
"""
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SessionCreate(BaseModel):
    title: str = "New Conversation"


class SessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class MessageCreate(BaseModel):
    content: str
    session_id: int | None = None  # None = create new session


class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    role: str
    content: str
    created_at: datetime


class ChatResponse(BaseModel):
    session_id: int
    user_message: MessageRead
    assistant_message: MessageRead


class SessionWithMessages(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    is_active: bool
    created_at: datetime
    messages: list[MessageRead]
