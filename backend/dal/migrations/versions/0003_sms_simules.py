"""SMS simulés (US-016).

Révision : 0003
Précédente : 0002
Créée le : 2026-11-06
"""

from alembic import op
import sqlalchemy as sa


revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sms_simules",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("destinataire", sa.String(length=20), nullable=False),
        sa.Column("texte", sa.Text(), nullable=False),
        sa.Column("reference_dossier", sa.String(length=20), nullable=True),
        sa.Column("envoye_le", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sms_simules_reference_dossier", "sms_simules", ["reference_dossier"])


def downgrade() -> None:
    op.drop_index("ix_sms_simules_reference_dossier", table_name="sms_simules")
    op.drop_table("sms_simules")
