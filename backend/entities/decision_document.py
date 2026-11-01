"""Entité DecisionDocument — Couche Domain (US-013).

Chaque décision du personnel sur une pièce (validation ou refus) est conservée telle quelle : qui, quand, pourquoi.
L'historique est en ajout seul. Il ne se modifie ni ne se supprime, même quand le candidat remplace ensuite la pièce
(AGENTS.md, fait critique 5).

Règle absolue (Clean Architecture) : aucun import de framework ni de couche externe.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DecisionDocument:
    id: str
    document_id: str
    candidat_id: str
    document_requis_id: str
    statut: str  # valide | rejete
    motif: str | None  # obligatoire pour un refus, visible par le candidat
    decide_par: str  # identifiant de l'utilisateur du personnel
    decide_le: datetime  # UTC
