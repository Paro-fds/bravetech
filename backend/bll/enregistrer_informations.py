"""Cas d'utilisation : enregistrer les informations personnelles d'un candidat — Couche BLL (US-005).

Le formulaire est enregistré dès l'étape 1 : un candidat dont la connexion coupe reprend son brouillon.
"""

import uuid
from datetime import datetime, timezone
from typing import Any

from backend.bll.validation_informations import valider_informations
from backend.entities.candidat import CAMPAGNE_COURANTE, Candidat
from backend.entities.candidature import STATUT_BROUILLON, Candidature
from backend.entities.erreurs import CandidatureDejaExistante, CandidatureDejaSoumise, CandidatureIntrouvable
from backend.ports.candidature_repository import ICandidatureRepository


class EnregistrerInformationsUseCase:
    """Crée le candidat et sa candidature en brouillon à partir de l'étape 1."""

    def __init__(self, repository: ICandidatureRepository) -> None:
        self._repository = repository

    def executer(self, donnees: dict[str, Any]) -> tuple[Candidat, Candidature]:
        propres = valider_informations(donnees)

        if self._repository.trouver_candidat_par_email_campagne(propres["email"], CAMPAGNE_COURANTE):
            raise CandidatureDejaExistante()

        maintenant = datetime.now(timezone.utc)
        candidat = Candidat(
            id=str(uuid.uuid4()),
            campagne=CAMPAGNE_COURANTE,
            created_at=maintenant,
            **propres,
        )
        candidature = Candidature(id=str(uuid.uuid4()), candidat_id=candidat.id, created_at=maintenant)
        self._repository.creer(candidat, candidature)
        return candidat, candidature


class MettreAJourInformationsUseCase:
    """Met à jour les informations personnelles d'un brouillon existant (retour à l'étape 1)."""

    def __init__(self, repository: ICandidatureRepository) -> None:
        self._repository = repository

    def executer(self, candidature_id: str, donnees: dict[str, Any]) -> tuple[Candidat, Candidature]:
        candidature = self._repository.obtenir_candidature(candidature_id)
        if candidature is None:
            raise CandidatureIntrouvable()
        if candidature.statut != STATUT_BROUILLON:
            raise CandidatureDejaSoumise()

        candidat = self._repository.obtenir_candidat(candidature.candidat_id)
        if candidat is None:
            raise CandidatureIntrouvable()

        propres = valider_informations(donnees)

        if propres["email"] != candidat.email:
            existant = self._repository.trouver_candidat_par_email_campagne(propres["email"], candidat.campagne)
            if existant is not None and existant.id != candidat.id:
                raise CandidatureDejaExistante()

        for champ, valeur in propres.items():
            setattr(candidat, champ, valeur)
        self._repository.enregistrer_candidat(candidat)
        return candidat, candidature
