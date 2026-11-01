"""Limitation de débit — Couche Présentation / API (US-007, US-009, US-011).

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

    def _purger(self, cle: str) -> deque[float]:
        maintenant = self._horloge()
        appels = self._appels[cle]
        while appels and maintenant - appels[0] >= self._fenetre:
            appels.popleft()
        return appels

    def est_atteint(self, cle: str) -> bool:
        """Indique si la limite est atteinte, sans enregistrer d'appel."""
        return len(self._purger(cle)) >= self._max

    def enregistrer(self, cle: str) -> None:
        """Compte un appel (par exemple une tentative de connexion échouée)."""
        self._purger(cle).append(self._horloge())

    def autoriser(self, cle: str) -> bool:
        """Enregistre l'appel et retourne False si la limite est atteinte."""
        if self.est_atteint(cle):
            return False
        self.enregistrer(cle)
        return True

    def reinitialiser(self) -> None:
        self._appels.clear()


limiteur_envois = LimiteurDebit()


def adresse_client(request: Request) -> str:
    # Derrière Nginx, l'adresse réelle du visiteur est dans X-Forwarded-For (premier élément)
    transmis = request.headers.get("x-forwarded-for", "")
    if transmis:
        return transmis.split(",")[0].strip()
    return request.client.host if request.client else "inconnu"


# Consultation de dossier (US-009) : les références sont séquentielles, donc devinables ; on freine l'énumération
limiteur_suivi = LimiteurDebit(max_requetes=20)


def limiter_suivi(request: Request) -> None:
    """Dépendance FastAPI : refuse (429) un client qui multiplie les consultations de dossier."""
    if not limiteur_suivi.autoriser(adresse_client(request)):
        raise HTTPException(
            status_code=429,
            detail="Trop de recherches en peu de temps. Patientez une minute puis réessayez.",
            headers={"Retry-After": "60"},
        )


# Remplacement d'une pièce (US-010) : 5 échecs d'identité (référence + email) par minute et par IP, comme la connexion
limiteur_identite = LimiteurDebit(max_requetes=5)


def limiter_envois(request: Request) -> None:
    """Dépendance FastAPI : refuse (429) un client qui dépasse la limite d'envois."""
    if not limiteur_envois.autoriser(adresse_client(request)):
        raise HTTPException(
            status_code=429,
            detail="Trop d'envois en peu de temps. Patientez une minute puis réessayez.",
            headers={"Retry-After": "60"},
        )
