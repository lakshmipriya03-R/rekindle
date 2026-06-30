"""
Shared FastAPI dependency functions.
"""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Temporary debug version.
    Always returns the first active user.
    """

    user = (
        db.query(User)
        .filter(User.is_active == True)
        .first()
    )

    if user is None:
        raise Exception("No active user found.")

    return user