"""Adaptateurs d'envoi d'email — Couche DAL (implémentations de IEmailSender).

- `ConsoleEmailSender` : écrit le message dans les journaux ; sert en développement et sans clé d'API.
- `ResendEmailSender` : envoie via l'API REST de Resend (ADR-005). Aucune dépendance externe : bibliothèque standard.
Le choix se fait par la variable d'environnement `RESEND_API_KEY` (voir `creer_email_sender`).
"""

import json
import logging
import os
import urllib.request

from backend.ports.email_sender import IEmailSender, MessageEmail

logger = logging.getLogger("fds.email")

URL_RESEND = "https://api.resend.com/emails"
EXPEDITEUR_PAR_DEFAUT = "FDS Portail <onboarding@resend.dev>"
DELAI_ENVOI_SECONDES = 10


class ConsoleEmailSender(IEmailSender):
    """Journalise l'email au lieu de l'envoyer (mode développement)."""

    def envoyer(self, message: MessageEmail) -> None:
        logger.info("[EMAIL console] à=%s | sujet=%s\n%s", message.destinataire, message.sujet, message.texte)


class ResendEmailSender(IEmailSender):
    """Envoie un email transactionnel via l'API REST de Resend."""

    def __init__(self, cle_api: str, expediteur: str = EXPEDITEUR_PAR_DEFAUT) -> None:
        self._cle_api = cle_api
        self._expediteur = expediteur

    def envoyer(self, message: MessageEmail) -> None:
        corps = {
            "from": self._expediteur,
            "to": [message.destinataire],
            "subject": message.sujet,
            "text": message.texte,
        }
        if message.html:
            corps["html"] = message.html
        requete = urllib.request.Request(
            URL_RESEND,
            data=json.dumps(corps).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self._cle_api}",
                "Content-Type": "application/json",
                # Resend (derrière Cloudflare) refuse le User-Agent par défaut de urllib
                "User-Agent": "fds-portail/1.0",
            },
            method="POST",
        )
        # Lève HTTPError / URLError / TimeoutError en cas d'échec : l'appelant le traite comme non bloquant
        with urllib.request.urlopen(requete, timeout=DELAI_ENVOI_SECONDES) as reponse:
            if reponse.status >= 300:
                raise RuntimeError(f"Resend a répondu {reponse.status}")


def creer_email_sender() -> IEmailSender:
    """Resend si `RESEND_API_KEY` est définie, sinon la version console (le service reste utilisable sans clé)."""
    cle = os.getenv("RESEND_API_KEY", "").strip()
    if not cle:
        return ConsoleEmailSender()
    return ResendEmailSender(cle, os.getenv("EMAIL_FROM", EXPEDITEUR_PAR_DEFAUT))
