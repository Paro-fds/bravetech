"""Modèles ORM SQLAlchemy — Couche DAL (Data Access Layer).

Représentation relationnelle des tables dynamiques et transactionnelles en base de données.
Note : Les informations de cursus sont des données de référence statiques stockées sous forme de
fichiers JSON dans `cursus/` et ne nécessitent pas de tables SQL (cf. JsonCursusRepository).
Les pièces requises d'admission sont définies par le domaine (`pieces_admission`).

Modèles introduits : `candidats` et `candidatures` (US-005), `documents_soumis` (US-007).
`utilisateurs` suivra avec US-011.
"""

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)

from backend.dal.database import Base


class CandidatModel(Base):
    """Table `candidats` : informations personnelles, unicité (email, campagne) — ADR-008."""
    __tablename__ = "candidats"
    __table_args__ = (UniqueConstraint("email", "campagne", name="uq_candidats_email_campagne"),)

    id = Column(String(36), primary_key=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    date_naissance = Column(Date, nullable=False)
    sexe = Column(String(1), nullable=False)
    telephone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    departement = Column(String(50), nullable=False)
    commune = Column(String(100), nullable=False)
    campagne = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)


class CandidatureModel(Base):
    """Table `candidatures` : dossier d'un candidat (une candidature par candidat)."""
    __tablename__ = "candidatures"

    id = Column(String(36), primary_key=True)
    candidat_id = Column(String(36), ForeignKey("candidats.id", ondelete="CASCADE"), nullable=False, unique=True)
    deplacement_physique = Column(Boolean, nullable=True)  # NULL tant que la question n'est pas répondue
    statut_paiement = Column(String(50), nullable=False, default="en_attente")
    methode_paiement = Column(String(20), nullable=True)  # MONCASH | NATCASH (paiement simulé, US-006)
    reference_paiement = Column(String(30), unique=True, nullable=True)  # PAY-SIM-AAAA-NNNN
    numero_paiement = Column(String(20), nullable=True)
    reference_dossier = Column(String(20), unique=True, nullable=True)
    statut = Column(String(20), nullable=False, default="brouillon")
    created_at = Column(DateTime(timezone=True), nullable=False)


class DocumentSoumisModel(Base):
    """Table `documents_soumis` : une ligne par (candidat, pièce requise) — le remplacement est un upsert."""
    __tablename__ = "documents_soumis"
    __table_args__ = (UniqueConstraint("candidat_id", "document_requis_id", name="uq_documents_candidat_piece"),)

    id = Column(String(36), primary_key=True)
    candidat_id = Column(String(36), ForeignKey("candidats.id", ondelete="CASCADE"), nullable=False)
    document_requis_id = Column(String(100), nullable=False)
    nom_fichier = Column(String(255), nullable=False)
    cle_stockage = Column(String(500), nullable=False)
    type_mime = Column(String(50), nullable=False)
    taille_octets = Column(Integer, nullable=False)
    statut_validation = Column(String(20), nullable=False, default="en_attente")
    motif_rejet = Column(Text, nullable=True)
    soumis_le = Column(DateTime(timezone=True), nullable=False)
    valide_par = Column(String(36), nullable=True)  # deviendra une clé étrangère vers `utilisateurs` (US-011)
    date_validation = Column(DateTime(timezone=True), nullable=True)
