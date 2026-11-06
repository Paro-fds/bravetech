"""Calendrier d'admission, côté public (US-028) — Couche Présentation / API v1.

Expose les dates de la session en cours, et fournit le contrôle de période posé sur la création et la soumission
d'une candidature (`exiger_periode_ouverte`).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.api.v1.dto.calendrier_dto import CalendrierPublicResponse
from backend.bll.calendrier_admission import ConsulterCalendrierUseCase, ControlerPeriodeUseCase
from backend.dal.calendrier_repository_sql import SqlCalendrierRepository
from backend.dal.database import get_db
from backend.entities.calendrier_admission import CalendrierAdmission
from backend.entities.erreurs import CandidaturesFermees
from backend.ports.calendrier_repository import ICalendrierRepository

router = APIRouter(prefix="/calendrier", tags=["Calendrier d'admission"])

_DATES = ("date_ouverture", "date_limite", "date_concours", "date_resultats", "date_rentree")


def get_calendrier_repository(db: Session = Depends(get_db)) -> ICalendrierRepository:
    return SqlCalendrierRepository(db)


def dates_du_calendrier(calendrier: CalendrierAdmission | None) -> dict:
    return {champ: getattr(calendrier, champ) for champ in _DATES} if calendrier else {}


@router.get("", response_model=CalendrierPublicResponse, summary="Dates de la session d'admission en cours (public)")
def obtenir_calendrier(calendriers: ICalendrierRepository = Depends(get_calendrier_repository)):
    calendrier, etat = ConsulterCalendrierUseCase(calendriers).executer()
    return CalendrierPublicResponse(etat=etat, **dates_du_calendrier(calendrier))


def exiger_periode_ouverte(calendriers: ICalendrierRepository = Depends(get_calendrier_repository)) -> None:
    """403 `candidatures_fermees` avant l'ouverture ou après la date limite, avec les dates pour le message."""
    try:
        ControlerPeriodeUseCase(calendriers).executer()
    except CandidaturesFermees as erreur:
        dates = {champ: valeur.isoformat() for champ, valeur in dates_du_calendrier(erreur.calendrier).items() if valeur}
        raise HTTPException(
            status_code=403,
            detail={"code": "candidatures_fermees", "message": "Les candidatures sont fermées.", **dates},
        )
