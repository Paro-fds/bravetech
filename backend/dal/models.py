"""Modèles ORM SQLAlchemy — Couche DAL (Data Access Layer).

Représentation relationnelle des tables en base de données.
"""

from sqlalchemy import Column, String, Integer, Boolean, JSON
from backend.dal.database import Base


class CursusModel(Base):
    """Table relationnelle 'cursus' stockant les filières et programmes de la FDS."""

    __tablename__ = "cursus"

    id = Column(String(50), primary_key=True, index=True)  # slug: mpc, genie-civil...
    nom = Column(String(255), nullable=False)
    duree_annees = Column(Integer, nullable=False)
    description_courte = Column(String(500), nullable=False)
    description_longue = Column(String(2000), nullable=True)
    date_ouverture_inscription = Column(String(50), nullable=False)
    date_fermeture_inscription = Column(String(50), nullable=False)
    est_ouvert = Column(Boolean, default=True, nullable=False)
    niveaux = Column(JSON, nullable=True)  # Structure des semestres/cours
