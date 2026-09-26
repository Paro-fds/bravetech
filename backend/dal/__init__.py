"""Couche DAL (Data Access Layer) — Adapters d'infrastructure (SQLAlchemy, Cloudinary, Resend).
"""

from backend.dal.database import get_db, SessionLocal, Base, engine
from backend.dal.models import CursusModel
from backend.dal.cursus_repository_sql import SQLAlchemyCursusRepository

__all__ = ["get_db", "SessionLocal", "Base", "engine", "CursusModel", "SQLAlchemyCursusRepository"]
