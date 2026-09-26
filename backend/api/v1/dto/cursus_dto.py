"""DTOs (Data Transfer Objects) pour les cursus — Couche Présentation / API.
"""

from typing import Any
from pydantic import BaseModel, ConfigDict


class DocumentRequisResponse(BaseModel):
    """Représentation d'une pièce justificative requise."""
    id: str
    nom: str
    description: str
    format_accepte: str
    taille_max_mo: int
    est_obligatoire: bool

    model_config = ConfigDict(from_attributes=True)


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
    """Réponse détaillée avec la maquette pédagogique complète et les pièces exigées."""
    description_longue: str
    niveaux: dict[str, list[dict[str, Any]]]
    documents_requis: list[DocumentRequisResponse] = []

    model_config = ConfigDict(from_attributes=True)
