"""Tests d'intégration du remplacement d'une pièce refusée par le candidat (US-010) : SQLite en mémoire, stockage temporaire.
"""

import pytest

from backend.api.v1.candidatures import get_email_sender
from backend.dal.models import DecisionDocumentModel, DocumentSoumisModel
from backend.main import app

from tests.integration.test_admin_dossiers_api import LISTE, _environnement, _soumettre  # noqa: F401
from tests.integration.test_candidatures_api import SAISIE, URL
from tests.integration.test_decisions_api import _decider, _documents, _EnPanne, _Enregistreur, agent  # noqa: F401
from tests.integration.test_documents_api import LES_CINQ, PHOTOS
from tests.unit.bll.fakes_documents import EXE, JPG, PDF

EMAIL = "louismy@exemple.com"
RELEVE = LES_CINQ[2]


def _remplacer(client, ref, piece=RELEVE, email=EMAIL, nom="nouveau.pdf", contenu=PDF):
    return client.post(
        f"{URL}/{ref}/pieces/{piece}/remplacement",
        data={"email": email},
        files={"fichier": (nom, contenu, "application/octet-stream")},
    )


@pytest.fixture
def dossier_refuse(client, agent):  # noqa: F811
    """Dossier soumis dont le relevé de notes a été refusé ; retourne (référence, en-tête agent, id du document)."""
    _, entete = agent
    ref = _soumettre(client, EMAIL)
    document_id = _documents(client, entete, ref)[RELEVE]["document_id"]
    assert _decider(client, entete, document_id, "rejete", "Document illisible").status_code == 200
    return ref, entete, document_id


def test_remplacement_repasse_en_attente_sans_doublon(client, dossier_refuse, session_factory, dossier_uploads):
    ref, entete, document_id = dossier_refuse
    with session_factory() as db:
        ancienne_cle = db.get(DocumentSoumisModel, document_id).cle_stockage
    assert (dossier_uploads / ancienne_cle).exists()

    reponse = _remplacer(client, ref)
    assert reponse.status_code == 200
    assert reponse.json()["id"] == RELEVE and reponse.json()["statut"] == "en_attente"

    with session_factory() as db:
        assert db.query(DocumentSoumisModel).count() == 5  # aucun doublon : même document logique
        ligne = db.get(DocumentSoumisModel, document_id)
        assert ligne.statut_validation == "en_attente" and ligne.nom_fichier == "nouveau.pdf"
        assert ligne.motif_rejet is None and ligne.valide_par is None and ligne.date_validation is None
        assert db.query(DecisionDocumentModel).count() == 1  # le refus reste dans l'historique
        nouvelle_cle = ligne.cle_stockage
    assert nouvelle_cle != ancienne_cle
    assert (dossier_uploads / nouvelle_cle).exists() and not (dossier_uploads / ancienne_cle).exists()

    # Le suivi public reflète le nouvel état immédiatement
    suivi = client.get(f"{URL}/{ref}/statut", params={"date_naissance": SAISIE["date_naissance"]}).json()
    assert suivi["statut_global"] == "en_examen"
    piece = next(p for p in suivi["pieces"] if p["id"] == RELEVE)
    assert piece["statut"] == "en_attente" and piece["motif_rejet"] is None


def test_la_piece_remplacee_peut_etre_decidee_de_nouveau(client, dossier_refuse):
    ref, entete, document_id = dossier_refuse
    assert _remplacer(client, ref).status_code == 200
    assert _decider(client, entete, document_id, "valide").status_code == 200
    historique = client.get(f"{LISTE}/{ref}", headers=entete).json()["decisions"]
    assert [h["statut"] for h in historique] == ["rejete", "valide"]


def test_email_insensible_a_la_casse_et_aux_espaces(client, dossier_refuse):
    ref, *_ = dossier_refuse
    assert _remplacer(client, ref.lower(), email="  LouisMy@Exemple.COM ").status_code == 200


def test_email_de_confirmation_du_remplacement(client, dossier_refuse):
    ref, *_ = dossier_refuse
    emails = _Enregistreur()
    app.dependency_overrides[get_email_sender] = lambda: emails
    assert _remplacer(client, ref).status_code == 200
    (message,) = emails.messages
    assert message.destinataire == EMAIL and "Nouvelle pièce reçue" in message.sujet
    assert f"/suivi/{ref}" in message.html


def test_panne_d_email_n_annule_pas_le_remplacement(client, dossier_refuse, session_factory):
    ref, _, document_id = dossier_refuse
    app.dependency_overrides[get_email_sender] = lambda: _EnPanne()
    assert _remplacer(client, ref).status_code == 200
    with session_factory() as db:
        assert db.get(DocumentSoumisModel, document_id).statut_validation == "en_attente"


def test_mauvais_email_ou_reference_inconnue_meme_reponse(client, dossier_refuse):
    ref, *_ = dossier_refuse
    mauvais_email = _remplacer(client, ref, email="autre@exemple.com")
    inconnue = _remplacer(client, "CAN-2026-9999")
    assert mauvais_email.status_code == inconnue.status_code == 403
    assert mauvais_email.json() == inconnue.json() == {"detail": "Référence ou email incorrect."}


def test_echecs_d_identite_limites_par_ip(client, dossier_refuse):
    ref, *_ = dossier_refuse
    codes = [_remplacer(client, ref, email=f"devine{n}@exemple.com").status_code for n in range(5)]
    assert codes == [403] * 5
    bloque = _remplacer(client, ref, email=EMAIL)  # même avec le bon email, tant que la fenêtre court
    assert bloque.status_code == 429 and bloque.headers["retry-after"] == "60"


def test_seule_une_piece_refusee_se_remplace(client, dossier_refuse, agent):  # noqa: F811
    ref, entete, _ = dossier_refuse
    en_attente = _remplacer(client, ref, piece=LES_CINQ[0])
    assert en_attente.status_code == 409
    valide_id = _documents(client, entete, ref)[LES_CINQ[1]]["document_id"]
    _decider(client, entete, valide_id, "valide")
    assert _remplacer(client, ref, piece=LES_CINQ[1]).status_code == 409
    assert _documents(client, entete, ref)[LES_CINQ[1]]["statut"] == "valide"  # intacte


def test_fichier_invalide_laisse_la_piece_refusee_et_l_ancien_fichier(client, dossier_refuse, session_factory, dossier_uploads):
    ref, _, document_id = dossier_refuse
    with session_factory() as db:
        cle = db.get(DocumentSoumisModel, document_id).cle_stockage

    deguise = _remplacer(client, ref, nom="virus.pdf", contenu=EXE)
    assert deguise.status_code == 422 and "fichier" in deguise.json()["detail"]["erreurs"]
    assert _remplacer(client, ref, nom="releve.exe", contenu=PDF).status_code == 422
    trop_gros = _remplacer(client, ref, contenu=PDF + b"0" * (5 * 1024 * 1024))
    assert trop_gros.status_code == 413

    with session_factory() as db:
        ligne = db.get(DocumentSoumisModel, document_id)
        assert ligne.statut_validation == "rejete" and ligne.cle_stockage == cle
    assert (dossier_uploads / cle).exists()
    assert len(list(dossier_uploads.rglob("*"))) == len([p for p in dossier_uploads.rglob("*") if p.is_dir()]) + 5  # aucun fichier orphelin


def test_format_propre_a_la_piece_et_piece_inconnue(client, dossier_refuse, agent):  # noqa: F811
    ref, entete, _ = dossier_refuse
    photos = _documents(client, entete, ref)[PHOTOS]["document_id"]
    _decider(client, entete, photos, "rejete", "Photos trop sombres")
    assert _remplacer(client, ref, piece=PHOTOS, nom="photos.pdf", contenu=PDF).status_code == 422  # les photos : JPG/PNG
    assert _remplacer(client, ref, piece=PHOTOS, nom="photos.jpg", contenu=JPG).status_code == 200
    assert _remplacer(client, ref, piece="mpc-inconnue").status_code == 404
