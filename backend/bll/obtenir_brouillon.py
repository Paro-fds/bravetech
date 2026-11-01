"""Cas d'utilisation : reprendre un brouillon de candidature — Couche BLL (US-005).
"""

from backend.entities.candidat import Candidat
from backend.entities.candidature import Candidature
from backend.entities.erreurs import CandidatureIntrouvable
from backend.ports.candidature_repository import ICandidatureRepository


class ObtenirBrouillonUseCase:
    """Retourne le candidat et la candidature associés à un identifiant de brouillon."""

    def __init__(self, repository: ICandidatureRepository) -> None:
        self._repository = repository

    def executer(self, candidature_id: str) -> tuple[Candidat, Candidature]:
        candidature = self._repository.obtenir_candidature(candidature_id)
        if candidature is None:
            raise CandidatureIntrouvable()
        candidat = self._repository.obtenir_candidat(candidature.candidat_id)
        if candidat is None:
            raise CandidatureIntrouvable()
        return candidat, candidature
