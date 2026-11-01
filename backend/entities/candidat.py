"""Entité Candidat — Couche Domain.

Un Candidat est la personne qui postule pour une campagne d'admission donnée.
L'admission est unique (Premier cycle MPC, ADR-008) : aucun cursus n'est porté par le Candidat.
L'unicité est portée par le couple (email, campagne).

Règle absolue (Clean Architecture) :
Aucun import de framework (FastAPI, SQLAlchemy), ni d'aucune couche externe (dal, bll, api).
"""

from dataclasses import dataclass
from datetime import date, datetime

# Campagne d'admission en cours
CAMPAGNE_COURANTE = 2026

SEXES = ("M", "F")

DEPARTEMENTS = (
    "Artibonite",
    "Centre",
    "Grand'Anse",
    "Nippes",
    "Nord",
    "Nord-Est",
    "Nord-Ouest",
    "Ouest",
    "Sud",
    "Sud-Est",
)


@dataclass
class Candidat:
    """Informations personnelles d'une personne candidate à l'admission."""
    id: str
    nom: str
    prenom: str
    date_naissance: date
    sexe: str
    telephone: str  # format normalisé : +509XXXXXXXX
    email: str  # en minuscules
    departement: str
    commune: str
    campagne: int
    created_at: datetime
