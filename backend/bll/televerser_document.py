"""Cas d'utilisation : téléverser une pièce justificative — Couche BLL (US-007).

Le dépôt est un upsert sur (candidat, pièce requise) : redéposer remplace le fichier précédent,
sans jamais créer de doublon (AGENTS.md, fait critique 4). Un document déjà validé ne se remplace plus.
"""

import uuid
from datetime import datetime, timezone

from backend.bll.validation_fichier import nettoyer_nom_fichier, valider_fichier
from backend.entities.candidature import STATUT_BROUILLON, STATUT_PAIEMENT_SIMULE
from backend.entities.document_requis import DocumentRequis
from backend.entities.document_soumis import STATUT_EN_ATTENTE, STATUT_MANQUANT, STATUT_VALIDE, DocumentSoumis
from backend.entities.erreurs import (
    CandidatureDejaSoumise,
    CandidatureIntrouvable,
    DocumentDejaValide,
    DocumentRequisInconnu,
    EtapePrecedenteIncomplete,
)
from backend.entities.pieces_admission import pieces_admission
from backend.ports.candidature_repository import ICandidatureRepository
from backend.ports.document_repository import IDocumentRepository
from backend.ports.stockage_fichiers import IStockageFichiers


def trouver_piece(document_requis_id: str) -> DocumentRequis:
    """Retourne la pièce requise d'admission, ou lève `DocumentRequisInconnu`."""
    for piece in pieces_admission():
        if piece.id == document_requis_id:
            return piece
    raise DocumentRequisInconnu()


class TeleverserDocumentUseCase:
    """Valide puis stocke un fichier pour une pièce requise d'un brouillon de candidature."""

    def __init__(
        self,
        candidatures: ICandidatureRepository,
        documents: IDocumentRepository,
        stockage: IStockageFichiers,
    ) -> None:
        self._candidatures = candidatures
        self._documents = documents
        self._stockage = stockage

    def executer(
        self, candidature_id: str, document_requis_id: str, nom_fichier: str | None, contenu: bytes
    ) -> DocumentSoumis:
        candidature = self._candidatures.obtenir_candidature(candidature_id)
        if candidature is None:
            raise CandidatureIntrouvable()
        if candidature.statut != STATUT_BROUILLON:
            raise CandidatureDejaSoumise()
        # Le dépôt des pièces vient après le paiement simulé (étape 4 du tunnel)
        if candidature.statut_paiement != STATUT_PAIEMENT_SIMULE:
            raise EtapePrecedenteIncomplete()

        piece = trouver_piece(document_requis_id)
        fichier = valider_fichier(nom_fichier, contenu, piece.format_accepte, piece.taille_max_mo)

        existant = self._documents.obtenir(candidature.candidat_id, piece.id)
        if existant is not None and existant.statut_validation == STATUT_VALIDE:
            raise DocumentDejaValide()

        cle = f"{candidature.id}/{piece.id}-{uuid.uuid4().hex}.{fichier.extension}"
        self._stockage.enregistrer(cle, contenu)

        document = DocumentSoumis(
            # Même identifiant en cas de remplacement : c'est le même document logique
            id=existant.id if existant else str(uuid.uuid4()),
            candidat_id=candidature.candidat_id,
            document_requis_id=piece.id,
            nom_fichier=nettoyer_nom_fichier(nom_fichier),
            cle_stockage=cle,
            type_mime=fichier.type_mime,
            taille_octets=len(contenu),
            soumis_le=datetime.now(timezone.utc),
            statut_validation=STATUT_EN_ATTENTE,
        )
        try:
            self._documents.enregistrer(document)
        except Exception:
            # La base reste la source de vérité : un fichier sans ligne ne doit pas rester orphelin
            self._stockage.supprimer(cle)
            raise

        if existant is not None and existant.cle_stockage != cle:
            self._stockage.supprimer(existant.cle_stockage)  # ancien fichier remplacé
        return document


class PieceDossier:
    """Une pièce requise avec l'état du fichier déposé (ou « manquant »)."""

    def __init__(self, piece: DocumentRequis, document: DocumentSoumis | None) -> None:
        self.piece = piece
        self.document = document

    @property
    def statut(self) -> str:
        return self.document.statut_validation if self.document else STATUT_MANQUANT


class ListerPiecesDossierUseCase:
    """Retourne les 5 pièces requises avec le statut de chaque dépôt."""

    def __init__(self, candidatures: ICandidatureRepository, documents: IDocumentRepository) -> None:
        self._candidatures = candidatures
        self._documents = documents

    def executer(self, candidature_id: str) -> list[PieceDossier]:
        candidature = self._candidatures.obtenir_candidature(candidature_id)
        if candidature is None:
            raise CandidatureIntrouvable()
        deposes = {d.document_requis_id: d for d in self._documents.lister(candidature.candidat_id)}
        return [PieceDossier(piece, deposes.get(piece.id)) for piece in pieces_admission()]
