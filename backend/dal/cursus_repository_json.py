"""Implémentation JSON (fichiers locaux) du port ICursusRepository — Couche DAL.

Lit directement les données officielles depuis les fichiers JSON du dossier `cursus/`.
Aucune table de base de données n'est requise pour les cursus.
"""

from typing import Optional
from backend.entities.cursus import Cursus
from backend.ports.cursus_repository import ICursusRepository
from backend.dal.cursus_loader import charger_cursus_depuis_disque


class JsonCursusRepository(ICursusRepository):
    """Adaptateur DAL fournissant l'accès aux données officielles de cursus via les fichiers JSON."""

    def __init__(self) -> None:
        self._cache: Optional[dict[str, Cursus]] = None

    def _charger_si_necessaire(self) -> dict[str, Cursus]:
        if self._cache is None:
            liste = charger_cursus_depuis_disque()
            self._cache = {c.id: c for c in liste}
        return self._cache

    def lister_tous(self) -> list[Cursus]:
        """Retourne l'ensemble des cursus chargés depuis les fichiers JSON."""
        cache = self._charger_si_necessaire()
        return list(cache.values())

    def obtenir_par_id(self, cursus_id: str) -> Optional[Cursus]:
        """Retourne un cursus par son identifiant unique (slug) depuis les fichiers JSON."""
        cache = self._charger_si_necessaire()
        return cache.get(cursus_id)

    def sauvegarder_tous(self, cursus_liste: list[Cursus]) -> None:
        """Met à jour le cache mémoire (les fichiers sources JSON restent la référence)."""
        if self._cache is None:
            self._cache = {}
        for c in cursus_liste:
            self._cache[c.id] = c
