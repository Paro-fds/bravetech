"""Cas d'utilisation : enregistrer la réponse à la question sur le déplacement physique — Couche BLL (US-005).

`deplacement_physique` est la métrique principale du MVP (cible : au moins 70 % à `False`, PRD §11).
La réponse est obligatoire et ne peut pas être modifiée une fois le dossier soumis.
"""

from typing import Any

from backend.entities.candidature import STATUT_BROUILLON, Candidature
from backend.entities.erreurs import CandidatureDejaSoumise, CandidatureIntrouvable, InformationsInvalides
from backend.ports.candidature_repository import ICandidatureRepository


class DefinirDeplacementPhysiqueUseCase:
    """Enregistre la réponse booléenne `deplacement_physique` sur un brouillon."""

    def __init__(self, repository: ICandidatureRepository) -> None:
        self._repository = repository

    def executer(self, candidature_id: str, deplacement_physique: Any) -> Candidature:
        # Pas de coercition : seule une vraie réponse (True ou False) est acceptée
        if not isinstance(deplacement_physique, bool):
            raise InformationsInvalides({"deplacement_physique": "Réponse obligatoire."})

        candidature = self._repository.obtenir_candidature(candidature_id)
        if candidature is None:
            raise CandidatureIntrouvable()
        if candidature.statut != STATUT_BROUILLON:
            raise CandidatureDejaSoumise()

        candidature.deplacement_physique = deplacement_physique
        self._repository.enregistrer_candidature(candidature)
        return candidature
