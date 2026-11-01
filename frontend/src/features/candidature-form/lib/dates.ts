/** Fuseau d'affichage des dates : l'heure d'Haïti. Les dates sont toujours stockées et échangées en UTC. */
const FUSEAU_AFFICHAGE = 'America/Port-au-Prince';

/** « 14 mai 2008 » à partir d'une date AAAA-MM-JJ (sans conversion de fuseau : c'est une date civile). */
export function formaterDateNaissance(valeur: string): string {
  const [annee, mois, jour] = valeur.split('-').map(Number);
  if (!annee || !mois || !jour) return valeur;
  return new Date(Date.UTC(annee, mois - 1, jour)).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  });
}

/** « 27 octobre 2026 » à partir d'un horodatage ISO-8601 en UTC, au jour d'Haïti. */
export function formaterJour(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric', timeZone: FUSEAU_AFFICHAGE });
}

/** « 1 novembre 2026 à 13:45 (heure d'Haïti) » à partir d'un horodatage ISO-8601 en UTC. */
export function formaterHorodatage(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  const jour = date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric', timeZone: FUSEAU_AFFICHAGE });
  const heure = date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit', timeZone: FUSEAU_AFFICHAGE });
  return `${jour} à ${heure} (heure d'Haïti)`;
}
