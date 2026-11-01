"""Cas d'utilisation : soumettre définitivement la candidature — Couche BLL (US-008).

La soumission ne dépend que de la base : elle vérifie que le dossier est complet, attribue la référence
officielle `CAN-AAAA-NNNN` et verrouille le dossier. L'email de confirmation est un effet de bord traité à part
(`NotifierConfirmationUseCase`) : son échec n'annule jamais la soumission.
"""

import logging
from datetime import datetime, timezone

from backend.bll.messages_email import message_confirmation
from backend.entities.candidat import CAMPAGNE_COURANTE, Candidat
from backend.entities.candidature import STATUT_BROUILLON, STATUT_PAIEMENT_SIMULE, STATUT_SOUMISE, Candidature
from backend.entities.erreurs import (
    CandidatureIntrouvable,
    DossierIncomplet,
    ErreurMetier,
    ReferenceDejaAttribuee,
)
from backend.entities.pieces_admission import pieces_admission
from backend.ports.candidature_repository import ICandidatureRepository
from backend.ports.document_repository import IDocumentRepository
from backend.ports.email_sender import IEmailSender

logger = logging.getLogger("fds.candidature")

_ESSAIS_REFERENCE = 5


def formater_reference(campagne: int, numero: int) -> str:
    """Format officiel : `CAN-2026-0089` (numéro sur 4 chiffres au minimum)."""
    return f"CAN-{campagne}-{numero:04d}"


class SoumettreCandidatureUseCase:
    """Vérifie le dossier, attribue la référence officielle et le verrouille."""

    def __init__(self, candidatures: ICandidatureRepository, documents: IDocumentRepository) -> None:
        self._candidatures = candidatures
        self._documents = documents

    def executer(self, candidature_id: str) -> tuple[Candidat, Candidature, bool]:
        """Retourne (candidat, candidature, vient_d_etre_soumise).

        Idempotent : soumettre un dossier déjà soumis le renvoie tel quel (même référence), sans nouvel email.
        """
        candidature = self._candidatures.obtenir_candidature(candidature_id)
        if candidature is None:
            raise CandidatureIntrouvable()
        candidat = self._candidatures.obtenir_candidat(candidature.candidat_id)
        if candidat is None:
            raise CandidatureIntrouvable()

        if candidature.statut == STATUT_SOUMISE:
            return candidat, candidature, False

        self._verifier_dossier_complet(candidature, candidat)

        maintenant = datetime.now(timezone.utc)
        for _ in range(_ESSAIS_REFERENCE):
            numero = self._candidatures.prochain_numero_reference(candidat.campagne)
            candidature.reference_dossier = formater_reference(candidat.campagne, numero)
            candidature.statut = STATUT_SOUMISE
            candidature.soumise_le = maintenant
            try:
                self._candidatures.enregistrer_candidature(candidature)
                return candidat, candidature, True
            except ReferenceDejaAttribuee:
                # Deux soumissions simultanées ont tiré le même numéro : on en retire un autre
                candidature.reference_dossier = None
                candidature.statut = STATUT_BROUILLON
                candidature.soumise_le = None
        raise ErreurMetier("Impossible d'attribuer une référence de dossier.")

    def _verifier_dossier_complet(self, candidature: Candidature, candidat: Candidat) -> None:
        manques: list[str] = []
        if candidature.deplacement_physique is None:
            manques.append("Réponse à la question sur le déplacement physique")
        if candidature.statut_paiement != STATUT_PAIEMENT_SIMULE:
            manques.append("Paiement simulé des frais de dossier")
        deposes = {d.document_requis_id for d in self._documents.lister(candidat.id)}
        manques.extend(piece.nom for piece in pieces_admission() if piece.id not in deposes)
        if manques:
            raise DossierIncomplet(manques)


class NotifierConfirmationUseCase:
    """Envoie l'email de confirmation. Ne lève JAMAIS : un échec est journalisé, la candidature reste valide."""

    def __init__(self, email_sender: IEmailSender, url_base: str) -> None:
        self._email_sender = email_sender
        self._url_base = url_base.rstrip("/")

    def executer(self, candidat: Candidat, candidature: Candidature) -> bool:
        """Retourne True si l'email est parti, False sinon (échec journalisé, sans donnée personnelle)."""
        try:
            url_suivi = f"{self._url_base}/suivi/{candidature.reference_dossier}"
            self._email_sender.envoyer(message_confirmation(candidat, candidature, url_suivi))
            return True
        except Exception as erreur:  # noqa: BLE001 — règle absolue : l'email ne doit jamais bloquer
            logger.error(
                "Email de confirmation non envoyé pour le dossier %s (%s). "
                "La candidature reste enregistrée ; la référence est affichée à l'écran.",
                candidature.reference_dossier,
                type(erreur).__name__,
            )
            return False
