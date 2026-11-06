"""Port d'envoi de SMS — Couche Ports (US-016).

Même règle que l'email : un SMS est une notification, son échec ne doit jamais annuler une candidature ni une décision.
En V1, l'adaptateur enregistre le SMS sans l'envoyer (simulation) ; un vrai fournisseur (Twilio, opérateur haïtien)
s'ajoutera derrière ce port sans toucher au métier.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from backend.entities.sms_simule import SmsSimule


@dataclass(frozen=True)
class MessageSms:
    destinataire: str  # +509XXXXXXXX
    texte: str  # ≤ LONGUEUR_MAX_SMS caractères
    reference_dossier: str | None = None


class ISmsSender(ABC):
    @abstractmethod
    def envoyer(self, message: MessageSms) -> None:
        """Envoie (ou simule) le SMS. Peut lever une exception : l'appelant la traite comme non bloquante."""


class IJournalSms(ABC):
    @abstractmethod
    def lister(self, limite: int) -> list[SmsSimule]:
        """Les SMS simulés, du plus récent au plus ancien."""
