import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { cursusApi, CursusCard, trierBranches } from '../../../entities/cursus';
import { FORMAT_REFERENCE, normaliserReference } from '../../../entities/candidature';
import { calendrierApi } from '../../../entities/calendrier';
import { formaterDateCivile } from '../../../features/candidature-form';
import { useT } from '../../../shared/i18n';
import { PhotoCampus } from '../../../shared/ui/PhotoCampus';
import { IllustrationDossier } from './IllustrationDossier';

const ETAPES = [1, 2, 3, 4, 5] as const;

const CLASSE_BOUTON = 'min-h-12 px-5 rounded-lg font-semibold flex items-center justify-center text-center transition-colors';

/** Badge du bandeau d'accueil, d'après le calendrier réglé par l'administration (US-028). */
const BadgeAdmissions: React.FC = () => {
  const t = useT();
  const { data: calendrier } = useQuery({ queryKey: ['calendrier'], queryFn: calendrierApi.obtenir });
  let texte = t('accueil.badge');
  if (calendrier?.etat === 'ouverte' && calendrier.date_limite) texte = t('accueil.badgeJusquau', { date: formaterDateCivile(calendrier.date_limite) });
  if (calendrier?.etat === 'a_venir' && calendrier.date_ouverture) texte = t('accueil.badgeAVenir', { date: formaterDateCivile(calendrier.date_ouverture) });
  if (calendrier?.etat === 'fermee') texte = t('accueil.badgeFermees');
  return <span className="self-start rounded-full bg-white/15 px-2.5 py-0.5 text-[13px] font-semibold">{texte}</span>;
};

/** Carte « Vous avez déjà candidaté ? » du bureau : la référence ouvre directement le suivi du dossier. */
const RechercheRapide: React.FC = () => {
  const t = useT();
  const navigate = useNavigate();
  const [saisie, setSaisie] = useState('');
  const [erreur, setErreur] = useState(false);

  const ouvrir = (e: React.FormEvent) => {
    e.preventDefault();
    const reference = normaliserReference(saisie);
    if (!FORMAT_REFERENCE.test(reference)) {
      setErreur(true);
      return;
    }
    navigate(`/suivi/${reference}`);
  };

  return (
    <form
      onSubmit={ouvrir}
      noValidate
      className="relative -mt-14 rounded-xl border border-fds-line bg-fds-surface p-5 shadow-lg shadow-fds-navy-d/10 flex flex-wrap items-end gap-4"
    >
      <div className="flex-[1_1_220px] flex flex-col gap-1 self-center">
        <h2 className="font-semibold">{t('accueil.dejaBureauTitre')}</h2>
        <p className="text-sm text-fds-mute">{t('accueil.dejaBureauTexte')}</p>
      </div>
      <div className="flex-[1_1_260px] flex flex-col gap-1.5">
        <label htmlFor="reference-rapide" className="text-[15px] font-semibold">
          {t('suivi.refLabel')}
        </label>
        <input
          id="reference-rapide"
          value={saisie}
          onChange={(e) => {
            setSaisie(e.target.value);
            setErreur(false);
          }}
          placeholder="CAN-2026-0089"
          autoCapitalize="characters"
          autoComplete="off"
          spellCheck={false}
          aria-invalid={erreur}
          aria-describedby={erreur ? 'reference-rapide-erreur' : undefined}
          className={`w-full min-h-12 rounded-lg border-[1.5px] bg-fds-surface px-3 text-base text-fds-ink focus:outline-none focus:ring-2 focus:ring-fds-accent ${erreur ? 'border-fds-bad' : 'border-fds-field'}`}
        />
      </div>
      <button type="submit" className={`${CLASSE_BOUTON} min-w-50 bg-fds-navy hover:bg-fds-navy-d text-white`}>
        {t('accueil.voirAvancement')}
      </button>
      {erreur && (
        <p id="reference-rapide-erreur" role="alert" className="basis-full text-[13px] font-semibold text-fds-bad">
          {t('suivi.formatErreur')}
        </p>
      )}
    </form>
  );
};

/** Accueil du portail (maquettes « Accueil » mobile et bureau). */
export const HomePage: React.FC = () => {
  const t = useT();
  const { data: cursusList = [], isLoading, isError, refetch } = useQuery({
    queryKey: ['cursus'],
    queryFn: cursusApi.getList,
  });

  // Admission unique : le MPC est le cursus d'entrée, les autres sont les branches choisies ensuite
  const admission = cursusList.find((c) => c.est_admission);
  const branches = trierBranches(cursusList.filter((c) => !c.est_admission));

  return (
    <>
      <section className="bg-fds-navy text-white">
        <div className="max-w-5xl mx-auto px-4 py-8 md:py-14 lg:pb-20 flex items-center gap-10">
          <div className="flex-[1_1_480px] flex flex-col gap-4">
            <BadgeAdmissions />
            <h1 className="font-fds-serif text-[30px] md:text-[44px] leading-tight font-bold">{t('accueil.titre')}</h1>
            <p className="text-fds-on-navy md:text-lg max-w-xl">{t('accueil.sousTitre')}</p>
            <div className="flex flex-col sm:flex-row gap-3 pt-1">
              <Link to="/postuler" className={`${CLASSE_BOUTON} sm:min-w-50 bg-fds-gold text-fds-on-light hover:brightness-95`}>
                {t('accueil.postuler')}
              </Link>
              <Link to="/suivi" className={`${CLASSE_BOUTON} sm:min-w-50 border-2 border-white text-white hover:bg-white/10`}>
                {t('accueil.suivre')}
              </Link>
            </div>
          </div>
          <IllustrationDossier className="hidden lg:block flex-[0_1_380px]" />
        </div>
      </section>

      <div className="max-w-5xl w-full mx-auto px-4 py-6 md:py-10 lg:pt-0 flex flex-col gap-8 md:gap-12">
        <div className="hidden lg:block">
          <RechercheRapide />
        </div>

        <section className="flex flex-col gap-4" aria-labelledby="comment">
          <h2 id="comment" className="font-fds-serif text-2xl md:text-3xl font-bold text-fds-title">
            {t('accueil.comment')}
          </h2>
          <ol className="rounded-xl border border-fds-line bg-fds-surface p-4 grid gap-4 md:grid-cols-3 lg:grid-cols-5 md:border-0 md:bg-transparent md:p-0">
            {ETAPES.map((n) => (
              <li key={n} className="flex gap-3 items-start md:flex-col md:gap-2.5 md:rounded-xl md:border md:border-fds-line md:bg-fds-surface md:p-4">
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
          <h2 id="cursus" className="font-fds-serif text-2xl md:text-3xl font-bold text-fds-title">
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
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {branches.map((c) => (
                  <CursusCard key={c.id} cursus={c} />
                ))}
              </div>
            </>
          )}
        </section>

        <div className="grid gap-6">
          {/* Sur ordinateur, la recherche rapide sous le bandeau remplace ce bloc (maquette bureau) */}
          <section className="lg:hidden rounded-xl border border-fds-accent-line bg-fds-navy-t p-4 md:p-6 flex flex-col gap-2.5">
            <h2 className="font-semibold text-lg">{t('accueil.dejaTitre')}</h2>
            <p className="text-sm">{t('accueil.dejaTexte')}</p>
            <Link to="/suivi" className={`${CLASSE_BOUTON} bg-fds-navy hover:bg-fds-navy-d text-white mt-auto`}>
              {t('accueil.suivre')}
            </Link>
          </section>
          {/* Sur ordinateur : texte à gauche, photo du campus à droite (maquette bureau) */}
          <section className="rounded-xl border border-fds-line bg-fds-surface flex flex-col lg:flex-row lg:items-stretch overflow-hidden lg:bg-fds-navy-t lg:border-fds-accent-line">
            <div className="flex flex-col gap-2.5 p-4 md:p-6 lg:p-8 lg:flex-1 lg:justify-center">
              <h2 className="font-semibold text-lg lg:font-fds-serif lg:text-2xl lg:font-bold lg:text-fds-title">{t('accueil.histoireTitre')}</h2>
              <p className="text-sm text-fds-mute lg:text-base lg:max-w-xl">{t('accueil.histoireTexte')}</p>
              <Link to="/histoire" className={`${CLASSE_BOUTON} border-2 border-fds-accent bg-fds-surface text-fds-accent mt-auto lg:mt-1.5 lg:self-start lg:min-w-55`}>
                {t('accueil.histoireLien')}
              </Link>
            </div>
            <figure className="hidden lg:block lg:flex-1 relative min-h-75 m-0">
              <PhotoCampus className="absolute inset-0 w-full h-full" />
            </figure>
          </section>
        </div>
      </div>
    </>
  );
};
