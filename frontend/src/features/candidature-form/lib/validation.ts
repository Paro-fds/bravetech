import {
  DEPARTEMENTS,
  type ErreursChamps,
  type InformationsPersonnelles,
} from '../../../entities/candidature';
import { traduireMaintenant as tr } from '../../../shared/i18n/useT';

const AGE_MINIMUM = 14;
const AGE_MAXIMUM = 90;

const RE_EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const RE_TELEPHONE = /^(?:\+?509)?[234]\d{7}$/;
const RE_LETTRE = /\p{L}/u;

/** Valide un numéro mobile haïtien (8 chiffres, indicatif +509 facultatif). Retourne un message d'erreur ou undefined. */
export function validerNumeroHaitien(valeur: string): string | undefined {
  const numero = valeur.replace(/[\s.-]/g, '');
  if (!numero) return tr('val.numObligatoire');
  if (!RE_TELEPHONE.test(numero)) return tr('val.numInvalide');
  return undefined;
}

function age(naissance: Date, aujourdhui: Date): number {
  let a = aujourdhui.getFullYear() - naissance.getFullYear();
  const avantAnniversaire =
    aujourdhui.getMonth() < naissance.getMonth() ||
    (aujourdhui.getMonth() === naissance.getMonth() && aujourdhui.getDate() < naissance.getDate());
  if (avantAnniversaire) a -= 1;
  return a;
}

function validerNom(valeur: string, libelle: string): string | undefined {
  const texte = valeur.trim();
  if (!texte) return tr('val.champObligatoire', { champ: libelle });
  if (texte.length > 100 || !RE_LETTRE.test(texte)) return tr('val.champInvalide', { champ: libelle });
  return undefined;
}

/**
 * Validation côté client de l'étape 1 : même règles que le serveur, pour un retour immédiat.
 * Le serveur reste l'autorité (il revalide toujours la saisie).
 */
export function validerInformations(
  v: InformationsPersonnelles,
  aujourdhui: Date = new Date(),
): ErreursChamps {
  const erreurs: ErreursChamps = {};

  const nom = validerNom(v.nom, tr('val.libNom'));
  if (nom) erreurs.nom = nom;
  const prenom = validerNom(v.prenom, tr('val.libPrenom'));
  if (prenom) erreurs.prenom = prenom;

  if (!v.date_naissance) {
    erreurs.date_naissance = tr('val.naissObligatoire');
  } else {
    const naissance = new Date(`${v.date_naissance}T00:00:00`);
    if (Number.isNaN(naissance.getTime())) {
      erreurs.date_naissance = tr('val.naissInvalide');
    } else if (naissance > aujourdhui) {
      erreurs.date_naissance = tr('val.naissFutur');
    } else if (age(naissance, aujourdhui) < AGE_MINIMUM || age(naissance, aujourdhui) > AGE_MAXIMUM) {
      erreurs.date_naissance = tr('val.naissAge', { min: AGE_MINIMUM, max: AGE_MAXIMUM });
    }
  }

  if (v.sexe !== 'M' && v.sexe !== 'F') erreurs.sexe = tr('val.sexeObligatoire');

  const telephone = v.telephone.replace(/[\s.-]/g, '');
  if (!telephone) erreurs.telephone = tr('val.telObligatoire');
  else if (!RE_TELEPHONE.test(telephone)) erreurs.telephone = tr('val.numInvalide');

  const email = v.email.trim();
  if (!email) erreurs.email = tr('val.emailObligatoire');
  else if (email.length > 255 || !RE_EMAIL.test(email)) erreurs.email = tr('val.emailInvalide');

  if (!v.departement) erreurs.departement = tr('val.deptObligatoire');
  else if (!(DEPARTEMENTS as readonly string[]).includes(v.departement)) erreurs.departement = tr('val.deptInconnu');

  const commune = v.commune.trim();
  if (!commune) erreurs.commune = tr('val.communeObligatoire');
  else if (commune.length > 100) erreurs.commune = tr('val.communeInvalide');

  return erreurs;
}
