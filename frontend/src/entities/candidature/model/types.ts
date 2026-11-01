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

export type ErreursChamps = Partial<
  Record<keyof InformationsPersonnelles | 'deplacement_physique' | 'methode_paiement' | 'numero_telephone', string>
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
