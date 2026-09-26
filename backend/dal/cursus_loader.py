"""Chargeur de données de cursus depuis les fichiers JSON officiels.

Lit les données présentes dans le dossier `cursus/` et les transforme en entités Cursus.
"""

import json
from pathlib import Path
from backend.entities.cursus import Cursus

# Chemin absolu vers le dossier cursus à la racine du projet
CURSUS_DIR = Path(__file__).resolve().parents[2] / "cursus"

DESCRIPTIONS: dict[str, tuple[str, str]] = {
    "mpc": (
        "Cycle préparatoire généraliste en Mathématiques, Physique et Chimie de la FDS-UEH.",
        "Le premier cycle des études générales et techniques (MPC) est le tronc commun obligatoire de 2 ans formant les étudiants aux fondamentaux scientifiques rigoureux avant l'orientation vers les départements d'ingénierie ou d'architecture."
    ),
    "genie-civil": (
        "Formation d'ingénieurs en calcul de structures, géotechnique, béton armé et hydraulique.",
        "Le département de Génie Civil forme des ingénieurs aptes à concevoir, bâtir et diriger les travaux d'infrastructures publiques, d'ouvrages d'art, de bâtiments parasismiques et de réseaux de transport en Haïti."
    ),
    "genie-electronique": (
        "Spécialisation d'ingénierie en électronique, traitement du signal et télécommunications.",
        "Le programme de Génie Électronique prépare des spécialistes en conception de circuits électroniques, télécommunications, systèmes de commande, réseaux et instrumentation de mesure industrielle."
    ),
    "genie-electromecanique": (
        "Formation polyvalente en conversion d'énergie, mécanique industrielle et électrotechnique.",
        "Le département de Génie Électromécanique allie les sciences mécaniques et électriques pour former des ingénieurs qualifiés en maintenance industrielle, motorisation, énergies et automatismes."
    ),
    "architecture": (
        "Formation complète en conception architecturale, urbanisme, histoire et habitat durable.",
        "Le département d'Architecture combine sens esthétique, rigueur technique et compréhension du tissu urbain pour concevoir des espaces de vie résilients et adaptés au contexte haïtien."
    ),
}

MAPPING_FICHIERS = [
    ("mpc", "mpc.json"),
    ("genie-civil", "genie-civil.json"),
    ("genie-electronique", "genie-electronique.json"),
    ("genie-electromecanique", "genie-electromecanique.json"),
    ("architecture", "architecture.json"),
]


def charger_cursus_depuis_disque() -> list[Cursus]:
    """Charge l'ensemble des cursus officiels depuis les fichiers JSON de cursus/."""
    resultats: list[Cursus] = []

    for slug, filename in MAPPING_FICHIERS:
        filepath = CURSUS_DIR / filename
        if not filepath.exists():
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        desc_courte, desc_longue = DESCRIPTIONS.get(
            slug,
            (f"Formation en {data.get('filiere', slug)} à la FDS.", f"Programme académique officiel de {data.get('filiere', slug)}.")
        )

        cursus = Cursus(
            id=slug,
            nom=data.get("filiere", slug),
            duree_annees=data.get("duree_annees", 3),
            description_courte=desc_courte,
            description_longue=desc_longue,
            date_ouverture_inscription="2026-08-01",
            date_fermeture_inscription="2026-10-31",
            est_ouvert=True,
            niveaux=data.get("niveaux", {}),
        )
        resultats.append(cursus)

    return resultats
