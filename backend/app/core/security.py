"""
Security utilities: JWT token creation/verification and password hashing.
"""

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import get_settings

settings = get_settings()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    if not isinstance(password, str):
        raise ValueError("Password must be a string")

    password = password.strip()

    print("=" * 60)
    print("PASSWORD RECEIVED:", repr(password))
    print("PASSWORD LENGTH :", len(password))
    print("=" * 60)

    if len(password) > 72:
        raise ValueError("Password cannot exceed 72 characters.")

    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain.strip(), hashed)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def create_refresh_token_str(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def decode_token(token: str):
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )


def get_user_id_from_token(token: str) -> int:
    payload = decode_token(token)

    if payload.get("type") != "access":
        raise JWTError("Invalid token")

    return int(payload["sub"])
