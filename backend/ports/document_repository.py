"""Port de persistance des documents soumis — Couche Ports.
"""

from abc import ABC, abstractmethod

from backend.entities.document_soumis import DocumentSoumis


class IDocumentRepository(ABC):
    """Interface abstraite d'accès aux documents soumis par les candidats."""

    @abstractmethod
    def obtenir(self, candidat_id: str, document_requis_id: str) -> DocumentSoumis | None:
        """Retourne le document d'un candidat pour une pièce requise, ou None."""

    @abstractmethod
    def lister(self, candidat_id: str) -> list[DocumentSoumis]:
        """Retourne tous les documents soumis d'un candidat."""

    @abstractmethod
    def enregistrer(self, document: DocumentSoumis) -> None:
        """Crée ou remplace (upsert) le document pour le couple (candidat, pièce requise)."""
