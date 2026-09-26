"""Configuration de la base de données — Couche DAL (Data Access Layer).

Supporte PostgreSQL en production/cible et SQLite en local / dev rapide.
"""

import os
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Chemin par défaut pour SQLite en local
DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "bravetech.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

# Si SQLite, activer check_same_thread=False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Générateur de session SQLAlchemy pour injection de dépendances."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
