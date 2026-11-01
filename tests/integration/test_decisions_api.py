"""Tests d'intégration des décisions du personnel sur les pièces (US-013) : base SQLite en mémoire.
"""

import uuid

import pytest

from backend.api.v1.securite import limiteur_connexion
from backend.dal.models import DecisionDocumentModel, DocumentSoumisModel
from backend.dal.securite import EmetteurJwt, HacheurBcrypt
from backend.dal.utilisateur_repository_sql import SqlUtilisateurRepository
from backend.entities.utilisateur import ROLE_ADMIN, ROLE_AGENT, Utilisateur

from tests.integration.test_admin_dossiers_api import LISTE, _environnement, _soumettre  # noqa: F401
from tests.integration.test_candidatures_api import URL
from tests.integration.test_documents_api import LES_CINQ

SECRET = "a" * 48


def _compte(session_factory, email, role=ROLE_AGENT):
    utilisateur = Utilisateur(str(uuid.uuid4()), email, HacheurBcrypt().hacher("x" * 12), role)
    with session_factory() as db:
        SqlUtilisateurRepository(db).creer(utilisateur)
    return utilisateur, {"Authorization": f"Bearer {EmetteurJwt(SECRET).emettre(utilisateur).jeton}"}


@pytest.fixture
def agent(session_factory):
    return _compte(session_factory, "agent@fds.ht")


def _documents(client, entete, reference):
    return {p["id"]: p for p in client.get(f"{LISTE}/{reference}", headers=entete).json()["pieces"]}


def _decider(client, entete, document_id, statut, motif=None):
    corps = {"statut": statut, **({"motif": motif} if motif is not None else {})}
    return client.put(f"/api/v1/admin/documents/{document_id}/statut", json=corps, headers=entete)


def test_decision_sans_jeton_refusee(client):
    assert client.put("/api/v1/admin/documents/x/statut", json={"statut": "valide"}).status_code == 401


def test_validation_enregistre_l_audit(client, agent, session_factory):
    utilisateur, entete = agent
    ref = _soumettre(client, "louismy@exemple.com")
    cin = _documents(client, entete, ref)[LES_CINQ[4]]
    reponse = _decider(client, entete, cin["document_id"], "valide")
    assert reponse.status_code == 200
    data = reponse.json()
    assert data["statut"] == "valide" and data["valide_par"] == utilisateur.id and data["date_validation"]

    with session_factory() as db:
        ligne = db.query(DocumentSoumisModel).filter_by(id=cin["document_id"]).one()
        assert ligne.statut_validation == "valide" and ligne.valide_par == utilisateur.id and ligne.date_validation
        (historique,) = db.query(DecisionDocumentModel).all()
        assert historique.decide_par == utilisateur.id and historique.statut == "valide"


def test_refus_exige_un_motif_puis_apparait_cote_candidat(client, agent):
    _, entete = agent
    ref = _soumettre(client, "louismy@exemple.com")
    releve = _documents(client, entete, ref)[LES_CINQ[2]]
    assert _decider(client, entete, releve["document_id"], "rejete").status_code == 422
    assert _decider(client, entete, releve["document_id"], "rejete", "ok").status_code == 422
    assert _documents(client, entete, ref)[LES_CINQ[2]]["statut"] == "en_attente"  # rien n'a été écrit

    assert _decider(client, entete, releve["document_id"], "rejete", "Document illisible, page coupée").status_code == 200
    # Le candidat voit le refus et son motif sur la page publique de suivi
    suivi = client.get(f"{URL}/{ref}/statut").json()
    assert suivi["statut_global"] == "action_requise"
    piece = next(p for p in suivi["pieces"] if p["id"] == LES_CINQ[2])
    assert piece["statut"] == "rejete" and piece["motif_rejet"] == "Document illisible, page coupée"
    # Et le tableau de bord le range dans « Action du candidat »
    assert client.get(LISTE, params={"statut": "action_requise"}, headers=entete).json()["total"] == 1


def test_une_decision_est_definitive(client, agent):
    _, entete = agent
    ref = _soumettre(client, "louismy@exemple.com")
    piece = _documents(client, entete, ref)[LES_CINQ[0]]
    assert _decider(client, entete, piece["document_id"], "valide").status_code == 200
    assert _decider(client, entete, piece["document_id"], "rejete", "Finalement non").status_code == 409
    assert _decider(client, entete, piece["document_id"], "valide").status_code == 409
    assert _documents(client, entete, ref)[LES_CINQ[0]]["statut"] == "valide"


def test_historique_dans_le_detail_du_dossier(client, agent, session_factory):
    _, entete_agent = agent
    _, entete_admin = _compte(session_factory, "admin@fds.ht", ROLE_ADMIN)
    ref = _soumettre(client, "louismy@exemple.com")
    pieces = _documents(client, entete_agent, ref)
    _decider(client, entete_agent, pieces[LES_CINQ[0]]["document_id"], "valide")
    _decider(client, entete_admin, pieces[LES_CINQ[1]]["document_id"], "rejete", "Photocopie floue")

    historique = client.get(f"{LISTE}/{ref}", headers=entete_admin).json()["decisions"]
    assert [(h["piece_id"], h["statut"], h["decide_par"]) for h in historique] == [
        (LES_CINQ[0], "valide", "agent@fds.ht"),
        (LES_CINQ[1], "rejete", "admin@fds.ht"),
    ]
    assert historique[1]["motif"] == "Photocopie floue" and historique[0]["decide_le"]
    assert historique[0]["piece_nom"]


def test_le_remplacement_d_une_piece_refusee_conserve_l_historique(client, agent, session_factory):
    """Le candidat redépose une pièce refusée (US-010 à venir) : l'ancienne décision reste dans l'historique."""
    from backend.dal.document_repository_sql import SqlDocumentRepository
    from backend.entities.document_soumis import DocumentSoumis
    from datetime import datetime, timezone

    _, entete = agent
    ref = _soumettre(client, "louismy@exemple.com")
    piece = _documents(client, entete, ref)[LES_CINQ[0]]
    _decider(client, entete, piece["document_id"], "rejete", "Illisible")

    with session_factory() as db:
        depot = SqlDocumentRepository(db)
        ancien = db.get(DocumentSoumisModel, piece["document_id"])
        depot.enregistrer(DocumentSoumis(
            ancien.id, ancien.candidat_id, ancien.document_requis_id, "nouveau.pdf", "k/nouveau.pdf", "application/pdf",
            40, datetime.now(timezone.utc),
        ))
    apres = _documents(client, entete, ref)[LES_CINQ[0]]
    assert apres["statut"] == "en_attente" and apres["valide_par"] is None  # nouveau cycle
    assert _decider(client, entete, piece["document_id"], "valide").status_code == 200  # décidable de nouveau
    historique = client.get(f"{LISTE}/{ref}", headers=entete).json()["decisions"]
    assert [h["statut"] for h in historique] == ["rejete", "valide"]


def test_document_inconnu_ou_corps_invalide(client, agent):
    _, entete = agent
    assert _decider(client, entete, "inconnu", "valide").status_code == 404
    assert client.put("/api/v1/admin/documents/x/statut", json={"statut": "valide", "autre": 1}, headers=entete).status_code == 422


def test_brouillon_non_decidable(client, agent, session_factory):
    _, entete = agent
    from tests.integration.test_soumission_api import _dossier

    _dossier(client, email="brouillon@exemple.com")  # pièces déposées mais dossier non soumis
    with session_factory() as db:
        document_id = db.query(DocumentSoumisModel).first().id
    assert _decider(client, entete, document_id, "valide").status_code == 404


def test_deux_agents_simultanes_un_seul_gagne(client, agent, session_factory):
    """Un second agent qui a lu le document « en attente » avant la décision du premier ne peut pas l'écraser."""
    from datetime import datetime, timezone

    from backend.dal.document_repository_sql import SqlDocumentRepository
    from backend.entities.decision_document import DecisionDocument
    from backend.entities.erreurs import DocumentDejaDecide

    utilisateur, entete = agent
    ref = _soumettre(client, "louismy@exemple.com")
    piece = _documents(client, entete, ref)[LES_CINQ[0]]
    with session_factory() as db:
        depot = SqlDocumentRepository(db)
        lu_trop_tot = depot.obtenir_par_id(piece["document_id"])  # état « en attente » lu par le second agent
        assert _decider(client, entete, piece["document_id"], "valide").status_code == 200  # le premier décide
        lu_trop_tot.statut_validation, lu_trop_tot.motif_rejet = "rejete", "Trop tard"
        decision = DecisionDocument(
            "d-tardive", lu_trop_tot.id, lu_trop_tot.candidat_id, lu_trop_tot.document_requis_id, "rejete", "Trop tard",
            utilisateur.id, datetime.now(timezone.utc),
        )
        with pytest.raises(DocumentDejaDecide):
            depot.enregistrer_decision(lu_trop_tot, decision)
    with session_factory() as db:
        assert db.query(DecisionDocumentModel).count() == 1  # la décision tardive n'a laissé aucune trace
        assert db.get(DocumentSoumisModel, piece["document_id"]).statut_validation == "valide"


# --- US-014 : email après décision ----------------------------------------------------------------

from backend.api.v1.candidatures import get_email_sender  # noqa: E402
from backend.main import app  # noqa: E402
from backend.ports.email_sender import IEmailSender  # noqa: E402


class _Enregistreur(IEmailSender):
    def __init__(self):
        self.messages = []

    def envoyer(self, message):
        self.messages.append(message)


class _EnPanne(IEmailSender):
    def envoyer(self, message):
        raise ConnectionError("Resend indisponible")


def test_la_decision_envoie_un_email_au_candidat(client, agent):
    _, entete = agent
    ref = _soumettre(client, "louismy@exemple.com")
    emails = _Enregistreur()
    app.dependency_overrides[get_email_sender] = lambda: emails  # après le dépôt : on ne compte que les décisions
    pieces = _documents(client, entete, ref)

    _decider(client, entete, pieces[LES_CINQ[0]]["document_id"], "valide")
    _decider(client, entete, pieces[LES_CINQ[2]]["document_id"], "rejete", "Page coupée")
    valide, refuse = emails.messages
    assert valide.destinataire == refuse.destinataire == "louismy@exemple.com"
    assert "validée" in valide.sujet and "à remplacer" in refuse.sujet
    assert "Page coupée" in refuse.texte and f"/suivi/{ref}" in refuse.html


def test_une_decision_refusee_n_envoie_rien(client, agent):
    _, entete = agent
    ref = _soumettre(client, "louismy@exemple.com")
    emails = _Enregistreur()
    app.dependency_overrides[get_email_sender] = lambda: emails
    piece = _documents(client, entete, ref)[LES_CINQ[0]]
    _decider(client, entete, piece["document_id"], "rejete")  # 422 : motif manquant
    _decider(client, entete, piece["document_id"], "valide")
    _decider(client, entete, piece["document_id"], "valide")  # 409 : déjà décidée
    assert len(emails.messages) == 1


def test_panne_d_email_n_annule_pas_la_decision(client, agent, caplog, session_factory):
    import logging

    _, entete = agent
    ref = _soumettre(client, "louismy@exemple.com")
    app.dependency_overrides[get_email_sender] = lambda: _EnPanne()
    piece = _documents(client, entete, ref)[LES_CINQ[0]]
    with caplog.at_level(logging.ERROR):
        reponse = _decider(client, entete, piece["document_id"], "valide")
    assert reponse.status_code == 200 and reponse.json()["statut"] == "valide"
    with session_factory() as db:
        assert db.get(DocumentSoumisModel, piece["document_id"]).statut_validation == "valide"
        assert db.query(DecisionDocumentModel).count() == 1
    assert "Email de décision non envoyé" in caplog.text and "louismy@exemple.com" not in caplog.text
