"""Modèles ORM SQLAlchemy — Couche DAL (Data Access Layer).

Représentation relationnelle des tables dynamiques et transactionnelles en base de données.
Note : Les informations de cursus sont des données de référence statiques stockées sous forme de
fichiers JSON dans `cursus/` et ne nécessitent pas de tables SQL (cf. JsonCursusRepository).
Les pièces requises d'admission sont définies par le domaine (`pieces_admission`).

Modèles introduits : `candidats` et `candidatures` (US-005), `documents_soumis` (US-007) ; `candidatures.soumise_le` (US-008).
`utilisateurs` (US-011). `calendriers_admission` (US-028).
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
    reference_dossier = Column(String(20), unique=True, nullable=True)  # CAN-AAAA-NNNN, attribuée à la soumission
    statut = Column(String(20), nullable=False, default="brouillon")
    soumise_le = Column(DateTime(timezone=True), nullable=True)
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


class UtilisateurModel(Base):
    """Table `utilisateurs` : comptes du personnel (admin, agent). Email unique, mot de passe haché (bcrypt)."""
    __tablename__ = "utilisateurs"

    id = Column(String(36), primary_key=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    mot_de_passe_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    est_actif = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False)


class DecisionDocumentModel(Base):
    """Table `decisions_documents` : historique des décisions du personnel, en ajout seul (jamais modifié ni supprimé).

    Le document porte l'état courant ; cette table garde la trace de chaque décision, même après un remplacement.
    """
    __tablename__ = "decisions_documents"

    id = Column(String(36), primary_key=True)
    document_id = Column(String(36), nullable=False, index=True)
    candidat_id = Column(String(36), ForeignKey("candidats.id", ondelete="CASCADE"), nullable=False, index=True)
    document_requis_id = Column(String(100), nullable=False)
    statut = Column(String(20), nullable=False)  # valide | rejete
    motif = Column(Text, nullable=True)
    decide_par = Column(String(36), ForeignKey("utilisateurs.id"), nullable=False)
    decide_le = Column(DateTime(timezone=True), nullable=False)


class CalendrierAdmissionModel(Base):
    """Table `calendriers_admission` (US-028) : versions successives du calendrier, en ajout seul.

    La version de plus grand `numero` est en vigueur ; les précédentes gardent qui a changé quelles dates, et quand.
    """
    __tablename__ = "calendriers_admission"

    numero = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(36), nullable=False, unique=True)
    date_ouverture = Column(Date, nullable=False)
    date_limite = Column(Date, nullable=False)
    date_concours = Column(Date, nullable=True)
    date_resultats = Column(Date, nullable=True)
    date_rentree = Column(Date, nullable=True)
    modifie_par = Column(String(36), ForeignKey("utilisateurs.id"), nullable=False)
    modifie_le = Column(DateTime(timezone=True), nullable=False)


class SmsSimuleModel(Base):
    """Table `sms_simules` (US-016) : SMS que le portail aurait envoyés (simulation, aucun fournisseur branché)."""
    __tablename__ = "sms_simules"

    id = Column(String(36), primary_key=True)
    destinataire = Column(String(20), nullable=False)
    texte = Column(Text, nullable=False)
    reference_dossier = Column(String(20), nullable=True, index=True)
    envoye_le = Column(DateTime(timezone=True), nullable=False)
