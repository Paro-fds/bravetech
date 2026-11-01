"""Implémentation SQLAlchemy du port ICandidatureRepository — Couche DAL.

Aucune logique métier ici : uniquement la traduction entre entités du domaine et lignes en base.
"""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.dal.models import CandidatModel, CandidatureModel
from backend.entities.candidat import Candidat
from backend.entities.candidature import Candidature
from backend.entities.erreurs import CandidatureDejaExistante
from backend.ports.candidature_repository import ICandidatureRepository

_CHAMPS_CANDIDAT = (
    "nom", "prenom", "date_naissance", "sexe", "telephone", "email", "departement", "commune", "campagne",
)
_CHAMPS_CANDIDATURE = (
    "deplacement_physique", "statut_paiement", "reference_dossier", "statut",
    "methode_paiement", "reference_paiement", "numero_paiement",
)


def _vers_candidat(modele: CandidatModel) -> Candidat:
    return Candidat(
        id=modele.id,
        created_at=modele.created_at,
        **{champ: getattr(modele, champ) for champ in _CHAMPS_CANDIDAT},
    )


def _vers_candidature(modele: CandidatureModel) -> Candidature:
    return Candidature(
        id=modele.id,
        candidat_id=modele.candidat_id,
        created_at=modele.created_at,
        **{champ: getattr(modele, champ) for champ in _CHAMPS_CANDIDATURE},
    )


class SqlCandidatureRepository(ICandidatureRepository):
    """Adaptateur DAL stockant candidats et candidatures dans PostgreSQL (SQLite en dev)."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def creer(self, candidat: Candidat, candidature: Candidature) -> None:
        self._session.add(CandidatModel(
            id=candidat.id,
            created_at=candidat.created_at,
            **{champ: getattr(candidat, champ) for champ in _CHAMPS_CANDIDAT},
        ))
        self._session.flush()  # le candidat doit exister avant la candidature (clé étrangère)
        self._session.add(CandidatureModel(
            id=candidature.id,
            candidat_id=candidature.candidat_id,
            created_at=candidature.created_at,
            **{champ: getattr(candidature, champ) for champ in _CHAMPS_CANDIDATURE},
        ))
        self._valider()

    def obtenir_candidature(self, candidature_id: str) -> Candidature | None:
        modele = self._session.get(CandidatureModel, candidature_id)
        return _vers_candidature(modele) if modele else None

    def obtenir_candidat(self, candidat_id: str) -> Candidat | None:
        modele = self._session.get(CandidatModel, candidat_id)
        return _vers_candidat(modele) if modele else None

    def trouver_candidat_par_email_campagne(self, email: str, campagne: int) -> Candidat | None:
        modele = (
            self._session.query(CandidatModel)
            .filter(CandidatModel.email == email, CandidatModel.campagne == campagne)
            .first()
        )
        return _vers_candidat(modele) if modele else None

    def reference_paiement_existe(self, reference: str) -> bool:
        return (
            self._session.query(CandidatureModel.id)
            .filter(CandidatureModel.reference_paiement == reference)
            .first()
            is not None
        )

    def enregistrer_candidat(self, candidat: Candidat) -> None:
        modele = self._session.get(CandidatModel, candidat.id)
        for champ in _CHAMPS_CANDIDAT:
            setattr(modele, champ, getattr(candidat, champ))
        self._valider()

    def enregistrer_candidature(self, candidature: Candidature) -> None:
        modele = self._session.get(CandidatureModel, candidature.id)
        for champ in _CHAMPS_CANDIDATURE:
            setattr(modele, champ, getattr(candidature, champ))
        self._valider()

    def _valider(self) -> None:
        """Valide la transaction ; une violation d'unicité devient une erreur métier."""
        try:
            self._session.commit()
        except IntegrityError as erreur:
            self._session.rollback()
            raise CandidatureDejaExistante() from erreur
