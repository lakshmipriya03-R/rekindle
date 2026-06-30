"""
Authentication router.
Routes: /auth/register, /auth/login, /auth/refresh, /auth/logout
No business logic — delegates entirely to auth_service.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.user import (
    UserCreate, LoginRequest, TokenResponse,
    RefreshRequest, AccessTokenResponse,
)
from app.services.auth_service import register_user, login_user, refresh_access_token, logout_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account and return JWT tokens."""
    return register_user(payload, db)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate credentials and return JWT tokens."""
    return login_user(payload, db)


@router.post("/refresh", response_model=AccessTokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    """Exchange a valid refresh token for a new access token."""
    return refresh_access_token(payload.refresh_token, db)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: RefreshRequest, db: Session = Depends(get_db)):
    """Revoke a refresh token to log out the current session."""
    logout_user(payload.refresh_token, db)
