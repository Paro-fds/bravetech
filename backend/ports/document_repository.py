"""Port de persistance des documents soumis — Couche Ports.
"""

from abc import ABC, abstractmethod

from backend.entities.decision_document import DecisionDocument
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
    def obtenir_par_id(self, document_id: str) -> DocumentSoumis | None:
        """Retourne un document soumis par son identifiant, ou None."""

    @abstractmethod
    def lister_par_candidats(self, candidat_ids: list[str]) -> dict[str, list[DocumentSoumis]]:
        """Retourne les documents de plusieurs candidats en une requête (clé : identifiant du candidat)."""

    @abstractmethod
    def enregistrer(self, document: DocumentSoumis) -> None:
        """Crée ou remplace (upsert) le document pour le couple (candidat, pièce requise)."""

    @abstractmethod
    def enregistrer_decision(self, document: DocumentSoumis, decision: DecisionDocument) -> None:
        """Enregistre en une seule transaction la décision (historique) et le nouveau statut du document.

        Lève `DocumentDejaDecide` si le document n'est plus en attente au moment de l'écriture (deux agents simultanés).
        """

    @abstractmethod
    def lister_decisions(self, candidat_id: str) -> list[DecisionDocument]:
        """Retourne l'historique des décisions d'un candidat, de la plus ancienne à la plus récente."""
