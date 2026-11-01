"""Router des candidatures — Couche Présentation / API v1 (US-005).

Le candidat n'a pas de compte : son brouillon est identifié par un identifiant UUID non devinable,
conservé par son navigateur pour reprendre le formulaire après une coupure de connexion.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.api.v1.dto.candidature_dto import (
    BrouillonResponse,
    DeplacementPhysiqueRequest,
    InformationsPersonnellesRequest,
    InformationsPersonnellesResponse,
    PaiementSimuleRequest,
)
from backend.bll.definir_deplacement_physique import DefinirDeplacementPhysiqueUseCase
from backend.bll.enregistrer_informations import EnregistrerInformationsUseCase, MettreAJourInformationsUseCase
from backend.bll.obtenir_brouillon import ObtenirBrouillonUseCase
from backend.bll.simuler_paiement import SimulerPaiementUseCase
from backend.dal.candidature_repository_sql import SqlCandidatureRepository
from backend.dal.database import get_db
from backend.entities.candidat import Candidat
from backend.entities.candidature import FRAIS_DOSSIER_HTG, Candidature
from backend.entities.erreurs import (
    CandidatureDejaExistante,
    CandidatureDejaSoumise,
    CandidatureIntrouvable,
    EtapePrecedenteIncomplete,
    InformationsInvalides,
)
from backend.ports.candidature_repository import ICandidatureRepository

router = APIRouter(prefix="/candidatures", tags=["Candidature"])

_MESSAGE_INTROUVABLE = "Brouillon de candidature introuvable."


def get_candidature_repository(db: Session = Depends(get_db)) -> ICandidatureRepository:
    """Fournisseur de dépendance pour le repository des candidatures (SQLAlchemy)."""
    return SqlCandidatureRepository(db)


def _reponse(candidat: Candidat, candidature: Candidature) -> BrouillonResponse:
    return BrouillonResponse(
        candidature_id=candidature.id,
        statut=candidature.statut,
        deplacement_physique=candidature.deplacement_physique,
        statut_paiement=candidature.statut_paiement,
        methode_paiement=candidature.methode_paiement,
        reference_paiement=candidature.reference_paiement,
        montant_htg=FRAIS_DOSSIER_HTG,
        informations=InformationsPersonnellesResponse.model_validate(candidat),
    )


def _vers_http(erreur: Exception) -> HTTPException:
    """Traduit une erreur métier en réponse HTTP, sans détail interne."""
    if isinstance(erreur, InformationsInvalides):
        return HTTPException(status_code=422, detail={"erreurs": erreur.erreurs})
    if isinstance(erreur, CandidatureIntrouvable):
        return HTTPException(status_code=404, detail=_MESSAGE_INTROUVABLE)
    if isinstance(erreur, CandidatureDejaExistante):
        return HTTPException(status_code=409, detail="Une candidature existe déjà pour cet email.")
    if isinstance(erreur, EtapePrecedenteIncomplete):
        return HTTPException(status_code=409, detail="Répondez d'abord aux étapes précédentes de la candidature.")
    if isinstance(erreur, CandidatureDejaSoumise):
        return HTTPException(status_code=409, detail="Cette candidature est déjà soumise et n'est plus modifiable.")
    raise erreur


@router.post("", response_model=BrouillonResponse, status_code=201, summary="Créer un brouillon (étape 1)")
def creer_brouillon(
    payload: InformationsPersonnellesRequest,
    repo: ICandidatureRepository = Depends(get_candidature_repository),
):
    """Valide les informations personnelles et crée le brouillon de candidature."""
    try:
        candidat, candidature = EnregistrerInformationsUseCase(repo).executer(payload.model_dump())
    except (InformationsInvalides, CandidatureDejaExistante) as erreur:
        raise _vers_http(erreur)
    return _reponse(candidat, candidature)


@router.get("/{candidature_id}", response_model=BrouillonResponse, summary="Reprendre un brouillon")
def obtenir_brouillon(
    candidature_id: str,
    repo: ICandidatureRepository = Depends(get_candidature_repository),
):
    """Retourne l'état d'un brouillon pour reprendre le formulaire."""
    try:
        candidat, candidature = ObtenirBrouillonUseCase(repo).executer(candidature_id)
    except CandidatureIntrouvable as erreur:
        raise _vers_http(erreur)
    return _reponse(candidat, candidature)


@router.put("/{candidature_id}/informations", response_model=BrouillonResponse, summary="Modifier l'étape 1")
def modifier_informations(
    candidature_id: str,
    payload: InformationsPersonnellesRequest,
    repo: ICandidatureRepository = Depends(get_candidature_repository),
):
    """Met à jour les informations personnelles d'un brouillon."""
    try:
        candidat, candidature = MettreAJourInformationsUseCase(repo).executer(candidature_id, payload.model_dump())
    except (InformationsInvalides, CandidatureIntrouvable, CandidatureDejaExistante, CandidatureDejaSoumise) as erreur:
        raise _vers_http(erreur)
    return _reponse(candidat, candidature)


@router.put(
    "/{candidature_id}/deplacement-physique",
    response_model=BrouillonResponse,
    summary="Répondre à la question sur le déplacement physique",
)
def definir_deplacement_physique(
    candidature_id: str,
    payload: DeplacementPhysiqueRequest,
    repo: ICandidatureRepository = Depends(get_candidature_repository),
):
    """Enregistre la réponse obligatoire `deplacement_physique`."""
    try:
        candidature = DefinirDeplacementPhysiqueUseCase(repo).executer(candidature_id, payload.deplacement_physique)
        candidat, candidature = ObtenirBrouillonUseCase(repo).executer(candidature.id)
    except (InformationsInvalides, CandidatureIntrouvable, CandidatureDejaSoumise) as erreur:
        raise _vers_http(erreur)
    return _reponse(candidat, candidature)


@router.post(
    "/{candidature_id}/paiement",
    response_model=BrouillonResponse,
    summary="Simuler le paiement des frais de dossier (aucun montant réel prélevé)",
)
def simuler_paiement(
    candidature_id: str,
    payload: PaiementSimuleRequest,
    repo: ICandidatureRepository = Depends(get_candidature_repository),
):
    """Enregistre un paiement SIMULÉ MonCash ou NatCash et attribue la référence `PAY-SIM-AAAA-NNNN`."""
    try:
        candidature = SimulerPaiementUseCase(repo).executer(candidature_id, payload.methode, payload.numero_telephone)
        candidat, candidature = ObtenirBrouillonUseCase(repo).executer(candidature.id)
    except (InformationsInvalides, CandidatureIntrouvable, EtapePrecedenteIncomplete, CandidatureDejaSoumise) as erreur:
        raise _vers_http(erreur)
    return _reponse(candidat, candidature)
