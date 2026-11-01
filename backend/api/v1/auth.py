"""Router d'authentification du personnel — Couche Présentation / API v1 (US-011).
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from backend.api.v1.limiteur import adresse_client
from backend.api.v1.securite import (
    get_emetteur_jeton,
    get_hacheur,
    get_utilisateur_repository,
    limiteur_connexion,
)
from backend.bll.authentification import AuthentifierUtilisateurUseCase
from backend.entities.erreurs import IdentifiantsInvalides
from backend.ports.securite import IEmetteurJeton, IHacheurMotDePasse
from backend.ports.utilisateur_repository import IUtilisateurRepository

router = APIRouter(prefix="/auth", tags=["Authentification"])
_journal = logging.getLogger(__name__)


class ConnexionRequest(BaseModel):
    email: str = Field(max_length=255)
    password: str = Field(max_length=128)


class JetonResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # secondes


@router.post("/token", response_model=JetonResponse, summary="Connexion du personnel (JWT, 60 minutes)")
def connexion(
    payload: ConnexionRequest,
    requete: Request,
    utilisateurs: IUtilisateurRepository = Depends(get_utilisateur_repository),
    hacheur: IHacheurMotDePasse = Depends(get_hacheur),
    emetteur: IEmetteurJeton = Depends(get_emetteur_jeton),
):
    """Retourne un jeton si les identifiants sont corrects. Même message pour tout échec ; 429 après 5 échecs en 60 s."""
    client = adresse_client(requete)
    if limiteur_connexion.est_atteint(client):
        raise HTTPException(
            status_code=429,
            detail="Trop de tentatives de connexion. Patientez une minute puis réessayez.",
            headers={"Retry-After": "60"},
        )
    try:
        jeton = AuthentifierUtilisateurUseCase(utilisateurs, hacheur, emetteur).executer(payload.email, payload.password)
    except IdentifiantsInvalides:
        limiteur_connexion.enregistrer(client)
        _journal.warning("Échec de connexion du personnel depuis %s", client)
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")
    return JetonResponse(access_token=jeton.jeton, expires_in=jeton.expire_dans_secondes)
