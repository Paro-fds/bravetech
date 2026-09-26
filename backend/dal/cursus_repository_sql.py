"""Implémentation SQLAlchemy du port ICursusRepository — Couche DAL.
"""

from sqlalchemy.orm import joinedload
from backend.entities.cursus import Cursus
from backend.entities.document_requis import DocumentRequis
from backend.ports.cursus_repository import ICursusRepository
from backend.dal.models import CursusModel, DocumentRequisModel
from backend.dal.database import SessionLocal, Base, engine
from backend.dal.cursus_loader import charger_cursus_depuis_disque


class SQLAlchemyCursusRepository(ICursusRepository):
    """Adaptateur de persistance utilisant SQLAlchemy pour stocker et interroger les cursus."""

    def __init__(self, session_factory=SessionLocal) -> None:
        self._session_factory = session_factory
        # Création automatique des tables
        Base.metadata.create_all(bind=engine)
        self._initialiser_si_vide()

    def _initialiser_si_vide(self) -> None:
        """Initialise la table avec les cursus et pièces requis depuis le disque s'il n'y a aucune donnée."""
        with self._session_factory() as session:
            count = session.query(CursusModel).count()
            if count == 0:
                donnees = charger_cursus_depuis_disque()
                self._sauvegarder_dans_session(session, donnees)
                session.commit()

    def _sauvegarder_dans_session(self, session, cursus_liste: list[Cursus]) -> None:
        for c in cursus_liste:
            model = session.query(CursusModel).filter(CursusModel.id == c.id).first()
            if not model:
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
            else:
                model.nom = c.nom
                model.duree_annees = c.duree_annees
                model.description_courte = c.description_courte
                model.description_longue = c.description_longue
                model.date_ouverture_inscription = c.date_ouverture_inscription
                model.date_fermeture_inscription = c.date_fermeture_inscription
                model.est_ouvert = c.est_ouvert
                model.niveaux = c.niveaux

            # Pièces requises
            session.query(DocumentRequisModel).filter(DocumentRequisModel.cursus_id == c.id).delete()
            for doc in c.documents_requis:
                doc_model = DocumentRequisModel(
                    id=doc.id,
                    cursus_id=c.id,
                    nom=doc.nom,
                    description=doc.description,
                    format_accepte=doc.format_accepte,
                    taille_max_mo=doc.taille_max_mo,
                    est_obligatoire=doc.est_obligatoire,
                )
                session.add(doc_model)

    def _model_to_entity(self, model: CursusModel) -> Cursus:
        docs = [
            DocumentRequis(
                id=d.id,
                cursus_id=d.cursus_id,
                nom=d.nom,
                description=d.description,
                format_accepte=d.format_accepte,
                taille_max_mo=d.taille_max_mo,
                est_obligatoire=d.est_obligatoire,
            )
            for d in (model.documents_requis or [])
        ]
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
            documents_requis=docs,
        )

    def lister_tous(self) -> list[Cursus]:
        with self._session_factory() as session:
            models = session.query(CursusModel).all()
            return [self._model_to_entity(m) for m in models]

    def obtenir_par_id(self, cursus_id: str) -> Cursus | None:
        with self._session_factory() as session:
            model = (
                session.query(CursusModel)
                .options(joinedload(CursusModel.documents_requis))
                .filter(CursusModel.id == cursus_id)
                .first()
            )
            if not model:
                return None
            return self._model_to_entity(model)

    def sauvegarder_tous(self, cursus_liste: list[Cursus]) -> None:
        with self._session_factory() as session:
            self._sauvegarder_dans_session(session, cursus_liste)
            session.commit()
