"""
Journal service.
All business logic for creating, reading, updating, deleting, and searching journals.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, extract
from app.models.journal import Journal
from app.models.emotion import EmotionAnalysis
from app.schemas.journal import JournalCreate, JournalUpdate, JournalRead, JournalListResponse
from app.core.exceptions import NotFoundException, ForbiddenException
from app.core.pagination import PaginationParams, paginate


def create_journal(user_id: int, payload: JournalCreate, db: Session) -> Journal:
    """Create a new journal entry for a user."""
    journal = Journal(
        user_id=user_id,
        title=payload.title,
        content=payload.content,
        mood_score=payload.mood_score,
    )
    db.add(journal)
    db.commit()
    db.refresh(journal)
    return journal


def get_journal(journal_id: int, user_id: int, db: Session) -> Journal:
    """Fetch a single journal entry, verifying ownership."""
    journal = db.query(Journal).filter(Journal.id == journal_id).first()
    if not journal:
        raise NotFoundException("Journal entry not found")
    if journal.user_id != user_id:
        raise ForbiddenException("You do not have access to this journal entry")
    return journal


def update_journal(journal_id: int, user_id: int, payload: JournalUpdate, db: Session) -> Journal:
    """Update journal fields that are provided in the payload."""
    journal = get_journal(journal_id, user_id, db)

    if payload.title is not None:
        journal.title = payload.title
    if payload.content is not None:
        journal.content = payload.content
    if payload.mood_score is not None:
        journal.mood_score = payload.mood_score

    db.commit()
    db.refresh(journal)
    return journal


def delete_journal(journal_id: int, user_id: int, db: Session) -> None:
    """Delete a journal entry, verifying ownership."""
    journal = get_journal(journal_id, user_id, db)
    db.delete(journal)
    db.commit()


def list_journals(
    user_id: int,
    db: Session,
    params: PaginationParams,
    search: str | None = None,
    emotion: str | None = None,
    month: int | None = None,
    year: int | None = None,
) -> JournalListResponse:
    """
    List journals with optional full-text search, emotion filter, and date filters.
    Returns paginated results.
    """
    query = db.query(Journal).filter(Journal.user_id == user_id)

    if search:
        term = f"%{search}%"
        query = query.filter(
            or_(Journal.title.ilike(term), Journal.content.ilike(term))
        )

    if emotion:
        query = query.join(
            EmotionAnalysis,
            EmotionAnalysis.journal_id == Journal.id,
        ).filter(EmotionAnalysis.dominant_emotion == emotion)

    if month:
        query = query.filter(extract("month", Journal.created_at) == month)

    if year:
        query = query.filter(extract("year", Journal.created_at) == year)

    query = query.order_by(Journal.created_at.desc())

    result = paginate(query, params)

    # Attach most recent emotion analysis to each journal
    items_with_emotion = []
    for journal in result["items"]:
        emotion_analysis = (
            db.query(EmotionAnalysis)
            .filter(EmotionAnalysis.journal_id == journal.id)
            .order_by(EmotionAnalysis.analyzed_at.desc())
            .first()
        )
        journal_data = JournalRead.model_validate(journal)
        if emotion_analysis:
            from app.schemas.emotion import EmotionRead
            journal_data.emotion = EmotionRead.model_validate(emotion_analysis)
        items_with_emotion.append(journal_data)

    return JournalListResponse(
        items=items_with_emotion,
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
    )
