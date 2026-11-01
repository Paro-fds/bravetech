"""Tests unitaires de la validation des fichiers téléversés (US-007) : taille, extension et magic bytes.
"""

import pytest

from backend.bll.validation_fichier import (
    OCTETS_PAR_MO,
    extensions_acceptees,
    nettoyer_nom_fichier,
    valider_fichier,
)
from backend.entities.erreurs import FichierInvalide, FichierTropVolumineux

from tests.unit.bll.fakes_documents import EXE, JPG, PDF, PNG

TOUS_FORMATS = "PDF, JPG, PNG"


@pytest.mark.parametrize(
    "nom, contenu, mime",
    [
        ("acte.pdf", PDF, "application/pdf"),
        ("photo.jpg", JPG, "image/jpeg"),
        ("photo.JPEG", JPG, "image/jpeg"),
        ("cin.png", PNG, "image/png"),
    ],
)
def test_fichier_valide(nom, contenu, mime):
    assert valider_fichier(nom, contenu, TOUS_FORMATS, 5).type_mime == mime


@pytest.mark.parametrize("nom", ["acte.pdf", "virus.exe.pdf", "photo.jpg", "image.png"])
def test_executable_deguise_est_refuse_quelle_que_soit_l_extension(nom):
    with pytest.raises(FichierInvalide):
        valider_fichier(nom, EXE, TOUS_FORMATS, 5)


def test_extension_ne_correspondant_pas_au_contenu():
    with pytest.raises(FichierInvalide, match="ne correspond pas"):
        valider_fichier("acte.pdf", PNG, TOUS_FORMATS, 5)


@pytest.mark.parametrize("nom", ["script.exe", "page.html", "image.gif", "sans_extension", ""])
def test_extension_non_acceptee(nom):
    with pytest.raises(FichierInvalide, match="Format non accepté"):
        valider_fichier(nom, PDF, TOUS_FORMATS, 5)


def test_format_restreint_par_piece():
    # Les photos d'identité n'acceptent pas le PDF
    with pytest.raises(FichierInvalide):
        valider_fichier("photos.pdf", PDF, "JPG, PNG", 5)
    assert valider_fichier("photos.png", PNG, "JPG, PNG", 5).extension == "png"


def test_fichier_vide():
    with pytest.raises(FichierInvalide, match="vide"):
        valider_fichier("acte.pdf", b"", TOUS_FORMATS, 5)


def test_taille_limite_exacte_acceptee():
    contenu = PDF + b"0" * (5 * OCTETS_PAR_MO - len(PDF))
    assert len(contenu) == 5 * OCTETS_PAR_MO
    valider_fichier("acte.pdf", contenu, TOUS_FORMATS, 5)


def test_fichier_trop_volumineux():
    contenu = PDF + b"0" * (5 * OCTETS_PAR_MO)
    with pytest.raises(FichierTropVolumineux) as exc:
        valider_fichier("acte.pdf", contenu, TOUS_FORMATS, 5)
    assert exc.value.taille_max_mo == 5


def test_extensions_acceptees():
    assert extensions_acceptees("PDF, JPG, PNG") == {"pdf", "jpg", "jpeg", "png"}
    assert extensions_acceptees("JPG, PNG") == {"jpg", "jpeg", "png"}
    assert extensions_acceptees("PDF") == {"pdf"}


@pytest.mark.parametrize(
    "brut, propre",
    [
        ("../../etc/passwd", "passwd"),
        ("C:\\Users\\moi\\acte.pdf", "acte.pdf"),
        ("acte\x00.pdf", "acte.pdf"),
        ("", "document"),
        (None, "document"),
        ("a" * 400 + ".pdf", ("a" * 400 + ".pdf")[:255]),
    ],
)
def test_nettoyage_du_nom(brut, propre):
    assert nettoyer_nom_fichier(brut) == propre
