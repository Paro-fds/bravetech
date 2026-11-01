"""Cas d'utilisation : export de la liste des dossiers — Couche BLL (US-015).

L'export sert aux commissions d'admission qui travaillent hors ligne. Minimisation des données : référence, identité
(nom, prénom), déplacement physique, statut, pièces validées et date de soumission ; ni email, ni téléphone, ni adresse.

Le CSV est écrit pour Excel en français : séparateur « ; » et BOM UTF-8 (accents corrects à l'ouverture). Toute cellule
qui commencerait par un caractère interprété comme une formule (= + - @) est neutralisée, car les noms viennent de
saisies de candidats (injection de formule CSV).
"""

import csv
import io
from datetime import datetime

from backend.bll.consulter_candidatures import LigneCandidature
from backend.bll.obtenir_statut_candidature import (
    STATUT_GLOBAL_ACTION_REQUISE,
    STATUT_GLOBAL_COMPLET,
    STATUT_GLOBAL_EN_EXAMEN,
)

COLONNES = [
    "reference_dossier",
    "nom",
    "prenom",
    "deplacement_physique",
    "statut",
    "pieces_validees",
    "soumise_le",
]

LIBELLES_STATUT = {
    STATUT_GLOBAL_EN_EXAMEN: "À examiner",
    STATUT_GLOBAL_ACTION_REQUISE: "Action du candidat",
    STATUT_GLOBAL_COMPLET: "Complet",
}

_DEBUTS_DE_FORMULE = ("=", "+", "-", "@", "\t", "\r")


def neutraliser(valeur: str) -> str:
    """Préfixe d'une apostrophe toute valeur que Excel ou Calc interpréterait comme une formule."""
    return "'" + valeur if valeur.startswith(_DEBUTS_DE_FORMULE) else valeur


def _horodatage(valeur: datetime | None) -> str:
    return valeur.strftime("%Y-%m-%dT%H:%M:%SZ") if valeur else ""


def vers_lignes(dossiers: list[LigneCandidature]) -> list[list[str]]:
    """Les dossiers sous forme de cellules texte, dans l'ordre de `COLONNES`."""
    lignes = []
    for d in dossiers:
        deplacement = d.candidature.deplacement_physique
        lignes.append([
            d.candidature.reference_dossier or "",
            neutraliser(d.candidat.nom),
            neutraliser(d.candidat.prenom),
            "" if deplacement is None else ("Oui" if deplacement else "Non"),
            LIBELLES_STATUT.get(d.statut_global, d.statut_global),
            f"{d.pieces_validees}/{d.pieces_total}",
            _horodatage(d.candidature.soumise_le),
        ])
    return lignes


def generer_csv(dossiers: list[LigneCandidature]) -> bytes:
    """CSV UTF-8 avec BOM, séparateur « ; », fins de ligne CRLF."""
    sortie = io.StringIO(newline="")
    ecrivain = csv.writer(sortie, delimiter=";", lineterminator="\r\n")
    ecrivain.writerow(COLONNES)
    ecrivain.writerows(vers_lignes(dossiers))
    return b"\xef\xbb\xbf" + sortie.getvalue().encode("utf-8")
