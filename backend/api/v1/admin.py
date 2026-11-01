"""Routes d'administration — Couche Présentation / API v1.

Toutes les routes de ce routeur exigent un jeton valide (`get_current_admin`) : la protection est posée sur le routeur,
donc une future route ajoutée ici ne peut pas l'oublier.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.api.v1.securite import get_current_admin
from backend.entities.utilisateur import Utilisateur

router = APIRouter(prefix="/admin", tags=["Administration"], dependencies=[Depends(get_current_admin)])


class UtilisateurCourantResponse(BaseModel):
    id: str
    email: str
    role: str


@router.get("/moi", response_model=UtilisateurCourantResponse, summary="Compte connecté")
def moi(utilisateur: Utilisateur = Depends(get_current_admin)):
    return UtilisateurCourantResponse(id=utilisateur.id, email=utilisateur.email, role=utilisateur.role)
