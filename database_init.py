"""
database/__init__.py
Database package initialization
"""

from database.connection import engine, SessionLocal, init_db
from database.models import Base, User, Prediction, SpamModel, ApiKey
from database.schemas import *

__all__ = [
    "engine",
    "SessionLocal",
    "init_db",
    "Base",
    "User",
    "Prediction",
    "SpamModel",
    "ApiKey",
]
