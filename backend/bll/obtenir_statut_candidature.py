"""Cas d'utilisation : suivre un dossier par sa référence et sa date de naissance — Couche BLL (US-009).

Les références `CAN-AAAA-NNNN` étant séquentielles, la consultation publique exige en complément la date de naissance
du candidat. Une référence inconnue, mal formée ou associée à une autre date de naissance lève la même erreur afin de ne
pas révéler quels numéros existent. La vue ne retourne que le strict nécessaire (prénom, initiale du nom, statut des
pièces), jamais l'email, le téléphone ni le nom des fichiers déposés.
"""

import re
from dataclasses import dataclass
from datetime import date, datetime

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


def analyser_date_naissance(saisie: str | date | None) -> date | None:
    """Convertit une saisie ISO `AAAA-MM-JJ` en `date`, ou retourne `None` si elle est absente ou invalide."""
    if isinstance(saisie, date) and not isinstance(saisie, datetime):
        return saisie
    texte = (saisie or "").strip() if isinstance(saisie, str) else ""
    if len(texte) != 10:
        return None
    try:
        return date.fromisoformat(texte)
    except ValueError:
        return None


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
    """Retourne l'état d'un dossier soumis si la référence et la date de naissance concordent."""

    def __init__(self, candidatures: ICandidatureRepository, documents: IDocumentRepository) -> None:
        self._candidatures = candidatures
        self._documents = documents

    def executer(self, saisie: str, date_naissance: str | date | None = None) -> SuiviDossier:
        reference = normaliser_reference(saisie)
        naissance = analyser_date_naissance(date_naissance)
        trouve = self._candidatures.trouver_par_reference(reference) if (reference and naissance) else None
        # Même erreur pour référence absente, brouillon ou date de naissance erronée (aucun oracle d'énumération)
        if trouve is None or trouve[1].statut != STATUT_SOUMISE or trouve[0].date_naissance != naissance:
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
