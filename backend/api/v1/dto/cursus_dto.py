"""DTOs (Data Transfer Objects) pour les cursus — Couche Présentation / API.
"""

from typing import Any
from pydantic import BaseModel, ConfigDict


class CursusListItemResponse(BaseModel):
    """Réponse allégée pour l'affichage dans la liste / catalogue d'accueil."""
    id: str
    nom: str
    duree_annees: int
    description_courte: str
    date_ouverture_inscription: str
    date_fermeture_inscription: str
    est_ouvert: bool

    model_config = ConfigDict(from_attributes=True)


class CursusDetailResponse(CursusListItemResponse):
    """Réponse détaillée avec la maquette pédagogique complète."""
    description_longue: str
    niveaux: dict[str, list[dict[str, Any]]]

    model_config = ConfigDict(from_attributes=True)
