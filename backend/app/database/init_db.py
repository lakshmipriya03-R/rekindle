"""
Initialize the database by creating all tables.
"""

from app.database.base import Base
from app.database.session import engine

# Import all models so SQLAlchemy registers them
from app.models.user import User
from app.models.journal import Journal
from app.models.chat import ConversationSession, ChatMessage
from app.models.emotion import EmotionAnalysis

Base.metadata.create_all(bind=engine)

print("Database created successfully.")