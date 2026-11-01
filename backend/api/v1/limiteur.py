"""Limitation de débit des envois de fichiers — Couche Présentation / API (US-007).

PRD §7 : 10 requêtes par fenêtre de 60 s et par IP sur le téléversement, pour empêcher d'épuiser le stockage.
Le compteur est en mémoire du processus : suffisant pour un seul conteneur, à remplacer par un stockage partagé
(Redis...) si l'API est un jour répliquée.
"""

import time
from collections import defaultdict, deque
from typing import Callable

from fastapi import HTTPException, Request


class LimiteurDebit:
    """Fenêtre glissante : au plus `max_requetes` par `fenetre_secondes` pour une même clé."""

    def __init__(
        self,
        max_requetes: int = 10,
        fenetre_secondes: float = 60.0,
        horloge: Callable[[], float] = time.monotonic,
    ) -> None:
        self._max = max_requetes
        self._fenetre = fenetre_secondes
        self._horloge = horloge
        self._appels: dict[str, deque[float]] = defaultdict(deque)

    def autoriser(self, cle: str) -> bool:
        """Enregistre l'appel et retourne False si la limite est atteinte."""
        maintenant = self._horloge()
        appels = self._appels[cle]
        while appels and maintenant - appels[0] >= self._fenetre:
            appels.popleft()
        if len(appels) >= self._max:
            return False
        appels.append(maintenant)
        return True

    def reinitialiser(self) -> None:
        self._appels.clear()


limiteur_envois = LimiteurDebit()


def _adresse_client(request: Request) -> str:
    # Derrière Nginx, l'adresse réelle du visiteur est dans X-Forwarded-For (premier élément)
    transmis = request.headers.get("x-forwarded-for", "")
    if transmis:
        return transmis.split(",")[0].strip()
    return request.client.host if request.client else "inconnu"


def limiter_envois(request: Request) -> None:
    """Dépendance FastAPI : refuse (429) un client qui dépasse la limite d'envois."""
    if not limiteur_envois.autoriser(_adresse_client(request)):
        raise HTTPException(
            status_code=429,
            detail="Trop d'envois en peu de temps. Patientez une minute puis réessayez.",
            headers={"Retry-After": "60"},
        )
