"""DTOs (Data Transfer Objects) des candidatures — Couche Présentation / API (US-005).
"""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, StrictBool


class InformationsPersonnellesRequest(BaseModel):
    """Saisie de l'étape 1. Les règles métier (format, plages) sont validées par la couche BLL."""
    nom: str = Field(max_length=255)
    prenom: str = Field(max_length=255)
    date_naissance: date
    sexe: str = Field(max_length=10)
    telephone: str = Field(max_length=50)
    email: str = Field(max_length=255)
    departement: str = Field(max_length=100)
    commune: str = Field(max_length=255)


class DeplacementPhysiqueRequest(BaseModel):
    """Réponse obligatoire à la question sur le déplacement physique (booléen strict)."""
    deplacement_physique: StrictBool


class PaiementSimuleRequest(BaseModel):
    """Simulation de paiement : opérateur choisi et numéro mobile (les règles sont validées par la BLL)."""
    methode: str = Field(max_length=20)
    numero_telephone: str = Field(max_length=50)


class InformationsPersonnellesResponse(BaseModel):
    nom: str
    prenom: str
    date_naissance: date
    sexe: str
    telephone: str
    email: str
    departement: str
    commune: str

    model_config = ConfigDict(from_attributes=True)


class BrouillonResponse(BaseModel):
    """État d'un brouillon de candidature, identifié par un identifiant non devinable."""
    candidature_id: str
    statut: str
    deplacement_physique: bool | None
    statut_paiement: str
    methode_paiement: str | None
    reference_paiement: str | None  # référence SIMULÉE : aucun montant réel n'est prélevé
    montant_htg: int
    reference_dossier: str | None  # CAN-AAAA-NNNN, attribuée à la soumission
    soumise_le: datetime | None  # UTC
    informations: InformationsPersonnellesResponse


class PieceSuiviResponse(BaseModel):
    """Statut public d'une pièce : ni nom de fichier, ni clé de stockage."""
    id: str
    nom: str
    statut: str  # manquant | en_attente | valide | rejete
    format_accepte: str  # utile au formulaire de remplacement d'une pièce refusée
    taille_max_mo: int
    motif_rejet: str | None = None
    depose_le: datetime | None = None  # UTC
    valide_le: datetime | None = None  # UTC


class SuiviDossierResponse(BaseModel):
    """Vue publique d'un dossier soumis (US-009) : prénom et initiale du nom seulement."""
    reference_dossier: str
    prenom: str
    initiale_nom: str
    admission: str
    soumise_le: datetime | None  # UTC
    statut_global: str  # en_examen | action_requise | complet
    pieces_validees: int
    pieces_total: int
    pieces: list[PieceSuiviResponse]


class PieceDossierResponse(BaseModel):
    """Une pièce requise avec l'état du fichier déposé ('manquant' tant que rien n'est déposé)."""
    id: str
    nom: str
    description: str
    format_accepte: str
    taille_max_mo: int
    est_obligatoire: bool
    statut: str  # manquant | en_attente | valide | rejete
    nom_fichier: str | None = None
    taille_octets: int | None = None
    motif_rejet: str | None = None
