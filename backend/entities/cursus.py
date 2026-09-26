"""Entité Cursus — Couche Domain.

Règle absolue (Clean Architecture) :
Aucun import de framework (FastAPI, SQLAlchemy), ni d'aucune couche externe (dal, bll, api).
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Matiere:
    """Représente une unité d'enseignement au sein d'un niveau."""
    item: int
    titre: str
    code: str | None = None
    heures: int | None = None
    heures_theorie: int | None = None
    heures_tp: int | None = None


@dataclass
class Cursus:
    """Entité pure représentant un cursus académique de la Faculté des Sciences."""
    id: str  # slug, ex: "mpc", "genie-civil", "genie-electronique"
    nom: str
    duree_annees: int
    description_courte: str
    description_longue: str
    date_ouverture_inscription: str
    date_fermeture_inscription: str
    est_ouvert: bool = True
    niveaux: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
