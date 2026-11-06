"""Cas d'utilisation du calendrier d'admission — Couche BLL (US-028).

Les dates sont des jours du calendrier d'Haïti : la période est ouverte du jour d'ouverture à 0 h jusqu'au jour limite
à 23 h 59, heure de Port-au-Prince, quel que soit le fuseau du serveur (UTC sur la VM).
"""

import uuid
from collections.abc import Callable
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

from backend.entities.calendrier_admission import (
    CalendrierAdmission,
    candidatures_acceptees,
    ecarts_chronologiques,
    etat_periode,
)
from backend.entities.erreurs import CandidaturesFermees, InformationsInvalides
from backend.entities.utilisateur import Utilisateur
from backend.ports.calendrier_repository import ICalendrierRepository

FUSEAU_HAITI = ZoneInfo("America/Port-au-Prince")

Horloge = Callable[[], datetime]


def maintenant_utc() -> datetime:
    return datetime.now(timezone.utc)


def jour_haiti(instant: datetime) -> date:
    return instant.astimezone(FUSEAU_HAITI).date()


class ConsulterCalendrierUseCase:
    """Calendrier en vigueur et état de la période aujourd'hui."""

    def __init__(self, calendriers: ICalendrierRepository, horloge: Horloge = maintenant_utc) -> None:
        self._calendriers = calendriers
        self._horloge = horloge

    def executer(self) -> tuple[CalendrierAdmission | None, str]:
        calendrier = self._calendriers.obtenir_en_vigueur()
        return calendrier, etat_periode(calendrier, jour_haiti(self._horloge()))


class ControlerPeriodeUseCase:
    """Refuse de commencer ou de soumettre une candidature hors période.

    Le suivi et le remplacement d'une pièce refusée ne passent pas par ce contrôle : ils restent possibles après la date
    limite, sinon un candidat ne pourrait plus corriger un dossier envoyé à temps.
    """

    def __init__(self, calendriers: ICalendrierRepository, horloge: Horloge = maintenant_utc) -> None:
        self._consulter = ConsulterCalendrierUseCase(calendriers, horloge)

    def executer(self) -> None:
        calendrier, etat = self._consulter.executer()
        if not candidatures_acceptees(etat):
            raise CandidaturesFermees(calendrier)


class ModifierCalendrierUseCase:
    """Enregistre une nouvelle version du calendrier, avec son auteur (audit)."""

    def __init__(self, calendriers: ICalendrierRepository, horloge: Horloge = maintenant_utc) -> None:
        self._calendriers = calendriers
        self._horloge = horloge

    def executer(self, dates: dict[str, date | None], auteur: Utilisateur) -> CalendrierAdmission:
        erreurs: dict[str, str] = {}
        if dates.get("date_ouverture") is None:
            erreurs["date_ouverture"] = "Indiquez la date d'ouverture des candidatures."
        if dates.get("date_limite") is None:
            erreurs["date_limite"] = "Indiquez la date limite de dépôt."
        erreurs = erreurs or ecarts_chronologiques(dates)
        if erreurs:
            raise InformationsInvalides(erreurs)

        calendrier = CalendrierAdmission(
            id=str(uuid.uuid4()),
            date_ouverture=dates["date_ouverture"],
            date_limite=dates["date_limite"],
            date_concours=dates.get("date_concours"),
            date_resultats=dates.get("date_resultats"),
            date_rentree=dates.get("date_rentree"),
            modifie_par=auteur.id,
            modifie_le=self._horloge(),
        )
        self._calendriers.ajouter(calendrier)
        return calendrier
