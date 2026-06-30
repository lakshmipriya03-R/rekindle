"""
Emotion service.
Runs emotion detection on text and stores/queries results.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.emotion import EmotionAnalysis, EmotionLabel, SourceType
from app.schemas.emotion import EmotionStats, EmotionSearchResult
from app.core.pagination import PaginationParams, paginate


def analyze_and_store(
    user_id: int,
    text: str,
    source_type: SourceType,
    db: Session,
    journal_id: int | None = None,
    chat_message_id: int | None = None,
) -> EmotionAnalysis:
    """
    Run the emotion detector on text and persist the results.
    Called after journal creation/update and after each chat message.
    """
    from app.ai.emotion_detector import get_emotion_detector

    detector = get_emotion_detector()
    scores = detector.analyze(text)

    # Find dominant emotion
    dominant = max(scores, key=scores.get)

    analysis = EmotionAnalysis(
        user_id=user_id,
        journal_id=journal_id,
        chat_message_id=chat_message_id,
        source_type=source_type,
        dominant_emotion=EmotionLabel(dominant),
        confidence=scores[dominant],
        joy_score=scores.get("joy", 0.0),
        sadness_score=scores.get("sadness", 0.0),
        fear_score=scores.get("fear", 0.0),
        anger_score=scores.get("anger", 0.0),
        surprise_score=scores.get("surprise", 0.0),
        disgust_score=scores.get("disgust", 0.0),
        neutral_score=scores.get("neutral", 0.0),
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


def search_emotions(
    user_id: int,
    db: Session,
    params: PaginationParams,
    emotion: str | None = None,
    source_type: str | None = None,
    month: int | None = None,
    year: int | None = None,
) -> dict:
    """Search emotion analyses by various filters."""
    from sqlalchemy import extract

    query = db.query(EmotionAnalysis).filter(EmotionAnalysis.user_id == user_id)

    if emotion:
        query = query.filter(EmotionAnalysis.dominant_emotion == emotion)

    if source_type:
        query = query.filter(EmotionAnalysis.source_type == source_type)

    if month:
        query = query.filter(extract("month", EmotionAnalysis.analyzed_at) == month)

    if year:
        query = query.filter(extract("year", EmotionAnalysis.analyzed_at) == year)

    query = query.order_by(EmotionAnalysis.analyzed_at.desc())
    return paginate(query, params)


def get_emotion_stats(user_id: int, db: Session) -> EmotionStats:
    """Aggregate emotion statistics for the dashboard."""
    analyses = db.query(EmotionAnalysis).filter(EmotionAnalysis.user_id == user_id).all()

    if not analyses:
        return EmotionStats(
            total_entries=0,
            emotion_distribution={},
            dominant_overall=None,
            average_joy=0.0,
            average_sadness=0.0,
            average_fear=0.0,
            average_anger=0.0,
            average_neutral=0.0,
        )

    distribution: dict[str, int] = {}
    for a in analyses:
        key = a.dominant_emotion.value
        distribution[key] = distribution.get(key, 0) + 1

    dominant_overall = max(distribution, key=distribution.get) if distribution else None
    total = len(analyses)

    return EmotionStats(
        total_entries=total,
        emotion_distribution=distribution,
        dominant_overall=dominant_overall,
        average_joy=sum(a.joy_score for a in analyses) / total,
        average_sadness=sum(a.sadness_score for a in analyses) / total,
        average_fear=sum(a.fear_score for a in analyses) / total,
        average_anger=sum(a.anger_score for a in analyses) / total,
        average_neutral=sum(a.neutral_score for a in analyses) / total,
    )


def get_emotion_trends(user_id: int, db: Session) -> list[dict]:
    """Return daily emotion counts for trend charts."""
    from sqlalchemy import cast, Date

    rows = (
        db.query(
            cast(EmotionAnalysis.analyzed_at, Date).label("date"),
            EmotionAnalysis.dominant_emotion,
            func.count().label("count"),
        )
        .filter(EmotionAnalysis.user_id == user_id)
        .group_by("date", EmotionAnalysis.dominant_emotion)
        .order_by("date")
        .all()
    )

    return [
        {"date": str(row.date), "dominant_emotion": row.dominant_emotion.value, "count": row.count}
        for row in rows
    ]
