"""Couche Domain / Entities — Dataclasses et règles métier pures.

Règle absolue : aucune dépendance vers dal, bll, api, ni vers des frameworks externes (FastAPI, SQLAlchemy).
"""

from backend.entities.cursus import Cursus, Matiere
from backend.entities.document_requis import DocumentRequis

__all__ = ["Cursus", "Matiere", "DocumentRequis"]
