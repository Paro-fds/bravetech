"""Entité DocumentRequis — Couche Domain.

Règle absolue (Clean Architecture) :
Aucun import de framework (FastAPI, SQLAlchemy), ni d'aucune couche externe (dal, bll, api).
"""

from dataclasses import dataclass


@dataclass
class DocumentRequis:
    """Pièce justificative exigée pour la constitution d'un dossier de candidature."""
    id: str  # ex: "mpc-acte-naissance", "mpc-bac"
    cursus_id: str
    nom: str
    description: str
    format_accepte: str = "PDF, JPG, PNG"
    taille_max_mo: int = 5
    est_obligatoire: bool = True
