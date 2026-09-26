import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { cursusApi, CursusCard, CursusDetailModal, type CursusListItem } from '../../../entities/cursus';
import { 
  Sparkles, 
  GraduationCap, 
  ShieldCheck, 
  Smartphone, 
  ArrowRight, 
  Compass, 
  RefreshCw
} from 'lucide-react';

export const HomePage: React.FC = () => {
  const [selectedCursus, setSelectedCursus] = useState<CursusListItem | null>(null);

  const { data: cursusList = [], isLoading, isError, error, refetch } = useQuery({
    queryKey: ['cursus'],
    queryFn: cursusApi.getList,
  });

  return (
    <div className="flex flex-col min-h-screen">
      {/* 1. HERO SECTION */}
      <section className="relative overflow-hidden hero-gradient text-white pt-20 pb-28 lg:pt-28 lg:pb-36">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="max-w-3xl">
            {/* Pill Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-500/10 border border-blue-400/20 text-blue-300 text-xs font-semibold uppercase tracking-wider mb-6 backdrop-blur-md">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              <span>Session d'Admission Officielle · FDS-UEH</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-[1.15] mb-6">
              L'excellence en <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-sky-300 to-amber-300">Ingénierie & Architecture</span> à votre portée.
            </h1>

            <p className="text-lg sm:text-xl text-slate-300 leading-relaxed font-light mb-8 max-w-2xl">
              Consultez les maquettes pédagogiques de la Faculté des Sciences et postulez directement depuis votre smartphone, sans obligation de déplacement physique.
            </p>

            <div className="flex flex-wrap items-center gap-4">
              <a
                href="#catalogue"
                className="px-7 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm shadow-xl shadow-blue-600/30 transition-all hover:scale-105 flex items-center gap-2"
              >
                <span>Découvrir les formations</span>
                <ArrowRight className="w-4 h-4" />
              </a>

              <a
                href="#processus"
                className="px-6 py-3.5 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 text-slate-200 border border-slate-700/80 font-semibold text-sm backdrop-blur-md transition-all"
              >
                Guide des inscriptions
              </a>
            </div>

            {/* Quick highlights */}
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-6 mt-12 pt-10 border-t border-slate-800/80 text-xs text-slate-400">
              <div className="flex items-center gap-2.5">
                <Smartphone className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Candidature mobile 100% en ligne</span>
              </div>
              <div className="flex items-center gap-2.5">
                <ShieldCheck className="w-4 h-4 text-blue-400 shrink-0" />
                <span>Données officielles garanties</span>
              </div>
              <div className="flex items-center gap-2.5 col-span-2 sm:col-span-1">
                <Compass className="w-4 h-4 text-amber-400 shrink-0" />
                <span>Suivi de dossier transparent</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. STATS BANNER */}
      <section className="bg-white border-y border-slate-200/80 py-8 relative -mt-8 mx-4 sm:mx-8 lg:max-w-6xl lg:mx-auto rounded-2xl shadow-xl shadow-slate-200/50 z-20">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center divide-y md:divide-y-0 md:divide-x divide-slate-100">
          <div className="p-3">
            <div className="text-3xl font-extrabold text-blue-900 tracking-tight">120+</div>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mt-1">Ans de tradition académique</div>
          </div>
          <div className="p-3">
            <div className="text-3xl font-extrabold text-blue-900 tracking-tight">5</div>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mt-1">Filières d'ingénierie & d'art</div>
          </div>
          <div className="p-3">
            <div className="text-3xl font-extrabold text-blue-900 tracking-tight">100%</div>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mt-1">Procédure dématérialisée</div>
          </div>
          <div className="p-3">
            <div className="text-3xl font-extrabold text-emerald-600 tracking-tight">Ouvert</div>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mt-1">Concours d'admission 2026</div>
          </div>
        </div>
      </section>

      {/* 3. CATALOGUE / CURSUS LIST (US-001 CORE) */}
      <section id="catalogue" className="py-20 lg:py-28 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-12">
          <div>
            <div className="inline-flex items-center gap-1.5 text-xs font-bold tracking-widest text-blue-600 uppercase mb-2">
              <GraduationCap className="w-4 h-4" />
              <span>Programmes Académiques</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
              Nos Formations Officielles
            </h2>
            <p className="text-base text-slate-600 max-w-2xl mt-2">
              Sélectionnez une filière pour consulter sa maquette pédagogique complète (volume horaire, matières par niveau et prérequis).
            </p>
          </div>

          <div className="text-xs text-slate-500 bg-slate-100 px-3.5 py-2 rounded-xl self-start md:self-auto font-medium">
            Source de données : Base relationnelle FDS
          </div>
        </div>

        {/* Loading state */}
        {isLoading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-96 rounded-2xl bg-white border border-slate-200 animate-pulse p-6 flex flex-col justify-between">
                <div>
                  <div className="h-4 bg-slate-200 rounded w-1/3 mb-4" />
                  <div className="h-6 bg-slate-200 rounded w-3/4 mb-3" />
                  <div className="h-4 bg-slate-200 rounded w-full mb-2" />
                  <div className="h-4 bg-slate-200 rounded w-4/5" />
                </div>
                <div className="h-10 bg-slate-200 rounded-xl" />
              </div>
            ))}
          </div>
        )}

        {/* Error state */}
        {isError && (
          <div className="rounded-2xl bg-rose-50 border border-rose-200 p-8 text-center max-w-lg mx-auto">
            <p className="text-rose-800 font-semibold mb-2">Impossible de charger les cursus pour le moment.</p>
            <p className="text-xs text-rose-600 mb-4">{error instanceof Error ? error.message : 'Erreur inconnue'}</p>
            <button
              onClick={() => refetch()}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-rose-600 text-white text-xs font-semibold hover:bg-rose-700 transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Réessayer
            </button>
          </div>
        )}

        {/* Cursus Grid */}
        {!isLoading && !isError && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {cursusList.map((cursus) => (
              <CursusCard
                key={cursus.id}
                cursus={cursus}
                onSelect={(c) => setSelectedCursus(c)}
              />
            ))}
          </div>
        )}
      </section>

      {/* 4. PROCESSUS D'ADMISSION */}
      <section id="processus" className="py-20 bg-slate-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl font-extrabold tracking-tight mb-4">
              Comment postuler à la FDS ?
            </h2>
            <p className="text-slate-400 text-sm sm:text-base">
              Une procédure transparente et dématérialisée, conçue pour vous éviter tout déplacement inutile.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-8 rounded-2xl bg-slate-800/80 border border-slate-700/80 relative">
              <span className="w-10 h-10 rounded-xl bg-blue-600 text-white font-extrabold flex items-center justify-center text-lg mb-6 shadow-md shadow-blue-600/30">
                1
              </span>
              <h3 className="text-lg font-bold mb-2">Consultez les filières</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Prenez connaissance des prérequis académiques et vérifiez les dates limites d'inscription propres à chaque département.
              </p>
            </div>

            <div className="p-8 rounded-2xl bg-slate-800/80 border border-slate-700/80 relative">
              <span className="w-10 h-10 rounded-xl bg-blue-600 text-white font-extrabold flex items-center justify-center text-lg mb-6 shadow-md shadow-blue-600/30">
                2
              </span>
              <h3 className="text-lg font-bold mb-2">Déposez votre dossier</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Remplissez le formulaire en ligne et téléversez vos pièces justificatives (acte de naissance, relevés, photo) au format PDF/JPG.
              </p>
            </div>

            <div className="p-8 rounded-2xl bg-slate-800/80 border border-slate-700/80 relative">
              <span className="w-10 h-10 rounded-xl bg-blue-600 text-white font-extrabold flex items-center justify-center text-lg mb-6 shadow-md shadow-blue-600/30">
                3
              </span>
              <h3 className="text-lg font-bold mb-2">Suivez votre statut</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Grâce à votre numéro de référence unique, suivez l'instruction de votre candidature et recevez vos convocations aux épreuves.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Modal Détail Cursus */}
      <CursusDetailModal
        cursus={selectedCursus}
        onClose={() => setSelectedCursus(null)}
      />
    </div>
  );
};
