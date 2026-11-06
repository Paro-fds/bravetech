"""DTO du calendrier d'admission (US-028) — Couche Présentation / API v1.
"""

from datetime import date, datetime

from pydantic import BaseModel


class CalendrierPublicResponse(BaseModel):
    """Dates de la session en cours et état de la période aujourd'hui (heure d'Haïti). Dates nulles : à confirmer."""

    etat: str  # non_definie | a_venir | ouverte | fermee
    date_ouverture: date | None = None
    date_limite: date | None = None
    date_concours: date | None = None
    date_resultats: date | None = None
    date_rentree: date | None = None


class CalendrierAdminResponse(CalendrierPublicResponse):
    modifie_par: str | None = None  # email de l'auteur de la dernière modification
    modifie_le: datetime | None = None


class CalendrierRequest(BaseModel):
    date_ouverture: date | None = None
    date_limite: date | None = None
    date_concours: date | None = None
    date_resultats: date | None = None
    date_rentree: date | None = None
