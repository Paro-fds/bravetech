"""Cas d'utilisation : un visiteur écrit au secrétariat — Couche BLL (US-019).

Contrairement aux autres emails du portail, celui-ci est l'objet même de l'action : il est envoyé tout de suite, et son
échec est signalé au visiteur (qui garde son texte et peut réessayer) au lieu d'être absorbé. Rien n'est perdu en silence.
"""

import logging
import re
from html import escape
from typing import Any

from backend.entities.erreurs import ContactIndisponible, EnvoiEmailEchoue, InformationsInvalides
from backend.ports.email_sender import IEmailSender, MessageEmail

logger = logging.getLogger(__name__)

SUJET = "Nouveau message depuis le formulaire de contact du portail"
NOM_MIN, NOM_MAX = 2, 100
MESSAGE_MIN, MESSAGE_MAX = 10, 2000

_RE_EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def valider_message_contact(donnees: dict[str, Any]) -> dict[str, str]:
    """Nettoie et valide nom, email et message. Lève `InformationsInvalides` (champ -> message)."""
    nom = " ".join(str(donnees.get("nom") or "").split())
    email = str(donnees.get("email") or "").strip().lower()
    message = str(donnees.get("message") or "").strip()
    erreurs: dict[str, str] = {}

    if not nom:
        erreurs["nom"] = "Votre nom est obligatoire."
    elif not NOM_MIN <= len(nom) <= NOM_MAX:
        erreurs["nom"] = f"Votre nom doit contenir entre {NOM_MIN} et {NOM_MAX} caractères."
    if not email:
        erreurs["email"] = "Votre email est obligatoire."
    elif len(email) > 255 or not _RE_EMAIL.fullmatch(email):
        erreurs["email"] = "Adresse email invalide."
    if not message:
        erreurs["message"] = "Votre message est obligatoire."
    elif len(message) < MESSAGE_MIN:
        erreurs["message"] = f"Votre message est trop court ({MESSAGE_MIN} caractères minimum)."
    elif len(message) > MESSAGE_MAX:
        erreurs["message"] = f"Votre message est trop long ({MESSAGE_MAX} caractères maximum)."

    if erreurs:
        raise InformationsInvalides(erreurs)
    return {"nom": nom, "email": email, "message": message}


class ContacterSecretariatUseCase:
    def __init__(self, email_sender: IEmailSender, destinataire: str) -> None:
        self._email_sender = email_sender
        self._destinataire = destinataire.strip()

    def executer(self, donnees: dict[str, Any]) -> None:
        propres = valider_message_contact(donnees)
        if not self._destinataire:
            # Adresse du secrétariat non configurée (CONTACT_EMAIL) : mieux vaut le dire que perdre le message
            logger.error("CONTACT_EMAIL n'est pas défini : message de contact refusé.")
            raise ContactIndisponible()

        texte = f"Nom : {propres['nom']}\nEmail : {propres['email']}\n\n{propres['message']}\n"
        html = (
            f"<p><strong>Nom :</strong> {escape(propres['nom'])}<br>"
            f"<strong>Email :</strong> {escape(propres['email'])}</p>"
            f"<p style=\"white-space:pre-wrap\">{escape(propres['message'])}</p>"
        )
        try:
            self._email_sender.envoyer(
                MessageEmail(
                    destinataire=self._destinataire, sujet=SUJET, texte=texte, html=html, repondre_a=propres["email"]
                )
            )
        except Exception as erreur:  # noqa: BLE001 — journal sans donnée personnelle, le visiteur est prévenu
            logger.error("Message de contact non envoyé au secrétariat (%s).", type(erreur).__name__)
            raise EnvoiEmailEchoue() from erreur
