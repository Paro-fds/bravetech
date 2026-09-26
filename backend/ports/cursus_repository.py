"""Port de persistance pour les cursus académiques — Couche Ports.

Définit le contrat abstrait que tout adaptateur de données (DAL) doit respecter.
"""

from abc import ABC, abstractmethod

from backend.entities.cursus import Cursus


class ICursusRepository(ABC):
    """Interface abstraite définissant les opérations d'accès aux données des cursus."""

    @abstractmethod
    def lister_tous(self) -> list[Cursus]:
        """Retourne l'ensemble des cursus disponibles."""
        pass

    @abstractmethod
    def obtenir_par_id(self, cursus_id: str) -> Cursus | None:
        """Retourne un cursus par son identifiant unique (slug)."""
        pass

    @abstractmethod
    def sauvegarder_tous(self, cursus_liste: list[Cursus]) -> None:
        """Persiste une liste de cursus."""
        pass
