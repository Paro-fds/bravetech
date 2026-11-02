import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { cursusApi, CursusCard } from '../../../entities/cursus';
import { useT } from '../../../shared/i18n/useT';

const ETAPES = [1, 2, 3, 4, 5] as const;

const CLASSE_BOUTON = 'min-h-12 px-5 rounded-lg font-semibold flex items-center justify-center text-center transition-colors';

/** Accueil du portail (maquettes « Accueil » mobile et bureau). */
export const HomePage: React.FC = () => {
  const t = useT();
  const { data: cursusList = [], isLoading, isError, refetch } = useQuery({
    queryKey: ['cursus'],
    queryFn: cursusApi.getList,
  });

  // Admission unique : le MPC est le cursus d'entrée, les autres sont les branches choisies ensuite
  const admission = cursusList.find((c) => c.est_admission);
  const branches = cursusList.filter((c) => !c.est_admission);

  return (
    <>
      <section className="bg-fds-navy text-white">
        <div className="max-w-5xl mx-auto px-4 py-8 md:py-14">
          <div className="flex flex-col gap-4 md:max-w-3xl">
          <span className="self-start rounded-full bg-white/15 px-2.5 py-0.5 text-[13px] font-semibold">{t('accueil.badge')}</span>
          <h1 className="font-fds-serif text-[30px] md:text-[44px] leading-tight font-bold">
            {t('accueil.titre')}
          </h1>
          <p className="text-fds-on-navy md:text-lg">
            {t('accueil.sousTitre')}
          </p>
          <div className="flex flex-col sm:flex-row gap-3 pt-1">
            <Link to="/postuler" className={`${CLASSE_BOUTON} bg-fds-gold text-fds-on-light hover:brightness-95`}>
              {t('accueil.postuler')}
            </Link>
            <Link to="/suivi" className={`${CLASSE_BOUTON} border-2 border-white text-white hover:bg-white/10`}>
              {t('accueil.suivre')}
            </Link>
          </div>
          </div>
        </div>
      </section>

      <div className="max-w-5xl w-full mx-auto px-4 py-6 md:py-10 flex flex-col gap-8 md:gap-12">
        <section className="flex flex-col gap-4" aria-labelledby="comment">
          <h2 id="comment" className="font-fds-serif text-2xl font-bold text-fds-title">
            {t('accueil.comment')}
          </h2>
          <ol className="rounded-xl border border-fds-line bg-fds-surface p-4 md:p-6 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {ETAPES.map((n) => (
              <li key={n} className="flex gap-3 items-start">
                <span className="w-8 h-8 rounded-full bg-fds-navy text-white font-bold flex items-center justify-center shrink-0" aria-hidden="true">
                  {n}
                </span>
                <div>
                  <div className="font-semibold">{t(`accueil.etape${n}.titre`)}</div>
                  <div className="text-sm text-fds-mute">{t(`accueil.etape${n}.texte`)}</div>
                </div>
              </li>
            ))}
          </ol>
        </section>

        <section className="flex flex-col gap-4" aria-labelledby="cursus">
          <h2 id="cursus" className="font-fds-serif text-2xl font-bold text-fds-title">
            {t('accueil.cursusTitre')}
          </h2>

          {isLoading && (
            <p className="text-fds-mute" role="status">
              {t('accueil.chargement')}
            </p>
          )}
          {isError && (
            <div role="alert" className="rounded-[10px] border border-fds-bad-line bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad flex flex-col gap-2">
              <span>{t('accueil.erreur')}</span>
              <button type="button" onClick={() => void refetch()} className="self-start min-h-11 font-semibold underline">
                {t('commun.reessayer')}
              </button>
            </div>
          )}

          {admission && <CursusCard cursus={admission} />}

          {branches.length > 0 && (
            <>
              <h3 className="font-fds-serif text-lg font-bold text-fds-title pt-2">{t('accueil.branches')}</h3>
              <div className="grid gap-4 md:grid-cols-2">
                {branches.map((c) => (
                  <CursusCard key={c.id} cursus={c} />
                ))}
              </div>
            </>
          )}
        </section>

        <div className="grid gap-6 md:grid-cols-2">
          <section className="rounded-xl border border-fds-accent-line bg-fds-navy-t p-4 md:p-6 flex flex-col gap-2.5">
            <h2 className="font-semibold text-lg">{t('accueil.dejaTitre')}</h2>
            <p className="text-sm">{t('accueil.dejaTexte')}</p>
            <Link to="/suivi" className={`${CLASSE_BOUTON} bg-fds-navy hover:bg-fds-navy-d text-white mt-auto`}>
              {t('accueil.suivre')}
            </Link>
          </section>
          <section className="rounded-xl border border-fds-line bg-fds-surface p-4 md:p-6 flex flex-col gap-2.5">
            <h2 className="font-semibold text-lg">{t('accueil.histoireTitre')}</h2>
            <p className="text-sm text-fds-mute">
              {t('accueil.histoireTexte')}
            </p>
            <Link to="/histoire" className={`${CLASSE_BOUTON} border-2 border-fds-accent bg-fds-surface text-fds-accent mt-auto`}>
              {t('accueil.histoireLien')}
            </Link>
          </section>
        </div>
      </div>
    </>
  );
};
