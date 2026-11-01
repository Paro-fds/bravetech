"""Tests d'intégration de la soumission définitive (US-008) : base SQLite en mémoire, stockage temporaire.
"""

import logging
import re

import pytest

from backend.api.v1.candidatures import get_email_sender
from backend.api.v1.limiteur import limiteur_envois
from backend.dal.models import CandidatureModel
from backend.main import app
from backend.ports.email_sender import IEmailSender

from tests.integration.test_candidatures_api import SAISIE, URL
from tests.integration.test_documents_api import LES_CINQ, PHOTOS
from tests.unit.bll.fakes_documents import JPG, PDF


class EmailEnregistreur(IEmailSender):
    def __init__(self):
        self.messages = []

    def envoyer(self, message):
        self.messages.append(message)


class EmailEnPanne(IEmailSender):
    def envoyer(self, message):
        raise ConnectionError("Resend indisponible")


@pytest.fixture
def emails():
    enregistreur = EmailEnregistreur()
    app.dependency_overrides[get_email_sender] = lambda: enregistreur
    return enregistreur


def _dossier(client, email="louismy@exemple.com", pieces=LES_CINQ, paye=True):
    """Construit un dossier par l'API : informations, déplacement, paiement simulé, puis les pièces données."""
    cid = client.post(URL, json={**SAISIE, "email": email}).json()["candidature_id"]
    client.put(f"{URL}/{cid}/deplacement-physique", json={"deplacement_physique": False})
    if paye:
        client.post(f"{URL}/{cid}/paiement", json={"methode": "NATCASH", "numero_telephone": "47123456"})
        for piece in pieces:
            nom, contenu = ("photos.jpg", JPG) if piece == PHOTOS else (f"{piece}.pdf", PDF)
            client.post(f"{URL}/{cid}/documents/{piece}", files={"fichier": (nom, contenu, "application/octet-stream")})
    return cid


def test_soumission_complete(client, emails, session_factory):
    cid = _dossier(client)
    reponse = client.post(f"{URL}/{cid}/soumission")
    assert reponse.status_code == 200
    data = reponse.json()
    assert re.fullmatch(r"CAN-2026-\d{4}", data["reference_dossier"])
    assert data["statut"] == "soumise"
    assert data["soumise_le"].endswith("Z") or data["soumise_le"].endswith("+00:00")  # horodatage UTC
    assert data["montant_htg"] == 500 and data["statut_paiement"] == "SIMULE_PAYE"

    with session_factory() as db:
        ligne = db.query(CandidatureModel).one()
        assert ligne.reference_dossier == data["reference_dossier"] and ligne.statut == "soumise"

    # L'email de confirmation est parti, avec la référence et le lien de suivi
    (message,) = emails.messages
    assert message.destinataire == "louismy@exemple.com"
    assert data["reference_dossier"] in message.sujet
    assert f"/suivi/{data['reference_dossier']}" in message.texte


def test_reprise_apres_soumission(client, emails):
    cid = _dossier(client)
    reference = client.post(f"{URL}/{cid}/soumission").json()["reference_dossier"]
    reprise = client.get(f"{URL}/{cid}").json()
    assert reprise["statut"] == "soumise" and reprise["reference_dossier"] == reference


def test_regle_absolue_email_en_panne_ne_bloque_pas_la_candidature(client, session_factory, caplog):
    app.dependency_overrides[get_email_sender] = lambda: EmailEnPanne()
    cid = _dossier(client)
    with caplog.at_level(logging.ERROR, logger="fds.candidature"):
        reponse = client.post(f"{URL}/{cid}/soumission")

    assert reponse.status_code == 200  # jamais de 500 à cause de l'email
    reference = reponse.json()["reference_dossier"]
    assert re.fullmatch(r"CAN-2026-\d{4}", reference)  # la référence est quand même renvoyée
    with session_factory() as db:  # et le dossier est bien enregistré
        ligne = db.query(CandidatureModel).one()
        assert ligne.reference_dossier == reference and ligne.statut == "soumise"
    assert reference in caplog.text  # l'échec est journalisé


def test_dossier_incomplet_liste_ce_qui_manque(client, emails):
    cid = _dossier(client, pieces=LES_CINQ[:3])
    reponse = client.post(f"{URL}/{cid}/soumission")
    assert reponse.status_code == 409
    detail = reponse.json()["detail"]
    assert len(detail["manques"]) == 2 and detail["message"]
    assert emails.messages == []
    assert client.get(f"{URL}/{cid}").json()["statut"] == "brouillon"


def test_dossier_sans_paiement_refuse(client, emails):
    cid = _dossier(client, paye=False)
    reponse = client.post(f"{URL}/{cid}/soumission")
    assert reponse.status_code == 409
    assert "Paiement simulé des frais de dossier" in reponse.json()["detail"]["manques"]


def test_double_soumission_idempotente(client, emails):
    cid = _dossier(client)
    premiere = client.post(f"{URL}/{cid}/soumission").json()
    seconde = client.post(f"{URL}/{cid}/soumission").json()
    assert seconde["reference_dossier"] == premiere["reference_dossier"]
    assert seconde["soumise_le"] == premiere["soumise_le"]
    assert len(emails.messages) == 1  # un seul email, pas de doublon


def test_references_distinctes_et_sequentielles(client, emails):
    refs = []
    for i in range(3):
        limiteur_envois.reinitialiser()  # 3 dossiers x 5 pièces dépassent la limite de 10 envois par minute
        cid = _dossier(client, email=f"c{i}@exemple.com")
        refs.append(client.post(f"{URL}/{cid}/soumission").json()["reference_dossier"])
    assert refs == ["CAN-2026-0001", "CAN-2026-0002", "CAN-2026-0003"]


def test_dossier_verrouille_apres_soumission(client, emails):
    cid = _dossier(client)
    client.post(f"{URL}/{cid}/soumission")
    assert client.put(f"{URL}/{cid}/informations", json=SAISIE).status_code == 409
    assert client.put(f"{URL}/{cid}/deplacement-physique", json={"deplacement_physique": True}).status_code == 409
    envoi = client.post(f"{URL}/{cid}/documents/{LES_CINQ[0]}", files={"fichier": ("a.pdf", PDF, "application/pdf")})
    assert envoi.status_code == 409


def test_soumission_candidature_inconnue(client, emails):
    assert client.post(f"{URL}/inconnu/soumission").status_code == 404
