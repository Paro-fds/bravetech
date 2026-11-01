"""Tests d'intégration de l'API des candidatures (US-005) sur une base SQLite en mémoire.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.dal import models  # noqa: F401  (enregistre les tables)
from backend.dal.database import Base, get_db
from backend.dal.models import CandidatModel, CandidatureModel
from backend.main import app

URL = "/api/v1/candidatures"

SAISIE = {
    "nom": "Louis",
    "prenom": "Louismy",
    "date_naissance": "2008-05-14",
    "sexe": "M",
    "telephone": "37 12 34 56",
    "email": "louismy@exemple.com",
    "departement": "Ouest",
    "commune": "Pétion-Ville",
}


@pytest.fixture
def session_factory():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False)


@pytest.fixture
def client(session_factory):
    def _db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_creation_du_brouillon(client, session_factory):
    reponse = client.post(URL, json=SAISIE)
    assert reponse.status_code == 201
    data = reponse.json()
    assert data["statut"] == "brouillon"
    assert data["deplacement_physique"] is None
    assert data["informations"]["telephone"] == "+50937123456"
    assert data["informations"]["email"] == "louismy@exemple.com"
    assert "cursus_slug" not in data and "cursus_slug" not in data["informations"]

    with session_factory() as db:
        assert db.query(CandidatModel).count() == 1
        assert db.query(CandidatureModel).count() == 1


def test_validation_renvoie_un_message_par_champ(client, session_factory):
    reponse = client.post(URL, json={**SAISIE, "email": "x", "telephone": "1", "departement": "Atlantide"})
    assert reponse.status_code == 422
    assert set(reponse.json()["detail"]["erreurs"]) == {"email", "telephone", "departement"}
    with session_factory() as db:
        assert db.query(CandidatModel).count() == 0


def test_champ_manquant_est_refuse(client):
    incomplet = {k: v for k, v in SAISIE.items() if k != "nom"}
    assert client.post(URL, json=incomplet).status_code == 422


def test_doublon_email_campagne(client):
    assert client.post(URL, json=SAISIE).status_code == 201
    doublon = client.post(URL, json={**SAISIE, "nom": "Autre", "email": "LOUISMY@exemple.com"})
    assert doublon.status_code == 409


def test_reprise_du_brouillon(client):
    cree = client.post(URL, json=SAISIE).json()
    reponse = client.get(f"{URL}/{cree['candidature_id']}")
    assert reponse.status_code == 200
    assert reponse.json()["informations"]["nom"] == "Louis"


def test_brouillon_inconnu(client):
    assert client.get(f"{URL}/inconnu").status_code == 404
    assert client.put(f"{URL}/inconnu/deplacement-physique", json={"deplacement_physique": True}).status_code == 404


@pytest.mark.parametrize("reponse", [True, False])
def test_deplacement_physique_persiste(client, session_factory, reponse):
    cree = client.post(URL, json=SAISIE).json()
    resultat = client.put(f"{URL}/{cree['candidature_id']}/deplacement-physique", json={"deplacement_physique": reponse})
    assert resultat.status_code == 200
    assert resultat.json()["deplacement_physique"] is reponse
    assert client.get(f"{URL}/{cree['candidature_id']}").json()["deplacement_physique"] is reponse

    with session_factory() as db:
        assert db.query(CandidatureModel).one().deplacement_physique is reponse


@pytest.mark.parametrize("corps", [{}, {"deplacement_physique": None}, {"deplacement_physique": "oui"}, {"deplacement_physique": 1}])
def test_deplacement_physique_obligatoire(client, corps):
    cree = client.post(URL, json=SAISIE).json()
    assert client.put(f"{URL}/{cree['candidature_id']}/deplacement-physique", json=corps).status_code == 422


def test_modification_des_informations(client):
    cree = client.post(URL, json=SAISIE).json()
    reponse = client.put(f"{URL}/{cree['candidature_id']}/informations", json={**SAISIE, "commune": "Delmas"})
    assert reponse.status_code == 200
    assert reponse.json()["informations"]["commune"] == "Delmas"


def test_modification_vers_email_deja_pris(client):
    client.post(URL, json=SAISIE)
    autre = client.post(URL, json={**SAISIE, "email": "autre@exemple.com"}).json()
    reponse = client.put(f"{URL}/{autre['candidature_id']}/informations", json=SAISIE)
    assert reponse.status_code == 409
