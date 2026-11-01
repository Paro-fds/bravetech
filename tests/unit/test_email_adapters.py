"""Tests des adaptateurs d'email (US-008) : aucun appel réseau, `urlopen` est remplacé.
"""

import json
import logging
import urllib.error

import pytest

from backend.dal import email_adapters
from backend.dal.email_adapters import ConsoleEmailSender, ResendEmailSender, creer_email_sender
from backend.ports.email_sender import MessageEmail

MESSAGE = MessageEmail(
    destinataire="louismy@exemple.com",
    sujet="Confirmation — CAN-2026-0089",
    texte="Bonjour",
    html="<p>Bonjour</p>",
)


class _Reponse:
    def __init__(self, status=200):
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


def test_console_journalise_le_message(caplog):
    with caplog.at_level(logging.INFO, logger="fds.email"):
        ConsoleEmailSender().envoyer(MESSAGE)
    assert "louismy@exemple.com" in caplog.text and "CAN-2026-0089" in caplog.text


def test_resend_construit_la_requete(monkeypatch):
    captures = {}

    def faux_urlopen(requete, timeout):
        captures.update(requete=requete, timeout=timeout)
        return _Reponse(200)

    monkeypatch.setattr(email_adapters.urllib.request, "urlopen", faux_urlopen)
    ResendEmailSender("re_cle_secrete", "FDS <no-reply@fds.ht>").envoyer(MESSAGE)

    requete = captures["requete"]
    assert requete.full_url == "https://api.resend.com/emails"
    assert requete.get_method() == "POST"
    assert requete.get_header("Authorization") == "Bearer re_cle_secrete"
    assert requete.get_header("User-agent") == "fds-portail/1.0"
    assert requete.get_header("Content-type") == "application/json"
    corps = json.loads(requete.data)
    assert corps == {
        "from": "FDS <no-reply@fds.ht>",
        "to": ["louismy@exemple.com"],
        "subject": "Confirmation — CAN-2026-0089",
        "text": "Bonjour",
        "html": "<p>Bonjour</p>",
    }
    assert captures["timeout"] == 10  # un service lent ne doit pas bloquer indéfiniment


def test_resend_sans_html(monkeypatch):
    captures = {}
    monkeypatch.setattr(
        email_adapters.urllib.request, "urlopen", lambda r, timeout: captures.update(r=r) or _Reponse(200)
    )
    ResendEmailSender("cle").envoyer(MessageEmail("a@b.ht", "Sujet", "Texte"))
    assert "html" not in json.loads(captures["r"].data)


def test_resend_propage_les_erreurs_http(monkeypatch):
    def en_erreur(requete, timeout):
        raise urllib.error.HTTPError(requete.full_url, 403, "Forbidden", {}, None)

    monkeypatch.setattr(email_adapters.urllib.request, "urlopen", en_erreur)
    with pytest.raises(urllib.error.HTTPError):
        ResendEmailSender("cle").envoyer(MESSAGE)  # c'est à l'appelant de l'absorber (non bloquant)


def test_resend_statut_inattendu(monkeypatch):
    monkeypatch.setattr(email_adapters.urllib.request, "urlopen", lambda r, timeout: _Reponse(302))
    with pytest.raises(RuntimeError):
        ResendEmailSender("cle").envoyer(MESSAGE)


def test_fabrique_sans_cle_choisit_la_console(monkeypatch):
    monkeypatch.delenv("RESEND_API_KEY", raising=False)
    assert isinstance(creer_email_sender(), ConsoleEmailSender)
    monkeypatch.setenv("RESEND_API_KEY", "   ")
    assert isinstance(creer_email_sender(), ConsoleEmailSender)


def test_fabrique_avec_cle_choisit_resend(monkeypatch):
    monkeypatch.setenv("RESEND_API_KEY", "re_abc")
    monkeypatch.setenv("EMAIL_FROM", "FDS <admission@fds.ht>")
    sender = creer_email_sender()
    assert isinstance(sender, ResendEmailSender)
    assert sender._expediteur == "FDS <admission@fds.ht>"
