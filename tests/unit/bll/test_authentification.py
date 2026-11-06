"""Tests unitaires de l'authentification du personnel (US-011) : cas d'utilisation, bcrypt et JWT.
"""

import time
import uuid

import jwt
import pytest

from backend.bll.authentification import AuthentifierUtilisateurUseCase, ObtenirUtilisateurCourantUseCase
from backend.dal.securite import EmetteurJwt, HacheurBcrypt, SecretJwtManquant
from backend.entities.erreurs import AccesInterdit, IdentifiantsInvalides, JetonInvalide
from backend.entities.utilisateur import ROLE_ADMIN, ROLE_AGENT, Utilisateur
from backend.ports.utilisateur_repository import IUtilisateurRepository

SECRET = "s" * 48
MOT_DE_PASSE = "Mot-de-passe-solide-42"


class FakeUtilisateurs(IUtilisateurRepository):
    def __init__(self):
        self.lignes: dict[str, Utilisateur] = {}

    def trouver_par_email(self, email):
        return next((u for u in self.lignes.values() if u.email == email), None)

    def obtenir(self, utilisateur_id):
        return self.lignes.get(utilisateur_id)

    def creer(self, utilisateur):
        self.lignes[utilisateur.id] = utilisateur

    def lister(self):
        return list(self.lignes.values())

    def mettre_a_jour(self, utilisateur):
        self.lignes[utilisateur.id] = utilisateur

    def compter_admins_actifs(self):
        return sum(1 for u in self.lignes.values() if u.role == ROLE_ADMIN and u.est_actif)


@pytest.fixture(scope="module")
def hacheur():
    return HacheurBcrypt()


@pytest.fixture
def emetteur():
    return EmetteurJwt(SECRET)


@pytest.fixture
def depot(hacheur):
    d = FakeUtilisateurs()
    d.creer(Utilisateur(str(uuid.uuid4()), "admin@fds.ht", hacheur.hacher(MOT_DE_PASSE), ROLE_ADMIN))
    d.creer(Utilisateur(str(uuid.uuid4()), "agent@fds.ht", hacheur.hacher(MOT_DE_PASSE), ROLE_AGENT))
    d.creer(Utilisateur(str(uuid.uuid4()), "parti@fds.ht", hacheur.hacher(MOT_DE_PASSE), ROLE_AGENT, est_actif=False))
    return d


def test_connexion_reussie_emet_un_jeton_de_60_minutes(depot, hacheur, emetteur):
    jeton = AuthentifierUtilisateurUseCase(depot, hacheur, emetteur).executer("  Admin@FDS.ht ", MOT_DE_PASSE)
    assert jeton.expire_dans_secondes == 3600
    charge = jwt.decode(jeton.jeton, SECRET, algorithms=["HS256"])
    assert charge["role"] == ROLE_ADMIN and charge["exp"] - charge["iat"] == 3600


@pytest.mark.parametrize(
    "email, mot_de_passe",
    [("admin@fds.ht", "mauvais"), ("inconnu@fds.ht", MOT_DE_PASSE), ("parti@fds.ht", MOT_DE_PASSE), ("", ""), ("admin@fds.ht", "é" * 100)],
)
def test_tout_echec_leve_la_meme_erreur(depot, hacheur, emetteur, email, mot_de_passe):
    with pytest.raises(IdentifiantsInvalides):
        AuthentifierUtilisateurUseCase(depot, hacheur, emetteur).executer(email, mot_de_passe)


def test_bcrypt_sale_et_verifie(hacheur):
    a, b = hacheur.hacher(MOT_DE_PASSE), hacheur.hacher(MOT_DE_PASSE)
    assert a != b and a.startswith("$2")  # sel différent à chaque empreinte
    assert hacheur.verifier(MOT_DE_PASSE, a) and not hacheur.verifier("autre", a)
    assert not hacheur.verifier(MOT_DE_PASSE, "empreinte-illisible")


def test_jeton_valide_donne_l_utilisateur(depot, emetteur):
    admin = depot.trouver_par_email("admin@fds.ht")
    utilisateur = ObtenirUtilisateurCourantUseCase(depot, emetteur).executer(emetteur.emettre(admin).jeton)
    assert utilisateur.id == admin.id


def test_jeton_expire_falsifie_ou_sans_expiration_est_refuse(depot, emetteur):
    admin = depot.trouver_par_email("admin@fds.ht")
    cas = [
        EmetteurJwt(SECRET, duree_minutes=-1).emettre(admin).jeton,  # expiré
        EmetteurJwt("autre-secret-de-48-caracteres-" + "x" * 20).emettre(admin).jeton,  # signé par un autre secret
        emetteur.emettre(admin).jeton[:-3] + "abc",  # signature altérée
        jwt.encode({"sub": admin.id, "role": "admin"}, SECRET, algorithm="HS256"),  # sans expiration
        jwt.encode({"sub": admin.id, "exp": int(time.time()) + 600}, algorithm="none", key=None),  # alg: none
        "n-importe-quoi",
    ]
    for jeton in cas:
        with pytest.raises(JetonInvalide):
            ObtenirUtilisateurCourantUseCase(depot, emetteur).executer(jeton)


def test_compte_desactive_perd_l_acces_meme_avec_un_jeton_valide(depot, emetteur):
    agent = depot.trouver_par_email("parti@fds.ht")
    with pytest.raises(JetonInvalide):
        ObtenirUtilisateurCourantUseCase(depot, emetteur).executer(emetteur.emettre(agent).jeton)


def test_le_role_fait_foi_en_base_pas_dans_le_jeton(depot, emetteur):
    agent = depot.trouver_par_email("agent@fds.ht")
    jeton = emetteur.emettre(agent).jeton
    ObtenirUtilisateurCourantUseCase(depot, emetteur).executer(jeton)  # un agent passe
    with pytest.raises(AccesInterdit):
        ObtenirUtilisateurCourantUseCase(depot, emetteur).executer(jeton, (ROLE_ADMIN,))


@pytest.mark.parametrize("secret", ["", "trop-court"])
def test_secret_absent_ou_trop_court_refuse(secret):
    with pytest.raises(SecretJwtManquant):
        EmetteurJwt(secret)
