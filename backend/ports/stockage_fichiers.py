"""Port de stockage des fichiers téléversés — Couche Ports.

Le stockage est un effet de bord : PostgreSQL reste la seule source de vérité des dossiers.
"""

from abc import ABC, abstractmethod


class IStockageFichiers(ABC):
    """Interface abstraite de stockage binaire (volume local, Cloudinary...)."""

    @abstractmethod
    def enregistrer(self, cle: str, contenu: bytes) -> None:
        """Enregistre le contenu sous la clé donnée."""

    @abstractmethod
    def lire(self, cle: str) -> bytes | None:
        """Retourne le contenu stocké, ou None si la clé est inconnue."""

    @abstractmethod
    def supprimer(self, cle: str) -> None:
        """Supprime le contenu stocké ; sans effet si la clé est inconnue."""
