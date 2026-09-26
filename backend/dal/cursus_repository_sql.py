"""Implémentation SQLAlchemy du port ICursusRepository — Couche DAL.
"""

from sqlalchemy.orm import Session
from backend.entities.cursus import Cursus
from backend.ports.cursus_repository import ICursusRepository
from backend.dal.models import CursusModel
from backend.dal.database import SessionLocal, Base, engine
from backend.dal.cursus_loader import charger_cursus_depuis_disque


class SQLAlchemyCursusRepository(ICursusRepository):
    """Adaptateur de persistance utilisant SQLAlchemy pour stocker et interroger les cursus."""

    def __init__(self, session_factory=SessionLocal) -> None:
        self._session_factory = session_factory
        # Création automatique de la table si elle n'existe pas encore
        Base.metadata.create_all(bind=engine)
        self._initialiser_si_vide()

    def _initialiser_si_vide(self) -> None:
        """Initialise la table avec les cursus officiels depuis le disque s'il n'y a aucune donnée."""
        with self._session_factory() as session:
            count = session.query(CursusModel).count()
            if count == 0:
                donnees = charger_cursus_depuis_disque()
                for c in donnees:
                    model = CursusModel(
                        id=c.id,
                        nom=c.nom,
                        duree_annees=c.duree_annees,
                        description_courte=c.description_courte,
                        description_longue=c.description_longue,
                        date_ouverture_inscription=c.date_ouverture_inscription,
                        date_fermeture_inscription=c.date_fermeture_inscription,
                        est_ouvert=c.est_ouvert,
                        niveaux=c.niveaux,
                    )
                    session.add(model)
                session.commit()

    def _model_to_entity(self, model: CursusModel) -> Cursus:
        return Cursus(
            id=model.id,
            nom=model.nom,
            duree_annees=model.duree_annees,
            description_courte=model.description_courte,
            description_longue=model.description_longue or "",
            date_ouverture_inscription=model.date_ouverture_inscription,
            date_fermeture_inscription=model.date_fermeture_inscription,
            est_ouvert=model.est_ouvert,
            niveaux=model.niveaux or {},
        )

    def lister_tous(self) -> list[Cursus]:
        with self._session_factory() as session:
            models = session.query(CursusModel).all()
            return [self._model_to_entity(m) for m in models]

    def obtenir_par_id(self, cursus_id: str) -> Cursus | None:
        with self._session_factory() as session:
            model = session.query(CursusModel).filter(CursusModel.id == cursus_id).first()
            if not model:
                return None
            return self._model_to_entity(model)

    def sauvegarder_tous(self, cursus_liste: list[Cursus]) -> None:
        with self._session_factory() as session:
            for c in cursus_liste:
                model = session.query(CursusModel).filter(CursusModel.id == c.id).first()
                if model:
                    model.nom = c.nom
                    model.duree_annees = c.duree_annees
                    model.description_courte = c.description_courte
                    model.description_longue = c.description_longue
                    model.date_ouverture_inscription = c.date_ouverture_inscription
                    model.date_fermeture_inscription = c.date_fermeture_inscription
                    model.est_ouvert = c.est_ouvert
                    model.niveaux = c.niveaux
                else:
                    session.add(CursusModel(
                        id=c.id,
                        nom=c.nom,
                        duree_annees=c.duree_annees,
                        description_courte=c.description_courte,
                        description_longue=c.description_longue,
                        date_ouverture_inscription=c.date_ouverture_inscription,
                        date_fermeture_inscription=c.date_fermeture_inscription,
                        est_ouvert=c.est_ouvert,
                        niveaux=c.niveaux,
                    ))
            session.commit()
