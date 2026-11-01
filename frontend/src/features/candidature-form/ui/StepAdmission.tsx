import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { BarreAction, CLASSE_BOUTON_PRIMAIRE, CLASSE_BOUTON_SECONDAIRE } from './BarreAction';
import { useT } from '../../../shared/i18n/useT';
import type { Cle } from '../../../shared/i18n/fr';

interface StepAdmissionProps {
  deplacementPhysique: boolean | null;
  onChange: (valeur: boolean) => void;
  /** Envoie la réponse au serveur ; rejette en cas d'erreur. */
  onSoumettre: (valeur: boolean) => Promise<void>;
  onRetour: () => void;
}

const OPTIONS: { valeur: boolean; cle: Cle }[] = [
  { valeur: false, cle: 'adm.optNon' },
  { valeur: true, cle: 'adm.optOui' },
];

/** Étape 2 : rappel de l'admission unique au MPC et question obligatoire sur le déplacement physique (maquette 2/4). */
export const StepAdmission: React.FC<StepAdmissionProps> = ({ deplacementPhysique, onChange, onSoumettre, onRetour }) => {
  const t = useT();
  const [erreur, setErreur] = useState<string | null>(null);
  const [enCours, setEnCours] = useState(false);

  const soumettre = async (e: React.FormEvent) => {
    e.preventDefault();
    if (deplacementPhysique === null) {
      setErreur(t('adm.repondre'));
      return;
    }
    setErreur(null);
    setEnCours(true);
    try {
      await onSoumettre(deplacementPhysique);
    } catch {
      setErreur(t('adm.erreur'));
    } finally {
      setEnCours(false);
    }
  };

  return (
    <form onSubmit={soumettre} noValidate className="flex flex-col gap-[22px] flex-1">
      <section className="flex flex-col gap-3">
        <h1 className="font-fds-serif text-2xl font-bold text-fds-navy-d">{t('adm.titre')}</h1>
        <div className="rounded-xl border-2 border-fds-navy bg-fds-navy-t p-4 flex flex-col gap-2">
          <span className="self-start rounded-full bg-fds-ok-bg text-fds-ok text-[13px] font-semibold px-2.5 py-0.5">
            {t('cursus.badgeAdmission')}
          </span>
          <h2 className="font-fds-serif text-lg font-bold text-fds-navy-d">{t('adm.mpc')}</h2>
          <p className="text-sm">{t('adm.texte')}</p>
        </div>
        <Link to="/cursus/mpc" className="text-fds-navy font-semibold underline min-h-11 inline-flex items-center self-start">
          {t('adm.lienFiche')}
        </Link>
      </section>

      <hr className="border-fds-line" />

      <fieldset className="flex flex-col gap-2.5" aria-describedby={erreur ? 'erreur-deplacement' : undefined}>
        <legend className="font-fds-serif text-xl font-bold text-fds-navy-d mb-1">{t('adm.dernier')}</legend>
        <p className="text-sm text-fds-mute">
          {t('adm.aide')} <strong className="text-fds-ink">{t('adm.obligatoire')}</strong>
        </p>
        <p className="font-semibold">{t('adm.question')}</p>
        {OPTIONS.map((option) => {
          const choisi = deplacementPhysique === option.valeur;
          return (
            <label
              key={String(option.valeur)}
              className={`flex items-center gap-3 rounded-[10px] border-2 p-3.5 min-h-12 cursor-pointer ${
                choisi ? 'border-fds-navy bg-fds-navy-t' : 'border-fds-line bg-white'
              }`}
            >
              <input
                type="radio"
                name="deplacement_physique"
                className="w-5 h-5 accent-[#01346d]"
                checked={choisi}
                onChange={() => {
                  onChange(option.valeur);
                  setErreur(null);
                }}
              />
              <span className="font-semibold">{t(option.cle)}</span>
            </label>
          );
        })}
        {erreur && (
          <p id="erreur-deplacement" role="alert" className="text-sm font-semibold text-fds-bad">
            {erreur}
          </p>
        )}
      </fieldset>

      <BarreAction>
        <div className="flex gap-3">
          <button type="button" onClick={onRetour} className={CLASSE_BOUTON_SECONDAIRE}>
            {t('commun.retour')}
          </button>
          <button type="submit" disabled={enCours} className={`${CLASSE_BOUTON_PRIMAIRE} flex-1`}>
            <span>{enCours ? t('cand.enregistrement') : t('cand.continuer')}</span>
            {!enCours && <ArrowRight className="w-5 h-5" aria-hidden="true" />}
          </button>
        </div>
      </BarreAction>
    </form>
  );
};
