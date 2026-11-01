"""Tests unitaires de l'email de décision (US-014) : contenu, lien de remplacement, échec non bloquant, interrupteur.
"""

import logging
from datetime import date, datetime, timezone

import pytest

from backend.bll.messages_email import message_decision
from backend.bll.notifier_decision import NotifierDecisionUseCase
from backend.dal.email_adapters import ConsoleEmailSender, EmailDesactive, creer_email_sender
from backend.entities.candidat import Candidat
from backend.entities.candidature import Candidature
from backend.entities.decision_document import DecisionDocument
from backend.ports.email_sender import IEmailSender

MAINTENANT = datetime(2026, 10, 27, 9, 0, tzinfo=timezone.utc)
URL = "https://candidature.fds.ueh.edu.ht"
CANDIDAT = Candidat("c1", "Louis", "Louismy", date(2008, 5, 14), "M", "+50937123456", "louismy@exemple.com", "Ouest", "Pétion-Ville", 2026, MAINTENANT)
CANDIDATURE = Candidature("k1", "c1", MAINTENANT, statut="soumise", reference_dossier="CAN-2026-0089")


def _decision(statut, motif=None):
    return DecisionDocument("x", "d1", "c1", "mpc-releve-notes-bac", statut, motif, "agent-1", MAINTENANT)


class Enregistreur(IEmailSender):
    def __init__(self):
        self.messages = []

    def envoyer(self, message):
        self.messages.append(message)


class EnPanne(IEmailSender):
    def envoyer(self, message):
        raise TimeoutError("Resend ne répond pas à louismy@exemple.com")


def test_email_de_validation():
    envoi = Enregistreur()
    assert NotifierDecisionUseCase(envoi, URL + "/").executer(CANDIDAT, CANDIDATURE, _decision("valide")) is True
    (m,) = envoi.messages
    assert m.destinataire == "louismy@exemple.com" and "validée" in m.sujet and "CAN-2026-0089" in m.sujet
    assert "Relevé de notes" in m.texte and "Relevé de notes" in m.html
    assert f"{URL}/suivi/CAN-2026-0089" in m.texte  # barre finale de l'URL de base ignorée


def test_email_de_refus_avec_motif_et_bouton_de_remplacement():
    envoi = Enregistreur()
    NotifierDecisionUseCase(envoi, URL).executer(CANDIDAT, CANDIDATURE, _decision("rejete", "Document illisible"))
    (m,) = envoi.messages
    assert "à remplacer" in m.sujet
    assert "Motif : Document illisible" in m.texte
    assert f'href="{URL}/suivi/CAN-2026-0089"' in m.html and "Remplacer le document →" in m.html
    assert "Document illisible" in m.html


def test_le_html_echappe_le_motif_et_le_prenom():
    candidat = Candidat("c1", "Louis", "<b>Louismy</b>", date(2008, 5, 14), "M", "+50937123456", "l@exemple.com", "Ouest", "x", 2026, MAINTENANT)
    m = message_decision(candidat, CANDIDATURE, "Relevé", "rejete", '<script>alert("x")</script>', URL)
    assert "<script>" not in m.html and "&lt;script&gt;" in m.html and "&lt;b&gt;" in m.html


def test_echec_d_envoi_non_bloquant_et_journal_sans_donnee_personnelle(caplog):
    with caplog.at_level(logging.ERROR):
        assert NotifierDecisionUseCase(EnPanne(), URL).executer(CANDIDAT, CANDIDATURE, _decision("valide")) is False
    assert "CAN-2026-0089" in caplog.text and "TimeoutError" in caplog.text
    assert "louismy@exemple.com" not in caplog.text  # ni l'adresse, ni le message brut de l'erreur


def test_interrupteur_email_enabled(monkeypatch):
    monkeypatch.delenv("RESEND_API_KEY", raising=False)
    monkeypatch.delenv("EMAIL_ENABLED", raising=False)
    assert isinstance(creer_email_sender(), ConsoleEmailSender)  # activé par défaut
    for valeur in ("false", "FALSE", "0", " no "):
        monkeypatch.setenv("EMAIL_ENABLED", valeur)
        assert isinstance(creer_email_sender(), EmailDesactive)
    monkeypatch.setenv("EMAIL_ENABLED", "false")
    monkeypatch.setenv("RESEND_API_KEY", "re_cle")
    assert isinstance(creer_email_sender(), EmailDesactive)  # même avec une clé d'API
    monkeypatch.setenv("EMAIL_ENABLED", "true")
    assert not isinstance(creer_email_sender(), EmailDesactive)


def test_email_desactive_n_envoie_ni_ne_leve():
    EmailDesactive().envoyer(message_decision(CANDIDAT, CANDIDATURE, "Relevé", "valide", None, URL))
