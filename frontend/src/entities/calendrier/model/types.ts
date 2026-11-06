/** Calendrier d'admission (US-028). Les dates sont des jours civils AAAA-MM-JJ ; `null` : à confirmer par la Faculté. */
export type EtatPeriode = 'non_definie' | 'a_venir' | 'ouverte' | 'fermee';

export interface DatesCalendrier {
  date_ouverture: string | null;
  date_limite: string | null;
  date_concours: string | null;
  date_resultats: string | null;
  date_rentree: string | null;
}

export interface CalendrierPublic extends DatesCalendrier {
  etat: EtatPeriode;
}

export interface CalendrierAdmin extends CalendrierPublic {
  /** Email de l'auteur de la dernière modification. */
  modifie_par: string | null;
  /** Horodatage ISO-8601 UTC de la dernière modification. */
  modifie_le: string | null;
}

/** Champs dans l'ordre chronologique attendu par le serveur. */
export const CHAMPS_DATES: (keyof DatesCalendrier)[] = ['date_ouverture', 'date_limite', 'date_concours', 'date_resultats', 'date_rentree'];

/** Sans calendrier enregistré, le portail reste ouvert (comportement d'avant US-028). */
export const candidaturesAcceptees = (etat: EtatPeriode | undefined) => etat === undefined || etat === 'ouverte' || etat === 'non_definie';
