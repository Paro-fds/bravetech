"""Mise à jour du schéma de la base par les migrations Alembic (US-023) — Couche DAL.

Remplace `Base.metadata.create_all`, qui crée les tables manquantes mais ne modifie jamais une table existante.
"""

import logging
from pathlib import Path

from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from sqlalchemy import Connection, Engine, inspect

from backend.dal import models  # noqa: F401  (enregistre les tables)
from backend.dal.database import Base

DOSSIER_MIGRATIONS = Path(__file__).resolve().parent / "migrations"

# Schéma tel que `create_all` le produisait avant Alembic (base de la VM créée le 2026-11-04)
REVISION_INITIALE = "0001"

journal = logging.getLogger(__name__)


def configuration_alembic() -> Config:
    config = Config()
    config.set_main_option("script_location", str(DOSSIER_MIGRATIONS))
    return config


def _ecarts_bloquants(connexion: Connection) -> list:
    """Ce qui manque à la base par rapport aux modèles. Une table en trop (reste d'un ancien schéma) est tolérée."""
    ecarts = compare_metadata(MigrationContext.configure(connexion), Base.metadata)
    return [e for e in ecarts if not (isinstance(e, tuple) and e[0].startswith("remove_"))]


def mettre_a_jour_schema(engine: Engine) -> None:
    """Applique les migrations en attente, dans une seule transaction.

    Une base créée par `create_all` (tables présentes, pas de table `alembic_version`) est d'abord marquée
    à la révision initiale, qui reproduit exactement ce schéma : ses données sont gardées telles quelles.
    Si elle est plus ancienne (colonne ou table manquante), l'adoption est refusée plutôt que de mentir sur son état.
    """
    config = configuration_alembic()
    with engine.begin() as connexion:
        config.attributes["connection"] = connexion
        tables = set(inspect(connexion).get_table_names())
        if "alembic_version" not in tables and "candidats" in tables:
            if ecarts := _ecarts_bloquants(connexion):
                raise RuntimeError(
                    f"Base créée sans Alembic mais différente du schéma {REVISION_INITIALE} : adoption refusée. "
                    f"Écarts : {ecarts}"
                )
            journal.info("Base créée sans Alembic : adoptée à la révision %s.", REVISION_INITIALE)
            command.stamp(config, REVISION_INITIALE)
        command.upgrade(config, "head")
