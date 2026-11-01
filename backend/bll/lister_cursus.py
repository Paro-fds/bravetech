"""Cas d'utilisation : Lister les cursus académiques — Couche BLL (Business Logic Layer).

Orchestre la récupération des cursus via l'interface abstraite ICursusRepository.
"""

from backend.entities.cursus import Cursus
from backend.ports.cursus_repository import ICursusRepository


class ListerCursusUseCase:
    """Cas d'utilisation permettant à un candidat ou visiteur de lister les cursus."""

    def __init__(self, repository: ICursusRepository) -> None:
        self._repository = repository

    def executer(self) -> list[Cursus]:
        """Exécute le cas d'utilisation et retourne la liste triée des cursus."""
        cursus_liste = self._repository.lister_tous()
        # Règle métier : le cursus d'admission (MPC) est présenté en premier, puis les branches
        return sorted(cursus_liste, key=lambda c: (0 if c.est_admission else 1, c.nom))
