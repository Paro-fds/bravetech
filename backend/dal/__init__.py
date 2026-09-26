"""Couche DAL (Data Access Layer) — Adapters d'infrastructure (SQLAlchemy, Cloudinary, Resend).
"""

from backend.dal.database import get_db, SessionLocal, Base, engine
from backend.dal.cursus_repository_json import JsonCursusRepository

__all__ = ["get_db", "SessionLocal", "Base", "engine", "JsonCursusRepository"]
