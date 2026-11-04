"""Environnement Alembic (US-023) : les migrations comparent la base aux modèles de `backend/dal/models.py`.

Une connexion passée par `config.attributes["connection"]` (voir `backend/dal/schema.py`, et les tests) est utilisée
telle quelle ; sinon on se connecte à DATABASE_URL.
"""

from alembic import context

from backend.dal import models  # noqa: F401  (enregistre les tables dans Base.metadata)
from backend.dal.database import DATABASE_URL, Base, engine

cible = Base.metadata


def _executer(connexion) -> None:
    # SQLite ne sait pas modifier une colonne : le mode « batch » recrée la table (développement et tests)
    context.configure(
        connection=connexion,
        target_metadata=cible,
        render_as_batch=connexion.dialect.name == "sqlite",
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    context.configure(url=DATABASE_URL, target_metadata=cible, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
elif (connexion_fournie := context.config.attributes.get("connection")) is not None:
    _executer(connexion_fournie)
else:
    with engine.connect() as connexion:
        _executer(connexion)
