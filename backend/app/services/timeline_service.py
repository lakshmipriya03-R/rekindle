"""
Timeline service.
Merges journal entries and emotion events into a chronological feed.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.journal import Journal
from app.models.emotion import EmotionAnalysis, SourceType
from app.core.pagination import PaginationParams


def get_timeline(user_id: int, db: Session, params: PaginationParams) -> dict:
    """
    Build a unified timeline of journal entries ordered by date.
    Each item includes the associated emotion if available.
    """
    from app.schemas.journal import JournalRead
    from app.schemas.emotion import EmotionRead

    query = (
        db.query(Journal)
        .filter(Journal.user_id == user_id)
        .order_by(Journal.created_at.desc())
    )

    total = query.count()
    journals = query.offset(params.offset).limit(params.page_size).all()

    items = []
    for journal in journals:
        emotion = (
            db.query(EmotionAnalysis)
            .filter(
                EmotionAnalysis.journal_id == journal.id,
                EmotionAnalysis.source_type == SourceType.journal,
            )
            .order_by(EmotionAnalysis.analyzed_at.desc())
            .first()
        )
        journal_data = JournalRead.model_validate(journal)
        if emotion:
            journal_data.emotion = EmotionRead.model_validate(emotion)

        items.append({
            "type": "journal",
            "date": journal.created_at.isoformat(),
            "data": journal_data,
        })

    import math
    return {
        "items": items,
        "total": total,
        "page": params.page,
        "page_size": params.page_size,
        "total_pages": math.ceil(total / params.page_size) if total > 0 else 0,
    }
