"""Tests d'intégration de la consultation des dossiers par le personnel (US-012) : base SQLite en mémoire.
"""

import uuid

import pytest

from backend.api.v1.candidatures import get_email_sender
from backend.api.v1.limiteur import limiteur_envois
from backend.api.v1.securite import limiteur_connexion
from backend.dal.models import CandidatureModel, DocumentSoumisModel
from backend.dal.securite import EmetteurJwt, HacheurBcrypt
from backend.dal.utilisateur_repository_sql import SqlUtilisateurRepository
from backend.entities.utilisateur import ROLE_AGENT, Utilisateur
from backend.main import app
from backend.ports.email_sender import IEmailSender

from tests.integration.test_candidatures_api import SAISIE, URL
from tests.integration.test_documents_api import LES_CINQ, PHOTOS
from tests.integration.test_soumission_api import _dossier
from tests.unit.bll.fakes_documents import JPG, PDF

SECRET = "a" * 48
LISTE = "/api/v1/admin/candidatures"


class EmailMuet(IEmailSender):
    def envoyer(self, message):
        pass


@pytest.fixture(autouse=True)
def _environnement(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", SECRET)
    app.dependency_overrides[get_email_sender] = lambda: EmailMuet()
    limiteur_connexion.reinitialiser()


@pytest.fixture
def entete(session_factory):
    agent = Utilisateur(str(uuid.uuid4()), "agent@fds.ht", HacheurBcrypt().hacher("x" * 12), ROLE_AGENT)
    with session_factory() as db:
        SqlUtilisateurRepository(db).creer(agent)
    return {"Authorization": f"Bearer {EmetteurJwt(SECRET).emettre(agent).jeton}"}


def _soumettre(client, email, nom="Louis", prenom="Louismy"):
    """Crée et soumet un dossier complet ; retourne sa référence."""
    cid = client.post(URL, json={**SAISIE, "email": email, "nom": nom, "prenom": prenom}).json()["candidature_id"]
    client.put(f"{URL}/{cid}/deplacement-physique", json={"deplacement_physique": False})
    client.post(f"{URL}/{cid}/paiement", json={"methode": "NATCASH", "numero_telephone": "47123456"})
    for piece in LES_CINQ:
        nom, contenu = ("photos.jpg", JPG) if piece == PHOTOS else (f"{piece}.pdf", PDF)
        client.post(f"{URL}/{cid}/documents/{piece}", files={"fichier": (nom, contenu, "application/octet-stream")})
    limiteur_envois.reinitialiser()
    return client.post(f"{URL}/{cid}/soumission").json()["reference_dossier"]


def _decider(session_factory, reference, **statuts):
    """Simule des décisions admin (US-013 pas encore construite) : {id de pièce: statut}."""
    with session_factory() as db:
        candidat_id = db.query(CandidatureModel).filter_by(reference_dossier=reference).one().candidat_id
        for piece, statut in statuts.items():
            ligne = db.query(DocumentSoumisModel).filter_by(candidat_id=candidat_id, document_requis_id=piece).one()
            ligne.statut_validation = statut
        db.commit()


def test_liste_sans_jeton_refusee(client):
    assert client.get(LISTE).status_code == 401
    assert client.get(f"{LISTE}/CAN-2026-0001").status_code == 401
    assert client.get("/api/v1/admin/proxy-document/x").status_code == 401


def test_liste_vide(client, entete):
    data = client.get(LISTE, headers=entete).json()
    assert data["total"] == 0 and data["items"] == []
    assert data["statistiques"]["dossiers_soumis"] == 0


def test_liste_pagination_et_champs(client, entete, session_factory):
    refs = [_soumettre(client, f"c{n}@exemple.com", prenom=f"Cand{n}") for n in range(3)]
    page1 = client.get(f"{LISTE}?page=1&limit=2", headers=entete).json()
    assert (page1["total"], page1["page"], page1["limit"]) == (3, 1, 2)
    assert [i["reference_dossier"] for i in page1["items"]] == refs[:2]  # du plus ancien au plus récent
    assert [i["reference_dossier"] for i in client.get(f"{LISTE}?page=2&limit=2", headers=entete).json()["items"]] == refs[2:]
    ligne = page1["items"][0]
    assert ligne["nom"] == "Louis" and ligne["prenom"] == "Cand0" and ligne["deplacement_physique"] is False
    assert ligne["statut_paiement"] == "SIMULE_PAYE" and ligne["statut"] == "en_examen"
    assert (ligne["pieces_total"], ligne["pieces_en_attente"], ligne["pieces_validees"], ligne["pieces_rejetees"]) == (5, 5, 0, 0)
    assert ligne["soumise_le"] and ligne["created_at"]
    assert "email" not in ligne and "telephone" not in ligne  # la liste ne montre pas les coordonnées


def test_les_brouillons_ne_sont_pas_listes(client, entete):
    _soumettre(client, "a@exemple.com")
    _dossier(client, email="brouillon@exemple.com")  # jamais soumis
    assert client.get(LISTE, headers=entete).json()["total"] == 1


def test_limites_de_pagination_validees(client, entete):
    assert client.get(f"{LISTE}?limit=101", headers=entete).status_code == 422
    assert client.get(f"{LISTE}?page=0", headers=entete).status_code == 422
    assert client.get(f"{LISTE}?statut=nimporte", headers=entete).status_code == 422


def test_filtres_statut_deplacement_et_recherche(client, entete, session_factory):
    a = _soumettre(client, "a@exemple.com", nom="Éloïse", prenom="Marie")
    b = _soumettre(client, "b@exemple.com", nom="Pierre", prenom="Jean")
    c = _soumettre(client, "c@exemple.com", nom="Joseph", prenom="Paul")
    _decider(session_factory, b, **{LES_CINQ[0]: "rejete"})
    _decider(session_factory, c, **{p: "valide" for p in LES_CINQ})
    with session_factory() as db:
        db.query(CandidatureModel).filter_by(reference_dossier=a).one().deplacement_physique = True
        db.commit()

    def refs(**params):
        reponse = client.get(LISTE, params=params, headers=entete).json()
        return [i["reference_dossier"] for i in reponse["items"]]

    assert refs(statut="en_examen") == [a]
    assert refs(statut="action_requise") == [b]
    assert refs(statut="complet") == [c]
    assert refs(deplacement_physique="true") == [a]
    assert refs(deplacement_physique="false") == [b, c]
    assert refs(q="eloise") == [a]  # sans accent ni majuscule
    assert refs(q="pierre jean") == [b] and refs(q="jean pierre") == [b]  # « nom prénom » comme « prénom nom »
    assert refs(q="pierre") == [b]
    assert refs(q="jean marie") == []  # pas de recoupement entre deux candidats
    assert refs(q=c.lower()) == [c]
    assert refs(q="zzz") == []


def test_statistiques_portent_sur_tous_les_dossiers(client, entete, session_factory):
    a = _soumettre(client, "a@exemple.com")
    b = _soumettre(client, "b@exemple.com")
    _decider(session_factory, a, **{LES_CINQ[0]: "valide", LES_CINQ[1]: "rejete"})
    with session_factory() as db:
        db.query(CandidatureModel).filter_by(reference_dossier=b).one().deplacement_physique = True
        db.commit()
    stats = client.get(f"{LISTE}?limit=1&statut=complet", headers=entete).json()["statistiques"]  # filtre sans effet sur les stats
    assert stats == {
        "dossiers_soumis": 2, "sans_deplacement": 1, "pieces_a_examiner": 8, "pieces_deposees": 10, "pieces_refusees": 1,
    }


def test_detail_du_dossier(client, entete, session_factory):
    ref = _soumettre(client, "louismy@exemple.com")
    _decider(session_factory, ref, **{LES_CINQ[2]: "rejete"})
    reponse = client.get(f"{LISTE}/{ref.lower()}", headers=entete)
    assert reponse.status_code == 200
    d = reponse.json()
    assert d["reference_dossier"] == ref and d["statut"] == "action_requise" and d["admission"] == "Premier cycle MPC"
    assert d["email"] == "louismy@exemple.com" and d["montant_htg"] == 500 and d["reference_paiement"].startswith("PAY-SIM-")
    assert [p["id"] for p in d["pieces"]] == LES_CINQ
    rejetee = d["pieces"][2]
    assert rejetee["statut"] == "rejete" and rejetee["document_id"] and rejetee["nom_fichier"].endswith(".pdf")
    assert "cle_stockage" not in reponse.text  # le chemin interne de stockage ne sort jamais


def test_detail_inconnu_ou_brouillon(client, entete):
    cid = _dossier(client, email="brouillon@exemple.com")
    assert client.get(f"{LISTE}/CAN-2026-9999", headers=entete).status_code == 404
    assert client.get(f"{LISTE}/{cid}", headers=entete).status_code == 404


def test_proxy_document(client, entete):
    ref = _soumettre(client, "louismy@exemple.com")
    piece = client.get(f"{LISTE}/{ref}", headers=entete).json()["pieces"][0]
    reponse = client.get(f"/api/v1/admin/proxy-document/{piece['document_id']}", headers=entete)
    assert reponse.status_code == 200
    assert reponse.content == PDF and reponse.headers["content-type"] == "application/pdf"
    assert reponse.headers["x-content-type-options"] == "nosniff"
    assert "sandbox" in reponse.headers["content-security-policy"] and "no-store" in reponse.headers["cache-control"]
    assert "inline" in reponse.headers["content-disposition"]
    assert client.get("/api/v1/admin/proxy-document/inconnu", headers=entete).status_code == 404
