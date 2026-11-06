"""Implémentation SQLAlchemy du port ICalendrierRepository — Couche DAL (US-028).

Aucune logique métier ici : uniquement la traduction entre entité du domaine et ligne en base.
"""

from datetime import timezone

from sqlalchemy.orm import Session

from backend.dal.models import CalendrierAdmissionModel
from backend.entities.calendrier_admission import CalendrierAdmission
from backend.ports.calendrier_repository import ICalendrierRepository

_CHAMPS = ("date_ouverture", "date_limite", "date_concours", "date_resultats", "date_rentree", "modifie_par", "modifie_le")


class SqlCalendrierRepository(ICalendrierRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def obtenir_en_vigueur(self) -> CalendrierAdmission | None:
        modele = self._session.query(CalendrierAdmissionModel).order_by(CalendrierAdmissionModel.numero.desc()).first()
        if modele is None:
            return None
        valeurs = {champ: getattr(modele, champ) for champ in _CHAMPS}
        if valeurs["modifie_le"].tzinfo is None:  # SQLite restitue des dates sans fuseau
            valeurs["modifie_le"] = valeurs["modifie_le"].replace(tzinfo=timezone.utc)
        return CalendrierAdmission(id=modele.id, **valeurs)

    def ajouter(self, calendrier: CalendrierAdmission) -> None:
        self._session.add(
            CalendrierAdmissionModel(id=calendrier.id, **{champ: getattr(calendrier, champ) for champ in _CHAMPS})
        )
        self._session.commit()
