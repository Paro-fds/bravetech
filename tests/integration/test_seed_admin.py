"""Création du premier compte administrateur (US-011) : script `backend.scripts.seed_admin`."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.dal.utilisateur_repository_sql import SqlUtilisateurRepository
from backend.scripts import seed_admin

MOT_DE_PASSE = "mot-de-passe-solide"


@pytest.fixture
def base(tmp_path, monkeypatch):
    """Base SQLite temporaire, migrée par le script lui-même, à la place de la base réelle."""
    moteur = create_engine(f"sqlite:///{tmp_path / 'seed.db'}")
    sessions = sessionmaker(bind=moteur, autoflush=False)
    monkeypatch.setattr(seed_admin, "engine", moteur)
    monkeypatch.setattr(seed_admin, "SessionLocal", sessions)
    yield sessions
    moteur.dispose()


def _admin(sessions, email: str):
    with sessions() as session:
        return SqlUtilisateurRepository(session).trouver_par_email(email)


def test_cree_le_compte_puis_ne_fait_rien_la_seconde_fois(base, monkeypatch, capsys):
    monkeypatch.setenv("ADMIN_SEED_EMAIL", "  Admin@FDS.ueh.edu.ht ")
    monkeypatch.setenv("ADMIN_SEED_PASSWORD", MOT_DE_PASSE)

    assert seed_admin.main() == 0
    assert "créé" in capsys.readouterr().out
    admin = _admin(base, "admin@fds.ueh.edu.ht")  # email normalisé
    assert admin is not None and admin.role == "admin"
    assert admin.mot_de_passe_hash != MOT_DE_PASSE  # jamais stocké en clair

    assert seed_admin.main() == 0
    assert "existe déjà" in capsys.readouterr().out


def test_sans_variables_le_script_refuse(base, monkeypatch, capsys):
    monkeypatch.delenv("ADMIN_SEED_EMAIL", raising=False)
    monkeypatch.delenv("ADMIN_SEED_PASSWORD", raising=False)
    assert seed_admin.main() == 1
    assert "doivent être définis" in capsys.readouterr().err


@pytest.mark.parametrize("email, mot_de_passe, message", [
    ("pas-une-adresse", MOT_DE_PASSE, "adresse email"),
    ("admin@fds.ueh.edu.ht", "court", "12 caractères"),
])
def test_valeurs_inacceptables_refusees_sans_rien_creer(base, monkeypatch, capsys, email, mot_de_passe, message):
    monkeypatch.setenv("ADMIN_SEED_EMAIL", email)
    monkeypatch.setenv("ADMIN_SEED_PASSWORD", mot_de_passe)
    assert seed_admin.main() == 1
    assert message in capsys.readouterr().err
    assert _admin(base, "admin@fds.ueh.edu.ht") is None
