import React, { useState } from 'react';
import { ArrowRight, Info } from 'lucide-react';
import {
  DEPARTEMENTS,
  extraireErreursChamps,
  type ErreursChamps,
  type InformationsPersonnelles,
} from '../../../entities/candidature';
import { ApiError } from '../../../shared/api/client';
import { validerInformations } from '../lib/validation';
import { BarreAction, CLASSE_BOUTON_PRIMAIRE } from './BarreAction';
import { ChampTexte } from './ChampTexte';

interface StepInformationsProps {
  valeurs: InformationsPersonnelles;
  onChange: (valeurs: InformationsPersonnelles) => void;
  /** Envoie la saisie au serveur ; rejette en cas d'erreur (réseau, validation, doublon). */
  onSoumettre: (valeurs: InformationsPersonnelles) => Promise<void>;
}

/** Étape 1 : informations personnelles (maquette « Candidature 1/4 - Identité »). */
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
    <form onSubmit={soumettre} noValidate className="flex flex-col gap-[18px] flex-1">
      <h1 className="font-fds-serif text-2xl font-bold text-fds-navy-d">Qui êtes-vous ?</h1>

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

      <div className="flex gap-2.5 items-start rounded-[10px] border border-[#b9cbe3] bg-fds-navy-t px-3.5 py-3 text-sm text-fds-navy-d">
        <Info className="w-5 h-5 shrink-0" aria-hidden="true" />
        <span>Vos réponses sont enregistrées à chaque étape. Si votre connexion coupe, vous reprenez là où vous étiez.</span>
      </div>

      {messageGlobal && (
        <p role="alert" className="rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
          {messageGlobal}
        </p>
      )}

      <BarreAction>
        <button type="submit" disabled={enCours} className={CLASSE_BOUTON_PRIMAIRE}>
          <span>{enCours ? 'Enregistrement…' : 'Continuer'}</span>
          {!enCours && <ArrowRight className="w-5 h-5" aria-hidden="true" />}
        </button>
      </BarreAction>
    </form>
  );
};
