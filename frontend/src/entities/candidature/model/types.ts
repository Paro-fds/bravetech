export type Sexe = 'M' | 'F';

/** Saisie de l'étape 1. Les champs restent des chaînes tant que le formulaire n'est pas validé. */
export interface InformationsPersonnelles {
  nom: string;
  prenom: string;
  date_naissance: string; // AAAA-MM-JJ
  sexe: Sexe | '';
  telephone: string;
  email: string;
  departement: string;
  commune: string;
}

export type MethodePaiement = 'MONCASH' | 'NATCASH';

/** Statut renvoyé par l'API une fois le paiement simulé enregistré. */
export const STATUT_PAIEMENT_SIMULE = 'SIMULE_PAYE';

/** Statut d'un dossier définitivement soumis. */
export const STATUT_SOUMISE = 'soumise';

/** État d'un brouillon de candidature renvoyé par l'API. */
export interface Brouillon {
  candidature_id: string;
  statut: string;
  deplacement_physique: boolean | null;
  statut_paiement: string;
  methode_paiement: MethodePaiement | null;
  /** Référence SIMULÉE (PAY-SIM-AAAA-NNNN) : aucun montant réel n'est prélevé. */
  reference_paiement: string | null;
  montant_htg: number;
  /** Référence officielle CAN-AAAA-NNNN, attribuée à la soumission. */
  reference_dossier: string | null;
  /** Horodatage UTC de la soumission (ISO-8601). */
  soumise_le: string | null;
  informations: InformationsPersonnelles;
}

/** Statut d'une pièce requise : « manquant » tant qu'aucun fichier n'est déposé. */
export type StatutPiece = 'manquant' | 'en_attente' | 'valide' | 'rejete';

/** Pièce requise d'admission avec l'état du fichier déposé. */
export interface PieceDossier {
  id: string;
  nom: string;
  description: string;
  format_accepte: string;
  taille_max_mo: number;
  est_obligatoire: boolean;
  statut: StatutPiece;
  nom_fichier: string | null;
  taille_octets: number | null;
  motif_rejet: string | null;
}

/** Statut public d'une pièce dans la page de suivi (« manquant » n'arrive que si le dépôt a été purgé). */
export interface PieceSuivi {
  id: string;
  nom: string;
  statut: StatutPiece;
  motif_rejet: string | null;
  depose_le: string | null;
  valide_le: string | null;
}

export type StatutGlobal = 'en_examen' | 'action_requise' | 'complet';

/** Vue publique d'un dossier soumis : prénom et initiale du nom seulement, aucune coordonnée. */
export interface SuiviDossier {
  reference_dossier: string;
  prenom: string;
  initiale_nom: string;
  admission: string;
  soumise_le: string | null;
  statut_global: StatutGlobal;
  pieces_validees: number;
  pieces_total: number;
  pieces: PieceSuivi[];
}

/** Format d'une référence de dossier : CAN-AAAA-NNNN. */
export const FORMAT_REFERENCE = /^CAN-\d{4}-\d{4,}$/;

export type ErreursChamps = Partial<
  Record<keyof InformationsPersonnelles | 'deplacement_physique' | 'methode_paiement' | 'numero_telephone' | 'fichier', string>
>;

export const DEPARTEMENTS = [
  'Artibonite',
  'Centre',
  "Grand'Anse",
  'Nippes',
  'Nord',
  'Nord-Est',
  'Nord-Ouest',
  'Ouest',
  'Sud',
  'Sud-Est',
] as const;

export const INFORMATIONS_VIDES: InformationsPersonnelles = {
  nom: '',
  prenom: '',
  date_naissance: '',
  sexe: '',
  telephone: '',
  email: '',
  departement: '',
  commune: '',
};
