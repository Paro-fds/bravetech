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
