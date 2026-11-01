import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { cursusApi, CursusCard } from '../../../entities/cursus';

const ETAPES = [
  { titre: 'Découvrez le parcours', texte: 'Lisez la fiche du MPC, les pièces à fournir et les dates clés.' },
  { titre: 'Remplissez le formulaire', texte: 'Vos informations, en quelques minutes.' },
  { titre: 'Payez les frais (simulation)', texte: "MonCash ou NatCash. Aucun argent réel n'est prélevé pendant cette phase." },
  { titre: 'Déposez vos pièces', texte: 'Photographiez ou importez vos documents (PDF ou JPG, 5 Mo max).' },
  { titre: 'Suivez votre dossier', texte: 'Une référence vous est remise. Pas besoin de compte.' },
];

const CLASSE_BOUTON = 'min-h-12 px-5 rounded-lg font-semibold flex items-center justify-center text-center transition-colors';

/** Accueil du portail (maquettes « Accueil » mobile et bureau). */
export const HomePage: React.FC = () => {
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
          <span className="self-start rounded-full bg-white/15 px-2.5 py-0.5 text-[13px] font-semibold">Admissions ouvertes</span>
          <h1 className="font-fds-serif text-[30px] md:text-[44px] leading-tight font-bold">
            Candidatez à la Faculté des Sciences, sans vous déplacer.
          </h1>
          <p className="text-[#dbe6f5] md:text-lg">
            Consultez les cursus, déposez votre dossier et suivez son traitement depuis votre téléphone.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 pt-1">
            <Link to="/postuler" className={`${CLASSE_BOUTON} bg-fds-gold text-fds-navy-d hover:brightness-95`}>
              Postuler maintenant
            </Link>
            <Link to="/suivi" className={`${CLASSE_BOUTON} border-2 border-white text-white hover:bg-white/10`}>
              Suivre mon dossier
            </Link>
          </div>
          </div>
        </div>
      </section>

      <div className="max-w-5xl w-full mx-auto px-4 py-6 md:py-10 flex flex-col gap-8 md:gap-12">
        <section className="flex flex-col gap-4" aria-labelledby="comment">
          <h2 id="comment" className="font-fds-serif text-2xl font-bold text-fds-navy-d">
            Comment ça marche
          </h2>
          <ol className="rounded-xl border border-fds-line bg-white p-4 md:p-6 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {ETAPES.map((etape, i) => (
              <li key={etape.titre} className="flex gap-3 items-start">
                <span className="w-8 h-8 rounded-full bg-fds-navy text-white font-bold flex items-center justify-center shrink-0" aria-hidden="true">
                  {i + 1}
                </span>
                <div>
                  <div className="font-semibold">{etape.titre}</div>
                  <div className="text-sm text-fds-mute">{etape.texte}</div>
                </div>
              </li>
            ))}
          </ol>
        </section>

        <section className="flex flex-col gap-4" aria-labelledby="cursus">
          <h2 id="cursus" className="font-fds-serif text-2xl font-bold text-fds-navy-d">
            Une admission, puis votre branche
          </h2>

          {isLoading && (
            <p className="text-fds-mute" role="status">
              Chargement des cursus…
            </p>
          )}
          {isError && (
            <div role="alert" className="rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad flex flex-col gap-2">
              <span>Impossible de charger les cursus pour le moment. Vérifiez votre connexion.</span>
              <button type="button" onClick={() => void refetch()} className="self-start min-h-11 font-semibold underline">
                Réessayer
              </button>
            </div>
          )}

          {admission && <CursusCard cursus={admission} />}

          {branches.length > 0 && (
            <>
              <h3 className="font-fds-serif text-lg font-bold text-fds-navy-d pt-2">Ensuite, vous choisissez votre branche (3 ans)</h3>
              <div className="grid gap-4 md:grid-cols-2">
                {branches.map((c) => (
                  <CursusCard key={c.id} cursus={c} />
                ))}
              </div>
            </>
          )}
        </section>

        <div className="grid gap-6 md:grid-cols-2">
          <section className="rounded-xl border border-[#b9cbe3] bg-fds-navy-t p-4 md:p-6 flex flex-col gap-2.5">
            <h2 className="font-semibold text-lg">Déjà candidat ?</h2>
            <p className="text-sm">Entrez votre référence (par exemple CAN-2026-0089) pour voir où en est votre dossier.</p>
            <Link to="/suivi" className={`${CLASSE_BOUTON} bg-fds-navy hover:bg-fds-navy-d text-white mt-auto`}>
              Suivre mon dossier
            </Link>
          </section>
          <section className="rounded-xl border border-fds-line bg-white p-4 md:p-6 flex flex-col gap-2.5">
            <h2 className="font-semibold text-lg">Une institution historique</h2>
            <p className="text-sm text-fds-mute">
              Fondée en 1902, la Faculté des Sciences est l'un des plus anciens établissements d'enseignement supérieur d'Haïti.
            </p>
            <Link to="/histoire" className={`${CLASSE_BOUTON} border-2 border-fds-navy bg-white text-fds-navy mt-auto`}>
              Lire notre histoire
            </Link>
          </section>
        </div>
      </div>
    </>
  );
};
