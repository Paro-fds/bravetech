"""SMS simulés (US-016) : messages courts, contenu utile, jamais bloquants."""

import uuid
from datetime import date, datetime, timezone

from backend.bll.notifier_sms import NotifierSmsUseCase, sms_confirmation, sms_decision
from backend.entities.candidat import Candidat
from backend.entities.candidature import Candidature
from backend.entities.decision_document import DecisionDocument
from backend.entities.sms_simule import LONGUEUR_MAX_SMS
from backend.ports.sms_sender import ISmsSender, MessageSms

URL = "https://dorfilus.ueh.edu.ht/suivi/CAN-2026-0042"


def _candidat() -> Candidat:
    return Candidat(
        id="c1", nom="Louis", prenom="Louismy", date_naissance=date(2007, 5, 1), sexe="M",
        telephone="+50937000000", email="louismy@exemple.com", departement="Sud", commune="Les Cayes",
        campagne=2026, created_at=datetime.now(timezone.utc),
    )


def _candidature() -> Candidature:
    return Candidature(id="d1", candidat_id="c1", created_at=datetime.now(timezone.utc), reference_dossier="CAN-2026-0042")


def _decision(statut: str) -> DecisionDocument:
    return DecisionDocument(
        id=str(uuid.uuid4()), document_id="doc", candidat_id="c1", document_requis_id="mpc-cin",
        statut=statut, motif="Photo floue" if statut == "rejete" else None, decide_par="u1",
        decide_le=datetime.now(timezone.utc),
    )


class EnvoiMemoire(ISmsSender):
    def __init__(self) -> None:
        self.envoyes: list[MessageSms] = []

    def envoyer(self, message: MessageSms) -> None:
        self.envoyes.append(message)


class EnvoiEnPanne(ISmsSender):
    def envoyer(self, message: MessageSms) -> None:
        raise ConnectionError("opérateur injoignable")


def test_la_confirmation_donne_la_reference_et_le_lien_au_numero_du_candidat():
    sms = sms_confirmation(_candidat(), _candidature(), URL)
    assert sms.destinataire == "+50937000000"
    assert "CAN-2026-0042" in sms.texte and URL in sms.texte
    assert len(sms.texte) <= LONGUEUR_MAX_SMS


def test_un_refus_annonce_la_piece_a_remplacer_sans_le_motif():
    sms = sms_decision(_candidat(), _candidature(), "Pièce d'identité (CIN)", "rejete", URL)
    assert "à remplacer" in sms.texte and "Pièce d'identité (CIN)" in sms.texte
    assert "Photo floue" not in sms.texte  # le motif est dans l'email et sur la page de suivi
    assert len(sms.texte) <= LONGUEUR_MAX_SMS


def test_un_texte_trop_long_est_coupe_a_160_caracteres():
    sms = sms_decision(_candidat(), _candidature(), "x" * 200, "valide", URL)
    assert len(sms.texte) == LONGUEUR_MAX_SMS and sms.texte.endswith("…")


def test_le_notificateur_envoie_confirmation_et_decisions():
    envoi = EnvoiMemoire()
    notifier = NotifierSmsUseCase(envoi, "https://dorfilus.ueh.edu.ht/")
    assert notifier.confirmation(_candidat(), _candidature()) is True
    assert notifier.decision(_candidat(), _candidature(), _decision("valide")) is True
    assert [("validée" in m.texte) for m in envoi.envoyes] == [False, True]
    assert envoi.envoyes[0].texte.count("//suivi") == 0  # pas de double barre oblique dans le lien


def test_une_panne_n_est_jamais_remontee(caplog):
    notifier = NotifierSmsUseCase(EnvoiEnPanne(), "https://dorfilus.ueh.edu.ht")
    assert notifier.decision(_candidat(), _candidature(), _decision("rejete")) is False
    assert "CAN-2026-0042" in caplog.text and "+50937000000" not in caplog.text
