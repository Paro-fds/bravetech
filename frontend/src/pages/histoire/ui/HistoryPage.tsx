import React from 'react';
import { Link } from 'react-router-dom';
import { CONSEIL_DE_DIRECTION } from '../../../shared/config/institution';
import { useT } from '../../../shared/i18n/useT';
import { PhotoCampus } from '../../../shared/ui/PhotoCampus';

const ANNEES_REPERES = ['1902', '1905', '1906', '1945', '1947', '1961', '1986'] as const;

const CLASSE_TITRE_SECTION = 'font-fds-serif text-xl lg:text-3xl font-bold text-fds-title';
const CLASSE_BOUTON = 'min-h-12 px-4 rounded-lg font-semibold flex items-center justify-center text-center';

/**
 * Histoire de la Faculté (maquettes « Histoire » et « Histoire bureau », texte fourni par la Faculté).
 * Sur ordinateur : bandeau sur la photo du campus, texte à gauche, repères dans une colonne fixe à droite.
 */
export const HistoryPage: React.FC = () => {
  const t = useT();
  return (
    <>
      <section className="relative overflow-hidden bg-fds-navy text-white lg:bg-fds-navy-d lg:min-h-100 lg:flex lg:items-end">
        <PhotoCampus tailles="100vw" className="hidden lg:block absolute inset-0 w-full h-full" />
        {/* Voile marine : le titre blanc reste lisible sur la photo */}
        <div aria-hidden="true" className="hidden lg:block absolute inset-0 bg-fds-navy-d/75" />
        <div className="relative w-full max-w-3xl lg:max-w-6xl mx-auto px-4 py-8 lg:pt-14 lg:pb-12 flex flex-col gap-2.5 lg:gap-3">
          <span className="self-start rounded-full bg-white/15 px-2.5 py-0.5 text-[13px] font-semibold">{t('histoire.badge')}</span>
          <h1 className="font-fds-serif text-[28px] lg:text-[46px] leading-tight font-bold lg:max-w-3xl">{t('histoire.titre')}</h1>
          <p className="text-fds-on-navy lg:text-white/90 lg:text-lg">{t('histoire.sousTitre')}</p>
        </div>
      </section>

      <div className="max-w-3xl lg:max-w-6xl w-full mx-auto px-4 py-6 lg:py-12 grid gap-6 lg:grid-cols-[3fr_1fr] lg:gap-x-12 lg:gap-y-9 lg:text-lg">
        <section className="flex flex-col gap-3 lg:col-start-1">
          <h2 className={CLASSE_TITRE_SECTION}>{t('histoire.fondationTitre')}</h2>
          <p>{t('histoire.fondation1')}</p>
          <p>{t('histoire.fondation2')}</p>
        </section>

        {/* Sur ordinateur, les repères forment la colonne de droite et restent visibles au défilement */}
        <section className="flex flex-col gap-3.5 lg:col-start-2 lg:row-start-1 lg:row-span-3 lg:self-start lg:sticky lg:top-4" aria-labelledby="reperes">
          <h2 id="reperes" className="font-fds-serif text-xl font-bold text-fds-title">
            {t('histoire.reperesTitre')}
          </h2>
          <ol className="rounded-xl border border-fds-line bg-fds-surface p-4 flex flex-col gap-3.5 lg:text-base">
            {ANNEES_REPERES.map((annee) => (
              <li key={annee} className="flex gap-3 items-start">
                <span className="min-w-14 text-center rounded-lg bg-fds-navy text-white text-sm font-bold px-2 py-1">{annee}</span>
                <span className="flex-1 text-sm pt-1">{t(`histoire.repere.${annee}`)}</span>
              </li>
            ))}
          </ol>
        </section>

        <section className="flex flex-col gap-3 lg:col-start-1">
          <h2 className={CLASSE_TITRE_SECTION}>{t('histoire.offreTitre')}</h2>
          <p>{t('histoire.offre1')}</p>
          <p>{t('histoire.offre2')}</p>
        </section>

        <section className="flex flex-col gap-3 lg:col-start-1">
          <h2 className={CLASSE_TITRE_SECTION}>{t('histoire.gouvernanceTitre')}</h2>
          <p>{t('histoire.gouvernance')}</p>
          {CONSEIL_DE_DIRECTION.confirme && (
            <div className="rounded-xl border border-fds-line bg-fds-surface p-4 flex flex-col gap-1.5">
              <div className="text-sm text-fds-mute">{t('histoire.conseil')}</div>
              {CONSEIL_DE_DIRECTION.membres.map((nom) => (
                <div key={nom} className="font-semibold">
                  {nom}
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="lg:col-span-2 rounded-xl border border-fds-accent-line bg-fds-navy-t p-4 lg:p-8 flex flex-col lg:flex-row lg:items-center gap-2.5 lg:gap-6 lg:text-base">
          <div className="flex flex-col gap-2.5 lg:flex-1">
            <h2 className="font-semibold text-lg lg:font-fds-serif lg:text-2xl lg:font-bold lg:text-fds-title">{t('histoire.aujourdhuiTitre')}</h2>
            <p className="text-sm lg:text-base">{t('histoire.aujourdhuiTexte')}</p>
          </div>
          <Link to="/postuler" className={`${CLASSE_BOUTON} bg-fds-navy hover:bg-fds-navy-d text-white lg:min-w-55`}>
            {t('histoire.rejoindre')}
          </Link>
          <Link to="/" className={`${CLASSE_BOUTON} border-2 border-fds-accent bg-fds-surface text-fds-accent lg:min-w-55`}>
            {t('histoire.voirCursus')}
          </Link>
        </section>
      </div>
    </>
  );
};
