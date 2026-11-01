import React, { useState } from 'react';
import { ArrowRight } from 'lucide-react';
import {
  DEPARTEMENTS,
  extraireErreursChamps,
  type ErreursChamps,
  type InformationsPersonnelles,
} from '../../../entities/candidature';
import { ApiError } from '../../../shared/api/client';
import { validerInformations } from '../lib/validation';
import { ChampTexte } from './ChampTexte';

interface StepInformationsProps {
  valeurs: InformationsPersonnelles;
  onChange: (valeurs: InformationsPersonnelles) => void;
  /** Envoie la saisie au serveur ; rejette en cas d'erreur (réseau, validation, doublon). */
  onSoumettre: (valeurs: InformationsPersonnelles) => Promise<void>;
}

/** Étape 1 : informations personnelles. */
export const StepInformations: React.FC<StepInformationsProps> = ({ valeurs, onChange, onSoumettre }) => {
  const [erreurs, setErreurs] = useState<ErreursChamps>({});
  const [messageGlobal, setMessageGlobal] = useState<string | null>(null);
  const [enCours, setEnCours] = useState(false);

  const maj = (champ: keyof InformationsPersonnelles) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    onChange({ ...valeurs, [champ]: e.target.value });
    if (erreurs[champ]) setErreurs((prec) => ({ ...prec, [champ]: undefined }));
  };

  const soumettre = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessageGlobal(null);

    const erreursLocales = validerInformations(valeurs);
    if (Object.keys(erreursLocales).length > 0) {
      setErreurs(erreursLocales);
      return;
    }

    setEnCours(true);
    try {
      await onSoumettre(valeurs);
    } catch (erreur) {
      const erreursServeur = extraireErreursChamps(erreur);
      if (erreursServeur) {
        setErreurs(erreursServeur);
      } else if (erreur instanceof ApiError && erreur.status === 409) {
        setErreurs({ email: 'Une candidature existe déjà avec cet email.' });
      } else {
        setMessageGlobal(
          "Impossible d'enregistrer vos informations pour le moment. Vérifiez votre connexion : ce que vous avez saisi est conservé, vous pouvez réessayer.",
        );
      }
    } finally {
      setEnCours(false);
    }
  };

  return (
    <form onSubmit={soumettre} noValidate className="flex flex-col gap-5">
      <h1 className="text-2xl font-extrabold text-slate-900">Qui êtes-vous ?</h1>

      <ChampTexte id="nom" libelle="Nom" erreur={erreurs.nom}>
        {(p) => <input {...p} type="text" autoComplete="family-name" value={valeurs.nom} onChange={maj('nom')} />}
      </ChampTexte>

      <ChampTexte id="prenom" libelle="Prénom" erreur={erreurs.prenom}>
        {(p) => <input {...p} type="text" autoComplete="given-name" value={valeurs.prenom} onChange={maj('prenom')} />}
      </ChampTexte>

      <ChampTexte id="date_naissance" libelle="Date de naissance" erreur={erreurs.date_naissance}>
        {(p) => (
          <input
            {...p}
            type="date"
            autoComplete="bday"
            value={valeurs.date_naissance}
            onChange={maj('date_naissance')}
          />
        )}
      </ChampTexte>

      <ChampTexte id="sexe" libelle="Sexe" erreur={erreurs.sexe}>
        {(p) => (
          <select {...p} value={valeurs.sexe} onChange={maj('sexe')}>
            <option value="">Choisir</option>
            <option value="F">Féminin</option>
            <option value="M">Masculin</option>
          </select>
        )}
      </ChampTexte>

      <ChampTexte
        id="telephone"
        libelle="Téléphone (WhatsApp)"
        erreur={erreurs.telephone}
        aide="Numéro haïtien à 8 chiffres. Nous l'utilisons pour vous joindre si besoin."
      >
        {(p) => (
          <input
            {...p}
            type="tel"
            inputMode="tel"
            autoComplete="tel"
            placeholder="37 12 34 56"
            value={valeurs.telephone}
            onChange={maj('telephone')}
          />
        )}
      </ChampTexte>

      <ChampTexte
        id="email"
        libelle="Adresse email"
        erreur={erreurs.email}
        aide="Votre référence de dossier y sera envoyée."
      >
        {(p) => (
          <input
            {...p}
            type="email"
            inputMode="email"
            autoComplete="email"
            placeholder="nom@exemple.com"
            value={valeurs.email}
            onChange={maj('email')}
          />
        )}
      </ChampTexte>

      <ChampTexte id="departement" libelle="Département de résidence" erreur={erreurs.departement}>
        {(p) => (
          <select {...p} value={valeurs.departement} onChange={maj('departement')}>
            <option value="">Choisir un département</option>
            {DEPARTEMENTS.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        )}
      </ChampTexte>

      <ChampTexte id="commune" libelle="Commune" erreur={erreurs.commune}>
        {(p) => <input {...p} type="text" autoComplete="address-level2" value={valeurs.commune} onChange={maj('commune')} />}
      </ChampTexte>

      <p className="rounded-xl bg-blue-50 border border-blue-200 px-3.5 py-3 text-sm text-blue-900">
        Vos réponses sont enregistrées à chaque étape. Si votre connexion coupe, vous reprenez là où vous étiez.
      </p>

      {messageGlobal && (
        <p role="alert" className="rounded-xl bg-rose-50 border border-rose-200 px-3.5 py-3 text-sm text-rose-800">
          {messageGlobal}
        </p>
      )}

      <button
        type="submit"
        disabled={enCours}
        className="min-h-12 rounded-xl bg-blue-700 hover:bg-blue-600 disabled:opacity-60 text-white font-bold flex items-center justify-center gap-2 transition-colors"
      >
        <span>{enCours ? 'Enregistrement…' : 'Continuer'}</span>
        {!enCours && <ArrowRight className="w-4 h-4" />}
      </button>
    </form>
  );
};
