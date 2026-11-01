"""Tests unitaires du cas d'utilisation « téléverser une pièce » (US-007), avec des dépôts en mémoire.
"""

import pytest

from backend.bll.definir_deplacement_physique import DefinirDeplacementPhysiqueUseCase
from backend.bll.enregistrer_informations import EnregistrerInformationsUseCase
from backend.bll.simuler_paiement import SimulerPaiementUseCase
from backend.bll.televerser_document import ListerPiecesDossierUseCase, TeleverserDocumentUseCase
from backend.entities.candidature import STATUT_SOUMISE
from backend.entities.document_soumis import STATUT_EN_ATTENTE, STATUT_MANQUANT, STATUT_VALIDE
from backend.entities.erreurs import (
    CandidatureDejaSoumise,
    CandidatureIntrouvable,
    DocumentDejaValide,
    DocumentRequisInconnu,
    EtapePrecedenteIncomplete,
    FichierInvalide,
    FichierTropVolumineux,
)
from backend.entities.pieces_admission import pieces_admission

from tests.unit.bll.fakes import FakeCandidatureRepository, donnees_valides
from tests.unit.bll.fakes_documents import EXE, JPG, PDF, PNG, FakeDocumentRepository, FakeStockage

ACTE = "mpc-acte-naissance"
PHOTOS = "mpc-photos-identite"


@pytest.fixture
def ctx():
    repo, docs, stock = FakeCandidatureRepository(), FakeDocumentRepository(), FakeStockage()
    candidat, candidature = EnregistrerInformationsUseCase(repo).executer(donnees_valides())
    DefinirDeplacementPhysiqueUseCase(repo).executer(candidature.id, False)
    SimulerPaiementUseCase(repo).executer(candidature.id, "MONCASH", "37123456")
    return repo, docs, stock, candidat, repo.obtenir_candidature(candidature.id)


def _cas(ctx):
    repo, docs, stock, *_ = ctx
    return TeleverserDocumentUseCase(repo, docs, stock)


def test_depot_valide(ctx):
    repo, docs, stock, candidat, candidature = ctx
    document = _cas(ctx).executer(candidature.id, ACTE, "acte.pdf", PDF)
    assert document.statut_validation == STATUT_EN_ATTENTE
    assert document.type_mime == "application/pdf"
    assert document.taille_octets == len(PDF)
    assert document.cle_stockage.startswith(f"{candidature.id}/{ACTE}-")
    assert stock.lire(document.cle_stockage) == PDF
    assert docs.obtenir(candidat.id, ACTE).nom_fichier == "acte.pdf"


def test_remplacement_est_un_upsert_sans_doublon(ctx):
    repo, docs, stock, candidat, candidature = ctx
    premier = _cas(ctx).executer(candidature.id, ACTE, "acte.pdf", PDF)
    second = _cas(ctx).executer(candidature.id, ACTE, "acte_v2.png", PNG)

    assert len(docs.lister(candidat.id)) == 1  # jamais deux lignes pour la même pièce
    assert second.id == premier.id  # même document logique
    assert second.nom_fichier == "acte_v2.png"
    assert stock.lire(second.cle_stockage) == PNG
    assert stock.lire(premier.cle_stockage) is None  # l'ancien fichier est supprimé
    assert len(stock.fichiers) == 1


def test_document_valide_non_remplacable(ctx):
    repo, docs, stock, candidat, candidature = ctx
    document = _cas(ctx).executer(candidature.id, ACTE, "acte.pdf", PDF)
    document.statut_validation = STATUT_VALIDE
    docs.enregistrer(document)
    with pytest.raises(DocumentDejaValide):
        _cas(ctx).executer(candidature.id, ACTE, "acte2.pdf", PDF)
    assert stock.lire(document.cle_stockage) == PDF


def test_fichier_refuse_ne_stocke_rien(ctx):
    repo, docs, stock, candidat, candidature = ctx
    for nom, contenu in [("acte.pdf", EXE), ("acte.exe", PDF), ("acte.pdf", b"")]:
        with pytest.raises(FichierInvalide):
            _cas(ctx).executer(candidature.id, ACTE, nom, contenu)
    assert stock.fichiers == {} and docs.documents == {}


def test_fichier_trop_volumineux(ctx):
    _, docs, stock, _, candidature = ctx
    with pytest.raises(FichierTropVolumineux):
        _cas(ctx).executer(candidature.id, ACTE, "acte.pdf", PDF + b"0" * (5 * 1024 * 1024))
    assert stock.fichiers == {}


def test_photos_refusent_le_pdf(ctx):
    _, _, _, _, candidature = ctx
    with pytest.raises(FichierInvalide):
        _cas(ctx).executer(candidature.id, PHOTOS, "photos.pdf", PDF)
    _cas(ctx).executer(candidature.id, PHOTOS, "photos.jpg", JPG)


def test_piece_inconnue(ctx):
    _, _, _, _, candidature = ctx
    with pytest.raises(DocumentRequisInconnu):
        _cas(ctx).executer(candidature.id, "mpc-bonne-vie-et-moeurs", "x.pdf", PDF)
    with pytest.raises(DocumentRequisInconnu):
        _cas(ctx).executer(candidature.id, "../../etc/passwd", "x.pdf", PDF)


def test_candidature_introuvable(ctx):
    with pytest.raises(CandidatureIntrouvable):
        _cas(ctx).executer("inconnu", ACTE, "acte.pdf", PDF)


def test_exige_le_paiement_simule():
    repo, docs, stock = FakeCandidatureRepository(), FakeDocumentRepository(), FakeStockage()
    _, candidature = EnregistrerInformationsUseCase(repo).executer(donnees_valides())
    with pytest.raises(EtapePrecedenteIncomplete):
        TeleverserDocumentUseCase(repo, docs, stock).executer(candidature.id, ACTE, "acte.pdf", PDF)


def test_dossier_soumis_verrouille(ctx):
    repo, _, _, _, candidature = ctx
    candidature.statut = STATUT_SOUMISE
    repo.enregistrer_candidature(candidature)
    with pytest.raises(CandidatureDejaSoumise):
        _cas(ctx).executer(candidature.id, ACTE, "acte.pdf", PDF)


def test_echec_de_la_base_ne_laisse_pas_de_fichier_orphelin(ctx):
    repo, docs, stock, _, candidature = ctx

    def _echec(_):
        raise RuntimeError("base indisponible")

    docs.enregistrer = _echec
    with pytest.raises(RuntimeError):
        _cas(ctx).executer(candidature.id, ACTE, "acte.pdf", PDF)
    assert stock.fichiers == {}


def test_liste_des_pieces(ctx):
    repo, docs, stock, candidat, candidature = ctx
    liste = ListerPiecesDossierUseCase(repo, docs)
    avant = liste.executer(candidature.id)
    assert [p.piece.id for p in avant] == [p.id for p in pieces_admission()]
    assert {p.statut for p in avant} == {STATUT_MANQUANT}

    _cas(ctx).executer(candidature.id, ACTE, "acte.pdf", PDF)
    apres = {p.piece.id: p.statut for p in liste.executer(candidature.id)}
    assert apres[ACTE] == STATUT_EN_ATTENTE
    assert sum(1 for s in apres.values() if s == STATUT_MANQUANT) == 4


def test_liste_candidature_introuvable(ctx):
    repo, docs, *_ = ctx
    with pytest.raises(CandidatureIntrouvable):
        ListerPiecesDossierUseCase(repo, docs).executer("inconnu")
