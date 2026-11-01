"""Port de persistance des utilisateurs du personnel — Couche Ports (US-011).
"""

from abc import ABC, abstractmethod

from backend.entities.utilisateur import Utilisateur


class IUtilisateurRepository(ABC):
    """Interface abstraite d'accès aux comptes du personnel."""

    @abstractmethod
    def trouver_par_email(self, email: str) -> Utilisateur | None:
        """Retourne l'utilisateur portant cet email (déjà en minuscules), ou None."""

    @abstractmethod
    def obtenir(self, utilisateur_id: str) -> Utilisateur | None:
        """Retourne l'utilisateur par son identifiant, ou None."""

    @abstractmethod
    def creer(self, utilisateur: Utilisateur) -> None:
        """Persiste un nouvel utilisateur."""
