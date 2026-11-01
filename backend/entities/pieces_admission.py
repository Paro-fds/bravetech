"""Pièces requises d'admission — Couche Domain.

L'admission à la Faculté est unique : tout candidat est admis au Premier cycle MPC (ADR-008).
La liste des pièces est donc identique pour tous les candidats.

Règle absolue (Clean Architecture) :
Aucun import de framework (FastAPI, SQLAlchemy), ni d'aucune couche externe (dal, bll, api).
"""

from backend.entities.document_requis import DocumentRequis

# Identifiant du cursus auquel on candidate (Premier cycle MPC)
ID_CURSUS_ADMISSION = "mpc"


def pieces_admission() -> list[DocumentRequis]:
    """Retourne la liste unique des 5 pièces obligatoires du dossier d'admission."""
    cursus_id = ID_CURSUS_ADMISSION
    return [
        DocumentRequis(
            id=f"{cursus_id}-acte-naissance",
            cursus_id=cursus_id,
            nom="Acte de naissance ou extrait d'archives",
            description="Extrait officiel des Archives Nationales ou acte de naissance légalisé.",
            format_accepte="PDF, JPG, PNG",
            taille_max_mo=5,
            est_obligatoire=True,
        ),
        DocumentRequis(
            id=f"{cursus_id}-diplome-bac",
            cursus_id=cursus_id,
            nom="Certificat de fin d'études secondaires (Bac II)",
            description="Certificat officiel attestant de la réussite aux épreuves du Baccalauréat (Bac II) ou NS4.",
            format_accepte="PDF, JPG, PNG",
            taille_max_mo=5,
            est_obligatoire=True,
        ),
        DocumentRequis(
            id=f"{cursus_id}-releve-notes-bac",
            cursus_id=cursus_id,
            nom="Relevé de notes officiel",
            description="Relevé de notes complet délivré par le MENFP.",
            format_accepte="PDF, JPG, PNG",
            taille_max_mo=5,
            est_obligatoire=True,
        ),
        DocumentRequis(
            id=f"{cursus_id}-photos-identite",
            cursus_id=cursus_id,
            nom="Deux photos d'identité récentes",
            description="Deux photos d'identité récentes de face, sur fond blanc uni.",
            format_accepte="JPG, PNG",
            taille_max_mo=5,
            est_obligatoire=True,
        ),
        DocumentRequis(
            id=f"{cursus_id}-cin",
            cursus_id=cursus_id,
            nom="Pièce d'identité (CIN)",
            description="Copie lisible de la Carte d'Identification Nationale (CIN).",
            format_accepte="PDF, JPG, PNG",
            taille_max_mo=5,
            est_obligatoire=True,
        ),
    ]
