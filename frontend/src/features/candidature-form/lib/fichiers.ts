import type { PieceDossier } from '../../../entities/candidature';
import { traduireMaintenant as tr } from '../../../shared/i18n/useT';

const OCTETS_PAR_MO = 1024 * 1024;

/** Format français : « 1,2 Mo » ou « 340 Ko ». */
export function formaterTaille(octets: number): string {
  if (octets >= OCTETS_PAR_MO) return `${(octets / OCTETS_PAR_MO).toFixed(1).replace('.', ',')} Mo`;
  return `${Math.max(1, Math.round(octets / 1024))} Ko`;
}

const EXTENSIONS_PAR_FORMAT: Record<string, string[]> = {
  PDF: ['pdf'],
  JPG: ['jpg', 'jpeg'],
  JPEG: ['jpg', 'jpeg'],
  PNG: ['png'],
};

/** Extensions acceptées pour une pièce, d'après son champ `format_accepte` (« PDF, JPG, PNG »). */
export function extensionsAcceptees(formatAccepte: string): string[] {
  const extensions = formatAccepte
    .split(',')
    .flatMap((libelle) => EXTENSIONS_PAR_FORMAT[libelle.trim().toUpperCase()] ?? []);
  return [...new Set(extensions)];
}

/** Valeur de l'attribut `accept` d'un sélecteur de fichier. */
export function attributAccept(formatAccepte: string): string {
  return extensionsAcceptees(formatAccepte)
    .map((e) => `.${e}`)
    .join(',');
}

/**
 * Contrôle rapide côté client avant l'envoi (retour immédiat, sans consommer de données mobiles).
 * Le serveur reste l'autorité : il revérifie la taille, l'extension et les octets d'en-tête du fichier.
 */
export function validerFichierLocal(
  fichier: File,
  piece: Pick<PieceDossier, 'taille_max_mo' | 'format_accepte'>,
): string | undefined {
  if (fichier.size === 0) return tr('fichier.vide');
  if (fichier.size > piece.taille_max_mo * OCTETS_PAR_MO) {
    return tr('fichier.lourd', { taille: formaterTaille(fichier.size), max: piece.taille_max_mo });
  }
  const extension = fichier.name.includes('.') ? fichier.name.split('.').pop()!.toLowerCase() : '';
  if (!extensionsAcceptees(piece.format_accepte).includes(extension)) {
    return tr('fichier.format', { formats: piece.format_accepte });
  }
  return undefined;
}
