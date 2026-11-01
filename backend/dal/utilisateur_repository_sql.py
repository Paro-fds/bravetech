"""Implémentation SQLAlchemy du port IUtilisateurRepository — Couche DAL (US-011).
"""

from datetime import timezone

from sqlalchemy.orm import Session

from backend.dal.models import UtilisateurModel
from backend.entities.utilisateur import Utilisateur
from backend.ports.utilisateur_repository import IUtilisateurRepository

_CHAMPS = ("id", "email", "mot_de_passe_hash", "role", "est_actif")


def _vers_entite(modele: UtilisateurModel) -> Utilisateur:
    cree = modele.created_at
    if cree is not None and cree.tzinfo is None:
        cree = cree.replace(tzinfo=timezone.utc)  # SQLite restitue des dates sans fuseau
    return Utilisateur(created_at=cree, **{champ: getattr(modele, champ) for champ in _CHAMPS})


class SqlUtilisateurRepository(IUtilisateurRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def trouver_par_email(self, email: str) -> Utilisateur | None:
        modele = self._session.query(UtilisateurModel).filter(UtilisateurModel.email == email).first()
        return _vers_entite(modele) if modele else None

    def obtenir(self, utilisateur_id: str) -> Utilisateur | None:
        modele = self._session.get(UtilisateurModel, utilisateur_id)
        return _vers_entite(modele) if modele else None

    def creer(self, utilisateur: Utilisateur) -> None:
        self._session.add(UtilisateurModel(
            created_at=utilisateur.created_at, **{champ: getattr(utilisateur, champ) for champ in _CHAMPS}
        ))
        self._session.commit()
