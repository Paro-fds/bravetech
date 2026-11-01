"""Entité Candidature — Couche Domain.

Une Candidature est le dossier d'un Candidat. Elle naît en brouillon (US-005), puis reçoit le
paiement simulé (US-006), les pièces (US-007) et sa référence `CAN-YYYY-NNNN` à la soumission (US-008).

Règle absolue (Clean Architecture) :
Aucun import de framework (FastAPI, SQLAlchemy), ni d'aucune couche externe (dal, bll, api).
"""

from dataclasses import dataclass
from datetime import datetime

STATUT_BROUILLON = "brouillon"
STATUT_SOUMISE = "soumise"


@dataclass
class Candidature:
    """Dossier de candidature d'un Candidat (admission unique au MPC)."""
    id: str
    candidat_id: str
    created_at: datetime
    # Réponse obligatoire avant de passer à l'étape suivante : None tant qu'elle n'est pas donnée
    deplacement_physique: bool | None = None
    statut_paiement: str = "en_attente"
    reference_dossier: str | None = None
    statut: str = STATUT_BROUILLON
