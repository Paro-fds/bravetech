"""Tests d'intégration de l'API des candidatures (US-005) sur une base SQLite en mémoire.
"""

import pytest

from backend.dal.models import CandidatModel, CandidatureModel

# Les fixtures `client` et `session_factory` viennent de tests/integration/conftest.py

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


# --- US-006 : paiement simulé ---------------------------------------------------------------

def _brouillon_pret(client, deplacement=False):
    cree = client.post(URL, json=SAISIE).json()
    if deplacement is not None:
        client.put(f"{URL}/{cree['candidature_id']}/deplacement-physique", json={"deplacement_physique": deplacement})
    return cree["candidature_id"]


def test_brouillon_expose_le_montant_et_un_paiement_en_attente(client):
    cree = client.post(URL, json=SAISIE).json()
    assert cree["montant_htg"] == 500
    assert cree["statut_paiement"] == "en_attente"
    assert cree["reference_paiement"] is None
    assert cree["methode_paiement"] is None


@pytest.mark.parametrize("methode, attendu", [("MONCASH", "MONCASH"), ("natcash", "NATCASH")])
def test_simulation_de_paiement(client, session_factory, methode, attendu):
    cid = _brouillon_pret(client)
    reponse = client.post(f"{URL}/{cid}/paiement", json={"methode": methode, "numero_telephone": "37 12 34 56"})
    assert reponse.status_code == 200
    data = reponse.json()
    assert data["statut_paiement"] == "SIMULE_PAYE"
    assert data["methode_paiement"] == attendu
    assert data["montant_htg"] == 500
    assert data["reference_paiement"].startswith("PAY-SIM-2026-") and len(data["reference_paiement"]) == 17

    # Le paiement est attaché à la candidature et retrouvé à la reprise
    reprise = client.get(f"{URL}/{cid}").json()
    assert reprise["reference_paiement"] == data["reference_paiement"]
    with session_factory() as db:
        ligne = db.query(CandidatureModel).one()
        assert ligne.statut_paiement == "SIMULE_PAYE"
        assert ligne.numero_paiement == "+50937123456"


def test_simulation_idempotente(client):
    cid = _brouillon_pret(client)
    corps = {"methode": "MONCASH", "numero_telephone": "37123456"}
    premiere = client.post(f"{URL}/{cid}/paiement", json=corps).json()
    seconde = client.post(f"{URL}/{cid}/paiement", json={"methode": "NATCASH", "numero_telephone": "47123456"}).json()
    assert seconde["reference_paiement"] == premiere["reference_paiement"]
    assert seconde["methode_paiement"] == "MONCASH"


def test_references_differentes_pour_deux_candidats(client):
    refs = set()
    for email in ("a@exemple.com", "b@exemple.com", "c@exemple.com"):
        cree = client.post(URL, json={**SAISIE, "email": email}).json()
        cid = cree["candidature_id"]
        client.put(f"{URL}/{cid}/deplacement-physique", json={"deplacement_physique": False})
        refs.add(client.post(f"{URL}/{cid}/paiement", json={"methode": "MONCASH", "numero_telephone": "37123456"}).json()["reference_paiement"])
    assert len(refs) == 3


def test_simulation_validation(client):
    cid = _brouillon_pret(client)
    reponse = client.post(f"{URL}/{cid}/paiement", json={"methode": "PAYPAL", "numero_telephone": "123"})
    assert reponse.status_code == 422
    assert set(reponse.json()["detail"]["erreurs"]) == {"methode_paiement", "numero_telephone"}
    assert client.get(f"{URL}/{cid}").json()["statut_paiement"] == "en_attente"


def test_simulation_refusee_avant_la_question_de_deplacement(client):
    cid = _brouillon_pret(client, deplacement=None)
    reponse = client.post(f"{URL}/{cid}/paiement", json={"methode": "MONCASH", "numero_telephone": "37123456"})
    assert reponse.status_code == 409


def test_simulation_brouillon_inconnu(client):
    reponse = client.post(f"{URL}/inconnu/paiement", json={"methode": "MONCASH", "numero_telephone": "37123456"})
    assert reponse.status_code == 404
