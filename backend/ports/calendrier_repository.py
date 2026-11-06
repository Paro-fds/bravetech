"""Port de persistance du calendrier d'admission — Couche Ports (US-028).
"""

from abc import ABC, abstractmethod

from backend.entities.calendrier_admission import CalendrierAdmission


class ICalendrierRepository(ABC):
    """Versions successives du calendrier d'admission (ajout seul)."""

    @abstractmethod
    def obtenir_en_vigueur(self) -> CalendrierAdmission | None:
        """Retourne la version la plus récente, ou None si aucun calendrier n'a été enregistré."""

    @abstractmethod
    def ajouter(self, calendrier: CalendrierAdmission) -> None:
        """Enregistre une nouvelle version ; les précédentes ne sont jamais modifiées."""
