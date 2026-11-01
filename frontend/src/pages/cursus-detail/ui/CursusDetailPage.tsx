import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { cursusApi } from '../../../entities/cursus';
import {
  ArrowLeft,
  Calendar,
  Clock,
  CheckCircle2,
  FileCheck2,
  BookOpen,
  Layers,
  ArrowRight,
  AlertCircle,
  HelpCircle
} from 'lucide-react';

export const CursusDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [activeNiveau, setActiveNiveau] = useState<string>('');

  const { data: cursus, isLoading, isError, error } = useQuery({
    queryKey: ['cursus', id],
    queryFn: () => cursusApi.getById(id || ''),
    enabled: Boolean(id),
  });

  // Sélecteur de niveau par défaut
  React.useEffect(() => {
    if (cursus?.niveaux) {
      const keys = Object.keys(cursus.niveaux);
      if (keys.length > 0 && !activeNiveau) {
        setActiveNiveau(keys[0]);
      }
    }
  }, [cursus, activeNiveau]);

  if (isLoading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-16">
        <div className="h-6 w-32 bg-slate-200 rounded animate-pulse mb-8" />
        <div className="h-10 w-3/4 bg-slate-200 rounded animate-pulse mb-4" />
        <div className="h-4 w-1/2 bg-slate-200 rounded animate-pulse mb-12" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-2 h-96 bg-slate-200 rounded-2xl animate-pulse" />
          <div className="h-96 bg-slate-200 rounded-2xl animate-pulse" />
        </div>
      </div>
    );
  }

  if (isError || !cursus) {
    return (
      <div className="max-w-xl mx-auto px-4 py-24 text-center">
        <div className="w-16 h-16 rounded-2xl bg-rose-100 text-rose-600 flex items-center justify-center mx-auto mb-6">
          <AlertCircle className="w-8 h-8" />
        </div>
        <h1 className="text-2xl font-bold text-slate-900 mb-2">Formation introuvable</h1>
        <p className="text-slate-600 text-sm mb-6">
          {error instanceof Error ? error.message : `Le cursus demandé "${id}" n'existe pas ou n'est plus proposé.`}
        </p>
        <Link
          to="/"
          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-blue-600 text-white font-semibold text-sm hover:bg-blue-700 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Retour à l'accueil des cursus</span>
        </Link>
      </div>
    );
  }

  const matieres = cursus.niveaux?.[activeNiveau] || [];
  const niveauxKeys = Object.keys(cursus.niveaux || {});

  return (
    <div className="bg-slate-50 min-h-screen pb-24">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-blue-950 via-slate-900 to-indigo-950 text-white pt-8 pb-16 border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Back link */}
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-xs font-semibold text-blue-300 hover:text-white transition-colors mb-6"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Tous les cursus académiques</span>
          </Link>

          <div className="flex flex-wrap items-center gap-2 mb-4">
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              <CheckCircle2 className="w-3.5 h-3.5 inline mr-1" />
              Inscriptions Ouvertes 2026
            </span>
            <span className="text-xs font-medium text-slate-400">
              {cursus.est_admission ? 'FDS-UEH · Admission unique' : 'FDS-UEH · Branche, après le MPC'}
            </span>
          </div>

          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white mb-4">
            {cursus.nom}
          </h1>

          <p className="text-base sm:text-lg text-slate-300 max-w-3xl leading-relaxed mb-8">
            {cursus.description_longue || cursus.description_courte}
          </p>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md max-w-3xl text-xs">
            <div>
              <span className="text-slate-400 block mb-1 flex items-center gap-1">
                <Clock className="w-3.5 h-3.5 text-blue-400" />
                Durée :
              </span>
              <strong className="text-sm font-bold text-white">{cursus.duree_annees} ans</strong>
            </div>

            <div>
              <span className="text-slate-400 block mb-1 flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5 text-blue-400" />
                Ouverture :
              </span>
              <strong className="text-sm font-bold text-white">{cursus.date_ouverture_inscription}</strong>
            </div>

            <div>
              <span className="text-slate-400 block mb-1 flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5 text-amber-400" />
                Clôture :
              </span>
              <strong className="text-sm font-bold text-white">{cursus.date_fermeture_inscription}</strong>
            </div>

            <div>
              <span className="text-slate-400 block mb-1 flex items-center gap-1">
                <FileCheck2 className="w-3.5 h-3.5 text-emerald-400" />
                {cursus.est_admission ? 'Pièces exigées :' : 'Accès :'}
              </span>
              <strong className="text-sm font-bold text-white">
                {cursus.est_admission ? `${cursus.documents_requis?.length || 0} documents` : 'Après le MPC'}
              </strong>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column : Maquette Académique (2 cols) */}
          <div className="lg:col-span-2 space-y-6">
            {cursus.est_admission && (
              <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm">
                <h2 className="text-xl font-bold text-slate-900 mb-4">Votre parcours en 5 ans</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="rounded-2xl border-2 border-blue-600 bg-blue-50 p-4">
                    <span className="inline-block text-[11px] font-bold uppercase tracking-wide bg-amber-400 text-slate-900 px-2.5 py-0.5 rounded-full mb-2">
                      Vous candidatez ici
                    </span>
                    <div className="font-bold text-slate-900">Années 1 et 2 : MPC</div>
                    <p className="text-sm text-slate-600 mt-1">Tout le monde commence par ce cycle d'études générales et techniques.</p>
                  </div>
                  <div className="rounded-2xl border border-slate-200 p-4">
                    <div className="font-bold text-slate-900">Années 3 à 5 : votre branche</div>
                    <p className="text-sm text-slate-600 mt-1">
                      Génie Civil, Génie Électromécanique, Génie Électronique ou Architecture, choisie après le MPC.
                    </p>
                  </div>
                </div>
              </div>
            )}

            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                    <BookOpen className="w-5 h-5 text-blue-600" />
                    <span>Programme & Maquette Pédagogique</span>
                  </h2>
                  <p className="text-xs text-slate-500 mt-1">
                    Répartition des matières et volumes horaires par niveau.
                  </p>
                </div>
              </div>

              {/* Niveau Selector Tabs */}
              {niveauxKeys.length > 0 && (
                <div className="mb-6">
                  <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
                    <Layers className="w-4 h-4 text-blue-600" />
                    <span>Sélectionner le niveau :</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {niveauxKeys.map((k) => (
                      <button
                        key={k}
                        onClick={() => setActiveNiveau(k)}
                        className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${
                          activeNiveau === k
                            ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                            : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                        }`}
                      >
                        {k}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Courses Table */}
              <div className="rounded-2xl border border-slate-200 overflow-hidden divide-y divide-slate-100">
                {matieres.map((mat, idx) => (
                  <div key={idx} className="p-4 hover:bg-slate-50 transition-colors flex items-center justify-between gap-4">
                    <div className="flex items-start gap-3">
                      <span className="w-6 h-6 rounded-lg bg-blue-50 text-blue-700 font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                        {mat.item || idx + 1}
                      </span>
                      <div>
                        <div className="text-sm font-semibold text-slate-900">{mat.titre}</div>
                        {mat.code && (
                          <span className="text-[11px] font-mono text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded">
                            {mat.code}
                          </span>
                        )}
                      </div>
                    </div>

                    <div className="text-xs text-slate-600 font-medium shrink-0">
                      {mat.heures ? (
                        <span className="bg-slate-100 px-2.5 py-1 rounded-lg">
                          {mat.heures}h
                        </span>
                      ) : (
                        <div className="flex items-center gap-1.5">
                          {mat.heures_theorie !== null && mat.heures_theorie !== undefined && (
                            <span className="bg-slate-100 px-2 py-0.5 rounded">Th: {mat.heures_theorie}h</span>
                          )}
                          {mat.heures_tp !== null && mat.heures_tp !== undefined && (
                            <span className="bg-amber-50 text-amber-800 px-2 py-0.5 rounded">TP: {mat.heures_tp}h</span>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column : Pièces Justificatives Exigées (US-002) */}
          <div className="space-y-6">
            {!cursus.est_admission && (
              <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm sticky top-24">
                <h3 className="text-xl font-bold text-slate-900 mb-2">Cette branche s'ouvre après le MPC</h3>
                <p className="text-sm text-slate-600 mb-6">
                  Vous ne candidatez pas directement à une branche : l'admission se fait une seule fois, au Premier cycle MPC.
                  Vous choisirez votre branche à la fin du MPC.
                </p>
                <Link
                  to="/cursus/mpc"
                  className="w-full py-3.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm flex items-center justify-center gap-2 transition-colors"
                >
                  <span>Voir l'admission au MPC</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            )}

            {cursus.est_admission && (
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm sticky top-24">
              <div className="flex items-center gap-2 text-xl font-bold text-slate-900 mb-2">
                <FileCheck2 className="w-5 h-5 text-emerald-600" />
                <h3>Pièces à fournir</h3>
              </div>
              <p className="text-xs text-slate-500 mb-6">
                Documents obligatoires au format numérique pour valider votre dossier d'admission.
              </p>

              <div className="space-y-3.5 mb-8">
                {cursus.documents_requis?.map((doc) => (
                  <div key={doc.id} className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 flex flex-col gap-1">
                    <div className="flex items-start justify-between gap-2">
                      <span className="text-xs font-bold text-slate-900 leading-snug">
                        {doc.nom}
                      </span>
                      {doc.est_obligatoire && (
                        <span className="text-[10px] font-bold text-emerald-700 bg-emerald-100/70 px-2 py-0.5 rounded-full shrink-0">
                          Requis
                        </span>
                      )}
                    </div>
                    <p className="text-[11px] text-slate-500 leading-relaxed">
                      {doc.description}
                    </p>
                    <div className="flex items-center gap-2 text-[10px] font-semibold text-slate-400 mt-1">
                      <span>Format : {doc.format_accepte}</span>
                      <span>•</span>
                      <span>Max : {doc.taille_max_mo} Mo</span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Action Button */}
              <div className="pt-4 border-t border-slate-100">
                <Link
                  to="/postuler"
                  className="w-full py-3.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm flex items-center justify-center gap-2 transition-colors"
                >
                  <span>Déposer ma candidature</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
                <p className="text-[11px] text-slate-400 text-center mt-2 flex items-center justify-center gap-1">
                  <HelpCircle className="w-3.5 h-3.5" />
                  <span>Sans déplacement. Sans compte à créer.</span>
                </p>
              </div>
            </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
