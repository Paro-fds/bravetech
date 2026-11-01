"""Cas d'utilisation : informer le candidat d'une décision sur une pièce — Couche BLL (US-014).

Même règle absolue que la confirmation de dépôt (AGENTS.md, fait 2) : l'email ne bloque jamais. La décision est déjà
enregistrée quand on arrive ici ; un échec d'envoi est journalisé sans donnée personnelle et n'est pas remonté.
"""

import logging

from backend.bll.messages_email import message_decision
from backend.bll.televerser_document import trouver_piece
from backend.entities.candidat import Candidat
from backend.entities.candidature import Candidature
from backend.entities.decision_document import DecisionDocument
from backend.ports.email_sender import IEmailSender

logger = logging.getLogger(__name__)


class NotifierDecisionUseCase:
    def __init__(self, email_sender: IEmailSender, url_base: str) -> None:
        self._email_sender = email_sender
        self._url_base = url_base.rstrip("/")

    def executer(self, candidat: Candidat, candidature: Candidature, decision: DecisionDocument) -> bool:
        """Retourne True si l'email est parti, False sinon. Ne lève jamais."""
        try:
            url_suivi = f"{self._url_base}/suivi/{candidature.reference_dossier}"
            message = message_decision(
                candidat,
                candidature,
                trouver_piece(decision.document_requis_id).nom,
                decision.statut,
                decision.motif,
                url_suivi,
            )
            self._email_sender.envoyer(message)
            return True
        except Exception as erreur:  # noqa: BLE001 — règle absolue : l'email ne doit jamais annuler une décision
            logger.error(
                "Email de décision non envoyé pour le dossier %s, pièce %s (%s). La décision reste enregistrée.",
                candidature.reference_dossier,
                decision.document_requis_id,
                type(erreur).__name__,
            )
            return False
