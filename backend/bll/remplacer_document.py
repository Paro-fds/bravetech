"""Cas d'utilisation : le candidat remplace une pièce refusée — Couche BLL (US-010).

Le candidat n'a pas de compte : il s'identifie par la référence de son dossier ET l'email de sa candidature. La référence
seule ne suffit pas, car elle est séquentielle donc devinable (voir US-009). Une référence inconnue et un email incorrect
donnent la même erreur, pour ne pas révéler quels dossiers existent.

Seule une pièce REFUSÉE se remplace : une pièce en attente ou validée reste intacte. Le remplacement est un upsert sur
(candidat, pièce) : même document logique, jamais de doublon (AGENTS.md, fait 4). Le statut repasse à « en attente » ; la
décision précédente reste dans l'historique (US-013).
"""

import uuid
from datetime import datetime, timezone

from backend.bll.obtenir_statut_candidature import normaliser_reference
from backend.bll.televerser_document import trouver_piece
from backend.bll.validation_fichier import nettoyer_nom_fichier, valider_fichier
from backend.entities.candidat import Candidat
from backend.entities.candidature import STATUT_SOUMISE, Candidature
from backend.entities.document_soumis import STATUT_EN_ATTENTE, STATUT_REJETE, DocumentSoumis
from backend.entities.erreurs import IdentiteNonVerifiee, RemplacementNonAutorise
from backend.ports.candidature_repository import ICandidatureRepository
from backend.ports.document_repository import IDocumentRepository
from backend.ports.stockage_fichiers import IStockageFichiers


class RemplacerDocumentUseCase:
    def __init__(
        self, candidatures: ICandidatureRepository, documents: IDocumentRepository, stockage: IStockageFichiers
    ) -> None:
        self._candidatures = candidatures
        self._documents = documents
        self._stockage = stockage

    def executer(
        self, reference: str, email: str, document_requis_id: str, nom_fichier: str | None, contenu: bytes
    ) -> tuple[Candidat, Candidature, DocumentSoumis]:
        candidat, candidature = self._identifier(reference, email)

        piece = trouver_piece(document_requis_id)
        existant = self._documents.obtenir(candidat.id, piece.id)
        if existant is None or existant.statut_validation != STATUT_REJETE:
            raise RemplacementNonAutorise()

        fichier = valider_fichier(nom_fichier, contenu, piece.format_accepte, piece.taille_max_mo)

        cle = f"{candidature.id}/{piece.id}-{uuid.uuid4().hex}.{fichier.extension}"
        self._stockage.enregistrer(cle, contenu)
        document = DocumentSoumis(
            id=existant.id,  # même document logique : jamais de doublon
            candidat_id=candidat.id,
            document_requis_id=piece.id,
            nom_fichier=nettoyer_nom_fichier(nom_fichier),
            cle_stockage=cle,
            type_mime=fichier.type_mime,
            taille_octets=len(contenu),
            soumis_le=datetime.now(timezone.utc),
            statut_validation=STATUT_EN_ATTENTE,  # motif et décision précédents effacés ; l'historique les garde
        )
        try:
            self._documents.enregistrer(document)
        except Exception:
            self._stockage.supprimer(cle)  # la base reste la source de vérité : pas de fichier orphelin
            raise
        self._stockage.supprimer(existant.cle_stockage)  # ancien fichier remplacé
        return candidat, candidature, document

    def _identifier(self, reference: str, email: str) -> tuple[Candidat, Candidature]:
        normalisee = normaliser_reference(reference)
        trouve = self._candidatures.trouver_par_reference(normalisee) if normalisee else None
        if trouve is None:
            raise IdentiteNonVerifiee()
        candidat, candidature = trouve
        if candidature.statut != STATUT_SOUMISE or candidat.email != (email or "").strip().lower():
            raise IdentiteNonVerifiee()
        return candidat, candidature
