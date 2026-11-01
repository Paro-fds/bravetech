"""Cas d'utilisation : suivre un dossier par sa référence — Couche BLL (US-009).

La page de suivi est publique : la référence tient lieu de secret partagé. On n'en tire donc que le strict
nécessaire (prénom et initiale du nom, statut des pièces), jamais l'email, le téléphone, la date de naissance
ni le nom des fichiers déposés.
"""

import re
from dataclasses import dataclass
from datetime import datetime

from backend.bll.televerser_document import ListerPiecesDossierUseCase, PieceDossier
from backend.entities.candidature import STATUT_SOUMISE
from backend.entities.document_soumis import STATUT_REJETE, STATUT_VALIDE
from backend.entities.erreurs import CandidatureIntrouvable
from backend.ports.candidature_repository import ICandidatureRepository
from backend.ports.document_repository import IDocumentRepository

STATUT_GLOBAL_EN_EXAMEN = "en_examen"
STATUT_GLOBAL_ACTION_REQUISE = "action_requise"
STATUT_GLOBAL_COMPLET = "complet"

_FORMAT_REFERENCE = re.compile(r"CAN-\d{4}-\d{4,}")


def normaliser_reference(saisie: str) -> str | None:
    """« can-2026-0089 » → « CAN-2026-0089 » ; None si le format n'est pas celui d'une référence de dossier."""
    reference = (saisie or "").strip().upper()
    return reference if _FORMAT_REFERENCE.fullmatch(reference) else None


@dataclass
class SuiviDossier:
    """Vue publique d'un dossier soumis."""
    reference: str
    prenom: str
    initiale_nom: str
    soumise_le: datetime | None
    statut_global: str
    pieces_validees: int
    pieces: list[PieceDossier]


def statut_global_depuis_comptes(validees: int, rejetees: int, total: int) -> str:
    """Complet si toutes les pièces sont validées ; action requise dès qu'une pièce est refusée ; sinon en examen."""
    if rejetees:
        return STATUT_GLOBAL_ACTION_REQUISE
    if total and validees == total:
        return STATUT_GLOBAL_COMPLET
    return STATUT_GLOBAL_EN_EXAMEN


def statut_global(pieces: list[PieceDossier]) -> str:
    return statut_global_depuis_comptes(
        sum(1 for p in pieces if p.statut == STATUT_VALIDE),
        sum(1 for p in pieces if p.statut == STATUT_REJETE),
        len(pieces),
    )


class ObtenirStatutCandidatureUseCase:
    """Retourne l'état d'un dossier soumis. Une référence mal formée ou inconnue lève la même erreur."""

    def __init__(self, candidatures: ICandidatureRepository, documents: IDocumentRepository) -> None:
        self._candidatures = candidatures
        self._documents = documents

    def executer(self, saisie: str) -> SuiviDossier:
        reference = normaliser_reference(saisie)
        trouve = self._candidatures.trouver_par_reference(reference) if reference else None
        # Seuls les dossiers soumis ont une référence ; on revérifie le statut par prudence
        if trouve is None or trouve[1].statut != STATUT_SOUMISE:
            raise CandidatureIntrouvable()
        candidat, candidature = trouve
        pieces = ListerPiecesDossierUseCase(self._candidatures, self._documents).executer(candidature.id)
        return SuiviDossier(
            reference=candidature.reference_dossier,
            prenom=candidat.prenom,
            initiale_nom=(candidat.nom.strip()[:1] or "").upper(),
            soumise_le=candidature.soumise_le,
            statut_global=statut_global(pieces),
            pieces_validees=sum(1 for p in pieces if p.statut == STATUT_VALIDE),
            pieces=pieces,
        )
