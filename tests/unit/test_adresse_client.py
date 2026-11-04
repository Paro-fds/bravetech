"""Adresse du visiteur derrière les proxys (US-024) : lue depuis la droite de X-Forwarded-For."""

import pytest
from starlette.requests import Request

from backend.api.v1.limiteur import adresse_client

# Adresses fictives : plages réservées à la documentation (RFC 5737) et adresses privées quelconques
APACHE_UEH = "10.0.0.2"
NGINX = "172.18.0.3"


def _requete(transmis: str | None = None, connexion: str = NGINX) -> Request:
    entetes = [(b"x-forwarded-for", transmis.encode())] if transmis is not None else []
    return Request({"type": "http", "headers": entetes, "client": (connexion, 50000)})


@pytest.fixture
def production(monkeypatch):
    """Chaîne de la VM : visiteur → Apache UEH → Nginx du conteneur → FastAPI."""
    monkeypatch.setenv("TRUSTED_PROXY_COUNT", "2")


def test_derriere_apache_et_nginx_l_adresse_du_visiteur_est_retenue(production):
    # Apache ajoute le visiteur, Nginx ajoute Apache
    assert adresse_client(_requete(f"203.0.113.10, {APACHE_UEH}")) == "203.0.113.10"


def test_un_en_tete_invente_par_le_visiteur_ne_change_rien(production):
    assert adresse_client(_requete(f"198.51.100.1, 203.0.113.10, {APACHE_UEH}")) == "203.0.113.10"
    assert adresse_client(_requete(f"198.51.100.2, 198.51.100.3, 203.0.113.10, {APACHE_UEH}")) == "203.0.113.10"


def test_deux_visiteurs_ont_deux_adresses_distinctes(production):
    assert adresse_client(_requete(f"203.0.113.10, {APACHE_UEH}")) != adresse_client(_requete(f"203.0.113.20, {APACHE_UEH}"))


def test_sans_apache_seul_le_proxy_nginx_compte(monkeypatch):
    monkeypatch.delenv("TRUSTED_PROXY_COUNT", raising=False)  # valeur par défaut : 1 (Nginx du conteneur)
    assert adresse_client(_requete("10.0.0.50")) == "10.0.0.50"
    assert adresse_client(_requete("198.51.100.1, 10.0.0.50")) == "10.0.0.50"


def test_moins_d_entrees_que_de_proxys_prend_la_plus_a_gauche(production):
    # Accès direct au port de la VM, sans passer par l'Apache : seule l'entrée ajoutée par Nginx existe
    assert adresse_client(_requete("10.0.0.50")) == "10.0.0.50"


def test_sans_proxy_l_adresse_de_la_connexion_est_utilisee(monkeypatch):
    monkeypatch.setenv("TRUSTED_PROXY_COUNT", "0")
    assert adresse_client(_requete("198.51.100.1", connexion="127.0.0.1")) == "127.0.0.1"


def test_sans_en_tete_l_adresse_de_la_connexion_est_utilisee(production):
    assert adresse_client(_requete(connexion="127.0.0.1")) == "127.0.0.1"


@pytest.mark.parametrize("valeur", ["abc", "-3", ""])
def test_une_valeur_invalide_ne_fait_pas_planter(monkeypatch, valeur):
    monkeypatch.setenv("TRUSTED_PROXY_COUNT", valeur)
    assert adresse_client(_requete("198.51.100.1, 10.0.0.9")) in {"10.0.0.9", NGINX}
