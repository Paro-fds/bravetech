"""Gestion des comptes du personnel par l'administrateur : création, rôle, activation/désactivation, mot de passe."""

import uuid

import pytest

from backend.dal.securite import EmetteurJwt, HacheurBcrypt
from backend.dal.utilisateur_repository_sql import SqlUtilisateurRepository
from backend.entities.utilisateur import ROLE_ADMIN, ROLE_AGENT, Utilisateur
from tests.integration.test_auth_api import MOI, MOT_DE_PASSE, SECRET, _connecter, _entete

URL = "/api/v1/admin/utilisateurs"


@pytest.fixture(autouse=True)
def _secret_jwt(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", SECRET)


def _creer(session_factory, email, role=ROLE_ADMIN, actif=True) -> Utilisateur:
    utilisateur = Utilisateur(str(uuid.uuid4()), email, HacheurBcrypt().hacher(MOT_DE_PASSE), role, est_actif=actif)
    with session_factory() as db:
        SqlUtilisateurRepository(db).creer(utilisateur)
    return utilisateur


def _jeton(utilisateur: Utilisateur) -> dict[str, str]:
    return _entete(EmetteurJwt(SECRET).emettre(utilisateur).jeton)


def test_l_admin_cree_un_agent_qui_peut_se_connecter(client, session_factory):
    admin = _creer(session_factory, "admin@fds.ht", ROLE_ADMIN)
    reponse = client.post(
        URL,
        json={"email": "  Agent.Un@FDS.ht ", "mot_de_passe": "Provisoire-2026!", "role": "agent"},
        headers=_jeton(admin),
    )
    assert reponse.status_code == 201
    cree = reponse.json()
    assert cree["email"] == "agent.un@fds.ht"
    assert cree["role"] == "agent" and cree["est_actif"] is True
    assert "mot_de_passe" not in cree and "mot_de_passe_hash" not in reponse.text

    # Le nouvel agent se connecte immédiatement avec son mot de passe provisoire
    connexion = _connecter(client, "agent.un@fds.ht", "Provisoire-2026!")
    assert connexion.status_code == 200

    # La liste des comptes contient l'admin et le nouvel agent
    liste = client.get(URL, headers=_jeton(admin))
    assert liste.status_code == 200
    assert {c["email"] for c in liste.json()} == {"admin@fds.ht", "agent.un@fds.ht"}


def test_un_agent_ne_peut_ni_lister_ni_modifier_les_comptes(client, session_factory):
    admin = _creer(session_factory, "admin@fds.ht", ROLE_ADMIN)
    agent = _creer(session_factory, "agent@fds.ht", ROLE_AGENT)
    entete_agent = _jeton(agent)

    assert client.get(URL, headers=entete_agent).status_code == 403
    assert client.post(URL, json={"email": "x@fds.ht", "mot_de_passe": "x" * 12, "role": "agent"}, headers=entete_agent).status_code == 403
    assert client.patch(f"{URL}/{admin.id}", json={"role": "agent"}, headers=entete_agent).status_code == 403
    assert client.put(f"{URL}/{admin.id}/mot-de-passe", json={"mot_de_passe": "x" * 12}, headers=entete_agent).status_code == 403


def test_validations_et_doublon_a_la_creation(client, session_factory):
    admin = _creer(session_factory, "admin@fds.ht", ROLE_ADMIN)
    entete = _jeton(admin)

    vide = client.post(URL, json={"email": "", "mot_de_passe": "court", "role": "inconnu"}, headers=entete)
    assert vide.status_code == 422
    assert set(vide.json()["detail"]["erreurs"]) == {"email", "mot_de_passe", "role"}

    invalide = client.post(URL, json={"email": "sans-arobase", "mot_de_passe": "x" * 12, "role": "agent"}, headers=entete)
    assert invalide.status_code == 422
    assert "email" in invalide.json()["detail"]["erreurs"]

    doublon = client.post(URL, json={"email": "ADMIN@fds.ht", "mot_de_passe": "x" * 12, "role": "agent"}, headers=entete)
    assert doublon.status_code == 409


def test_changer_role_desactiver_reactiver_et_reinitialiser_mot_de_passe(client, session_factory):
    admin = _creer(session_factory, "admin@fds.ht", ROLE_ADMIN)
    agent = _creer(session_factory, "agent@fds.ht", ROLE_AGENT)
    entete_admin = _jeton(admin)
    entete_agent = _jeton(agent)

    # Promotion en admin puis retour en agent
    promu = client.patch(f"{URL}/{agent.id}", json={"role": "admin"}, headers=entete_admin)
    assert promu.status_code == 200 and promu.json()["role"] == "admin"
    retrograde = client.patch(f"{URL}/{agent.id}", json={"role": "agent"}, headers=entete_admin)
    assert retrograde.status_code == 200 and retrograde.json()["role"] == "agent"

    # Désactivation : le jeton déjà émis est refusé aussitôt
    desactive = client.patch(f"{URL}/{agent.id}", json={"est_actif": False}, headers=entete_admin)
    assert desactive.status_code == 200 and desactive.json()["est_actif"] is False
    assert client.get(MOI, headers=entete_agent).status_code == 401

    # Réactivation + réinitialisation du mot de passe
    reactive = client.patch(f"{URL}/{agent.id}", json={"est_actif": True}, headers=entete_admin)
    assert reactive.status_code == 200 and reactive.json()["est_actif"] is True
    mdp = client.put(f"{URL}/{agent.id}/mot-de-passe", json={"mot_de_passe": "Nouveau-MotDePasse-99"}, headers=entete_admin)
    assert mdp.status_code == 200
    assert _connecter(client, "agent@fds.ht", "Nouveau-MotDePasse-99").status_code == 200


def test_garde_fous_autoprotection_dernier_admin_et_erreurs_modification(client, session_factory):
    admin = _creer(session_factory, "admin@fds.ht", ROLE_ADMIN)
    entete = _jeton(admin)

    # Un admin ne peut ni se désactiver ni se retirer le rôle admin lui-même
    assert client.patch(f"{URL}/{admin.id}", json={"est_actif": False}, headers=entete).status_code == 409
    assert client.patch(f"{URL}/{admin.id}", json={"role": "agent"}, headers=entete).status_code == 409

    # En revanche, un appel neutre (qui conserve admin actif) est accepté
    neutre = client.patch(f"{URL}/{admin.id}", json={"role": "admin", "est_actif": True}, headers=entete)
    assert neutre.status_code == 200

    # Rôle invalide, mot de passe trop court, ou identifiant introuvable
    assert client.patch(f"{URL}/{admin.id}", json={"role": "superadmin"}, headers=entete).status_code == 422
    assert client.patch(f"{URL}/inconnu", json={"est_actif": False}, headers=entete).status_code == 404
    assert client.put(f"{URL}/{admin.id}/mot-de-passe", json={"mot_de_passe": "court"}, headers=entete).status_code == 422
    assert client.put(f"{URL}/inconnu/mot-de-passe", json={"mot_de_passe": "x" * 12}, headers=entete).status_code == 404


def test_dernier_administrateur_actif_ne_peut_pas_etre_retire(client, session_factory, monkeypatch):
    admin_1 = _creer(session_factory, "admin1@fds.ht", ROLE_ADMIN)
    admin_2 = _creer(session_factory, "admin2@fds.ht", ROLE_ADMIN)
    monkeypatch.setattr(SqlUtilisateurRepository, "compter_admins_actifs", lambda self: 1)

    reponse = client.patch(f"{URL}/{admin_2.id}", json={"est_actif": False}, headers=_jeton(admin_1))
    assert reponse.status_code == 409
    assert "dernier administrateur" in reponse.json()["detail"]

