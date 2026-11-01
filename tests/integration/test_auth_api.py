"""Tests d'intégration de l'authentification du personnel (US-011) : base SQLite en mémoire.
"""

import uuid

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from backend.api.v1.securite import get_current_admin_complet, limiteur_connexion
from backend.dal.database import get_db
from backend.dal.securite import EmetteurJwt, HacheurBcrypt
from backend.dal.utilisateur_repository_sql import SqlUtilisateurRepository
from backend.entities.utilisateur import ROLE_ADMIN, ROLE_AGENT, Utilisateur

SECRET = "t" * 48
MOT_DE_PASSE = "Mot-de-passe-solide-42"
TOKEN = "/api/v1/auth/token"
MOI = "/api/v1/admin/moi"


@pytest.fixture(autouse=True)
def _secret_jwt(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", SECRET)
    limiteur_connexion.reinitialiser()
    yield
    limiteur_connexion.reinitialiser()


def _creer(session_factory, email, role=ROLE_ADMIN, actif=True) -> Utilisateur:
    utilisateur = Utilisateur(str(uuid.uuid4()), email, HacheurBcrypt().hacher(MOT_DE_PASSE), role, est_actif=actif)
    with session_factory() as db:
        SqlUtilisateurRepository(db).creer(utilisateur)
    return utilisateur


def _connecter(client, email="admin@fds.ht", mot_de_passe=MOT_DE_PASSE):
    return client.post(TOKEN, json={"email": email, "password": mot_de_passe})


def _entete(jeton):
    return {"Authorization": f"Bearer {jeton}"}


def test_connexion_puis_acces_a_une_route_admin(client, session_factory):
    _creer(session_factory, "admin@fds.ht")
    reponse = _connecter(client, "Admin@FDS.ht")
    assert reponse.status_code == 200
    data = reponse.json()
    assert data["token_type"] == "bearer" and data["expires_in"] == 3600
    moi = client.get(MOI, headers=_entete(data["access_token"]))
    assert moi.status_code == 200
    assert moi.json()["email"] == "admin@fds.ht" and moi.json()["role"] == "admin"
    assert "mot_de_passe_hash" not in moi.text


def test_un_agent_accede_aux_routes_admin(client, session_factory):
    _creer(session_factory, "agent@fds.ht", ROLE_AGENT)
    jeton = _connecter(client, "agent@fds.ht").json()["access_token"]
    assert client.get(MOI, headers=_entete(jeton)).status_code == 200


def test_identifiants_incorrects_meme_message(client, session_factory):
    _creer(session_factory, "admin@fds.ht")
    _creer(session_factory, "parti@fds.ht", ROLE_AGENT, actif=False)
    messages = {
        _connecter(client, "admin@fds.ht", "mauvais").json()["detail"],
        _connecter(client, "inconnu@fds.ht").json()["detail"],
        _connecter(client, "parti@fds.ht").json()["detail"],
    }
    assert messages == {"Email ou mot de passe incorrect."}
    assert _connecter(client, "admin@fds.ht", "mauvais").status_code == 401


def test_route_admin_sans_jeton_ou_avec_jeton_invalide(client, session_factory):
    admin = _creer(session_factory, "admin@fds.ht")
    sans = client.get(MOI)
    assert sans.status_code == 401 and sans.headers["www-authenticate"] == "Bearer"
    assert client.get(MOI, headers=_entete("n-importe-quoi")).status_code == 401
    expire = EmetteurJwt(SECRET, duree_minutes=-1).emettre(admin).jeton
    assert client.get(MOI, headers=_entete(expire)).status_code == 401


def test_cinq_echecs_puis_429(client, session_factory):
    _creer(session_factory, "admin@fds.ht")
    codes = [_connecter(client, "admin@fds.ht", "mauvais").status_code for _ in range(5)]
    assert codes == [401] * 5
    bloque = _connecter(client, "admin@fds.ht", "mauvais")
    assert bloque.status_code == 429 and bloque.headers["retry-after"] == "60"
    # Même avec le bon mot de passe, tant que la fenêtre n'est pas écoulée
    assert _connecter(client).status_code == 429


def test_les_connexions_reussies_ne_comptent_pas_comme_echecs(client, session_factory):
    _creer(session_factory, "admin@fds.ht")
    assert [_connecter(client).status_code for _ in range(8)] == [200] * 8


def test_secret_jwt_absent_desactive_la_connexion(client, session_factory, monkeypatch):
    _creer(session_factory, "admin@fds.ht")
    monkeypatch.delenv("JWT_SECRET")
    assert _connecter(client).status_code == 503
    assert client.get(MOI, headers=_entete("x")).status_code == 503


def test_route_reservee_au_role_admin_refuse_un_agent(session_factory):
    mini = FastAPI()

    @mini.get("/reserve")
    def reserve(_=Depends(get_current_admin_complet)):
        return {"ok": True}

    def _db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    mini.dependency_overrides[get_db] = _db
    emetteur = EmetteurJwt(SECRET)
    agent = _creer(session_factory, "agent@fds.ht", ROLE_AGENT)
    admin = _creer(session_factory, "admin@fds.ht")
    http = TestClient(mini)
    assert http.get("/reserve", headers=_entete(emetteur.emettre(agent).jeton)).status_code == 403
    assert http.get("/reserve", headers=_entete(emetteur.emettre(admin).jeton)).status_code == 200


def test_toutes_les_routes_admin_exigent_un_jeton():
    """Garde-fou : toute route sous /admin/ ajoutée plus tard doit refuser l'accès anonyme."""
    from backend.main import app

    chemins = {c: ops for c, ops in app.openapi()["paths"].items() if c.startswith("/api/v1/admin")}
    assert chemins
    http = TestClient(app)
    for chemin, operations in chemins.items():
        for methode in operations:
            url = chemin.replace("{", "x").replace("}", "")
            assert http.request(methode.upper(), url).status_code in (401, 503), (methode, chemin)
