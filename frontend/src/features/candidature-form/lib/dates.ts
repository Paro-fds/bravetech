import { useLangue } from '../../../shared/i18n/useLangue';

/** Fuseau d'affichage des dates : l'heure d'Haïti. Les dates sont toujours stockées et échangées en UTC. */
const FUSEAU_AFFICHAGE = 'America/Port-au-Prince';

const MOIS_KREYOL = ['janvye', 'fevriye', 'mas', 'avril', 'me', 'jen', 'jiyè', 'out', 'septanm', 'oktòb', 'novanm', 'desanm'];

const estKreyol = () => useLangue.getState().langue === 'kr';

/** Jour, mois (1 à 12) et année d'un instant, lus dans le fuseau d'Haïti. */
function composantes(date: Date): { jour: number; mois: number; annee: number } {
  const parties = new Intl.DateTimeFormat('fr-FR', {
    timeZone: FUSEAU_AFFICHAGE,
    day: 'numeric',
    month: 'numeric',
    year: 'numeric',
  }).formatToParts(date);
  const lire = (type: string) => Number(parties.find((p) => p.type === type)?.value);
  return { jour: lire('day'), mois: lire('month'), annee: lire('year') };
}

/** « 14 mai 2008 » / « 14 me 2008 » à partir d'une date AAAA-MM-JJ (sans conversion de fuseau : c'est une date civile). */
export function formaterDateNaissance(valeur: string): string {
  const [annee, mois, jour] = valeur.split('-').map(Number);
  if (!annee || !mois || !jour) return valeur;
  if (estKreyol()) return `${jour} ${MOIS_KREYOL[mois - 1]} ${annee}`;
  return new Date(Date.UTC(annee, mois - 1, jour)).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  });
}

/** « 27 octobre 2026 » / « 27 oktòb 2026 » à partir d'un horodatage ISO-8601 en UTC, au jour d'Haïti. */
export function formaterJour(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  if (estKreyol()) {
    const { jour, mois, annee } = composantes(date);
    return `${jour} ${MOIS_KREYOL[mois - 1]} ${annee}`;
  }
  return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric', timeZone: FUSEAU_AFFICHAGE });
}

/** « 27/10/2026 » à partir d'un horodatage ISO-8601 en UTC, au jour d'Haïti (tableaux de l'administration). */
export function formaterJourCourt(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return date.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', timeZone: FUSEAU_AFFICHAGE });
}

/** « 1 novembre 2026 à 13:45 (heure d'Haïti) » / « 1 novanm 2026 a 13:45 (lè Ayiti) » à partir d'un horodatage ISO-8601 en UTC. */
export function formaterHorodatage(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  const jour = formaterJour(iso);
  const heure = date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit', timeZone: FUSEAU_AFFICHAGE });
  return estKreyol() ? `${jour} a ${heure} (lè Ayiti)` : `${jour} à ${heure} (heure d'Haïti)`;
}
