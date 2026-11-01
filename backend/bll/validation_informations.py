"""Règles de validation des informations personnelles — Couche BLL.

Fonctions pures : nettoient et valident la saisie de l'étape 1 de la candidature.
"""

import re
from datetime import date
from typing import Any

from backend.entities.candidat import DEPARTEMENTS, SEXES
from backend.entities.erreurs import InformationsInvalides

AGE_MINIMUM = 14
AGE_MAXIMUM = 90

_RE_EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
_RE_TELEPHONE = re.compile(r"(?:\+?509)?([234]\d{7})")
_RE_LETTRE = re.compile(r"[^\W\d_]")


def _nettoyer_texte(valeur: Any) -> str:
    return re.sub(r"\s+", " ", str(valeur or "")).strip()


def normaliser_telephone_haitien(valeur: Any) -> str | None:
    """Retourne le numéro au format +509XXXXXXXX, ou None s'il n'est pas un numéro haïtien valide."""
    brut = re.sub(r"[\s.\-]", "", str(valeur or ""))
    correspondance = _RE_TELEPHONE.fullmatch(brut)
    return f"+509{correspondance.group(1)}" if correspondance else None


def _age(naissance: date, aujourdhui: date) -> int:
    avant_anniversaire = (aujourdhui.month, aujourdhui.day) < (naissance.month, naissance.day)
    return aujourdhui.year - naissance.year - (1 if avant_anniversaire else 0)


def _valider_nom(champ: str, valeur: Any, libelle: str, erreurs: dict[str, str]) -> str:
    texte = _nettoyer_texte(valeur)
    if not texte:
        erreurs[champ] = f"{libelle} obligatoire."
    elif len(texte) > 100 or not _RE_LETTRE.search(texte):
        erreurs[champ] = f"{libelle} invalide."
    return texte


def valider_informations(donnees: dict[str, Any], aujourdhui: date | None = None) -> dict[str, Any]:
    """Valide et normalise les informations personnelles.

    Retourne les valeurs nettoyées, ou lève `InformationsInvalides` avec un message par champ fautif.
    """
    aujourdhui = aujourdhui or date.today()
    erreurs: dict[str, str] = {}
    propres: dict[str, Any] = {}

    propres["nom"] = _valider_nom("nom", donnees.get("nom"), "Nom", erreurs)
    propres["prenom"] = _valider_nom("prenom", donnees.get("prenom"), "Prénom", erreurs)

    naissance = donnees.get("date_naissance")
    if not isinstance(naissance, date):
        erreurs["date_naissance"] = "Date de naissance obligatoire."
    elif naissance > aujourdhui:
        erreurs["date_naissance"] = "La date de naissance ne peut pas être dans le futur."
    elif not AGE_MINIMUM <= _age(naissance, aujourdhui) <= AGE_MAXIMUM:
        erreurs["date_naissance"] = f"Date de naissance invalide (âge attendu : {AGE_MINIMUM} à {AGE_MAXIMUM} ans)."
    propres["date_naissance"] = naissance

    sexe = _nettoyer_texte(donnees.get("sexe")).upper()
    if sexe not in SEXES:
        erreurs["sexe"] = "Sexe obligatoire (M ou F)."
    propres["sexe"] = sexe

    telephone = _nettoyer_texte(donnees.get("telephone"))
    telephone_normalise = normaliser_telephone_haitien(telephone)
    if not telephone:
        erreurs["telephone"] = "Téléphone obligatoire."
    elif telephone_normalise is None:
        erreurs["telephone"] = "Numéro haïtien invalide (8 chiffres, ex. 37 12 34 56)."
    propres["telephone"] = telephone_normalise or telephone

    email = _nettoyer_texte(donnees.get("email")).lower()
    if not email:
        erreurs["email"] = "Email obligatoire."
    elif len(email) > 255 or not _RE_EMAIL.fullmatch(email):
        erreurs["email"] = "Adresse email invalide."
    propres["email"] = email

    departement = _nettoyer_texte(donnees.get("departement"))
    if not departement:
        erreurs["departement"] = "Département obligatoire."
    elif departement not in DEPARTEMENTS:
        erreurs["departement"] = "Département inconnu."
    propres["departement"] = departement

    commune = _nettoyer_texte(donnees.get("commune"))
    if not commune:
        erreurs["commune"] = "Commune obligatoire."
    elif len(commune) > 100:
        erreurs["commune"] = "Commune invalide."
    propres["commune"] = commune

    if erreurs:
        raise InformationsInvalides(erreurs)
    return propres
