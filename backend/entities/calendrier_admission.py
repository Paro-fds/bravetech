"""Entité CalendrierAdmission — Couche Domain (US-028).

Dates de la session d'admission en cours, réglées par l'administration. Chaque modification est enregistrée comme une
nouvelle version (ajout seul) : la plus récente est en vigueur, les précédentes forment l'audit (AGENTS.md, fait
critique 5). Les dates sont des jours du calendrier d'Haïti ; la conversion depuis l'heure UTC est faite par la BLL.

Règle absolue (Clean Architecture) : aucun import de framework ni de couche externe.
"""

from dataclasses import dataclass
from datetime import date, datetime

# État de la période de candidature un jour donné
PERIODE_NON_DEFINIE = "non_definie"  # aucun calendrier enregistré : le portail reste ouvert (comportement d'avant US-028)
PERIODE_A_VENIR = "a_venir"
PERIODE_OUVERTE = "ouverte"
PERIODE_FERMEE = "fermee"

# Ordre chronologique attendu des dates renseignées (champ, libellé pour les messages d'erreur)
ORDRE_DATES = (
    ("date_ouverture", "l'ouverture des candidatures"),
    ("date_limite", "la date limite de dépôt"),
    ("date_concours", "le concours d'admission"),
    ("date_resultats", "la publication des résultats"),
    ("date_rentree", "la rentrée"),
)


@dataclass(frozen=True)
class CalendrierAdmission:
    id: str
    date_ouverture: date
    date_limite: date  # dernier jour de dépôt, inclus
    date_concours: date | None
    date_resultats: date | None
    date_rentree: date | None
    modifie_par: str  # identifiant de l'utilisateur du personnel
    modifie_le: datetime  # UTC


def etat_periode(calendrier: CalendrierAdmission | None, jour: date) -> str:
    """État de la période de candidature pour un jour du calendrier d'Haïti."""
    if calendrier is None:
        return PERIODE_NON_DEFINIE
    if jour < calendrier.date_ouverture:
        return PERIODE_A_VENIR
    if jour > calendrier.date_limite:
        return PERIODE_FERMEE
    return PERIODE_OUVERTE


def candidatures_acceptees(etat: str) -> bool:
    return etat in (PERIODE_OUVERTE, PERIODE_NON_DEFINIE)


def ecarts_chronologiques(dates: dict[str, date | None]) -> dict[str, str]:
    """Champ -> message pour chaque date renseignée antérieure à une date renseignée qui la précède dans `ORDRE_DATES`."""
    erreurs: dict[str, str] = {}
    precedente: tuple[date, str] | None = None
    for champ, libelle in ORDRE_DATES:
        valeur = dates.get(champ)
        if valeur is None:
            continue
        if precedente is not None and valeur < precedente[0]:
            erreurs[champ] = f"Cette date doit être postérieure ou égale à {precedente[1]}."
        else:
            precedente = (valeur, libelle)
    return erreurs
