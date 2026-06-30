"""
Emotions router.
Routes: /emotions (search, stats, trends)
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.emotion import EmotionStats
from app.services.emotion_service import search_emotions, get_emotion_stats, get_emotion_trends
from app.core.pagination import PaginationParams

router = APIRouter(prefix="/emotions", tags=["Emotions"])


@router.get("/stats", response_model=EmotionStats)
def stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return aggregate emotion statistics for the authenticated user."""
    return get_emotion_stats(current_user.id, db)


@router.get("/trends")
def trends(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return daily emotion trend data for charting."""
    return get_emotion_trends(current_user.id, db)


@router.get("")
def search(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    emotion: str | None = Query(None, description="Filter by emotion label"),
    source_type: str | None = Query(None, description="journal | chat"),
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = Query(None, ge=2000, le=2100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Search emotion analyses with filters. Returns paginated results."""
    params = PaginationParams(page=page, page_size=page_size)
    result = search_emotions(current_user.id, db, params, emotion=emotion, source_type=source_type, month=month, year=year)
    return result
