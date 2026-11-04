"""Applique les migrations de la base (US-023).

Lancé par le conteneur backend avant l'API (voir `backend/Dockerfile`). En développement :
    python -m backend.scripts.migrer

Sans migration en attente, ne fait rien. Une base créée avant Alembic est adoptée sans perte.
"""

import logging

from backend.dal.database import engine
from backend.dal.schema import mettre_a_jour_schema


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s [%(name)s] %(message)s")
    mettre_a_jour_schema(engine)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
