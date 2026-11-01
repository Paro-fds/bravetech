import type { StatutPiece } from '../../candidature';

/** Statut global d'un dossier vu du personnel (« en_examen » s'affiche « À examiner »). */
export type StatutDossier = 'en_examen' | 'action_requise' | 'complet';

export interface LigneDossier {
  reference_dossier: string;
  nom: string;
  prenom: string;
  statut_paiement: string;
  deplacement_physique: boolean | null;
  soumise_le: string | null;
  created_at: string;
  statut: StatutDossier;
  pieces_total: number;
  pieces_validees: number;
  pieces_en_attente: number;
  pieces_rejetees: number;
}

export interface Statistiques {
  dossiers_soumis: number;
  sans_deplacement: number;
  pieces_a_examiner: number;
  pieces_deposees: number;
  pieces_refusees: number;
}

export interface PageDossiers {
  total: number;
  page: number;
  limit: number;
  items: LigneDossier[];
  statistiques: Statistiques;
}

export interface FiltresDossiers {
  page: number;
  q: string;
  statut: StatutDossier | '';
  deplacement: 'oui' | 'non' | '';
}

export interface PieceAdmin {
  id: string;
  nom: string;
  statut: StatutPiece;
  document_id: string | null;
  nom_fichier: string | null;
  type_mime: string | null;
  taille_octets: number | null;
  depose_le: string | null;
  motif_rejet: string | null;
  valide_par: string | null;
  date_validation: string | null;
}

export interface DossierAdmin {
  reference_dossier: string;
  statut: StatutDossier;
  admission: string;
  soumise_le: string | null;
  nom: string;
  prenom: string;
  sexe: string;
  date_naissance: string;
  email: string;
  telephone: string;
  departement: string;
  commune: string;
  deplacement_physique: boolean | null;
  statut_paiement: string;
  methode_paiement: string | null;
  reference_paiement: string | null;
  montant_htg: number;
  pieces: PieceAdmin[];
}

/** Libellé et couleur d'un statut de dossier (maquette « Administration liste des dossiers »). */
export const BADGES_DOSSIER: Record<StatutDossier, { libelle: string; classe: string }> = {
  en_examen: { libelle: 'À examiner', classe: 'bg-fds-warn-bg text-fds-warn' },
  action_requise: { libelle: 'Action du candidat', classe: 'bg-fds-bad-bg text-fds-bad' },
  complet: { libelle: 'Complet', classe: 'bg-fds-ok-bg text-fds-ok' },
};

export const TAILLE_PAGE = 20;
