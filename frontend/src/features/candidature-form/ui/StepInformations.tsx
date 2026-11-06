import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Info } from 'lucide-react';
import {
  DEPARTEMENTS,
  extraireErreursChamps,
  type ErreursChamps,
  type InformationsPersonnelles,
} from '../../../entities/candidature';
import { ApiError } from '../../../shared/api';
import { validerInformations } from '../lib/validation';
import { BarreAction, CLASSE_BOUTON_PRIMAIRE, CLASSE_BOUTON_SECONDAIRE } from './BarreAction';
import { ChampTexte } from './ChampTexte';
import { useT } from '../../../shared/i18n';

interface StepInformationsProps {
  valeurs: InformationsPersonnelles;
  onChange: (valeurs: InformationsPersonnelles) => void;
  /** Envoie la saisie au serveur ; rejette en cas d'erreur (réseau, validation, doublon). */
  onSoumettre: (valeurs: InformationsPersonnelles) => Promise<void>;
}

/** Étape 1 : informations personnelles (maquette « Candidature 1/4 - Identité »). */
export const StepInformations: React.FC<StepInformationsProps> = ({ valeurs, onChange, onSoumettre }) => {
  const t = useT();
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
        setErreurs({ email: t('info.doublon') });
      } else {
        setMessageGlobal(t('info.erreurReseau'));
      }
    } finally {
      setEnCours(false);
    }
  };

  return (
    <form onSubmit={soumettre} noValidate className="flex flex-col gap-[18px] flex-1">
      <h1 className="font-fds-serif text-2xl font-bold text-fds-title">{t('info.titre')}</h1>

      <ChampTexte id="nom" libelle={t('info.nom')} erreur={erreurs.nom}>
        {(p) => <input {...p} type="text" autoComplete="family-name" value={valeurs.nom} onChange={maj('nom')} />}
      </ChampTexte>

      <ChampTexte id="prenom" libelle={t('info.prenom')} erreur={erreurs.prenom}>
        {(p) => <input {...p} type="text" autoComplete="given-name" value={valeurs.prenom} onChange={maj('prenom')} />}
      </ChampTexte>

      <ChampTexte id="date_naissance" libelle={t('info.naissance')} erreur={erreurs.date_naissance}>
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

      <ChampTexte id="sexe" libelle={t('info.sexe')} erreur={erreurs.sexe}>
        {(p) => (
          <select {...p} value={valeurs.sexe} onChange={maj('sexe')}>
            <option value="">{t('info.choisir')}</option>
            <option value="F">{t('info.feminin')}</option>
            <option value="M">{t('info.masculin')}</option>
          </select>
        )}
      </ChampTexte>

      <ChampTexte
        id="telephone"
        libelle={t('info.tel')}
        erreur={erreurs.telephone}
        aide={t('info.telAide')}
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
        libelle={t('info.email')}
        erreur={erreurs.email}
        aide={t('info.emailAide')}
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

      <ChampTexte id="departement" libelle={t('info.dept')} erreur={erreurs.departement}>
        {(p) => (
          <select {...p} value={valeurs.departement} onChange={maj('departement')}>
            <option value="">{t('info.choisirDept')}</option>
            {DEPARTEMENTS.map((d) => (
              <option key={d} value={d}>
                {t(`dept.${d}`)}
              </option>
            ))}
          </select>
        )}
      </ChampTexte>

      <ChampTexte id="commune" libelle={t('info.commune')} erreur={erreurs.commune}>
        {(p) => <input {...p} type="text" autoComplete="address-level2" value={valeurs.commune} onChange={maj('commune')} />}
      </ChampTexte>

      <div className="flex gap-2.5 items-start rounded-[10px] border border-fds-accent-line bg-fds-navy-t px-3.5 py-3 text-sm text-fds-title">
        <Info className="w-5 h-5 shrink-0" aria-hidden="true" />
        <span>{t('info.sauvegarde')}</span>
      </div>

      {messageGlobal && (
        <p role="alert" className="rounded-[10px] border border-fds-bad-line bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
          {messageGlobal}
        </p>
      )}

      <BarreAction>
        <div className="flex gap-3">
          {/* Les réponses sont gardées en brouillon : quitter ne perd rien (maquette « Étape 1 ») */}
          <Link to="/" className={CLASSE_BOUTON_SECONDAIRE}>
            {t('cand.quitter')}
          </Link>
          <button type="submit" disabled={enCours} className={`${CLASSE_BOUTON_PRIMAIRE} flex-1`}>
            <span>{enCours ? t('cand.enregistrement') : t('cand.continuer')}</span>
            {!enCours && <ArrowRight className="w-5 h-5" aria-hidden="true" />}
          </button>
        </div>
      </BarreAction>
    </form>
  );
};
