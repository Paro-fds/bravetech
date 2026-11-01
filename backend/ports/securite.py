"""Ports de sécurité — Couche Ports (US-011) : empreinte de mot de passe et jeton de session.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from backend.entities.utilisateur import Utilisateur


class IHacheurMotDePasse(ABC):
    @abstractmethod
    def hacher(self, mot_de_passe: str) -> str:
        """Retourne l'empreinte salée du mot de passe."""

    @abstractmethod
    def verifier(self, mot_de_passe: str, empreinte: str) -> bool:
        """Indique si le mot de passe correspond à l'empreinte (False, jamais d'exception, si l'entrée est inexploitable)."""


@dataclass
class JetonEmis:
    jeton: str
    expire_dans_secondes: int


@dataclass
class RevendicationsJeton:
    """Contenu vérifié d'un jeton : qui, avec quel rôle."""
    utilisateur_id: str
    role: str


class IEmetteurJeton(ABC):
    @abstractmethod
    def emettre(self, utilisateur: Utilisateur) -> JetonEmis:
        """Signe un jeton de session pour l'utilisateur."""

    @abstractmethod
    def decoder(self, jeton: str) -> RevendicationsJeton:
        """Vérifie signature et expiration. Lève `JetonInvalide` sinon."""
