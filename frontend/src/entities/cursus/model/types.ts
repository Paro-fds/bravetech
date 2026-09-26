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

export interface CursusDetail extends CursusListItem {
  description_longue: string;
  niveaux: Record<string, MatiereItem[]>;
}
