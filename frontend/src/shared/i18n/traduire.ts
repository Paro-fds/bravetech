/**
 * Logique pure de traduction (sans React ni import local, donc testable avec `node --test`).
 *
 * Le français est la langue de référence : toute clé absente du dictionnaire créole retombe sur le français, et une clé
 * inconnue des deux s'affiche telle quelle (visible en développement, jamais une page vide).
 */

export type Langue = 'fr' | 'kr';
export type Variables = Record<string, string | number>;
export type Dictionnaire = Record<string, string>;

/** Remplace `{nom}` par la valeur correspondante ; un marqueur sans valeur est laissé tel quel. */
export function interpoler(modele: string, variables?: Variables): string {
  if (!variables) return modele;
  return modele.replace(/\{(\w+)\}/g, (marqueur, nom: string) => (nom in variables ? String(variables[nom]) : marqueur));
}

/**
 * Traduit une clé : créole si la langue active l'est et que la clé existe, sinon français, sinon la clé elle-même.
 * `kr` vaut `null` tant que le dictionnaire créole n'est pas chargé (le français s'affiche alors).
 */
export function traduire(
  cle: string,
  langue: Langue,
  fr: Dictionnaire,
  kr: Dictionnaire | null,
  variables?: Variables,
): string {
  const brut = (langue === 'kr' ? kr?.[cle] : undefined) ?? fr[cle] ?? cle;
  return interpoler(brut, variables);
}

/** Valeur de l'attribut `lang` du document : le créole haïtien est `ht` (BCP 47). */
export function codeHtml(langue: Langue): string {
  return langue === 'kr' ? 'ht' : 'fr';
}

/** Valeur lue dans le stockage → langue valide, français par défaut. */
export function langueValide(valeur: unknown): Langue {
  return valeur === 'kr' ? 'kr' : 'fr';
}
