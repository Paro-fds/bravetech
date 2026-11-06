"""Calendrier d'admission réglable par l'administration (US-028).

Révision : 0002
Précédente : 0001
Créée le : 2026-11-06
"""

from alembic import op
import sqlalchemy as sa


revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "calendriers_admission",
        sa.Column("numero", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("date_ouverture", sa.Date(), nullable=False),
        sa.Column("date_limite", sa.Date(), nullable=False),
        sa.Column("date_concours", sa.Date(), nullable=True),
        sa.Column("date_resultats", sa.Date(), nullable=True),
        sa.Column("date_rentree", sa.Date(), nullable=True),
        sa.Column("modifie_par", sa.String(length=36), nullable=False),
        sa.Column("modifie_le", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["modifie_par"], ["utilisateurs.id"]),
        sa.PrimaryKeyConstraint("numero"),
        sa.UniqueConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("calendriers_admission")
