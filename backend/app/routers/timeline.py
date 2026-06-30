"""
Timeline router.
Routes: /timeline
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.timeline_service import get_timeline
from app.core.pagination import PaginationParams

router = APIRouter(prefix="/timeline", tags=["Timeline"])


@router.get("")
def timeline(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return a chronological timeline of journal entries with emotions."""
    params = PaginationParams(page=page, page_size=page_size)
    return get_timeline(current_user.id, db, params)
