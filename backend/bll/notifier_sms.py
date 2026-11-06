"""Cas d'utilisation : prévenir le candidat par SMS, en complément de l'email — Couche BLL (US-016).

Les SMS partent aux mêmes moments que les emails : dossier soumis, pièce validée, pièce refusée. Ils sont courts
(≤ 160 caractères) et renvoient au suivi en ligne pour le détail (le motif d'un refus n'y figure pas : il est dans
l'email et sur la page de suivi). Règle absolue de l'email reprise telle quelle : un échec est journalisé sans donnée
personnelle et n'est jamais remonté.
"""

import logging

from backend.bll.televerser_document import trouver_piece
from backend.entities.candidat import Candidat
from backend.entities.candidature import Candidature
from backend.entities.decision_document import DecisionDocument
from backend.entities.document_soumis import STATUT_VALIDE
from backend.entities.sms_simule import LONGUEUR_MAX_SMS
from backend.ports.sms_sender import ISmsSender, MessageSms

logger = logging.getLogger(__name__)

PREFIXE = "FDS-UEH"


def _borner(texte: str) -> str:
    """Un SMS ne dépasse jamais 160 caractères : on coupe proprement plutôt que de payer deux SMS."""
    return texte if len(texte) <= LONGUEUR_MAX_SMS else texte[: LONGUEUR_MAX_SMS - 1] + "…"


def sms_confirmation(candidat: Candidat, candidature: Candidature, url_suivi: str) -> MessageSms:
    reference = candidature.reference_dossier or ""
    texte = f"{PREFIXE} : votre dossier {reference} est bien reçu. Suivez-le sur {url_suivi}"
    return MessageSms(destinataire=candidat.telephone, texte=_borner(texte), reference_dossier=reference)


def sms_decision(candidat: Candidat, candidature: Candidature, nom_piece: str, statut: str, url_suivi: str) -> MessageSms:
    reference = candidature.reference_dossier or ""
    if statut == STATUT_VALIDE:
        texte = f"{PREFIXE} : pièce validée ({nom_piece}), dossier {reference}. Suivi : {url_suivi}"
    else:
        texte = f"{PREFIXE} : pièce à remplacer ({nom_piece}), dossier {reference}. Motif et remplacement : {url_suivi}"
    return MessageSms(destinataire=candidat.telephone, texte=_borner(texte), reference_dossier=reference)


class NotifierSmsUseCase:
    """Ne lève JAMAIS : la candidature ou la décision est déjà enregistrée quand on arrive ici."""

    def __init__(self, sms_sender: ISmsSender, url_base: str) -> None:
        self._sms_sender = sms_sender
        self._url_base = url_base.rstrip("/")

    def _envoyer(self, construire, reference: str | None, motif_journal: str) -> bool:
        try:
            self._sms_sender.envoyer(construire())
            return True
        except Exception as erreur:  # noqa: BLE001 — règle absolue : le SMS ne bloque jamais
            logger.error("SMS %s non envoyé pour le dossier %s (%s).", motif_journal, reference, type(erreur).__name__)
            return False

    def confirmation(self, candidat: Candidat, candidature: Candidature) -> bool:
        url = f"{self._url_base}/suivi/{candidature.reference_dossier}"
        return self._envoyer(lambda: sms_confirmation(candidat, candidature, url), candidature.reference_dossier, "de confirmation")

    def decision(self, candidat: Candidat, candidature: Candidature, decision: DecisionDocument) -> bool:
        url = f"{self._url_base}/suivi/{candidature.reference_dossier}"
        return self._envoyer(
            lambda: sms_decision(candidat, candidature, trouver_piece(decision.document_requis_id).nom, decision.statut, url),
            candidature.reference_dossier,
            "de décision",
        )
