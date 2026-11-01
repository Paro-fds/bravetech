"""Tests du formulaire de contact (US-019) : validation, envoi au secrétariat, échec visible, anti-spam.
"""

import logging

import pytest

from backend.api.v1.candidatures import get_email_sender
from backend.api.v1.contact import get_email_secretariat
from backend.bll.contacter_secretariat import MESSAGE_MAX, ContacterSecretariatUseCase
from backend.main import app
from backend.ports.email_sender import IEmailSender

URL = "/api/v1/contact"
SECRETARIAT = "secretariat@fds.ht"
VALIDE = {"nom": "Louismy Louis", "email": "Louismy@Exemple.com", "message": "Bonjour, j'ai perdu ma référence de dossier."}


class Enregistreur(IEmailSender):
    def __init__(self):
        self.messages = []

    def envoyer(self, message):
        self.messages.append(message)


class EnPanne(IEmailSender):
    def envoyer(self, message):
        raise ConnectionError("Resend indisponible pour louismy@exemple.com")


@pytest.fixture
def envoi():
    enregistreur = Enregistreur()
    app.dependency_overrides[get_email_sender] = lambda: enregistreur
    app.dependency_overrides[get_email_secretariat] = lambda: SECRETARIAT
    return enregistreur


def test_message_envoye_au_secretariat(client, envoi):
    reponse = client.post(URL, json=VALIDE)
    assert reponse.status_code == 200 and reponse.json() == {"envoye": True}
    (m,) = envoi.messages
    assert m.destinataire == SECRETARIAT
    assert m.repondre_a == "louismy@exemple.com"  # le secrétariat répond directement au visiteur
    assert "Louismy Louis" in m.texte and "perdu ma référence" in m.texte
    assert "contact" in m.sujet.lower() and "Louismy" not in m.sujet  # sujet fixe : aucune saisie dans les en-têtes


def test_le_html_echappe_la_saisie(client, envoi):
    client.post(URL, json={**VALIDE, "message": '<script>alert("x")</script> bonjour tout le monde'})
    html = envoi.messages[0].html
    assert "<script>" not in html and "&lt;script&gt;" in html


@pytest.mark.parametrize(
    "corps, champ",
    [
        ({**VALIDE, "nom": ""}, "nom"),
        ({**VALIDE, "nom": "x"}, "nom"),
        ({**VALIDE, "email": "pas-un-email"}, "email"),
        ({**VALIDE, "email": ""}, "email"),
        ({**VALIDE, "message": "court"}, "message"),
        ({**VALIDE, "message": "x" * (MESSAGE_MAX + 1)}, "message"),
    ],
)
def test_champs_invalides_renvoient_422_et_rien_ne_part(client, envoi, corps, champ):
    reponse = client.post(URL, json=corps)
    assert reponse.status_code == 422 and champ in reponse.json()["detail"]["erreurs"]
    assert envoi.messages == []


def test_echec_d_envoi_est_signale_au_visiteur(client, caplog):
    app.dependency_overrides[get_email_sender] = lambda: EnPanne()
    app.dependency_overrides[get_email_secretariat] = lambda: SECRETARIAT
    with caplog.at_level(logging.ERROR):
        reponse = client.post(URL, json=VALIDE)
    assert reponse.status_code == 503 and "réessayez" in reponse.json()["detail"].lower()
    assert "ConnectionError" in caplog.text and "louismy@exemple.com" not in caplog.text


def test_secretariat_non_configure_est_signale(client, envoi):
    app.dependency_overrides[get_email_secretariat] = lambda: ""
    assert client.post(URL, json=VALIDE).status_code == 503
    assert envoi.messages == []


def test_robot_pris_au_piege_sans_envoi(client, envoi):
    reponse = client.post(URL, json={**VALIDE, "site_web": "http://spam.example"})
    assert reponse.status_code == 200 and envoi.messages == []


def test_limitation_a_trois_messages(client, envoi):
    codes = [client.post(URL, json=VALIDE).status_code for _ in range(4)]
    assert codes == [200, 200, 200, 429]
    assert len(envoi.messages) == 3


def test_les_messages_invalides_ne_consomment_pas_le_quota_utilement_mais_restent_bornes(client, envoi):
    """Même les tentatives invalides comptent : un robot ne peut pas sonder le formulaire sans limite."""
    codes = [client.post(URL, json={**VALIDE, "message": "court"}).status_code for _ in range(4)]
    assert codes == [422, 422, 422, 429]


def test_cas_d_usage_destinataire_nettoye():
    envoi = Enregistreur()
    ContacterSecretariatUseCase(envoi, "  secretariat@fds.ht ").executer(VALIDE)
    assert envoi.messages[0].destinataire == "secretariat@fds.ht"
