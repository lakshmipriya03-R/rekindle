"""
User service.
Handles profile updates, password change, and account deletion.
"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserUpdate, PasswordChange, UserRead
from app.core.security import hash_password, verify_password
from app.core.exceptions import BadRequestException, CredentialsException


def update_profile(user: User, payload: UserUpdate, db: Session) -> UserRead:
    """Update the user's profile fields."""
    if payload.full_name is not None:
        user.full_name = payload.full_name
    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user)


def change_password(user: User, payload: PasswordChange, db: Session) -> None:
    """Verify current password then update to new password."""
    if not verify_password(payload.current_password, user.hashed_password):
        raise CredentialsException("Current password is incorrect")
    user.hashed_password = hash_password(payload.new_password)
    db.commit()


def delete_account(user: User, db: Session) -> None:
    """
    Permanently delete the user account and all associated data.
    Cascade deletes handle journals, sessions, emotions, tokens.
    """
    db.delete(user)
    db.commit()
