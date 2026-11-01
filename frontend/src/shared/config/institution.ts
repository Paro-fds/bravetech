/**
 * Informations institutionnelles affichées sur les pages Histoire et Contact.
 *
 * Une valeur à `null` n'est PAS affichée : elle reste à fournir ou à confirmer par la Faculté (US-019). Ne jamais mettre
 * ici une valeur supposée. Dès qu'elle est confirmée, la renseigner suffit à la publier.
 */
// L'adresse est dans les dictionnaires (clé `marque.adresse`) : elle se traduit.
export const INSTITUTION = {
  telephone: null as string | null,
  email: null as string | null,
  horaires: null as string | null,
} as const;

/**
 * Conseil de direction actuel. Les noms, prénoms et titres exacts doivent être confirmés par la Faculté avant publication
 * (functional-specs WS-01 §1.4) : tant que `confirme` est faux, le bloc n'est pas affiché.
 */
export const CONSEIL_DE_DIRECTION = {
  confirme: false,
  membres: ['J.E. Etienne', 'Hervé (prénom à confirmer)', 'Jadin Jadotte'] as string[],
};
