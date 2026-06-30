"""
SQLAlchemy declarative base shared by all models.
Importing the models registers them with SQLAlchemy so
Base.metadata.create_all() can create every table.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Register all models
from app.models.user import User
from app.models.journal import Journal
from app.models.chat import ConversationSession, ChatMessage
from app.models.emotion import EmotionAnalysis