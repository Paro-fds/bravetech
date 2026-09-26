"""Chargeur de données de cursus depuis les fichiers JSON officiels.

Lit les données présentes dans le dossier `cursus/` et les transforme en entités Cursus et DocumentRequis.
"""

import json
from pathlib import Path
from backend.entities.cursus import Cursus
from backend.entities.document_requis import DocumentRequis

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


def _creer_documents_requis_par_defaut(cursus_id: str) -> list[DocumentRequis]:
    """Génère la liste officielle des pièces justificatives exigées pour un cursus."""
    pieces = [
        DocumentRequis(
            id=f"{cursus_id}-acte-naissance",
            cursus_id=cursus_id,
            nom="Acte de naissance",
            description="Extrait officiel des Archives Nationales ou acte de naissance légalisé.",
            format_accepte="PDF, JPG, PNG",
            taille_max_mo=5,
            est_obligatoire=True,
        ),
        DocumentRequis(
            id=f"{cursus_id}-diplome-bac",
            cursus_id=cursus_id,
            nom="Certificat du Baccalauréat / NS4",
            description="Certificat officiel attestant de la réussite aux épreuves du Baccalauréat ou NS4.",
            format_accepte="PDF, JPG, PNG",
            taille_max_mo=5,
            est_obligatoire=True,
        ),
        DocumentRequis(
            id=f"{cursus_id}-releve-notes-bac",
            cursus_id=cursus_id,
            nom="Relevé de notes officiel du Baccalauréat",
            description="Relevé de notes complet délivré par le MENFP.",
            format_accepte="PDF, JPG, PNG",
            taille_max_mo=5,
            est_obligatoire=True,
        ),
        DocumentRequis(
            id=f"{cursus_id}-photo-identite",
            cursus_id=cursus_id,
            nom="Photo d'identité récente",
            description="Photo d'identité récente de face, sur fond blanc uni.",
            format_accepte="JPG, PNG",
            taille_max_mo=3,
            est_obligatoire=True,
        ),
    ]

    # Pour les filières de spécialisation (non-MPC), le relevé du tronc commun MPC est requis
    if cursus_id != "mpc":
        pieces.append(
            DocumentRequis(
                id=f"{cursus_id}-attestation-mpc",
                cursus_id=cursus_id,
                nom="Attestation de validation du cycle MPC",
                description="Relevé officiel ou certificat de réussite du tronc commun MPC (FDS-UEH).",
                format_accepte="PDF",
                taille_max_mo=5,
                est_obligatoire=True,
            )
        )

    return pieces


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

        documents_requis = _creer_documents_requis_par_defaut(slug)

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
            documents_requis=documents_requis,
        )
        resultats.append(cursus)

    return resultats
