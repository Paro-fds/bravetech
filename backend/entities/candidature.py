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

# Paiement simulé (V1) : aucun argent réel n'est prélevé, le paiement réel est délégué à FDS Pay
STATUT_PAIEMENT_EN_ATTENTE = "en_attente"
STATUT_PAIEMENT_SIMULE = "SIMULE_PAYE"
# Issues simulées d'une tentative qui n'aboutit pas : le brouillon reste payable, le candidat peut relancer
STATUT_PAIEMENT_REFUSE = "REFUSE"  # refusé par l'opérateur (solde insuffisant)
STATUT_PAIEMENT_ECHOUE = "ECHOUE"  # échec technique (l'opérateur ne répond pas)
METHODE_MONCASH = "MONCASH"
METHODE_NATCASH = "NATCASH"
METHODES_PAIEMENT = (METHODE_MONCASH, METHODE_NATCASH)
FRAIS_DOSSIER_HTG = 500


@dataclass
class Candidature:
    """Dossier de candidature d'un Candidat (admission unique au MPC)."""
    id: str
    candidat_id: str
    created_at: datetime
    # Réponse obligatoire avant de passer à l'étape suivante : None tant qu'elle n'est pas donnée
    deplacement_physique: bool | None = None
    statut_paiement: str = STATUT_PAIEMENT_EN_ATTENTE
    reference_dossier: str | None = None
    statut: str = STATUT_BROUILLON
    methode_paiement: str | None = None
    reference_paiement: str | None = None  # PAY-SIM-AAAA-NNNN
    numero_paiement: str | None = None  # numéro mobile fourni pour la simulation, format +509XXXXXXXX
    soumise_le: datetime | None = None  # horodatage UTC de la soumission définitive (US-008)
