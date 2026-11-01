"""Implémentation SQLAlchemy du port ICandidatureRepository — Couche DAL.

Aucune logique métier ici : uniquement la traduction entre entités du domaine et lignes en base.
"""

import re
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.dal.models import CandidatModel, CandidatureModel
from backend.entities.candidat import Candidat
from backend.entities.candidature import Candidature
from backend.entities.erreurs import CandidatureDejaExistante, ReferenceDejaAttribuee
from backend.ports.candidature_repository import ICandidatureRepository

_CHAMPS_CANDIDAT = (
    "nom", "prenom", "date_naissance", "sexe", "telephone", "email", "departement", "commune", "campagne",
)
_CHAMPS_CANDIDATURE = (
    "deplacement_physique", "statut_paiement", "reference_dossier", "statut",
    "methode_paiement", "reference_paiement", "numero_paiement", "soumise_le",
)


def _en_utc(valeur: datetime | None) -> datetime | None:
    """SQLite restitue des dates sans fuseau : on les ramène en UTC (AGENTS.md : horodatages toujours en UTC)."""
    if valeur is not None and valeur.tzinfo is None:
        return valeur.replace(tzinfo=timezone.utc)
    return valeur


def _vers_candidat(modele: CandidatModel) -> Candidat:
    return Candidat(
        id=modele.id,
        created_at=_en_utc(modele.created_at),
        **{champ: getattr(modele, champ) for champ in _CHAMPS_CANDIDAT},
    )


def _vers_candidature(modele: CandidatureModel) -> Candidature:
    valeurs = {champ: getattr(modele, champ) for champ in _CHAMPS_CANDIDATURE}
    valeurs["soumise_le"] = _en_utc(valeurs["soumise_le"])
    return Candidature(
        id=modele.id,
        candidat_id=modele.candidat_id,
        created_at=_en_utc(modele.created_at),
        **valeurs,
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

    def trouver_par_reference(self, reference: str) -> tuple[Candidat, Candidature] | None:
        modele = (
            self._session.query(CandidatureModel)
            .filter(CandidatureModel.reference_dossier == reference)
            .first()
        )
        if modele is None:
            return None
        candidat = self._session.get(CandidatModel, modele.candidat_id)
        return _vers_candidat(candidat), _vers_candidature(modele)

    def reference_paiement_existe(self, reference: str) -> bool:
        return (
            self._session.query(CandidatureModel.id)
            .filter(CandidatureModel.reference_paiement == reference)
            .first()
            is not None
        )

    def prochain_numero_reference(self, campagne: int) -> int:
        prefixe = f"CAN-{campagne}-"
        references = (
            self._session.query(CandidatureModel.reference_dossier)
            .filter(CandidatureModel.reference_dossier.like(f"{prefixe}%"))
            .all()
        )
        numeros = [int(m.group(1)) for (r,) in references if (m := re.fullmatch(prefixe + r"(\d+)", r))]
        return max(numeros, default=0) + 1

    def enregistrer_candidat(self, candidat: Candidat) -> None:
        modele = self._session.get(CandidatModel, candidat.id)
        for champ in _CHAMPS_CANDIDAT:
            setattr(modele, champ, getattr(candidat, champ))
        self._valider()

    def enregistrer_candidature(self, candidature: Candidature) -> None:
        modele = self._session.get(CandidatureModel, candidature.id)
        for champ in _CHAMPS_CANDIDATURE:
            setattr(modele, champ, getattr(candidature, champ))
        self._valider(ReferenceDejaAttribuee)

    def _valider(self, erreur_metier: type[Exception] = CandidatureDejaExistante) -> None:
        """Valide la transaction ; une violation d'unicité devient l'erreur métier donnée."""
        try:
            self._session.commit()
        except IntegrityError as erreur:
            self._session.rollback()
            raise erreur_metier() from erreur
