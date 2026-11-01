"""Entité DocumentSoumis — Couche Domain.

Un DocumentSoumis est le fichier déposé par un candidat pour satisfaire une pièce requise.
Il est unique par couple (candidat, pièce requise) : le remplacement d'un document est un upsert,
jamais une seconde ligne (AGENTS.md, fait critique 4).

Règle absolue (Clean Architecture) :
Aucun import de framework (FastAPI, SQLAlchemy), ni d'aucune couche externe (dal, bll, api).
"""

from dataclasses import dataclass
from datetime import datetime

STATUT_EN_ATTENTE = "en_attente"
STATUT_VALIDE = "valide"
STATUT_REJETE = "rejete"
# Statut d'affichage d'une pièce pour laquelle aucun fichier n'a encore été déposé
STATUT_MANQUANT = "manquant"


@dataclass
class DocumentSoumis:
    """Fichier déposé pour une pièce requise, avec son statut de validation."""
    id: str
    candidat_id: str
    document_requis_id: str
    nom_fichier: str  # nom d'origine nettoyé, affiché au candidat et à l'administrateur
    cle_stockage: str  # clé interne dans le stockage de fichiers, jamais exposée au public
    type_mime: str
    taille_octets: int
    soumis_le: datetime
    statut_validation: str = STATUT_EN_ATTENTE
    motif_rejet: str | None = None
    # Audit des décisions administratives (US-013) : immuables une fois écrits
    valide_par: str | None = None
    date_validation: datetime | None = None
