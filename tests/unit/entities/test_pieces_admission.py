"""Tests unitaires de la liste unique des pièces d'admission (Couche Domain, ADR-008).
"""

from backend.entities.pieces_admission import ID_CURSUS_ADMISSION, pieces_admission


def test_cinq_pieces_obligatoires():
    pieces = pieces_admission()
    assert len(pieces) == 5
    assert all(p.est_obligatoire for p in pieces)


def test_liste_exacte_des_pieces():
    noms = [p.nom for p in pieces_admission()]
    assert noms == [
        "Acte de naissance ou extrait d'archives",
        "Certificat de fin d'études secondaires (Bac II)",
        "Relevé de notes officiel",
        "Deux photos d'identité récentes",
        "Pièce d'identité (CIN)",
    ]


def test_pieces_exclues():
    texte = " ".join(f"{p.nom} {p.description}" for p in pieces_admission()).lower()
    assert "bonne vie" not in texte
    assert "médical" not in texte
    assert "attestation" not in texte


def test_pieces_rattachees_au_cursus_d_admission():
    pieces = pieces_admission()
    assert ID_CURSUS_ADMISSION == "mpc"
    assert {p.cursus_id for p in pieces} == {"mpc"}
    assert len({p.id for p in pieces}) == 5


def test_taille_maximale_5_mo():
    assert all(p.taille_max_mo == 5 for p in pieces_admission())


def test_chaque_appel_retourne_une_liste_independante():
    a = pieces_admission()
    a.pop()
    assert len(pieces_admission()) == 5
