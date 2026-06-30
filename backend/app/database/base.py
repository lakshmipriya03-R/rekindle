"""
SQLAlchemy declarative base shared by all models.
Import Base here to avoid circular imports.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
