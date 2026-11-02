import React from 'react';
import { Link } from 'react-router-dom';
import { CONSEIL_DE_DIRECTION } from '../../../shared/config/institution';
import { useT } from '../../../shared/i18n/useT';

const ANNEES_REPERES = ['1902', '1905', '1906', '1945', '1947', '1961', '1986'] as const;

/** Histoire de la Faculté (maquette « Histoire », texte fourni par la Faculté). */
export const HistoryPage: React.FC = () => {
  const t = useT();
  return (
    <>
      <section className="bg-fds-navy text-white">
        <div className="max-w-3xl mx-auto px-4 py-8 flex flex-col gap-2.5">
          <span className="self-start rounded-full bg-white/15 px-2.5 py-0.5 text-[13px] font-semibold">{t('histoire.badge')}</span>
          <h1 className="font-fds-serif text-[28px] leading-tight font-bold">{t('histoire.titre')}</h1>
          <p className="text-[#dbe6f5]">{t('histoire.sousTitre')}</p>
        </div>
      </section>

      <div className="max-w-3xl w-full mx-auto px-4 py-6 flex flex-col gap-6">
        <section className="flex flex-col gap-3">
          <h2 className="font-fds-serif text-xl font-bold text-fds-navy-d">{t('histoire.fondationTitre')}</h2>
          <p>{t('histoire.fondation1')}</p>
          <p>{t('histoire.fondation2')}</p>
        </section>

        <section className="flex flex-col gap-3.5" aria-labelledby="reperes">
          <h2 id="reperes" className="font-fds-serif text-xl font-bold text-fds-navy-d">
            {t('histoire.reperesTitre')}
          </h2>
          <ol className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-3.5">
            {ANNEES_REPERES.map((annee) => (
              <li key={annee} className="flex gap-3 items-start">
                <span className="min-w-14 text-center rounded-lg bg-fds-navy text-white text-sm font-bold px-2 py-1">{annee}</span>
                <span className="flex-1 text-sm pt-1">{t(`histoire.repere.${annee}`)}</span>
              </li>
            ))}
          </ol>
        </section>

        <section className="flex flex-col gap-3">
          <h2 className="font-fds-serif text-xl font-bold text-fds-navy-d">{t('histoire.offreTitre')}</h2>
          <p>{t('histoire.offre1')}</p>
          <p>{t('histoire.offre2')}</p>
        </section>

        <section className="flex flex-col gap-3">
          <h2 className="font-fds-serif text-xl font-bold text-fds-navy-d">{t('histoire.gouvernanceTitre')}</h2>
          <p>{t('histoire.gouvernance')}</p>
          {CONSEIL_DE_DIRECTION.confirme && (
            <div className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-1.5">
              <div className="text-sm text-fds-mute">{t('histoire.conseil')}</div>
              {CONSEIL_DE_DIRECTION.membres.map((nom) => (
                <div key={nom} className="font-semibold">
                  {nom}
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="rounded-xl border border-[#b9cbe3] bg-fds-navy-t p-4 flex flex-col gap-2.5">
          <h2 className="font-semibold text-lg">{t('histoire.aujourdhuiTitre')}</h2>
          <p className="text-sm">{t('histoire.aujourdhuiTexte')}</p>
          <Link to="/postuler" className="min-h-12 px-4 rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white font-semibold flex items-center justify-center text-center">
            {t('histoire.rejoindre')}
          </Link>
          <Link to="/" className="min-h-12 px-4 rounded-lg border-2 border-fds-navy bg-white text-fds-navy font-semibold flex items-center justify-center">
            {t('histoire.voirCursus')}
          </Link>
        </section>
      </div>
    </>
  );
};
