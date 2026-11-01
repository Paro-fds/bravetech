"""Cas d'utilisation : confirmer au candidat la réception d'une pièce remplacée — Couche BLL (US-010).

Non bloquant, comme les autres notifications (AGENTS.md, fait 2) : le remplacement est déjà enregistré.
"""

import logging

from backend.bll.messages_email import message_remplacement
from backend.bll.televerser_document import trouver_piece
from backend.entities.candidat import Candidat
from backend.entities.candidature import Candidature
from backend.entities.document_soumis import DocumentSoumis
from backend.ports.email_sender import IEmailSender

logger = logging.getLogger(__name__)


class NotifierRemplacementUseCase:
    def __init__(self, email_sender: IEmailSender, url_base: str) -> None:
        self._email_sender = email_sender
        self._url_base = url_base.rstrip("/")

    def executer(self, candidat: Candidat, candidature: Candidature, document: DocumentSoumis) -> bool:
        """Retourne True si l'email est parti, False sinon. Ne lève jamais."""
        try:
            url_suivi = f"{self._url_base}/suivi/{candidature.reference_dossier}"
            nom_piece = trouver_piece(document.document_requis_id).nom
            self._email_sender.envoyer(message_remplacement(candidat, candidature, nom_piece, url_suivi))
            return True
        except Exception as erreur:  # noqa: BLE001 — règle absolue : l'email ne doit jamais annuler un remplacement
            logger.error(
                "Email de remplacement non envoyé pour le dossier %s, pièce %s (%s). Le remplacement reste enregistré.",
                candidature.reference_dossier,
                document.document_requis_id,
                type(erreur).__name__,
            )
            return False
