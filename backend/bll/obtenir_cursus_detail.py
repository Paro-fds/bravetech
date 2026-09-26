"""Cas d'utilisation : Obtenir la fiche détaillée d'un cursus — Couche BLL.
"""

from backend.entities.cursus import Cursus
from backend.ports.cursus_repository import ICursusRepository


class ObtenirCursusDetailUseCase:
    """Cas d'utilisation permettant d'accéder au détail complet d'un cursus."""

    def __init__(self, repository: ICursusRepository) -> None:
        self._repository = repository

    def executer(self, cursus_id: str) -> Cursus | None:
        """Retourne le cursus complet avec ses cours et ses pièces requises, ou None si introuvable."""
        return self._repository.obtenir_par_id(cursus_id)
