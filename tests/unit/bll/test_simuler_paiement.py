"""Tests unitaires du cas d'utilisation « simuler le paiement » (US-006), avec un dépôt en mémoire.
"""

import re

import pytest

from backend.bll.definir_deplacement_physique import DefinirDeplacementPhysiqueUseCase
from backend.bll.enregistrer_informations import EnregistrerInformationsUseCase
from backend.bll.simuler_paiement import SimulerPaiementUseCase
from backend.entities.candidature import (
    FRAIS_DOSSIER_HTG,
    STATUT_PAIEMENT_ECHOUE,
    STATUT_PAIEMENT_EN_ATTENTE,
    STATUT_PAIEMENT_REFUSE,
    STATUT_PAIEMENT_SIMULE,
    STATUT_SOUMISE,
)
from backend.entities.erreurs import (
    CandidatureDejaSoumise,
    CandidatureIntrouvable,
    ErreurMetier,
    EtapePrecedenteIncomplete,
    InformationsInvalides,
    PaiementEchoue,
    PaiementRefuse,
)

from tests.unit.bll.fakes import FakeCandidatureRepository, donnees_valides


@pytest.fixture
def repo():
    return FakeCandidatureRepository()


def _candidature(repo, deplacement=False, **surcharges):
    _, candidature = EnregistrerInformationsUseCase(repo).executer(donnees_valides(**surcharges))
    if deplacement is not None:
        DefinirDeplacementPhysiqueUseCase(repo).executer(candidature.id, deplacement)
    return candidature


def test_frais_de_dossier():
    assert FRAIS_DOSSIER_HTG == 500


@pytest.mark.parametrize("methode, attendu", [("moncash", "MONCASH"), ("NATCASH", "NATCASH"), (" MonCash ", "MONCASH")])
def test_paiement_simule(repo, methode, attendu):
    candidature = _candidature(repo)
    resultat = SimulerPaiementUseCase(repo).executer(candidature.id, methode, "37 12 34 56")
    assert resultat.statut_paiement == STATUT_PAIEMENT_SIMULE == "SIMULE_PAYE"
    assert resultat.methode_paiement == attendu
    assert resultat.numero_paiement == "+50937123456"
    assert re.fullmatch(r"PAY-SIM-2026-\d{4}", resultat.reference_paiement)
    assert repo.candidatures[candidature.id].reference_paiement == resultat.reference_paiement


def test_reference_formatee_sur_quatre_chiffres(repo):
    candidature = _candidature(repo)
    resultat = SimulerPaiementUseCase(repo, generer_numero=lambda: 7).executer(candidature.id, "MONCASH", "37123456")
    assert resultat.reference_paiement == "PAY-SIM-2026-0007"


def test_references_uniques_meme_en_cas_de_collision(repo):
    premiere = _candidature(repo, email="a@exemple.com")
    seconde = _candidature(repo, email="b@exemple.com")
    tirages = iter([412, 412, 413])
    cas = SimulerPaiementUseCase(repo, generer_numero=lambda: next(tirages))
    ref_a = cas.executer(premiere.id, "MONCASH", "37123456").reference_paiement
    ref_b = cas.executer(seconde.id, "NATCASH", "37123457").reference_paiement
    assert (ref_a, ref_b) == ("PAY-SIM-2026-0412", "PAY-SIM-2026-0413")


def test_impossible_de_generer_une_reference(repo):
    premiere = _candidature(repo, email="a@exemple.com")
    seconde = _candidature(repo, email="b@exemple.com")
    cas = SimulerPaiementUseCase(repo, generer_numero=lambda: 1)
    cas.executer(premiere.id, "MONCASH", "37123456")
    with pytest.raises(ErreurMetier):
        cas.executer(seconde.id, "MONCASH", "37123457")


def test_double_envoi_ne_cree_pas_un_second_paiement(repo):
    candidature = _candidature(repo)
    cas = SimulerPaiementUseCase(repo)
    premier = cas.executer(candidature.id, "MONCASH", "37123456")
    second = cas.executer(candidature.id, "NATCASH", "47123456")
    assert second.reference_paiement == premier.reference_paiement
    assert second.methode_paiement == "MONCASH"


@pytest.mark.parametrize("methode", [None, "", "PAYPAL", "visa"])
def test_methode_invalide(repo, methode):
    candidature = _candidature(repo)
    with pytest.raises(InformationsInvalides) as exc:
        SimulerPaiementUseCase(repo).executer(candidature.id, methode, "37123456")
    assert "methode_paiement" in exc.value.erreurs
    assert repo.candidatures[candidature.id].statut_paiement == STATUT_PAIEMENT_EN_ATTENTE


@pytest.mark.parametrize("numero", [None, "", "1234", "17123456", "+33 6 12 34 56 78"])
def test_numero_invalide(repo, numero):
    candidature = _candidature(repo)
    with pytest.raises(InformationsInvalides) as exc:
        SimulerPaiementUseCase(repo).executer(candidature.id, "MONCASH", numero)
    assert "numero_telephone" in exc.value.erreurs
    assert repo.candidatures[candidature.id].reference_paiement is None


def test_numero_haitien_avec_indicatif_accepte(repo):
    candidature = _candidature(repo)
    resultat = SimulerPaiementUseCase(repo).executer(candidature.id, "NATCASH", "+509 47 12 34 56")
    assert resultat.numero_paiement == "+50947123456"


def test_exige_la_reponse_a_la_question_de_deplacement(repo):
    candidature = _candidature(repo, deplacement=None)
    with pytest.raises(EtapePrecedenteIncomplete):
        SimulerPaiementUseCase(repo).executer(candidature.id, "MONCASH", "37123456")


def test_candidature_introuvable(repo):
    with pytest.raises(CandidatureIntrouvable):
        SimulerPaiementUseCase(repo).executer("inconnu", "MONCASH", "37123456")


def test_dossier_soumis_non_modifiable(repo):
    candidature = _candidature(repo)
    candidature.statut = STATUT_SOUMISE
    repo.enregistrer_candidature(candidature)
    with pytest.raises(CandidatureDejaSoumise):
        SimulerPaiementUseCase(repo).executer(candidature.id, "MONCASH", "37123456")


# --- Cas qui n'aboutissent pas : refus, échec technique, relance (simulation de tous les cas d'un vrai paiement) ---

def test_numero_finissant_par_0000_refuse_et_ne_debloque_rien(repo):
    candidature = _candidature(repo)
    with pytest.raises(PaiementRefuse):
        SimulerPaiementUseCase(repo).executer(candidature.id, "MONCASH", "37 12 00 00")
    stockee = repo.candidatures[candidature.id]
    assert stockee.statut_paiement == STATUT_PAIEMENT_REFUSE
    assert stockee.reference_paiement is None


def test_un_refus_se_repete_avec_le_meme_numero_mais_un_autre_compte_aboutit(repo):
    candidature = _candidature(repo)
    for _ in range(2):
        with pytest.raises(PaiementRefuse):
            SimulerPaiementUseCase(repo).executer(candidature.id, "MONCASH", "37120000")
    resultat = SimulerPaiementUseCase(repo).executer(candidature.id, "NATCASH", "41 12 34 56")
    assert resultat.statut_paiement == STATUT_PAIEMENT_SIMULE
    assert resultat.methode_paiement == "NATCASH"


def test_echec_technique_puis_relance_qui_aboutit(repo):
    candidature = _candidature(repo)
    with pytest.raises(PaiementEchoue):
        SimulerPaiementUseCase(repo).executer(candidature.id, "MONCASH", "37 12 99 99")
    assert repo.candidatures[candidature.id].statut_paiement == STATUT_PAIEMENT_ECHOUE
    assert repo.candidatures[candidature.id].reference_paiement is None

    relance = SimulerPaiementUseCase(repo).executer(candidature.id, "MONCASH", "37 12 99 99")
    assert relance.statut_paiement == STATUT_PAIEMENT_SIMULE
    assert re.fullmatch(r"PAY-SIM-2026-\d{4}", relance.reference_paiement)


def test_un_refus_ne_compte_pas_comme_un_echec_technique_deja_subi(repo):
    candidature = _candidature(repo)
    with pytest.raises(PaiementRefuse):
        SimulerPaiementUseCase(repo).executer(candidature.id, "MONCASH", "37120000")
    with pytest.raises(PaiementEchoue):
        SimulerPaiementUseCase(repo).executer(candidature.id, "MONCASH", "37129999")

