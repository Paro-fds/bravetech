"""Implémentation SQLAlchemy du port IDocumentRepository — Couche DAL.

Aucune logique métier ici : uniquement la traduction entre entité du domaine et ligne en base.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.dal.models import DocumentSoumisModel
from backend.entities.document_soumis import DocumentSoumis
from backend.ports.document_repository import IDocumentRepository

_CHAMPS = (
    "candidat_id", "document_requis_id", "nom_fichier", "cle_stockage", "type_mime", "taille_octets",
    "statut_validation", "motif_rejet", "soumis_le", "valide_par", "date_validation",
)


def _en_utc(valeur: datetime | None) -> datetime | None:
    """SQLite restitue des dates sans fuseau : on les ramène en UTC."""
    if valeur is not None and valeur.tzinfo is None:
        return valeur.replace(tzinfo=timezone.utc)
    return valeur


def _vers_entite(modele: DocumentSoumisModel) -> DocumentSoumis:
    valeurs = {champ: getattr(modele, champ) for champ in _CHAMPS}
    valeurs["soumis_le"] = _en_utc(valeurs["soumis_le"])
    valeurs["date_validation"] = _en_utc(valeurs["date_validation"])
    return DocumentSoumis(id=modele.id, **valeurs)


class SqlDocumentRepository(IDocumentRepository):
    """Adaptateur DAL stockant les documents soumis dans PostgreSQL (SQLite en dev)."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def _requete(self, candidat_id: str):
        return self._session.query(DocumentSoumisModel).filter(DocumentSoumisModel.candidat_id == candidat_id)

    def obtenir(self, candidat_id: str, document_requis_id: str) -> DocumentSoumis | None:
        modele = self._requete(candidat_id).filter(DocumentSoumisModel.document_requis_id == document_requis_id).first()
        return _vers_entite(modele) if modele else None

    def lister(self, candidat_id: str) -> list[DocumentSoumis]:
        return [_vers_entite(m) for m in self._requete(candidat_id).order_by(DocumentSoumisModel.soumis_le).all()]

    def enregistrer(self, document: DocumentSoumis) -> None:
        """Upsert sur (candidat_id, document_requis_id) : jamais deux lignes pour la même pièce."""
        modele = (
            self._requete(document.candidat_id)
            .filter(DocumentSoumisModel.document_requis_id == document.document_requis_id)
            .first()
        )
        if modele is None:
            modele = DocumentSoumisModel(id=document.id)
            self._session.add(modele)
        for champ in _CHAMPS:
            setattr(modele, champ, getattr(document, champ))
        self._session.commit()
