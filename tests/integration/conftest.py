"""Fixtures communes des tests d'intégration : base SQLite en mémoire et stockage de fichiers temporaire.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.api.v1.candidatures import get_stockage_fichiers
from backend.api.v1.limiteur import limiteur_envois, limiteur_suivi
from backend.dal import models  # noqa: F401  (enregistre les tables)
from backend.dal.database import Base, get_db
from backend.dal.stockage_local import StockageLocal
from backend.main import app


@pytest.fixture
def session_factory():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False)


@pytest.fixture
def dossier_uploads(tmp_path):
    """Dossier temporaire servant de racine au stockage local pendant un test."""
    return tmp_path / "uploads"


@pytest.fixture
def client(session_factory, dossier_uploads):
    def _db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _db
    app.dependency_overrides[get_stockage_fichiers] = lambda: StockageLocal(dossier_uploads)
    limiteur_envois.reinitialiser()  # chaque test repart avec des compteurs de débit vides
    limiteur_suivi.reinitialiser()
    yield TestClient(app)
    app.dependency_overrides.clear()
    limiteur_envois.reinitialiser()
    limiteur_suivi.reinitialiser()
