"""Cas d'utilisation : simuler le paiement des frais de dossier — Couche BLL (US-006).

Aucune transaction réelle : le paiement réel est délégué à FDS Pay (hors périmètre V1).
La simulation attribue une référence `PAY-SIM-AAAA-NNNN` et débloque l'étape suivante (dépôt des pièces).
"""

import secrets
from typing import Any, Callable

from backend.bll.validation_informations import normaliser_telephone_haitien
from backend.entities.candidat import CAMPAGNE_COURANTE
from backend.entities.candidature import (
    METHODES_PAIEMENT,
    STATUT_BROUILLON,
    STATUT_PAIEMENT_SIMULE,
    Candidature,
)
from backend.entities.erreurs import (
    CandidatureDejaSoumise,
    CandidatureIntrouvable,
    EtapePrecedenteIncomplete,
    ErreurMetier,
    InformationsInvalides,
)
from backend.ports.candidature_repository import ICandidatureRepository

_ESSAIS_MAX = 20


def _numero_aleatoire() -> int:
    return secrets.randbelow(10_000)


class SimulerPaiementUseCase:
    """Enregistre un paiement simulé MonCash ou NatCash sur un brouillon de candidature."""

    def __init__(
        self,
        repository: ICandidatureRepository,
        generer_numero: Callable[[], int] = _numero_aleatoire,
    ) -> None:
        self._repository = repository
        self._generer_numero = generer_numero

    def executer(self, candidature_id: str, methode: Any, numero_telephone: Any) -> Candidature:
        candidature = self._repository.obtenir_candidature(candidature_id)
        if candidature is None:
            raise CandidatureIntrouvable()
        if candidature.statut != STATUT_BROUILLON:
            raise CandidatureDejaSoumise()
        # Le paiement vient après l'étape 2 : la question sur le déplacement physique doit être répondue
        if candidature.deplacement_physique is None:
            raise EtapePrecedenteIncomplete()
        # Idempotent : un double envoi (réponse perdue, double clic) ne crée jamais un second paiement
        if candidature.statut_paiement == STATUT_PAIEMENT_SIMULE:
            return candidature

        erreurs: dict[str, str] = {}
        methode_normalisee = str(methode or "").strip().upper()
        if methode_normalisee not in METHODES_PAIEMENT:
            erreurs["methode_paiement"] = "Choisissez MonCash ou NatCash."
        numero = normaliser_telephone_haitien(numero_telephone)
        if numero is None:
            erreurs["numero_telephone"] = "Numéro haïtien invalide (8 chiffres, ex. 37 12 34 56)."
        if erreurs:
            raise InformationsInvalides(erreurs)

        candidature.methode_paiement = methode_normalisee
        candidature.numero_paiement = numero
        candidature.reference_paiement = self._nouvelle_reference()
        candidature.statut_paiement = STATUT_PAIEMENT_SIMULE
        self._repository.enregistrer_candidature(candidature)
        return candidature

    def _nouvelle_reference(self) -> str:
        for _ in range(_ESSAIS_MAX):
            reference = f"PAY-SIM-{CAMPAGNE_COURANTE}-{self._generer_numero():04d}"
            if not self._repository.reference_paiement_existe(reference):
                return reference
        raise ErreurMetier("Impossible de générer une référence de paiement simulé.")
