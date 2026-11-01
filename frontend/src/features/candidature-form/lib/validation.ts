import {
  DEPARTEMENTS,
  type ErreursChamps,
  type InformationsPersonnelles,
} from '../../../entities/candidature';

const AGE_MINIMUM = 14;
const AGE_MAXIMUM = 90;

const RE_EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const RE_TELEPHONE = /^(?:\+?509)?[234]\d{7}$/;
const RE_LETTRE = /\p{L}/u;

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
  if (!texte) return `${libelle} obligatoire.`;
  if (texte.length > 100 || !RE_LETTRE.test(texte)) return `${libelle} invalide.`;
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

  const nom = validerNom(v.nom, 'Nom');
  if (nom) erreurs.nom = nom;
  const prenom = validerNom(v.prenom, 'Prénom');
  if (prenom) erreurs.prenom = prenom;

  if (!v.date_naissance) {
    erreurs.date_naissance = 'Date de naissance obligatoire.';
  } else {
    const naissance = new Date(`${v.date_naissance}T00:00:00`);
    if (Number.isNaN(naissance.getTime())) {
      erreurs.date_naissance = 'Date de naissance invalide.';
    } else if (naissance > aujourdhui) {
      erreurs.date_naissance = 'La date de naissance ne peut pas être dans le futur.';
    } else if (age(naissance, aujourdhui) < AGE_MINIMUM || age(naissance, aujourdhui) > AGE_MAXIMUM) {
      erreurs.date_naissance = `Date de naissance invalide (âge attendu : ${AGE_MINIMUM} à ${AGE_MAXIMUM} ans).`;
    }
  }

  if (v.sexe !== 'M' && v.sexe !== 'F') erreurs.sexe = 'Sexe obligatoire.';

  const telephone = v.telephone.replace(/[\s.-]/g, '');
  if (!telephone) erreurs.telephone = 'Téléphone obligatoire.';
  else if (!RE_TELEPHONE.test(telephone)) erreurs.telephone = 'Numéro haïtien invalide (8 chiffres, ex. 37 12 34 56).';

  const email = v.email.trim();
  if (!email) erreurs.email = 'Email obligatoire.';
  else if (email.length > 255 || !RE_EMAIL.test(email)) erreurs.email = 'Adresse email invalide.';

  if (!v.departement) erreurs.departement = 'Département obligatoire.';
  else if (!(DEPARTEMENTS as readonly string[]).includes(v.departement)) erreurs.departement = 'Département inconnu.';

  const commune = v.commune.trim();
  if (!commune) erreurs.commune = 'Commune obligatoire.';
  else if (commune.length > 100) erreurs.commune = 'Commune invalide.';

  return erreurs;
}
