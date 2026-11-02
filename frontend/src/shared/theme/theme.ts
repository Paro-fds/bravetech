/**
 * Règles du thème clair / sombre (US-017), sans dépendance au navigateur pour pouvoir être testées.
 * Le script en tête de index.html applique la même règle avant le premier affichage : les garder alignés.
 */
export type Theme = 'clair' | 'sombre';

/** Clé localStorage ; la valeur est brute ('clair' ou 'sombre') pour être lisible par le script de index.html. */
export const CLE_THEME = 'fds-theme';

/** Une valeur mémorisée invalide (ou absente) vaut « pas de choix » : on suit alors le système. */
export function themeValide(valeur: unknown): Theme | null {
  return valeur === 'clair' || valeur === 'sombre' ? valeur : null;
}

/** Le choix explicite de l'utilisateur l'emporte ; sans choix, la préférence système (prefers-color-scheme). */
export function themeEffectif(preference: Theme | null, systemeSombre: boolean): Theme {
  return preference ?? (systemeSombre ? 'sombre' : 'clair');
}

/** Valeur de l'attribut data-theme posé sur <html>. */
export function attributTheme(theme: Theme): 'light' | 'dark' {
  return theme === 'sombre' ? 'dark' : 'light';
}
