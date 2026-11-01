"""Implémentation SQLAlchemy du port IDocumentRepository — Couche DAL.

Aucune logique métier ici : uniquement la traduction entre entité du domaine et ligne en base.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.dal.models import DecisionDocumentModel, DocumentSoumisModel
from backend.entities.decision_document import DecisionDocument
from backend.entities.document_soumis import STATUT_EN_ATTENTE, DocumentSoumis
from backend.entities.erreurs import DocumentDejaDecide
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

    def obtenir_par_id(self, document_id: str) -> DocumentSoumis | None:
        modele = self._session.get(DocumentSoumisModel, document_id)
        return _vers_entite(modele) if modele else None

    def lister_par_candidats(self, candidat_ids: list[str]) -> dict[str, list[DocumentSoumis]]:
        resultat: dict[str, list[DocumentSoumis]] = {identifiant: [] for identifiant in candidat_ids}
        if not candidat_ids:
            return resultat
        modeles = (
            self._session.query(DocumentSoumisModel)
            .filter(DocumentSoumisModel.candidat_id.in_(candidat_ids))
            .order_by(DocumentSoumisModel.soumis_le)
            .all()
        )
        for modele in modeles:
            resultat[modele.candidat_id].append(_vers_entite(modele))
        return resultat

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

    def enregistrer_decision(self, document: DocumentSoumis, decision: DecisionDocument) -> None:
        # Mise à jour conditionnelle : si un autre agent a décidé entre-temps, aucune ligne n'est touchée
        modifiees = (
            self._session.query(DocumentSoumisModel)
            .filter(DocumentSoumisModel.id == document.id, DocumentSoumisModel.statut_validation == STATUT_EN_ATTENTE)
            .update(
                {
                    "statut_validation": document.statut_validation,
                    "motif_rejet": document.motif_rejet,
                    "valide_par": document.valide_par,
                    "date_validation": document.date_validation,
                },
                synchronize_session=False,
            )
        )
        if modifiees != 1:
            self._session.rollback()
            raise DocumentDejaDecide()
        self._session.add(DecisionDocumentModel(
            id=decision.id,
            document_id=decision.document_id,
            candidat_id=decision.candidat_id,
            document_requis_id=decision.document_requis_id,
            statut=decision.statut,
            motif=decision.motif,
            decide_par=decision.decide_par,
            decide_le=decision.decide_le,
        ))
        self._session.commit()  # document et historique sont écrits ensemble ou pas du tout

    def lister_decisions(self, candidat_id: str) -> list[DecisionDocument]:
        modeles = (
            self._session.query(DecisionDocumentModel)
            .filter(DecisionDocumentModel.candidat_id == candidat_id)
            .order_by(DecisionDocumentModel.decide_le)
            .all()
        )
        return [
            DecisionDocument(
                id=m.id,
                document_id=m.document_id,
                candidat_id=m.candidat_id,
                document_requis_id=m.document_requis_id,
                statut=m.statut,
                motif=m.motif,
                decide_par=m.decide_par,
                decide_le=_en_utc(m.decide_le),
            )
            for m in modeles
        ]
