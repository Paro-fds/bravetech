import type { Cle } from '../fr';
import { accueil } from './accueil';
import { candidature } from './candidature';
import { commun } from './commun';
import { contact } from './contact';
import { cursus } from './cursus';
import { histoire } from './histoire';
import { suivi } from './suivi';

/**
 * Dictionnaire créole, chargé à la demande (import dynamique) pour ne pas alourdir le premier chargement.
 * `Partial` : une clé non traduite retombe sur le français.
 */
export const kr: Partial<Record<Cle, string>> = { ...commun, ...accueil, ...cursus, ...histoire, ...contact, ...candidature, ...suivi };
