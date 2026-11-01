"""Cas d'utilisation : valider ou refuser une pièce — Couche BLL (US-013).

Une décision est définitive : seul un document « en attente » peut recevoir une décision. Un document refusé n'est de
nouveau décidable qu'après son remplacement par le candidat (nouveau dépôt, donc nouveau cycle). L'historique de toutes
les décisions est conservé (AGENTS.md, fait critique 5 : `valide_par` et `date_validation` ne sont jamais réécrits).
"""

import uuid
from datetime import datetime, timezone

from backend.entities.candidature import STATUT_SOUMISE
from backend.entities.decision_document import DecisionDocument
from backend.entities.document_soumis import STATUT_EN_ATTENTE, STATUT_REJETE, STATUT_VALIDE, DocumentSoumis
from backend.entities.erreurs import DocumentDejaDecide, DocumentIntrouvable, InformationsInvalides
from backend.entities.utilisateur import Utilisateur
from backend.ports.candidature_repository import ICandidatureRepository
from backend.ports.document_repository import IDocumentRepository

MOTIF_MIN = 5
MOTIF_MAX = 500


class DeciderDocumentUseCase:
    def __init__(self, candidatures: ICandidatureRepository, documents: IDocumentRepository) -> None:
        self._candidatures = candidatures
        self._documents = documents

    def executer(
        self, document_id: str, statut: str, motif: str | None, decideur: Utilisateur
    ) -> tuple[DocumentSoumis, DecisionDocument]:
        if statut not in (STATUT_VALIDE, STATUT_REJETE):
            raise InformationsInvalides({"statut": "La décision doit être « valide » ou « rejete »."})
        motif = (motif or "").strip() or None
        if statut == STATUT_REJETE:
            if motif is None or len(motif) < MOTIF_MIN:
                raise InformationsInvalides({"motif": f"Indiquez le motif du refus ({MOTIF_MIN} caractères minimum) : le candidat le verra."})
            if len(motif) > MOTIF_MAX:
                raise InformationsInvalides({"motif": f"Le motif ne doit pas dépasser {MOTIF_MAX} caractères."})
        else:
            motif = None  # une validation n'a pas de motif

        document = self._documents.obtenir_par_id(document_id)
        candidature = self._candidatures.obtenir_par_candidat(document.candidat_id) if document else None
        # Seules les pièces d'un dossier soumis sont visibles du personnel, donc décidables
        if document is None or candidature is None or candidature.statut != STATUT_SOUMISE:
            raise DocumentIntrouvable()
        if document.statut_validation != STATUT_EN_ATTENTE:
            raise DocumentDejaDecide()

        maintenant = datetime.now(timezone.utc)
        document.statut_validation = statut
        document.motif_rejet = motif
        document.valide_par = decideur.id
        document.date_validation = maintenant
        decision = DecisionDocument(
            id=str(uuid.uuid4()),
            document_id=document.id,
            candidat_id=document.candidat_id,
            document_requis_id=document.document_requis_id,
            statut=statut,
            motif=motif,
            decide_par=decideur.id,
            decide_le=maintenant,
        )
        self._documents.enregistrer_decision(document, decision)
        return document, decision
