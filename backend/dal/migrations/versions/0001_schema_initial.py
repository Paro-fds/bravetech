"""Schéma initial : les tables telles que `create_all` les créait avant Alembic (US-023).

Une base déjà créée par `create_all` est marquée à cette révision sans être modifiée (`backend/dal/schema.py`).
Les noms de contraintes sans nom explicite sont laissés au moteur, comme le faisait `create_all`.

Révision : 0001
Précédente : aucune
Créée le : 2026-11-04
"""

from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "candidats",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("nom", sa.String(length=100), nullable=False),
        sa.Column("prenom", sa.String(length=100), nullable=False),
        sa.Column("date_naissance", sa.Date(), nullable=False),
        sa.Column("sexe", sa.String(length=1), nullable=False),
        sa.Column("telephone", sa.String(length=20), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("departement", sa.String(length=50), nullable=False),
        sa.Column("commune", sa.String(length=100), nullable=False),
        sa.Column("campagne", sa.SmallInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", "campagne", name="uq_candidats_email_campagne"),
    )
    op.create_table(
        "utilisateurs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("mot_de_passe_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("est_actif", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_utilisateurs_email", "utilisateurs", ["email"], unique=True)
    op.create_table(
        "candidatures",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("candidat_id", sa.String(length=36), nullable=False),
        sa.Column("deplacement_physique", sa.Boolean(), nullable=True),
        sa.Column("statut_paiement", sa.String(length=50), nullable=False),
        sa.Column("methode_paiement", sa.String(length=20), nullable=True),
        sa.Column("reference_paiement", sa.String(length=30), nullable=True),
        sa.Column("numero_paiement", sa.String(length=20), nullable=True),
        sa.Column("reference_dossier", sa.String(length=20), nullable=True),
        sa.Column("statut", sa.String(length=20), nullable=False),
        sa.Column("soumise_le", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["candidat_id"], ["candidats.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("candidat_id"),
        sa.UniqueConstraint("reference_dossier"),
        sa.UniqueConstraint("reference_paiement"),
    )
    op.create_table(
        "decisions_documents",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("document_id", sa.String(length=36), nullable=False),
        sa.Column("candidat_id", sa.String(length=36), nullable=False),
        sa.Column("document_requis_id", sa.String(length=100), nullable=False),
        sa.Column("statut", sa.String(length=20), nullable=False),
        sa.Column("motif", sa.Text(), nullable=True),
        sa.Column("decide_par", sa.String(length=36), nullable=False),
        sa.Column("decide_le", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["candidat_id"], ["candidats.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["decide_par"], ["utilisateurs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_decisions_documents_candidat_id", "decisions_documents", ["candidat_id"])
    op.create_index("ix_decisions_documents_document_id", "decisions_documents", ["document_id"])
    op.create_table(
        "documents_soumis",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("candidat_id", sa.String(length=36), nullable=False),
        sa.Column("document_requis_id", sa.String(length=100), nullable=False),
        sa.Column("nom_fichier", sa.String(length=255), nullable=False),
        sa.Column("cle_stockage", sa.String(length=500), nullable=False),
        sa.Column("type_mime", sa.String(length=50), nullable=False),
        sa.Column("taille_octets", sa.Integer(), nullable=False),
        sa.Column("statut_validation", sa.String(length=20), nullable=False),
        sa.Column("motif_rejet", sa.Text(), nullable=True),
        sa.Column("soumis_le", sa.DateTime(timezone=True), nullable=False),
        sa.Column("valide_par", sa.String(length=36), nullable=True),
        sa.Column("date_validation", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["candidat_id"], ["candidats.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("candidat_id", "document_requis_id", name="uq_documents_candidat_piece"),
    )


def downgrade() -> None:
    op.drop_table("documents_soumis")
    op.drop_index("ix_decisions_documents_document_id", table_name="decisions_documents")
    op.drop_index("ix_decisions_documents_candidat_id", table_name="decisions_documents")
    op.drop_table("decisions_documents")
    op.drop_table("candidatures")
    op.drop_index("ix_utilisateurs_email", table_name="utilisateurs")
    op.drop_table("utilisateurs")
    op.drop_table("candidats")
