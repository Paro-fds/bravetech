export interface CursusListItem {
  id: string;
  nom: string;
  duree_annees: number;
  description_courte: string;
  date_ouverture_inscription: string;
  date_fermeture_inscription: string;
  est_ouvert: boolean;
}

export interface MatiereItem {
  item: number;
  titre: string;
  code?: string;
  heures?: number;
  heures_theorie?: number | null;
  heures_tp?: number | null;
}

export interface DocumentRequisItem {
  id: string;
  nom: string;
  description: string;
  format_accepte: string;
  taille_max_mo: number;
  est_obligatoire: boolean;
}

export interface CursusDetail extends CursusListItem {
  description_longue: string;
  niveaux: Record<string, MatiereItem[]>;
  documents_requis: DocumentRequisItem[];
}
