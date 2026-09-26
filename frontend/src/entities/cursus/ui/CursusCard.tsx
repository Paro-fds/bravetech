import React from 'react';
import type { CursusListItem } from '../model/types';
import { Calendar, Clock, ArrowRight, Award, CheckCircle2 } from 'lucide-react';

interface CursusCardProps {
  cursus: CursusListItem;
  onSelect?: (cursus: CursusListItem) => void;
}

export const CursusCard: React.FC<CursusCardProps> = ({ cursus, onSelect }) => {
  const isMpc = cursus.id === 'mpc';

  return (
    <div
      onClick={() => onSelect?.(cursus)}
      className={`group relative flex flex-col justify-between overflow-hidden rounded-2xl border transition-all duration-300 hover:-translate-y-1 hover:shadow-xl cursor-pointer ${
        isMpc
          ? 'bg-gradient-to-br from-blue-900 to-indigo-950 text-white border-blue-700/50 shadow-blue-900/10'
          : 'bg-white border-slate-200/90 text-slate-900 hover:border-blue-400 shadow-slate-100'
      }`}
    >
      {/* Top Banner accent */}
      <div
        className={`h-1.5 w-full ${
          isMpc
            ? 'bg-gradient-to-r from-amber-400 to-blue-400'
            : 'bg-gradient-to-r from-blue-600 to-indigo-600'
        }`}
      />

      <div className="p-6 md:p-7 flex flex-col flex-1">
        {/* Badges row */}
        <div className="flex items-center justify-between gap-2 mb-4">
          <span
            className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold tracking-wide ${
              cursus.est_ouvert
                ? isMpc
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                : 'bg-slate-100 text-slate-600'
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            {cursus.est_ouvert ? 'Inscriptions Ouvertes' : 'Fermé'}
          </span>

          <span
            className={`inline-flex items-center gap-1 text-xs font-medium ${
              isMpc ? 'text-blue-200' : 'text-slate-500'
            }`}
          >
            <Clock className="w-3.5 h-3.5" />
            {cursus.duree_annees} ans d'études
          </span>
        </div>

        {/* Title */}
        <h3
          className={`text-xl font-bold tracking-tight mb-3 transition-colors ${
            isMpc
              ? 'text-white group-hover:text-amber-300'
              : 'text-slate-900 group-hover:text-blue-600'
          }`}
        >
          {cursus.nom}
        </h3>

        {/* Short description */}
        <p
          className={`text-sm leading-relaxed mb-6 flex-1 ${
            isMpc ? 'text-blue-100/90' : 'text-slate-600'
          }`}
        >
          {cursus.description_courte}
        </p>

        {/* Key dates & meta */}
        <div
          className={`pt-4 border-t text-xs flex flex-col gap-2 mb-6 ${
            isMpc ? 'border-blue-800/60 text-blue-200' : 'border-slate-100 text-slate-500'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-blue-500" />
              Clôture :
            </span>
            <span className={`font-semibold ${isMpc ? 'text-white' : 'text-slate-800'}`}>
              {cursus.date_fermeture_inscription}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Award className="w-3.5 h-3.5 text-amber-500" />
              Niveau d'entrée :
            </span>
            <span className={`font-medium ${isMpc ? 'text-white' : 'text-slate-700'}`}>
              {isMpc ? 'Baccalauréat / Fin d’études secondaires' : 'Admis MPC'}
            </span>
          </div>
        </div>

        {/* Action button */}
        <div className="mt-auto">
          <div
            className={`w-full py-2.5 px-4 rounded-xl text-sm font-semibold flex items-center justify-center gap-2 transition-all ${
              isMpc
                ? 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-900/40'
                : 'bg-slate-100 hover:bg-blue-600 hover:text-white text-slate-800'
            }`}
          >
            <span>Consulter la formation</span>
            <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
          </div>
        </div>
      </div>
    </div>
  );
};
