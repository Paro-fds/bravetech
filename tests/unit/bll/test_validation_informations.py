"""Tests unitaires de la validation des informations personnelles (US-005).
"""

from datetime import date

import pytest

from backend.bll.validation_informations import valider_informations
from backend.entities.erreurs import InformationsInvalides

from tests.unit.bll.fakes import donnees_valides

AUJOURDHUI = date(2026, 11, 1)


def _erreurs(**surcharges) -> dict[str, str]:
    with pytest.raises(InformationsInvalides) as exc:
        valider_informations(donnees_valides(**surcharges), aujourdhui=AUJOURDHUI)
    return exc.value.erreurs


def test_saisie_valide_est_normalisee():
    propres = valider_informations(donnees_valides(nom="  Louis  ", prenom="Louismy   Jean"), aujourdhui=AUJOURDHUI)
    assert propres["nom"] == "Louis"
    assert propres["prenom"] == "Louismy Jean"
    assert propres["email"] == "louismy@exemple.com"
    assert propres["telephone"] == "+50937123456"
    assert propres["sexe"] == "M"


@pytest.mark.parametrize("champ", ["nom", "prenom", "date_naissance", "sexe", "telephone", "email", "departement", "commune"])
def test_champ_obligatoire(champ):
    assert champ in _erreurs(**{champ: None})


@pytest.mark.parametrize("telephone", ["+509 37 12 34 56", "509-3712-3456", "3712.3456", "37123456"])
def test_telephone_haitien_accepte(telephone):
    propres = valider_informations(donnees_valides(telephone=telephone), aujourdhui=AUJOURDHUI)
    assert propres["telephone"] == "+50937123456"


@pytest.mark.parametrize("telephone", ["1234", "17123456", "+33 6 12 34 56 78", "abcdefgh"])
def test_telephone_invalide(telephone):
    assert "telephone" in _erreurs(telephone=telephone)


@pytest.mark.parametrize("email", ["sans-arobase", "a@b", "a b@c.com", "@c.com"])
def test_email_invalide(email):
    assert "email" in _erreurs(email=email)


def test_date_naissance_dans_le_futur():
    assert "date_naissance" in _erreurs(date_naissance=date(2027, 1, 1))


def test_age_minimum():
    assert "date_naissance" in _erreurs(date_naissance=date(2015, 1, 1))
    valider_informations(donnees_valides(date_naissance=date(2012, 11, 1)), aujourdhui=AUJOURDHUI)


def test_age_maximum():
    assert "date_naissance" in _erreurs(date_naissance=date(1900, 1, 1))


def test_sexe_invalide():
    assert "sexe" in _erreurs(sexe="X")


def test_departement_inconnu():
    assert "departement" in _erreurs(departement="Atlantide")


def test_nom_sans_lettre():
    assert "nom" in _erreurs(nom="1234")


def test_plusieurs_erreurs_remontees_ensemble():
    erreurs = _erreurs(nom="", email="x", telephone="1")
    assert {"nom", "email", "telephone"} <= set(erreurs)
