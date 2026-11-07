"""Calendrier d'admission (US-028) : réglage par l'admin, affichage public, candidatures fermées hors période."""

import uuid
from datetime import date, timedelta

import pytest

from backend.dal.models import CalendrierAdmissionModel
from backend.dal.securite import EmetteurJwt, HacheurBcrypt
from backend.dal.utilisateur_repository_sql import SqlUtilisateurRepository
from backend.entities.utilisateur import ROLE_ADMIN, ROLE_AGENT, Utilisateur

from tests.integration.test_admin_dossiers_api import SECRET, _environnement, _soumettre  # noqa: F401
from tests.integration.test_candidatures_api import SAISIE, URL

PUBLIC = "/api/v1/calendrier"
ADMIN = "/api/v1/admin/calendrier"


def _entete(session_factory, email, role):
    utilisateur = Utilisateur(str(uuid.uuid4()), email, HacheurBcrypt().hacher("x" * 12), role)
    with session_factory() as db:
        SqlUtilisateurRepository(db).creer(utilisateur)
    return {"Authorization": f"Bearer {EmetteurJwt(SECRET).emettre(utilisateur).jeton}"}


@pytest.fixture
def admin(session_factory):
    return _entete(session_factory, "admin@fds.ht", ROLE_ADMIN)


@pytest.fixture
def agent(session_factory):
    return _entete(session_factory, "agent@fds.ht", ROLE_AGENT)


def _periode(debut_dans: int, fin_dans: int, **autres) -> dict:
    """Période relative à aujourd'hui (une marge d'un jour évite tout effet de fuseau autour de minuit)."""
    aujourd_hui = date.today()
    return {
        "date_ouverture": (aujourd_hui + timedelta(days=debut_dans)).isoformat(),
        "date_limite": (aujourd_hui + timedelta(days=fin_dans)).isoformat(),
        **autres,
    }


def test_sans_calendrier_le_public_voit_des_dates_a_confirmer(client):
    assert client.get(PUBLIC).json() == {
        "etat": "non_definie", "date_ouverture": None, "date_limite": None,
        "date_concours": None, "date_resultats": None, "date_rentree": None,
    }


def test_l_admin_regle_les_dates_et_le_public_les_voit(client, admin):
    dates = _periode(-5, 20, date_concours="2027-01-10", date_resultats="2027-02-01", date_rentree="2027-03-01")
    reponse = client.put(ADMIN, json=dates, headers=admin)
    assert reponse.status_code == 200
    assert reponse.json()["modifie_par"] == "admin@fds.ht"
    assert reponse.json()["modifie_le"] is not None

    public = client.get(PUBLIC).json()
    assert public["etat"] == "ouverte"
    assert public["date_limite"] == dates["date_limite"]
    assert public["date_concours"] == "2027-01-10"
    assert "modifie_par" not in public  # l'auteur n'est montré qu'au personnel


def test_chaque_modification_est_conservee(client, admin, session_factory):
    client.put(ADMIN, json=_periode(-5, 20), headers=admin)
    client.put(ADMIN, json=_periode(-5, 30), headers=admin)
    with session_factory() as db:
        assert db.query(CalendrierAdmissionModel).count() == 2
    assert client.get(PUBLIC).json()["date_limite"] == _periode(-5, 30)["date_limite"]


def test_un_agent_lit_le_calendrier_mais_ne_le_modifie_pas(client, agent):
    assert client.get(ADMIN, headers=agent).status_code == 200
    assert client.put(ADMIN, json=_periode(-5, 20), headers=agent).status_code == 403


def test_sans_jeton_la_modification_est_refusee(client):
    assert client.put(ADMIN, json=_periode(-5, 20)).status_code == 401


def test_des_dates_dans_le_desordre_sont_refusees(client, admin):
    reponse = client.put(ADMIN, json=_periode(10, 5), headers=admin)
    assert reponse.status_code == 422
    assert "date_limite" in reponse.json()["detail"]["erreurs"]


@pytest.mark.parametrize("debut, fin", [(5, 20), (-20, -5)])
def test_hors_periode_on_ne_peut_pas_commencer_une_candidature(client, admin, debut, fin):
    client.put(ADMIN, json=_periode(debut, fin), headers=admin)
    reponse = client.post(URL, json=SAISIE)
    assert reponse.status_code == 403
    detail = reponse.json()["detail"]
    assert detail["code"] == "candidatures_fermees"
    assert detail["date_limite"] == _periode(debut, fin)["date_limite"]


def test_apres_la_date_limite_un_brouillon_ne_peut_plus_etre_soumis(client, admin):
    cid = client.post(URL, json=SAISIE).json()["candidature_id"]
    client.put(ADMIN, json=_periode(-20, -5), headers=admin)
    reponse = client.post(f"{URL}/{cid}/soumission")
    assert reponse.status_code == 403
    assert reponse.json()["detail"]["code"] == "candidatures_fermees"


def test_apres_la_date_limite_un_dossier_soumis_reste_consultable(client, admin):
    reference = _soumettre(client, "louismy@exemple.com")
    client.put(ADMIN, json=_periode(-20, -5), headers=admin)
    assert client.get(f"{URL}/{reference}/statut", params={"date_naissance": SAISIE["date_naissance"]}).status_code == 200
