"""Tests unitaires des cas d'utilisation de la candidature (US-005), avec un dépôt en mémoire.
"""

import pytest

from backend.bll.definir_deplacement_physique import DefinirDeplacementPhysiqueUseCase
from backend.bll.enregistrer_informations import EnregistrerInformationsUseCase, MettreAJourInformationsUseCase
from backend.bll.obtenir_brouillon import ObtenirBrouillonUseCase
from backend.entities.candidat import CAMPAGNE_COURANTE
from backend.entities.candidature import STATUT_BROUILLON, STATUT_SOUMISE
from backend.entities.erreurs import (
    CandidatureDejaExistante,
    CandidatureDejaSoumise,
    CandidatureIntrouvable,
    InformationsInvalides,
)

from tests.unit.bll.fakes import FakeCandidatureRepository, donnees_valides


@pytest.fixture
def repo():
    return FakeCandidatureRepository()


def _creer(repo, **surcharges):
    return EnregistrerInformationsUseCase(repo).executer(donnees_valides(**surcharges))


def test_creation_du_brouillon(repo):
    candidat, candidature = _creer(repo)
    assert candidat.campagne == CAMPAGNE_COURANTE
    assert candidat.email == "louismy@exemple.com"
    assert candidature.candidat_id == candidat.id
    assert candidature.statut == STATUT_BROUILLON
    assert candidature.deplacement_physique is None  # question pas encore répondue
    assert candidature.reference_dossier is None  # attribuée à la soumission (US-008)


def test_aucune_donnee_de_cursus(repo):
    candidat, candidature = _creer(repo)
    assert not hasattr(candidat, "cursus_slug")
    assert not hasattr(candidature, "cursus_slug")


def test_informations_invalides_ne_creent_rien(repo):
    with pytest.raises(InformationsInvalides):
        _creer(repo, email="pas-un-email")
    assert repo.candidats == {} and repo.candidatures == {}


def test_unicite_email_campagne(repo):
    _creer(repo)
    with pytest.raises(CandidatureDejaExistante):
        _creer(repo, nom="Autre", email="LOUISMY@exemple.com")


def test_mise_a_jour_des_informations(repo):
    _, candidature = _creer(repo)
    candidat, _ = MettreAJourInformationsUseCase(repo).executer(
        candidature.id, donnees_valides(commune="Delmas", departement="Ouest")
    )
    assert candidat.commune == "Delmas"
    assert repo.candidats[candidat.id].commune == "Delmas"


def test_mise_a_jour_vers_un_email_deja_pris(repo):
    _creer(repo, email="a@exemple.com")
    _, autre = _creer(repo, email="b@exemple.com")
    with pytest.raises(CandidatureDejaExistante):
        MettreAJourInformationsUseCase(repo).executer(autre.id, donnees_valides(email="a@exemple.com"))


def test_mise_a_jour_en_gardant_son_email(repo):
    _, candidature = _creer(repo)
    MettreAJourInformationsUseCase(repo).executer(candidature.id, donnees_valides(prenom="Jean"))


def test_mise_a_jour_candidature_introuvable(repo):
    with pytest.raises(CandidatureIntrouvable):
        MettreAJourInformationsUseCase(repo).executer("inconnu", donnees_valides())


@pytest.mark.parametrize("reponse", [True, False])
def test_deplacement_physique_enregistre(repo, reponse):
    _, candidature = _creer(repo)
    resultat = DefinirDeplacementPhysiqueUseCase(repo).executer(candidature.id, reponse)
    assert resultat.deplacement_physique is reponse
    assert repo.candidatures[candidature.id].deplacement_physique is reponse


@pytest.mark.parametrize("reponse", [None, "oui", "true", 1, 0, ""])
def test_deplacement_physique_obligatoire_et_booleen_strict(repo, reponse):
    _, candidature = _creer(repo)
    with pytest.raises(InformationsInvalides) as exc:
        DefinirDeplacementPhysiqueUseCase(repo).executer(candidature.id, reponse)
    assert "deplacement_physique" in exc.value.erreurs
    assert repo.candidatures[candidature.id].deplacement_physique is None


def test_deplacement_physique_candidature_introuvable(repo):
    with pytest.raises(CandidatureIntrouvable):
        DefinirDeplacementPhysiqueUseCase(repo).executer("inconnu", True)


def test_dossier_soumis_non_modifiable(repo):
    _, candidature = _creer(repo)
    candidature.statut = STATUT_SOUMISE
    repo.enregistrer_candidature(candidature)
    with pytest.raises(CandidatureDejaSoumise):
        DefinirDeplacementPhysiqueUseCase(repo).executer(candidature.id, False)
    with pytest.raises(CandidatureDejaSoumise):
        MettreAJourInformationsUseCase(repo).executer(candidature.id, donnees_valides())


def test_reprise_du_brouillon(repo):
    candidat, candidature = _creer(repo)
    DefinirDeplacementPhysiqueUseCase(repo).executer(candidature.id, False)
    candidat_lu, candidature_lue = ObtenirBrouillonUseCase(repo).executer(candidature.id)
    assert candidat_lu.id == candidat.id
    assert candidature_lue.deplacement_physique is False


def test_reprise_brouillon_introuvable(repo):
    with pytest.raises(CandidatureIntrouvable):
        ObtenirBrouillonUseCase(repo).executer("inconnu")
