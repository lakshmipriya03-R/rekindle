"""
Journals router.
Routes: /journals (CRUD, search, pagination)
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.journal import JournalCreate, JournalUpdate, JournalRead, JournalListResponse
from app.services.journal_service import (
    create_journal, get_journal, update_journal, delete_journal, list_journals,
)
from app.services.emotion_service import analyze_and_store
from app.models.emotion import SourceType
from app.core.pagination import PaginationParams

router = APIRouter(prefix="/journals", tags=["Journals"])


@router.post("", response_model=JournalRead, status_code=status.HTTP_201_CREATED)
def create(
    payload: JournalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new journal entry and run emotion detection on the content."""
    journal = create_journal(current_user.id, payload, db)
    analyze_and_store(
        user_id=current_user.id,
        text=f"{payload.title}. {payload.content}",
        source_type=SourceType.journal,
        db=db,
        journal_id=journal.id,
    )
    return journal


@router.get("", response_model=JournalListResponse)
def list_all(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = Query(None, description="Full-text search across title and content"),
    emotion: str | None = Query(None, description="Filter by dominant emotion"),
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = Query(None, ge=2000, le=2100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List journals with optional filters. Supports pagination."""
    params = PaginationParams(page=page, page_size=page_size)
    return list_journals(current_user.id, db, params, search=search, emotion=emotion, month=month, year=year)


@router.get("/{journal_id}", response_model=JournalRead)
def get_one(
    journal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve a single journal entry by ID."""
    return get_journal(journal_id, current_user.id, db)


@router.patch("/{journal_id}", response_model=JournalRead)
def update(
    journal_id: int,
    payload: JournalUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a journal entry. Re-runs emotion detection if content changes."""
    journal = update_journal(journal_id, current_user.id, payload, db)
    if payload.content:
        analyze_and_store(
            user_id=current_user.id,
            text=f"{journal.title}. {journal.content}",
            source_type=SourceType.journal,
            db=db,
            journal_id=journal.id,
        )
    return journal


@router.delete("/{journal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    journal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a journal entry and all associated emotion data."""
    delete_journal(journal_id, current_user.id, db)
