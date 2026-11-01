import { accueil } from './accueil';
import { candidature } from './candidature';
import { commun } from './commun';
import { contact } from './contact';
import { cursus } from './cursus';
import { histoire } from './histoire';
import { suivi } from './suivi';

/** Dictionnaire français : langue de référence et repli. Chaque nouveau domaine s'ajoute ici. */
export const fr = { ...commun, ...accueil, ...cursus, ...histoire, ...contact, ...candidature, ...suivi } as const;

export type Cle = keyof typeof fr;
