"""
Rekindle — FastAPI application entry point.
Creates the app, registers middleware, and includes all routers.
"""
from app.database.base import Base
from app.database.session import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database.base import Base          # <-- ADD
from app.database.database import engine    # <-- ADD

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


def create_app() -> FastAPI:
    app = FastAPI(
        title="Rekindle API",
        description="AI Life Journal for Dementia and Alzheimer's Patients",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
Base.metadata.create_all(bind=engine)

    # Create database tables on startup
    Base.metadata.create_all(bind=engine)   # <-- ADD

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

    @app.get("/", tags=["Health"])
    def health():
        return {"status": "ok", "app": settings.app_name}

    return app


app = create_app()