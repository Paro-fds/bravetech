import { normaliserReference } from './types';

const CLE_STOCKAGE = 'fds-suivi-naissances';

function lireCarte(): Record<string, string> {
  try {
    const brut = sessionStorage.getItem(CLE_STOCKAGE);
    if (!brut) return {};
    const decode: unknown = JSON.parse(brut);
    return decode && typeof decode === 'object' ? (decode as Record<string, string>) : {};
  } catch {
    return {};
  }
}

function ecrireCarte(carte: Record<string, string>): void {
  try {
    sessionStorage.setItem(CLE_STOCKAGE, JSON.stringify(carte));
  } catch {
    // sessionStorage indisponible (navigation privée stricte) : ignoré sans erreur
  }
}

/** Date de naissance mémorisée pour l'onglet en cours (jamais exposée dans l'URL). */
export function lireNaissanceSuivi(reference: string): string | null {
  const cle = normaliserReference(reference);
  return cle ? lireCarte()[cle] ?? null : null;
}

/** Mémorise la date de naissance vérifiée d'un dossier pour la durée de l'onglet uniquement. */
export function memoriserNaissanceSuivi(reference: string, dateNaissance: string): void {
  const cle = normaliserReference(reference);
  const valeur = dateNaissance.trim();
  if (!cle || !valeur) return;
  const carte = lireCarte();
  carte[cle] = valeur;
  ecrireCarte(carte);
}

/** Retire la date de naissance mémorisée lorsqu'elle est refusée par le serveur. */
export function oublierNaissanceSuivi(reference: string): void {
  const cle = normaliserReference(reference);
  if (!cle) return;
  const carte = lireCarte();
  if (!(cle in carte)) return;
  delete carte[cle];
  ecrireCarte(carte);
}

