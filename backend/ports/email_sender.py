"""Port d'envoi d'email — Couche Ports.

L'email est une notification, jamais un état : son échec ne doit jamais annuler une candidature (AGENTS.md, fait 2).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class MessageEmail:
    """Un email transactionnel prêt à partir."""
    destinataire: str
    sujet: str
    texte: str
    html: str | None = None


class IEmailSender(ABC):
    """Interface abstraite d'envoi d'emails (console en développement, Resend en production)."""

    @abstractmethod
    def envoyer(self, message: MessageEmail) -> None:
        """Envoie le message. Peut lever une exception : l'appelant décide de la traiter comme non bloquante."""
