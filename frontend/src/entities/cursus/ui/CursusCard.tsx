import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { useT } from '../../../shared/i18n/useT';
import type { CursusListItem } from '../model/types';

interface CursusCardProps {
  cursus: CursusListItem;
}

/**
 * Carte de cursus de l'accueil (maquette « Accueil ») : le MPC, cursus d'admission, est mis en avant ;
 * les branches sont des cartes plus discrètes (elles se choisissent après le MPC).
 * Le nom et la description viennent des données de cursus et restent en français (spec WS-01 §1.6).
 */
export const CursusCard: React.FC<CursusCardProps> = ({ cursus }) => {
  const t = useT();
  const admission = cursus.est_admission;
  return (
    <Link
      to={`/cursus/${cursus.id}`}
      className={`rounded-xl border bg-white p-4 flex flex-col gap-2 no-underline text-inherit hover:shadow-md transition-shadow ${
        admission ? 'border-2 border-fds-navy bg-fds-navy-t' : 'border-fds-line'
      }`}
    >
      <div className="flex flex-wrap items-center gap-2">
        <h3 lang="fr" className="flex-1 basis-48 font-fds-serif text-lg font-bold text-fds-navy-d">{cursus.nom}</h3>
        {admission ? (
          <span className="rounded-full bg-fds-ok-bg text-fds-ok px-2.5 py-0.5 text-[13px] font-semibold whitespace-nowrap">{t('carte.candidatezIci')}</span>
        ) : (
          <span className="rounded-full bg-fds-navy-t text-fds-navy px-2.5 py-0.5 text-[13px] font-semibold whitespace-nowrap">{t('carte.ans', { n: cursus.duree_annees })}</span>
        )}
      </div>
      <p lang="fr" className={`text-sm ${admission ? '' : 'text-fds-mute'}`}>{cursus.description_courte}</p>
      <span className="mt-auto flex items-center gap-1.5 font-semibold text-fds-navy">
        {admission ? t('carte.voirFiche') : t('carte.decouvrir')}
        <ArrowRight className="w-5 h-5" aria-hidden="true" />
      </span>
    </Link>
  );
};
