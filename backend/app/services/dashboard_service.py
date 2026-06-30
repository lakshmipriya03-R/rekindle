"""
Dashboard service.
Aggregates statistics for the main dashboard view.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.journal import Journal
from app.models.emotion import EmotionAnalysis
from app.models.chat import ConversationSession, ChatMessage


def get_dashboard_stats(user_id: int, db: Session) -> dict:
    """
    Returns aggregated statistics for the dashboard:
    - Total journals
    - Total conversations
    - Total messages
    - Emotion distribution
    - Recent journal entries
    - Recent sessions
    """
    from app.schemas.journal import JournalRead
    from app.schemas.chat import SessionRead

    total_journals = db.query(func.count(Journal.id)).filter(Journal.user_id == user_id).scalar()
    total_sessions = (
        db.query(func.count(ConversationSession.id))
        .filter(ConversationSession.user_id == user_id)
        .scalar()
    )
    total_messages = (
        db.query(func.count(ChatMessage.id))
        .join(ConversationSession, ConversationSession.id == ChatMessage.session_id)
        .filter(ConversationSession.user_id == user_id)
        .scalar()
    )

    # Emotion distribution (last 30 days)
    from datetime import datetime, timedelta, timezone
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)

    emotion_rows = (
        db.query(EmotionAnalysis.dominant_emotion, func.count().label("count"))
        .filter(
            EmotionAnalysis.user_id == user_id,
            EmotionAnalysis.analyzed_at >= thirty_days_ago,
        )
        .group_by(EmotionAnalysis.dominant_emotion)
        .all()
    )
    emotion_distribution = {row.dominant_emotion.value: row.count for row in emotion_rows}

    # Recent journals (5)
    recent_journals = (
        db.query(Journal)
        .filter(Journal.user_id == user_id)
        .order_by(Journal.created_at.desc())
        .limit(5)
        .all()
    )

    # Recent sessions (5)
    recent_sessions = (
        db.query(ConversationSession)
        .filter(ConversationSession.user_id == user_id)
        .order_by(ConversationSession.updated_at.desc())
        .limit(5)
        .all()
    )

    # Mood trend (last 30 days, from journals with mood_score)
    mood_trend_rows = (
        db.query(
            func.date(Journal.created_at).label("date"),
            func.avg(Journal.mood_score).label("avg_mood"),
        )
        .filter(
            Journal.user_id == user_id,
            Journal.mood_score.isnot(None),
            Journal.created_at >= thirty_days_ago,
        )
        .group_by(func.date(Journal.created_at))
        .order_by(func.date(Journal.created_at))
        .all()
    )
    mood_trend = [
        {"date": str(row.date), "avg_mood": round(float(row.avg_mood), 2)}
        for row in mood_trend_rows
    ]

    return {
        "total_journals": total_journals,
        "total_sessions": total_sessions,
        "total_messages": total_messages,
        "emotion_distribution_30d": emotion_distribution,
        "mood_trend_30d": mood_trend,
        "recent_journals": [JournalRead.model_validate(j) for j in recent_journals],
        "recent_sessions": [SessionRead.model_validate(s) for s in recent_sessions],
    }
