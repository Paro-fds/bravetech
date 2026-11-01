"""Tests d'intégration de l'export CSV et PDF des dossiers (US-015) : SQLite en mémoire.
"""

import csv
import io
import logging
import re

import pytest

from backend.bll.exporter_candidatures import COLONNES, neutraliser
from backend.dal.models import CandidatModel, CandidatureModel

from tests.integration.test_admin_dossiers_api import (  # noqa: F401
    LISTE,
    _decider,
    _environnement,
    _soumettre,
    entete,
)
from tests.integration.test_documents_api import LES_CINQ

EXPORT = f"{LISTE}/export"


def _lire_csv(reponse):
    texte = reponse.content.decode("utf-8-sig")
    return list(csv.reader(io.StringIO(texte), delimiter=";"))


def test_export_sans_jeton_refuse(client):
    assert client.get(EXPORT).status_code == 401
    assert client.get(EXPORT, params={"format": "pdf"}).status_code == 401


def test_csv_telechargeable_avec_les_bonnes_colonnes(client, entete):
    a = _soumettre(client, "a@exemple.com", nom="Éloïse", prenom="Marie")
    b = _soumettre(client, "b@exemple.com", nom="Pierre", prenom="Jean")
    reponse = client.get(EXPORT, headers=entete)
    assert reponse.status_code == 200
    assert reponse.headers["content-type"].startswith("text/csv")
    assert re.fullmatch(r'attachment; filename="candidatures-\d{4}-\d{2}-\d{2}\.csv"', reponse.headers["content-disposition"])
    assert "no-store" in reponse.headers["cache-control"]
    assert reponse.content.startswith(b"\xef\xbb\xbf")  # BOM : Excel affiche bien les accents

    lignes = _lire_csv(reponse)
    assert lignes[0] == COLONNES
    assert [l[0] for l in lignes[1:]] == [a, b]  # ordre de traitement, comme le tableau de bord
    assert lignes[1][1:6] == ["Éloïse", "Marie", "Non", "À examiner", "0/5"]
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", lignes[1][6])


def test_aucune_coordonnee_dans_l_export(client, entete):
    _soumettre(client, "louismy@exemple.com")
    corps = client.get(EXPORT, headers=entete).content.decode("utf-8-sig")
    for secret in ("louismy@exemple.com", "37123456", "37 12 34 56", "Pétion", "2008"):
        assert secret not in corps


def test_filtres_comme_le_tableau_de_bord(client, entete, session_factory):
    a = _soumettre(client, "a@exemple.com")
    b = _soumettre(client, "b@exemple.com")
    c = _soumettre(client, "c@exemple.com")
    _decider(session_factory, b, **{LES_CINQ[0]: "rejete"})
    _decider(session_factory, c, **{p: "valide" for p in LES_CINQ})
    with session_factory() as db:
        db.query(CandidatureModel).filter_by(reference_dossier=a).one().deplacement_physique = True
        db.commit()

    def refs(**params):
        return [l[0] for l in _lire_csv(client.get(EXPORT, params=params, headers=entete))[1:]]

    assert refs() == [a, b, c]  # sans filtre : tout
    assert refs(statut="complet") == [c]
    assert refs(statut="action_requise") == [b]
    assert refs(deplacement_physique="false") == [b, c]
    assert refs(q=a.lower()) == [a]
    assert refs(statut="complet", deplacement_physique="true") == []  # aucun : en-tête seul
    assert _lire_csv(client.get(EXPORT, params={"statut": "complet"}, headers=entete))[1][4:6] == ["Complet", "5/5"]


def test_les_brouillons_ne_sont_pas_exportes(client, entete):
    from tests.integration.test_soumission_api import _dossier

    _dossier(client, email="brouillon@exemple.com")
    assert _lire_csv(client.get(EXPORT, headers=entete)) == [COLONNES]


def test_injection_de_formule_neutralisee(client, entete, session_factory):
    ref = _soumettre(client, "a@exemple.com")
    with session_factory() as db:
        candidat_id = db.query(CandidatureModel).filter_by(reference_dossier=ref).one().candidat_id
        candidat = db.get(CandidatModel, candidat_id)
        candidat.nom, candidat.prenom = '=HYPERLINK("http://evil.example")', "@SUM(A1)"
        db.commit()
    ligne = _lire_csv(client.get(EXPORT, headers=entete))[1]
    assert ligne[1] == "'=HYPERLINK(\"http://evil.example\")" and ligne[2] == "'@SUM(A1)"


@pytest.mark.parametrize("valeur, attendu", [("=1+1", "'=1+1"), ("+33", "'+33"), ("-2", "'-2"), ("@x", "'@x"), ("Jean", "Jean"), ("", "")])
def test_neutraliser(valeur, attendu):
    assert neutraliser(valeur) == attendu


def test_pdf_telechargeable(client, entete):
    _soumettre(client, "a@exemple.com", nom="Éloïse O'Brien", prenom="<b>Marie</b> & Co")  # saisie hostile : ne doit rien casser
    _soumettre(client, "b@exemple.com")
    reponse = client.get(EXPORT, params={"format": "pdf"}, headers=entete)
    assert reponse.status_code == 200
    assert reponse.headers["content-type"] == "application/pdf"
    assert re.fullmatch(r'attachment; filename="candidatures-\d{4}-\d{2}-\d{2}\.pdf"', reponse.headers["content-disposition"])
    assert reponse.content.startswith(b"%PDF-") and reponse.content.rstrip().endswith(b"%%EOF")


def test_pdf_sans_dossier_reste_un_pdf_valide(client, entete):
    reponse = client.get(EXPORT, params={"format": "pdf", "statut": "complet"}, headers=entete)
    assert reponse.status_code == 200 and reponse.content.startswith(b"%PDF-")


def test_pdf_de_nombreux_dossiers_sur_plusieurs_pages(entete):
    """Le tableau passe sur plusieurs pages (en-tête répété) sans erreur."""
    from backend.dal.export_pdf import generer_pdf

    lignes = [[f"CAN-2026-{n:04d}", f"Nom{n}", f"Prénom{n}", "Non", "À examiner", "0/5", "2026-10-27T09:00:00Z"] for n in range(1, 120)]
    pdf = generer_pdf("Candidatures", "tous les dossiers soumis", lignes)
    assert pdf.startswith(b"%PDF-") and pdf.count(b"/Type /Page\n") + pdf.count(b"/Type /Page ") >= 3


@pytest.mark.parametrize("params", [{"format": "xls"}, {"statut": "nimporte"}, {"format": "csv;rm"}])
def test_parametres_invalides(client, entete, params):
    assert client.get(EXPORT, params=params, headers=entete).status_code == 422


def test_l_export_est_journalise_sans_donnee_personnelle(client, entete, caplog):
    _soumettre(client, "louismy@exemple.com")
    with caplog.at_level(logging.INFO):
        client.get(EXPORT, params={"format": "csv"}, headers=entete)
    assert "Export csv de 1 dossier(s)" in caplog.text
    assert "louismy" not in caplog.text and "Louis" not in caplog.text


def test_export_n_est_pas_pris_pour_une_reference(client, entete):
    assert client.get(f"{LISTE}/export", headers=entete).headers["content-type"].startswith("text/csv")
    assert client.get(f"{LISTE}/CAN-2026-0001", headers=entete).status_code == 404
