import React, { useState, useEffect } from 'react';
import type { CursusListItem, CursusDetail } from '../model/types';
import { cursusApi } from '../api/cursusApi';
import { X, Clock, Calendar, BookOpen, Layers, CheckCircle2 } from 'lucide-react';

interface CursusDetailModalProps {
  cursus: CursusListItem | null;
  onClose: () => void;
}

export const CursusDetailModal: React.FC<CursusDetailModalProps> = ({ cursus, onClose }) => {
  const [detail, setDetail] = useState<CursusDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeNiveau, setActiveNiveau] = useState<string>('');

  useEffect(() => {
    if (!cursus) {
      setDetail(null);
      return;
    }

    setLoading(true);
    cursusApi.getById(cursus.id)
      .then((data) => {
        setDetail(data);
        const niveauxKeys = Object.keys(data.niveaux || {});
        if (niveauxKeys.length > 0) {
          setActiveNiveau(niveauxKeys[0]);
        }
      })
      .catch((err) => {
        console.error('Erreur chargement détail:', err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [cursus]);

  if (!cursus) return null;

  const matieres = detail?.niveaux?.[activeNiveau] || [];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-4xl max-h-[90vh] bg-white rounded-3xl shadow-2xl flex flex-col overflow-hidden border border-slate-100">
        {/* Header */}
        <div className="p-6 md:p-8 bg-gradient-to-r from-blue-900 to-indigo-900 text-white relative">
          <button
            onClick={onClose}
            className="absolute top-6 right-6 w-10 h-10 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors"
            aria-label="Fermer"
          >
            <X className="w-5 h-5" />
          </button>

          <div className="flex items-center gap-2 mb-2">
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              <CheckCircle2 className="w-3 h-3 inline mr-1" />
              Inscriptions Ouvertes
            </span>
            <span className="text-xs text-blue-200 font-medium">
              Durée : {cursus.duree_annees} ans
            </span>
          </div>

          <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight mb-2">
            {cursus.nom}
          </h2>
          <p className="text-sm md:text-base text-blue-100/90 leading-relaxed max-w-2xl">
            {detail?.description_longue || cursus.description_courte}
          </p>

          <div className="flex flex-wrap gap-4 mt-4 pt-4 border-t border-blue-800/60 text-xs text-blue-200">
            <div className="flex items-center gap-1.5">
              <Calendar className="w-4 h-4 text-amber-400" />
              <span>Inscriptions du <strong>{cursus.date_ouverture_inscription}</strong> au <strong>{cursus.date_fermeture_inscription}</strong></span>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 md:p-8 overflow-y-auto flex-1">
          {loading ? (
            <div className="flex flex-col items-center justify-center py-12 text-slate-500 gap-3">
              <div className="w-8 h-8 border-3 border-blue-600 border-t-transparent rounded-full animate-spin" />
              <p className="text-sm">Chargement du programme académique officiel...</p>
            </div>
          ) : detail ? (
            <div>
              {/* Niveau Selector Tabs */}
              {Object.keys(detail.niveaux || {}).length > 0 && (
                <div className="mb-6">
                  <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-500 mb-3">
                    <Layers className="w-4 h-4 text-blue-600" />
                    <span>Niveaux académiques / Semestres</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {Object.keys(detail.niveaux).map((niveauKey) => (
                      <button
                        key={niveauKey}
                        onClick={() => setActiveNiveau(niveauKey)}
                        className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${
                          activeNiveau === niveauKey
                            ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30 scale-105'
                            : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                        }`}
                      >
                        {niveauKey}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Matieres Table */}
              <div className="rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
                <div className="px-5 py-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
                  <div className="flex items-center gap-2 text-sm font-bold text-slate-800">
                    <BookOpen className="w-4 h-4 text-blue-600" />
                    <span>Matières enseignées — {activeNiveau}</span>
                  </div>
                  <span className="text-xs font-semibold px-2.5 py-1 bg-blue-100 text-blue-800 rounded-full">
                    {matieres.length} matières
                  </span>
                </div>

                <div className="divide-y divide-slate-100">
                  {matieres.map((mat, idx) => (
                    <div key={idx} className="p-4 hover:bg-slate-50/80 transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                      <div className="flex items-start gap-3">
                        <span className="w-6 h-6 rounded-md bg-slate-100 text-slate-600 text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                          {mat.item || idx + 1}
                        </span>
                        <div>
                          <div className="font-semibold text-slate-900 text-sm">{mat.titre}</div>
                          {mat.code && (
                            <span className="text-[11px] font-mono font-medium text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded">
                              Code : {mat.code}
                            </span>
                          )}
                        </div>
                      </div>

                      <div className="flex items-center gap-2 text-xs text-slate-500 shrink-0">
                        {mat.heures ? (
                          <span className="flex items-center gap-1 font-semibold text-blue-700 bg-blue-50 px-2.5 py-1 rounded-lg">
                            <Clock className="w-3.5 h-3.5" />
                            {mat.heures} heures
                          </span>
                        ) : (
                          <div className="flex items-center gap-2">
                            {mat.heures_theorie !== null && mat.heures_theorie !== undefined && (
                              <span className="bg-slate-100 text-slate-700 px-2 py-0.5 rounded">
                                Th : {mat.heures_theorie}h
                              </span>
                            )}
                            {mat.heures_tp !== null && mat.heures_tp !== undefined && (
                              <span className="bg-amber-50 text-amber-800 px-2 py-0.5 rounded">
                                TP : {mat.heures_tp}h
                              </span>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <p className="text-center text-slate-500 py-8">Information non disponible.</p>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 sm:p-6 bg-slate-50 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-slate-500 text-center sm:text-left">
            Source officielle : Maquettes pédagogiques de la Faculté des Sciences (UEH).
          </p>
          <div className="flex items-center gap-3 w-full sm:w-auto">
            <button
              onClick={onClose}
              className="flex-1 sm:flex-none px-5 py-2.5 rounded-xl border border-slate-300 text-slate-700 text-sm font-semibold hover:bg-slate-100 transition-colors"
            >
              Fermer
            </button>
            <a
              href="#processus"
              onClick={onClose}
              className="flex-1 sm:flex-none px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold shadow-md shadow-blue-600/30 transition-all text-center"
            >
              Postuler à ce cursus
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};
