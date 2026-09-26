"""Modèles ORM SQLAlchemy — Couche DAL (Data Access Layer).

Représentation relationnelle des tables en base de données.
"""

from sqlalchemy import Column, String, Integer, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
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

    documents_requis = relationship("DocumentRequisModel", back_populates="cursus", cascade="all, delete-orphan")


class DocumentRequisModel(Base):
    """Table relationnelle 'documents_requis' stockant les pièces exigées par cursus."""

    __tablename__ = "documents_requis"

    id = Column(String(100), primary_key=True, index=True)
    cursus_id = Column(String(50), ForeignKey("cursus.id", ondelete="CASCADE"), nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    description = Column(String(500), nullable=False)
    format_accepte = Column(String(100), default="PDF, JPG, PNG", nullable=False)
    taille_max_mo = Column(Integer, default=5, nullable=False)
    est_obligatoire = Column(Boolean, default=True, nullable=False)

    cursus = relationship("CursusModel", back_populates="documents_requis")
