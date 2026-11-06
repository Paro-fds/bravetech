"""Entité SmsSimule — Couche Domain (US-016).

Un SMS que le portail aurait envoyé au candidat. Comme le paiement MonCash / NatCash, l'envoi est **simulé** : aucun
fournisseur SMS n'est branché en V1, le message est seulement enregistré pour être consulté par le personnel.
C'est une trace de notification, jamais un état du dossier (AGENTS.md, fait critique 1).

Règle absolue (Clean Architecture) : aucun import de framework ni de couche externe.
"""

from dataclasses import dataclass
from datetime import datetime

LONGUEUR_MAX_SMS = 160  # un SMS standard (GSM 7 bits) ; au-delà, l'opérateur le découpe et le facture plusieurs fois


@dataclass(frozen=True)
class SmsSimule:
    id: str
    destinataire: str  # +509XXXXXXXX
    texte: str
    reference_dossier: str | None
    envoye_le: datetime  # UTC
