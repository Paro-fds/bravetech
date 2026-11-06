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
# Tables de cette révision : une base d'avant Alembic ne contient qu'elles. Les tables ajoutées par les migrations
# suivantes (`calendriers_admission`, US-028…) lui manquent forcément : `upgrade` les crée ensuite.
TABLES_INITIALES = frozenset({"candidats", "candidatures", "documents_soumis", "utilisateurs", "decisions_documents"})

journal = logging.getLogger(__name__)


def configuration_alembic() -> Config:
    config = Config()
    config.set_main_option("script_location", str(DOSSIER_MIGRATIONS))
    return config


def _ecart_tolere(ecart) -> bool:
    """Une table en trop (reste d'un ancien schéma), ou une table créée par une migration postérieure à l'initiale."""
    if not isinstance(ecart, tuple):
        return False
    if ecart[0].startswith("remove_"):
        return True
    # Une table postérieure, et ses index (signalés à part par autogenerate : `add_index`), arriveront par `upgrade`
    if ecart[0] == "add_table":
        return ecart[1].name not in TABLES_INITIALES
    if ecart[0] == "add_index":
        return ecart[1].table.name not in TABLES_INITIALES
    return False


def _ecarts_bloquants(connexion: Connection) -> list:
    """Ce qui manque à la base par rapport au schéma de la révision initiale."""
    ecarts = compare_metadata(MigrationContext.configure(connexion), Base.metadata)
    return [e for e in ecarts if not _ecart_tolere(e)]


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
