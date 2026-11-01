"""DTOs de l'administration — Couche Présentation / API (US-012).
"""

from datetime import date, datetime

from pydantic import BaseModel


class LigneCandidatureResponse(BaseModel):
    reference_dossier: str
    nom: str
    prenom: str
    statut_paiement: str
    deplacement_physique: bool | None
    soumise_le: datetime | None  # UTC
    created_at: datetime  # UTC
    statut: str  # en_examen | action_requise | complet
    pieces_total: int
    pieces_validees: int
    pieces_en_attente: int
    pieces_rejetees: int


class StatistiquesResponse(BaseModel):
    dossiers_soumis: int
    sans_deplacement: int
    pieces_a_examiner: int
    pieces_deposees: int
    pieces_refusees: int


class PageCandidaturesResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: list[LigneCandidatureResponse]
    statistiques: StatistiquesResponse


class PieceAdminResponse(BaseModel):
    id: str  # identifiant de la pièce requise (ex. mpc-cin)
    nom: str
    statut: str  # manquant | en_attente | valide | rejete
    document_id: str | None = None  # à passer à /admin/proxy-document/{document_id}
    nom_fichier: str | None = None
    type_mime: str | None = None
    taille_octets: int | None = None
    depose_le: datetime | None = None  # UTC
    motif_rejet: str | None = None
    valide_par: str | None = None
    date_validation: datetime | None = None  # UTC


class DossierAdminResponse(BaseModel):
    reference_dossier: str
    statut: str  # en_examen | action_requise | complet
    admission: str
    soumise_le: datetime | None
    nom: str
    prenom: str
    sexe: str
    date_naissance: date
    email: str
    telephone: str
    departement: str
    commune: str
    deplacement_physique: bool | None
    statut_paiement: str
    methode_paiement: str | None
    reference_paiement: str | None
    montant_htg: int
    pieces: list[PieceAdminResponse]
