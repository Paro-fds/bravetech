"""Entité Utilisateur — Couche Domain (US-011).

Un utilisateur est un membre du personnel de la Faculté (jamais un candidat, qui n'a pas de compte).
Deux rôles : `admin` (accès complet) et `agent` (consultation et décisions sur les pièces).

Règle absolue (Clean Architecture) : aucun import de framework ni de couche externe.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone

ROLE_ADMIN = "admin"
ROLE_AGENT = "agent"
ROLES = (ROLE_ADMIN, ROLE_AGENT)

LONGUEUR_MIN_MOT_DE_PASSE = 12

# Durée de vie d'une session : 60 minutes, sans renouvellement automatique (epic-003, Q1)
DUREE_SESSION_MINUTES = 60


@dataclass
class Utilisateur:
    """Compte du personnel. Le mot de passe n'est jamais conservé, seulement son empreinte."""
    id: str
    email: str  # en minuscules
    mot_de_passe_hash: str
    role: str
    est_actif: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
