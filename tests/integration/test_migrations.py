"""Migrations Alembic (US-023) : schéma identique aux modèles, adoption sans perte d'une base créée par `create_all`."""

from datetime import datetime, timezone

import pytest
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text

from backend.dal import models  # noqa: F401  (enregistre les tables)
from backend.dal.database import Base, normaliser_url
from backend.dal.schema import REVISION_INITIALE, TABLES_INITIALES, configuration_alembic, mettre_a_jour_schema


@pytest.fixture
def engine(tmp_path):
    moteur = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    yield moteur
    moteur.dispose()


def _revision_courante(engine) -> str | None:
    with engine.connect() as connexion:
        return MigrationContext.configure(connexion).get_current_revision()


def _base_d_avant_alembic(engine) -> None:
    """Ce que `create_all` produisait avant Alembic : les seules tables de la révision initiale."""
    Base.metadata.create_all(engine, tables=[t for t in Base.metadata.sorted_tables if t.name in TABLES_INITIALES])


def _tete() -> str:
    return ScriptDirectory.from_config(configuration_alembic()).get_current_head()


def test_les_migrations_reproduisent_exactement_les_modeles(engine):
    """Un modèle modifié sans migration fait échouer ce test : `alembic revision --autogenerate` à lancer."""
    mettre_a_jour_schema(engine)
    with engine.connect() as connexion:
        ecarts = compare_metadata(MigrationContext.configure(connexion, opts={"compare_type": True}), Base.metadata)
    assert ecarts == []
    assert _revision_courante(engine) == _tete()


def test_une_base_creee_par_create_all_est_adoptee_sans_perte(engine):
    _base_d_avant_alembic(engine)
    with engine.begin() as connexion:
        connexion.execute(text(
            "INSERT INTO candidats (id, nom, prenom, date_naissance, sexe, telephone, email, departement, commune,"
            " campagne, created_at) VALUES ('c1', 'Pierre', 'Anne', '2007-05-01', 'F', '+50937000000',"
            " 'anne@exemple.ht', 'Ouest', 'Delmas', 2026, :maintenant)"
        ), {"maintenant": datetime.now(timezone.utc)})

    mettre_a_jour_schema(engine)

    assert _revision_courante(engine) == _tete()
    with engine.connect() as connexion:
        assert connexion.execute(text("SELECT nom FROM candidats WHERE id = 'c1'")).scalar_one() == "Pierre"
    # Les tables des migrations suivantes sont créées après l'adoption (US-028)
    assert "calendriers_admission" in inspect(engine).get_table_names()


def test_une_table_en_trop_n_empeche_pas_l_adoption(engine):
    """Les anciennes bases de développement gardent des tables d'avant ADR-008 (`cursus`), que `create_all` ne supprimait pas."""
    _base_d_avant_alembic(engine)
    with engine.begin() as connexion:
        connexion.execute(text("CREATE TABLE cursus (id VARCHAR(50) PRIMARY KEY)"))

    mettre_a_jour_schema(engine)

    assert _revision_courante(engine) == _tete()


def test_une_base_plus_ancienne_que_le_schema_initial_est_refusee(engine):
    _base_d_avant_alembic(engine)
    with engine.begin() as connexion:
        connexion.execute(text("ALTER TABLE candidatures DROP COLUMN soumise_le"))

    with pytest.raises(RuntimeError, match="adoption refusée"):
        mettre_a_jour_schema(engine)
    assert _revision_courante(engine) is None


def test_les_tables_initiales_sont_celles_de_la_revision_0001(tmp_path):
    """`TABLES_INITIALES` doit rester la liste exacte des tables créées par 0001, sinon l'adoption se trompe."""
    from alembic import command

    moteur = create_engine(f"sqlite:///{tmp_path / 'initiale.db'}")
    config = configuration_alembic()
    with moteur.begin() as connexion:
        config.attributes["connection"] = connexion
        command.upgrade(config, REVISION_INITIALE)
    tables = set(inspect(moteur).get_table_names()) - {"alembic_version"}
    moteur.dispose()
    assert tables == TABLES_INITIALES


def test_relancer_les_migrations_ne_change_rien(engine):
    mettre_a_jour_schema(engine)
    mettre_a_jour_schema(engine)
    assert _revision_courante(engine) == _tete()
    assert "candidats" in inspect(engine).get_table_names()


def test_la_revision_initiale_existe():
    assert ScriptDirectory.from_config(configuration_alembic()).get_revision(REVISION_INITIALE) is not None


@pytest.mark.parametrize("url, attendue", [
    ("postgresql://u:p@db:5432/fds", "postgresql+psycopg2://u:p@db:5432/fds"),
    ("postgres://u:p@db:5432/fds", "postgresql+psycopg2://u:p@db:5432/fds"),
    ("postgresql+psycopg2://u:p@db:5432/fds", "postgresql+psycopg2://u:p@db:5432/fds"),
    ("sqlite:///bravetech.db", "sqlite:///bravetech.db"),
])
def test_le_pilote_postgresql_est_toujours_psycopg2(url, attendue):
    assert normaliser_url(url) == attendue
