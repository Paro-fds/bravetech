"""DTOs (Data Transfer Objects) des candidatures — Couche Présentation / API (US-005).
"""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field, StrictBool


class InformationsPersonnellesRequest(BaseModel):
    """Saisie de l'étape 1. Les règles métier (format, plages) sont validées par la couche BLL."""
    nom: str = Field(max_length=255)
    prenom: str = Field(max_length=255)
    date_naissance: date
    sexe: str = Field(max_length=10)
    telephone: str = Field(max_length=50)
    email: str = Field(max_length=255)
    departement: str = Field(max_length=100)
    commune: str = Field(max_length=255)


class DeplacementPhysiqueRequest(BaseModel):
    """Réponse obligatoire à la question sur le déplacement physique (booléen strict)."""
    deplacement_physique: StrictBool


class InformationsPersonnellesResponse(BaseModel):
    nom: str
    prenom: str
    date_naissance: date
    sexe: str
    telephone: str
    email: str
    departement: str
    commune: str

    model_config = ConfigDict(from_attributes=True)


class BrouillonResponse(BaseModel):
    """État d'un brouillon de candidature, identifié par un identifiant non devinable."""
    candidature_id: str
    statut: str
    deplacement_physique: bool | None
    informations: InformationsPersonnellesResponse
