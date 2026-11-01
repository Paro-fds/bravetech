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

    # Admission unique (ADR-008) : seul le MPC est le cursus d'admission
    assert data[0]["est_admission"] is True
    assert [c["id"] for c in data if c["est_admission"]] == ["mpc"]

    # Vérification des champs requis par US-001
    premier = data[0]
    assert "id" in premier
    assert "nom" in premier
    assert "description_courte" in premier
    assert "date_ouverture_inscription" in premier
    assert "date_fermeture_inscription" in premier
    assert "est_ouvert" in premier


def test_obtenir_branche_sans_pieces_requises():
    response = client.get("/api/v1/cursus/genie-civil")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "genie-civil"
    assert data["nom"] == "Génie Civil"
    assert data["est_admission"] is False
    assert "niveaux" in data
    assert "GC1" in data["niveaux"]

    # Admission unique (ADR-008) : une branche n'exige aucune pièce
    assert data["documents_requis"] == []


def test_obtenir_mpc_avec_les_cinq_pieces_requises():
    response = client.get("/api/v1/cursus/mpc")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "mpc"
    assert data["est_admission"] is True
    assert "MPC1" in data["niveaux"]

    # Liste unique de 5 pièces obligatoires (US-002, US-018)
    assert "documents_requis" in data
    assert isinstance(data["documents_requis"], list)
    assert len(data["documents_requis"]) == 5
    assert all(p["est_obligatoire"] for p in data["documents_requis"])

    texte = " ".join(p["nom"] for p in data["documents_requis"]).lower()
    assert "cin" in texte
    assert "bonne vie" not in texte
    assert "médical" not in texte

    premiere_piece = data["documents_requis"][0]
    assert "id" in premiere_piece
    assert "nom" in premiere_piece
    assert "description" in premiere_piece
    assert "format_accepte" in premiere_piece
    assert "taille_max_mo" in premiere_piece
    assert "est_obligatoire" in premiere_piece


def test_obtenir_cursus_inexistant():
    response = client.get("/api/v1/cursus/filiere-inconnue")
    assert response.status_code == 404
    assert "introuvable" in response.json()["detail"]
