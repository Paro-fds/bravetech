"""Tests d'intégration pour les routes API de Cursus.
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_lister_cursus():
    response = client.get("/api/v1/cursus")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5

    # Vérification que le premier élément est MPC (selon notre règle métier)
    assert data[0]["id"] == "mpc"

    # Vérification des champs requis par US-001
    premier = data[0]
    assert "id" in premier
    assert "nom" in premier
    assert "description_courte" in premier
    assert "date_ouverture_inscription" in premier
    assert "date_fermeture_inscription" in premier
    assert "est_ouvert" in premier


def test_obtenir_cursus_existant():
    response = client.get("/api/v1/cursus/genie-civil")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "genie-civil"
    assert data["nom"] == "Génie Civil"
    assert "niveaux" in data
    assert "GC1" in data["niveaux"]


def test_obtenir_cursus_inexistant():
    response = client.get("/api/v1/cursus/filiere-inconnue")
    assert response.status_code == 404
