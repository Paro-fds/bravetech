"""Tests d'intégration du suivi de dossier par référence et date de naissance (US-009) : base SQLite en mémoire.
"""

import json
import re

import pytest

from backend.api.v1.candidatures import get_email_sender
from backend.dal.models import DocumentSoumisModel
from backend.main import app
from backend.ports.email_sender import IEmailSender

from tests.integration.test_candidatures_api import SAISIE, URL
from tests.integration.test_documents_api import LES_CINQ
from tests.integration.test_soumission_api import _dossier

NAISSANCE = {"date_naissance": SAISIE["date_naissance"]}


class EmailMuet(IEmailSender):
    def envoyer(self, message):
        pass


@pytest.fixture(autouse=True)
def _sans_email_reel():
    app.dependency_overrides[get_email_sender] = lambda: EmailMuet()


def _dossier_soumis(client, email="louismy@exemple.com"):
    cid = _dossier(client, email=email)
    return client.post(f"{URL}/{cid}/soumission").json()["reference_dossier"]


def test_suivi_dossier_soumis(client):
    reference = _dossier_soumis(client)
    reponse = client.get(f"{URL}/{reference}/statut", params=NAISSANCE)
    assert reponse.status_code == 200
    data = reponse.json()
    assert data["reference_dossier"] == reference
    assert data["prenom"] == "Louismy" and data["initiale_nom"] == "L"
    assert data["admission"] == "Premier cycle MPC"
    assert data["soumise_le"].endswith("Z") or data["soumise_le"].endswith("+00:00")
    assert data["statut_global"] == "en_examen"
    assert data["pieces_validees"] == 0 and data["pieces_total"] == 5
    assert [p["id"] for p in data["pieces"]] == LES_CINQ
    assert {p["statut"] for p in data["pieces"]} == {"en_attente"}
    assert all(p["depose_le"] for p in data["pieces"])


def test_reference_insensible_a_la_casse_et_aux_espaces(client):
    reference = _dossier_soumis(client)
    assert client.get(f"{URL}/%20{reference.lower()}%20/statut", params=NAISSANCE).status_code == 200


def test_n_expose_aucune_donnee_personnelle(client):
    reference = _dossier_soumis(client)
    brut = json.dumps(client.get(f"{URL}/{reference}/statut", params=NAISSANCE).json(), ensure_ascii=False)
    # Ni le nom complet, ni l'email, ni le téléphone, ni la date de naissance, ni la commune, ni les noms de fichiers
    for secret in ("louismy@exemple.com", "37123456", "37 12 34 56", "2008", "Pétion", ".pdf", ".jpg"):
        assert secret not in brut, secret
    # Le nom de famille ne doit pas apparaître en entier (« Louis » est aussi contenu dans le prénom « Louismy »)
    assert not re.search(rf"\b{SAISIE['nom']}\b", brut)
    assert set(client.get(f"{URL}/{reference}/statut", params=NAISSANCE).json()) == {
        "reference_dossier", "prenom", "initiale_nom", "admission", "soumise_le",
        "statut_global", "pieces_validees", "pieces_total", "pieces",
    }


@pytest.mark.parametrize("saisie", ["CAN-2026-9999", "n-importe-quoi", "CAN-2026", "CAN-26-0001", "0001"])
def test_reference_inconnue_ou_mal_formee(client, saisie):
    _dossier_soumis(client)
    reponse = client.get(f"{URL}/{saisie}/statut", params=NAISSANCE)
    assert reponse.status_code == 404
    assert reponse.json()["detail"] == "Aucun dossier trouvé pour cette référence et cette date de naissance."


@pytest.mark.parametrize("date_erronee", ["", "2008-05-15", "1999-01-01", "14/05/2008", "invalide"])
def test_sans_date_de_naissance_exacte_meme_reponse_404(client, date_erronee):
    """La simple référence séquentielle ne permet jamais de consulter un dossier ni de savoir s'il existe."""
    reference = _dossier_soumis(client)
    reponse = client.get(f"{URL}/{reference}/statut", params={"date_naissance": date_erronee} if date_erronee else None)
    assert reponse.status_code == 404
    assert reponse.json()["detail"] == "Aucun dossier trouvé pour cette référence et cette date de naissance."


def test_un_brouillon_n_est_pas_consultable(client):
    # Un brouillon n'a pas de référence ; son identifiant (UUID) ne doit pas non plus ouvrir la page publique
    cid = _dossier(client, email="brouillon@exemple.com")
    assert client.get(f"{URL}/{cid}/statut", params=NAISSANCE).status_code == 404


def test_statuts_apres_decision(client, session_factory):
    reference = _dossier_soumis(client)
    with session_factory() as db:
        valides = db.query(DocumentSoumisModel).filter(DocumentSoumisModel.document_requis_id.in_(LES_CINQ[:2]))
        for ligne in valides:
            ligne.statut_validation = "valide"
        rejet = db.query(DocumentSoumisModel).filter(DocumentSoumisModel.document_requis_id == LES_CINQ[2]).one()
        rejet.statut_validation = "rejete"
        rejet.motif_rejet = "Document illisible"
        db.commit()

    data = client.get(f"{URL}/{reference}/statut", params=NAISSANCE).json()
    assert data["statut_global"] == "action_requise"
    assert data["pieces_validees"] == 2
    rejetee = next(p for p in data["pieces"] if p["id"] == LES_CINQ[2])
    assert rejetee["statut"] == "rejete" and rejetee["motif_rejet"] == "Document illisible"


def test_dossier_complet_quand_tout_est_valide(client, session_factory):
    reference = _dossier_soumis(client)
    with session_factory() as db:
        for ligne in db.query(DocumentSoumisModel):
            ligne.statut_validation = "valide"
        db.commit()
    data = client.get(f"{URL}/{reference}/statut", params=NAISSANCE).json()
    assert data["statut_global"] == "complet" and data["pieces_validees"] == 5


def test_limitation_de_debit_contre_l_enumeration(client):
    codes = [client.get(f"{URL}/CAN-2026-{n:04d}/statut", params=NAISSANCE).status_code for n in range(1, 26)]
    assert codes[:20] == [404] * 20
    assert codes[20:] == [429] * 5
