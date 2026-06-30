"""
Chat router.
Routes:
/chat/sessions
/chat/message
"""

from fastapi import APIRouter, Depends, Query, status, Body
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User

from app.schemas.chat import (
    SessionCreate,
    SessionRead,
    MessageCreate,
    ChatResponse,
    SessionWithMessages,
)

from app.services.chat_service import (
    create_session,
    get_sessions,
    get_session_with_messages,
    send_message,
    rename_session,
    delete_session,
)

from app.core.pagination import PaginationParams

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/sessions", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
def new_session(
    payload: SessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_session(current_user.id, payload, db)


@router.get("/sessions", response_model=dict)
def list_sessions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    params = PaginationParams(page=page, page_size=page_size)
    return get_sessions(current_user.id, db, params)


@router.get("/sessions/{session_id}", response_model=SessionWithMessages)
def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_session_with_messages(session_id, current_user.id, db)


@router.post("/message", response_model=ChatResponse)
def message(
    payload: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return send_message(
        user_id=current_user.id,
        content=payload.content,
        db=db,
        session_id=payload.session_id,
    )


# ----------------------------
# Rename Conversation
# ----------------------------
@router.patch("/sessions/{session_id}", response_model=SessionRead)
def rename_chat(
    session_id: int,
    title: str = Body(..., embed=True),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return rename_session(
        session_id=session_id,
        user_id=current_user.id,
        title=title,
        db=db,
    )


# ----------------------------
# Delete Conversation
# ----------------------------
@router.delete("/sessions/{session_id}")
def remove_chat(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_session(
        session_id=session_id,
        user_id=current_user.id,
        db=db,
    )