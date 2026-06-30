"""
Chat service.
Manages conversation sessions and message exchange with the AI companion.
"""

from sqlalchemy.orm import Session

from app.models.chat import ConversationSession, ChatMessage
from app.schemas.chat import (
    SessionCreate,
    ChatResponse,
    MessageRead,
    SessionWithMessages,
    SessionRead,
)
from app.core.exceptions import NotFoundException, ForbiddenException
from app.core.pagination import PaginationParams, paginate


def create_session(user_id: int, payload: SessionCreate, db: Session) -> ConversationSession:
    """Create a new conversation session for a user."""
    session = ConversationSession(
        user_id=user_id,
        title=payload.title,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def get_sessions(user_id: int, db: Session, params: PaginationParams) -> dict:
    """List all conversation sessions for a user."""

    query = (
        db.query(ConversationSession)
        .filter(ConversationSession.user_id == user_id)
        .order_by(ConversationSession.updated_at.desc())
    )

    result = paginate(query, params)

    result["items"] = [
        SessionRead.model_validate(item)
        for item in result["items"]
    ]

    return result


def get_session_with_messages(
    session_id: int,
    user_id: int,
    db: Session,
) -> ConversationSession:
    """Fetch a session with its messages."""

    session = (
        db.query(ConversationSession)
        .filter(ConversationSession.id == session_id)
        .first()
    )

    if not session:
        raise NotFoundException("Conversation session not found")

    if session.user_id != user_id:
        raise ForbiddenException("You do not have access to this session")

    return session


# -----------------------------
# NEW FEATURE
# Rename Conversation
# -----------------------------
def rename_session(
    session_id: int,
    user_id: int,
    title: str,
    db: Session,
):
    session = get_session_with_messages(session_id, user_id, db)

    session.title = title.strip()

    db.commit()
    db.refresh(session)

    return SessionRead.model_validate(session)


# -----------------------------
# NEW FEATURE
# Delete Conversation
# -----------------------------
def delete_session(
    session_id: int,
    user_id: int,
    db: Session,
):
    session = get_session_with_messages(session_id, user_id, db)

    db.query(ChatMessage).filter(
        ChatMessage.session_id == session.id
    ).delete()

    db.delete(session)
    db.commit()

    return {"message": "Conversation deleted successfully"}


def send_message(
    user_id: int,
    content: str,
    db: Session,
    session_id: int | None = None,
) -> ChatResponse:
    """
    Process a user message.
    """

    from app.ai.context_builder import build_chat_context
    from app.ai.base import get_ai_provider
    from app.services.emotion_service import analyze_and_store
    from app.models.emotion import SourceType

    if session_id:
        session = get_session_with_messages(session_id, user_id, db)
    else:
        session = ConversationSession(
            user_id=user_id,
            title=_generate_session_title(content),
        )

        db.add(session)
        db.commit()
        db.refresh(session)

    user_msg = ChatMessage(
        session_id=session.id,
        role="user",
        content=content,
    )

    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    messages_history = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session.id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    context = build_chat_context(
        user_id=user_id,
        messages=messages_history,
        db=db,
    )

    provider = get_ai_provider()

    ai_response = provider.complete(messages=context)

    assistant_msg = ChatMessage(
        session_id=session.id,
        role="assistant",
        content=ai_response,
    )

    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)

    analyze_and_store(
        user_id=user_id,
        text=content,
        source_type=SourceType.chat,
        db=db,
        chat_message_id=user_msg.id,
    )

    return ChatResponse(
        session_id=session.id,
        user_message=MessageRead.model_validate(user_msg),
        assistant_message=MessageRead.model_validate(assistant_msg),
    )


def _generate_session_title(first_message: str) -> str:
    """Generate a session title from first message."""
    return first_message[:60] + "..." if len(first_message) > 60 else first_message