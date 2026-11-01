"""Tests unitaires de la décision sur une pièce (US-013) : audit, motif, caractère définitif, atomicité.
"""

from datetime import date, datetime, timezone

import pytest

from backend.bll.decider_document import MOTIF_MAX, DeciderDocumentUseCase
from backend.entities.candidat import Candidat
from backend.entities.candidature import STATUT_BROUILLON, STATUT_SOUMISE, Candidature
from backend.entities.document_soumis import STATUT_EN_ATTENTE, STATUT_REJETE, STATUT_VALIDE, DocumentSoumis
from backend.entities.erreurs import DocumentDejaDecide, DocumentIntrouvable, InformationsInvalides
from backend.entities.utilisateur import ROLE_AGENT, Utilisateur

from tests.unit.bll.fakes import FakeCandidatureRepository
from tests.unit.bll.fakes_documents import FakeDocumentRepository

MAINTENANT = datetime(2026, 10, 27, 9, 0, tzinfo=timezone.utc)
AGENT = Utilisateur("agent-1", "agent@fds.ht", "hash", ROLE_AGENT)


def _monde(statut_candidature=STATUT_SOUMISE, statut_document=STATUT_EN_ATTENTE):
    candidats, documents = FakeCandidatureRepository(), FakeDocumentRepository()
    candidats.creer(
        Candidat("c1", "Louis", "Louismy", date(2008, 5, 14), "M", "+50937123456", "l@exemple.com", "Ouest", "Pétion-Ville", 2026, MAINTENANT),
        Candidature("k1", "c1", MAINTENANT, statut=statut_candidature, reference_dossier="CAN-2026-0001", soumise_le=MAINTENANT),
    )
    documents.enregistrer(DocumentSoumis(
        "d1", "c1", "mpc-cin", "cin.pdf", "k1/cin.pdf", "application/pdf", 40, MAINTENANT, statut_validation=statut_document
    ))
    return candidats, documents


def test_validation_enregistre_l_auteur_et_la_date():
    candidats, documents = _monde()
    document, decision = DeciderDocumentUseCase(candidats, documents).executer("d1", STATUT_VALIDE, "ignoré", AGENT)
    assert document.statut_validation == STATUT_VALIDE
    assert document.valide_par == "agent-1" and document.date_validation is not None
    assert document.date_validation.tzinfo is not None  # UTC
    assert document.motif_rejet is None  # une validation n'a pas de motif
    stocke = documents.obtenir("c1", "mpc-cin")
    assert stocke.valide_par == "agent-1" and stocke.statut_validation == STATUT_VALIDE
    assert [(d.statut, d.decide_par) for d in documents.lister_decisions("c1")] == [(STATUT_VALIDE, "agent-1")]
    assert decision.decide_le == document.date_validation


def test_refus_avec_motif():
    candidats, documents = _monde()
    document, _ = DeciderDocumentUseCase(candidats, documents).executer("d1", STATUT_REJETE, "  Document illisible  ", AGENT)
    assert document.statut_validation == STATUT_REJETE and document.motif_rejet == "Document illisible"
    assert documents.lister_decisions("c1")[0].motif == "Document illisible"


@pytest.mark.parametrize("motif", [None, "", "   ", "non", "x" * (MOTIF_MAX + 1)])
def test_refus_sans_motif_valable_refuse_et_rien_n_est_ecrit(motif):
    candidats, documents = _monde()
    with pytest.raises(InformationsInvalides) as erreur:
        DeciderDocumentUseCase(candidats, documents).executer("d1", STATUT_REJETE, motif, AGENT)
    assert "motif" in erreur.value.erreurs
    assert documents.obtenir("c1", "mpc-cin").statut_validation == STATUT_EN_ATTENTE and documents.decisions == []


def test_statut_inconnu_refuse():
    candidats, documents = _monde()
    with pytest.raises(InformationsInvalides):
        DeciderDocumentUseCase(candidats, documents).executer("d1", "en_attente", None, AGENT)


@pytest.mark.parametrize("deja", [STATUT_VALIDE, STATUT_REJETE])
def test_une_decision_est_definitive(deja):
    candidats, documents = _monde(statut_document=deja)
    with pytest.raises(DocumentDejaDecide):
        DeciderDocumentUseCase(candidats, documents).executer("d1", STATUT_VALIDE, None, AGENT)
    assert documents.decisions == []


def test_document_inconnu_ou_dossier_non_soumis():
    candidats, documents = _monde()
    with pytest.raises(DocumentIntrouvable):
        DeciderDocumentUseCase(candidats, documents).executer("inconnu", STATUT_VALIDE, None, AGENT)
    candidats, documents = _monde(statut_candidature=STATUT_BROUILLON)
    with pytest.raises(DocumentIntrouvable):
        DeciderDocumentUseCase(candidats, documents).executer("d1", STATUT_VALIDE, None, AGENT)
