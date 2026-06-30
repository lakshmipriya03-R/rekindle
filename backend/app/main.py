from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database.base import Base
from app.database.database import engine

# IMPORTANT: Import models so SQLAlchemy registers them
from app.models.user import User
from app.models.journal import Journal
from app.models.chat import ConversationSession, ChatMessage
from app.models.emotion import EmotionAnalysis

from app.routers import (
    auth_router,
    journals_router,
    emotions_router,
    chat_router,
    dashboard_router,
    timeline_router,
    users_router,
)

settings = get_settings()


def create_app():
    app = FastAPI(
        title="Rekindle API",
        version="1.0.0",
    )

    Base.metadata.create_all(bind=engine)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)
    app.include_router(journals_router)
    app.include_router(emotions_router)
    app.include_router(chat_router)
    app.include_router(dashboard_router)
    app.include_router(timeline_router)
    app.include_router(users_router)

    @app.get("/")
    def health():
        return {"status": "ok"}

    return app


app = create_app()