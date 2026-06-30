"""
Authentication service.
Handles registration, login, token refresh, and logout.
"""
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.user import User, RefreshToken
from app.schemas.user import UserCreate, LoginRequest, TokenResponse, AccessTokenResponse
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token_str,
    decode_token,
)
from app.core.exceptions import (
    ConflictException,
    CredentialsException,
)
from app.config import get_settings
from jose import JWTError

settings = get_settings()


def register_user(payload: UserCreate, db: Session) -> TokenResponse:
    existing = db.query(User).filter(User.email == payload.email).first()

    if existing:
        raise ConflictException("An account with this email already exists")

    print("=" * 60)
    print("REGISTER PAYLOAD")
    print("Name     :", payload.full_name)
    print("Email    :", payload.email)
    print("Password :", repr(payload.password))
    print("Length   :", len(payload.password))
    print("=" * 60)

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return _issue_tokens(user, db)


def login_user(payload: LoginRequest, db: Session) -> TokenResponse:
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise CredentialsException("Invalid email or password")

    if not user.is_active:
        raise CredentialsException("Account is deactivated")

    return _issue_tokens(user, db)


def refresh_access_token(refresh_token: str, db: Session) -> AccessTokenResponse:
    try:
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise JWTError()

        user_id = int(payload["sub"])

    except Exception:
        raise CredentialsException("Invalid refresh token")

    stored = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == refresh_token,
            RefreshToken.user_id == user_id,
        )
        .first()
    )

    if not stored:
        raise CredentialsException("Refresh token not recognised")

    expires = stored.expires_at

    if expires.tzinfo is not None:
        expires = expires.replace(tzinfo=None)

    if expires < datetime.utcnow():
        db.delete(stored)
        db.commit()
        raise CredentialsException("Refresh token expired")

    access_token = create_access_token(user_id)

    return AccessTokenResponse(
        access_token=access_token
    )


def logout_user(refresh_token: str, db: Session):
    token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == refresh_token)
        .first()
    )

    if token:
        db.delete(token)
        db.commit()


def _issue_tokens(user: User, db: Session) -> TokenResponse:
    from app.schemas.user import UserRead

    access = create_access_token(user.id)
    refresh = create_refresh_token_str(user.id)

    refresh_db = RefreshToken(
        token=refresh,
        user_id=user.id,
        expires_at=datetime.utcnow()
        + timedelta(days=settings.refresh_token_expire_days),
    )

    db.add(refresh_db)
    db.commit()

    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        user=UserRead.model_validate(user),
    )