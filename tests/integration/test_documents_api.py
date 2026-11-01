"""Tests d'intégration du dépôt des pièces justificatives (US-007) : base SQLite en mémoire, stockage temporaire.
"""

import pytest

from backend.dal.models import DocumentSoumisModel

from tests.integration.test_candidatures_api import SAISIE, URL
from tests.unit.bll.fakes_documents import EXE, JPG, PDF, PNG

ACTE = "mpc-acte-naissance"
BAC = "mpc-diplome-bac"
RELEVE = "mpc-releve-notes-bac"
PHOTOS = "mpc-photos-identite"
CIN = "mpc-cin"
LES_CINQ = [ACTE, BAC, RELEVE, PHOTOS, CIN]


def _dossier_pret(client, email="louismy@exemple.com", paye=True):
    """Crée un brouillon jusqu'au paiement simulé (préalable au dépôt des pièces)."""
    cid = client.post(URL, json={**SAISIE, "email": email}).json()["candidature_id"]
    client.put(f"{URL}/{cid}/deplacement-physique", json={"deplacement_physique": False})
    if paye:
        client.post(f"{URL}/{cid}/paiement", json={"methode": "MONCASH", "numero_telephone": "37123456"})
    return cid


def _envoyer(client, cid, piece, nom, contenu, type_mime="application/octet-stream"):
    return client.post(f"{URL}/{cid}/documents/{piece}", files={"fichier": (nom, contenu, type_mime)})


def _fichiers_stockes(dossier):
    return [p for p in dossier.rglob("*") if p.is_file()] if dossier.exists() else []


def test_liste_initiale_des_cinq_pieces(client):
    cid = _dossier_pret(client)
    reponse = client.get(f"{URL}/{cid}/documents")
    assert reponse.status_code == 200
    pieces = reponse.json()
    assert [p["id"] for p in pieces] == LES_CINQ
    assert {p["statut"] for p in pieces} == {"manquant"}
    assert all(p["est_obligatoire"] for p in pieces)
    assert all(p["nom_fichier"] is None for p in pieces)


def test_depot_valide(client, session_factory, dossier_uploads):
    cid = _dossier_pret(client)
    reponse = _envoyer(client, cid, ACTE, "acte_naissance.pdf", PDF)
    assert reponse.status_code == 200
    data = reponse.json()
    assert data["id"] == ACTE
    assert data["statut"] == "en_attente"
    assert data["nom_fichier"] == "acte_naissance.pdf"
    assert data["taille_octets"] == len(PDF)
    assert "cle_stockage" not in data  # la clé interne n'est jamais exposée

    fichiers = _fichiers_stockes(dossier_uploads)
    assert len(fichiers) == 1 and fichiers[0].read_bytes() == PDF
    with session_factory() as db:
        assert db.query(DocumentSoumisModel).count() == 1

    statuts = {p["id"]: p["statut"] for p in client.get(f"{URL}/{cid}/documents").json()}
    assert statuts[ACTE] == "en_attente" and statuts[BAC] == "manquant"


def test_remplacement_sans_doublon(client, session_factory, dossier_uploads):
    cid = _dossier_pret(client)
    _envoyer(client, cid, ACTE, "acte.pdf", PDF)
    reponse = _envoyer(client, cid, ACTE, "acte_v2.png", PNG)
    assert reponse.status_code == 200 and reponse.json()["nom_fichier"] == "acte_v2.png"

    with session_factory() as db:
        assert db.query(DocumentSoumisModel).count() == 1  # upsert : une seule ligne
    fichiers = _fichiers_stockes(dossier_uploads)
    assert len(fichiers) == 1 and fichiers[0].read_bytes() == PNG  # l'ancien fichier est supprimé


def test_les_cinq_pieces(client):
    cid = _dossier_pret(client)
    contenus = {ACTE: ("a.pdf", PDF), BAC: ("b.jpg", JPG), RELEVE: ("r.pdf", PDF), PHOTOS: ("p.png", PNG), CIN: ("c.jpg", JPG)}
    for piece, (nom, contenu) in contenus.items():
        assert _envoyer(client, cid, piece, nom, contenu).status_code == 200
    assert {p["statut"] for p in client.get(f"{URL}/{cid}/documents").json()} == {"en_attente"}


def test_executable_renomme_en_pdf_refuse(client, session_factory, dossier_uploads):
    cid = _dossier_pret(client)
    reponse = _envoyer(client, cid, ACTE, "acte.pdf", EXE, "application/pdf")  # le client ment sur le type
    assert reponse.status_code == 422
    assert "fichier" in reponse.json()["detail"]["erreurs"]
    assert _fichiers_stockes(dossier_uploads) == []
    with session_factory() as db:
        assert db.query(DocumentSoumisModel).count() == 0


@pytest.mark.parametrize("nom", ["virus.exe", "page.html", "image.gif"])
def test_extension_refusee(client, nom):
    cid = _dossier_pret(client)
    assert _envoyer(client, cid, ACTE, nom, PDF).status_code == 422


def test_extension_ne_correspond_pas_au_contenu(client):
    cid = _dossier_pret(client)
    assert _envoyer(client, cid, ACTE, "acte.pdf", PNG).status_code == 422


def test_photos_refusent_le_pdf(client):
    cid = _dossier_pret(client)
    assert _envoyer(client, cid, PHOTOS, "photos.pdf", PDF).status_code == 422
    assert _envoyer(client, cid, PHOTOS, "photos.jpg", JPG).status_code == 200


def test_fichier_vide(client):
    cid = _dossier_pret(client)
    assert _envoyer(client, cid, ACTE, "acte.pdf", b"").status_code == 422


def test_fichier_de_plus_de_5_mo(client, dossier_uploads):
    cid = _dossier_pret(client)
    reponse = _envoyer(client, cid, ACTE, "gros.pdf", PDF + b"0" * (5 * 1024 * 1024))
    assert reponse.status_code == 413
    assert "5 Mo" in reponse.json()["detail"]
    assert _fichiers_stockes(dossier_uploads) == []


def test_fichier_de_5_mo_exactement_accepte(client):
    cid = _dossier_pret(client)
    contenu = PDF + b"0" * (5 * 1024 * 1024 - len(PDF))
    assert _envoyer(client, cid, ACTE, "limite.pdf", contenu).status_code == 200


def test_depot_refuse_avant_le_paiement(client):
    cid = _dossier_pret(client, paye=False)
    assert _envoyer(client, cid, ACTE, "acte.pdf", PDF).status_code == 409


def test_piece_inconnue(client):
    cid = _dossier_pret(client)
    for piece in ["mpc-bonne-vie-et-moeurs", "mpc-certificat-medical", "..%2F..%2Fetc%2Fpasswd"]:
        assert _envoyer(client, cid, piece, "x.pdf", PDF).status_code == 404


def test_candidature_inconnue(client):
    assert _envoyer(client, "inconnu", ACTE, "acte.pdf", PDF).status_code == 404
    assert client.get(f"{URL}/inconnu/documents").status_code == 404


def test_requete_sans_fichier(client):
    cid = _dossier_pret(client)
    assert client.post(f"{URL}/{cid}/documents/{ACTE}").status_code == 422


def test_nom_de_fichier_dangereux_est_nettoye(client, dossier_uploads):
    cid = _dossier_pret(client)
    reponse = _envoyer(client, cid, ACTE, "../../../etc/passwd.pdf", PDF)
    assert reponse.status_code == 200
    assert reponse.json()["nom_fichier"] == "passwd.pdf"
    # Le fichier reste bien sous le dossier de stockage, avec un nom généré par le serveur
    for chemin in _fichiers_stockes(dossier_uploads):
        assert dossier_uploads.resolve() in chemin.resolve().parents


def test_dossiers_isoles_entre_candidats(client):
    cid_a = _dossier_pret(client, email="a@exemple.com")
    cid_b = _dossier_pret(client, email="b@exemple.com")
    _envoyer(client, cid_a, ACTE, "acte_a.pdf", PDF)
    pieces_b = {p["id"]: p["statut"] for p in client.get(f"{URL}/{cid_b}/documents").json()}
    assert pieces_b[ACTE] == "manquant"


def test_limite_de_debit_10_envois_par_minute(client):
    cid = _dossier_pret(client)
    codes = [_envoyer(client, cid, ACTE, "acte.pdf", PDF).status_code for _ in range(11)]
    assert codes[:10] == [200] * 10
    assert codes[10] == 429
    reponse = _envoyer(client, cid, ACTE, "acte.pdf", PDF)
    assert reponse.status_code == 429 and reponse.headers["retry-after"] == "60"


def test_limite_de_debit_par_adresse(client):
    cid = _dossier_pret(client)
    for _ in range(10):
        _envoyer(client, cid, ACTE, "acte.pdf", PDF)
    assert _envoyer(client, cid, ACTE, "acte.pdf", PDF).status_code == 429
    autre = client.post(
        f"{URL}/{cid}/documents/{ACTE}",
        files={"fichier": ("acte.pdf", PDF, "application/pdf")},
        headers={"X-Forwarded-For": "203.0.113.7"},
    )
    assert autre.status_code == 200
