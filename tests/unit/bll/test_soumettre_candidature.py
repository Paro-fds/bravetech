"""Tests unitaires de la soumission définitive et de l'email de confirmation (US-008), avec des dépôts en mémoire.
"""

import logging
import re

import pytest

from backend.bll.definir_deplacement_physique import DefinirDeplacementPhysiqueUseCase
from backend.bll.enregistrer_informations import EnregistrerInformationsUseCase
from backend.bll.messages_email import message_confirmation
from backend.bll.simuler_paiement import SimulerPaiementUseCase
from backend.bll.soumettre_candidature import (
    NotifierConfirmationUseCase,
    SoumettreCandidatureUseCase,
    formater_reference,
)
from backend.bll.televerser_document import TeleverserDocumentUseCase
from backend.entities.candidature import STATUT_BROUILLON, STATUT_SOUMISE
from backend.entities.erreurs import (
    CandidatureIntrouvable,
    DossierIncomplet,
    ErreurMetier,
    ReferenceDejaAttribuee,
)
from backend.entities.pieces_admission import pieces_admission
from backend.ports.email_sender import IEmailSender, MessageEmail

from tests.unit.bll.fakes import FakeCandidatureRepository, donnees_valides
from tests.unit.bll.fakes_documents import PDF, FakeDocumentRepository, FakeStockage


class EmailEnregistreur(IEmailSender):
    def __init__(self) -> None:
        self.messages: list[MessageEmail] = []

    def envoyer(self, message: MessageEmail) -> None:
        self.messages.append(message)


class EmailEnPanne(IEmailSender):
    def envoyer(self, message: MessageEmail) -> None:
        raise ConnectionError("Resend indisponible : 192.0.2.1 jean@secret.com")


@pytest.fixture
def repo():
    return FakeCandidatureRepository()


@pytest.fixture
def docs():
    return FakeDocumentRepository()


def _dossier_complet(repo, docs, email="louismy@exemple.com", pieces=True, paiement=True, deplacement=True):
    candidat, candidature = EnregistrerInformationsUseCase(repo).executer(donnees_valides(email=email))
    if deplacement:
        DefinirDeplacementPhysiqueUseCase(repo).executer(candidature.id, False)
    if paiement:
        SimulerPaiementUseCase(repo).executer(candidature.id, "MONCASH", "37123456")
    if pieces:
        televerser = TeleverserDocumentUseCase(repo, docs, FakeStockage())
        for piece in pieces_admission():
            extension = "jpg" if piece.id.endswith("photos-identite") else "pdf"
            contenu = PDF if extension == "pdf" else b"\xff\xd8\xff\xe0\x00\x10JFIF\x00" + b"\x00" * 20
            televerser.executer(candidature.id, piece.id, f"{piece.id}.{extension}", contenu)
    return candidat, repo.obtenir_candidature(candidature.id)


def test_format_de_la_reference():
    assert formater_reference(2026, 1) == "CAN-2026-0001"
    assert formater_reference(2026, 89) == "CAN-2026-0089"
    assert formater_reference(2026, 12345) == "CAN-2026-12345"


def test_soumission_attribue_la_reference_et_verrouille(repo, docs):
    candidat, candidature = _dossier_complet(repo, docs)
    candidat, resultat, nouvelle = SoumettreCandidatureUseCase(repo, docs).executer(candidature.id)
    assert nouvelle is True
    assert re.fullmatch(r"CAN-2026-\d{4}", resultat.reference_dossier)
    assert resultat.statut == STATUT_SOUMISE
    assert resultat.soumise_le is not None and resultat.soumise_le.tzinfo is not None  # UTC
    assert repo.candidatures[candidature.id].reference_dossier == resultat.reference_dossier


def test_references_sequentielles_et_uniques(repo, docs):
    refs = []
    for i in range(3):
        _, candidature = _dossier_complet(repo, docs, email=f"c{i}@exemple.com")
        refs.append(SoumettreCandidatureUseCase(repo, docs).executer(candidature.id)[1].reference_dossier)
    assert refs == ["CAN-2026-0001", "CAN-2026-0002", "CAN-2026-0003"]


def test_soumission_idempotente(repo, docs):
    _, candidature = _dossier_complet(repo, docs)
    cas = SoumettreCandidatureUseCase(repo, docs)
    _, premiere, nouvelle_1 = cas.executer(candidature.id)
    _, seconde, nouvelle_2 = cas.executer(candidature.id)
    assert (nouvelle_1, nouvelle_2) == (True, False)  # pas de nouvelle référence, donc pas de nouvel email
    assert seconde.reference_dossier == premiere.reference_dossier
    assert seconde.soumise_le == premiere.soumise_le


def test_dossier_sans_pieces_refuse(repo, docs):
    _, candidature = _dossier_complet(repo, docs, pieces=False)
    with pytest.raises(DossierIncomplet) as exc:
        SoumettreCandidatureUseCase(repo, docs).executer(candidature.id)
    assert len(exc.value.manques) == 5
    assert repo.candidatures[candidature.id].statut == STATUT_BROUILLON
    assert repo.candidatures[candidature.id].reference_dossier is None


def test_dossier_avec_une_piece_manquante(repo, docs):
    _, candidature = _dossier_complet(repo, docs)
    docs.documents.pop(next(iter(docs.documents)))
    with pytest.raises(DossierIncomplet) as exc:
        SoumettreCandidatureUseCase(repo, docs).executer(candidature.id)
    assert len(exc.value.manques) == 1


def test_dossier_sans_paiement_ni_deplacement(repo, docs):
    _, candidature = _dossier_complet(repo, docs, pieces=False, paiement=False, deplacement=False)
    with pytest.raises(DossierIncomplet) as exc:
        SoumettreCandidatureUseCase(repo, docs).executer(candidature.id)
    assert "Paiement simulé des frais de dossier" in exc.value.manques
    assert any("déplacement" in m for m in exc.value.manques)


def test_candidature_introuvable(repo, docs):
    with pytest.raises(CandidatureIntrouvable):
        SoumettreCandidatureUseCase(repo, docs).executer("inconnu")


def test_collision_de_reference_retire_un_numero(repo, docs):
    """Deux soumissions simultanées : la base refuse un doublon, on retire un numéro."""
    _, candidature = _dossier_complet(repo, docs)
    original = repo.enregistrer_candidature
    appels = []

    def enregistrer_avec_collision(c):
        appels.append(c.reference_dossier)
        if len(appels) == 1:
            raise ReferenceDejaAttribuee()
        original(c)

    repo.enregistrer_candidature = enregistrer_avec_collision
    _, resultat, _ = SoumettreCandidatureUseCase(repo, docs).executer(candidature.id)
    assert len(appels) == 2 and resultat.statut == STATUT_SOUMISE


def test_abandon_apres_trop_de_collisions(repo, docs):
    _, candidature = _dossier_complet(repo, docs)

    def toujours_en_conflit(_):
        raise ReferenceDejaAttribuee()

    repo.enregistrer_candidature = toujours_en_conflit
    with pytest.raises(ErreurMetier):
        SoumettreCandidatureUseCase(repo, docs).executer(candidature.id)


# --- email : jamais bloquant ---------------------------------------------------------------------

def _soumis(repo, docs):
    _, candidature = _dossier_complet(repo, docs)
    return SoumettreCandidatureUseCase(repo, docs).executer(candidature.id)[:2]


def test_email_de_confirmation(repo, docs):
    candidat, candidature = _soumis(repo, docs)
    envoyeur = EmailEnregistreur()
    assert NotifierConfirmationUseCase(envoyeur, "https://portail.exemple.ht/").executer(candidat, candidature) is True

    (message,) = envoyeur.messages
    assert message.destinataire == "louismy@exemple.com"
    assert candidature.reference_dossier in message.sujet
    assert candidature.reference_dossier in message.texte
    assert f"https://portail.exemple.ht/suivi/{candidature.reference_dossier}" in message.texte
    assert "simulation" in message.texte
    assert "Premier cycle MPC" in message.texte


def test_echec_email_ne_leve_jamais_et_ne_touche_pas_au_dossier(repo, docs, caplog):
    candidat, candidature = _soumis(repo, docs)
    with caplog.at_level(logging.ERROR, logger="fds.candidature"):
        envoye = NotifierConfirmationUseCase(EmailEnPanne(), "https://portail.exemple.ht").executer(candidat, candidature)
    assert envoye is False  # aucune exception
    assert repo.candidatures[candidature.id].statut == STATUT_SOUMISE  # la candidature reste enregistrée
    assert repo.candidatures[candidature.id].reference_dossier == candidature.reference_dossier

    journal = caplog.text
    assert candidature.reference_dossier in journal and "ConnectionError" in journal
    # Le journal ne contient ni le message d'erreur brut (adresse IP, email) ni l'adresse du candidat
    assert "192.0.2.1" not in journal and "jean@secret.com" not in journal and candidat.email not in journal


@pytest.mark.parametrize("exception", [RuntimeError("x"), TimeoutError(), OSError("réseau"), ValueError("y")])
def test_toute_exception_d_envoi_est_absorbee(repo, docs, exception):
    class Panne(IEmailSender):
        def envoyer(self, message):
            raise exception

    candidat, candidature = _soumis(repo, docs)
    assert NotifierConfirmationUseCase(Panne(), "http://x").executer(candidat, candidature) is False


def test_le_html_echappe_les_saisies_du_candidat(repo, docs):
    candidat, candidature = _soumis(repo, docs)
    candidat.prenom = '<script>alert("x")</script>'
    message = message_confirmation(candidat, candidature, "https://portail.exemple.ht/suivi/CAN-2026-0001")
    assert "<script>" not in message.html
    assert "&lt;script&gt;" in message.html
