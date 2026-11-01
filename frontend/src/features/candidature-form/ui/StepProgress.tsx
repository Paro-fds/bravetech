import React from 'react';

const TITRES = ['Vos informations', 'Admission et accès', 'Frais de dossier', 'Vos pièces'];

interface StepProgressProps {
  etape: number;
}

/** Barre de progression du tunnel de candidature (4 étapes). */
export const StepProgress: React.FC<StepProgressProps> = ({ etape }) => {
  const total = TITRES.length;
  const pourcentage = Math.round((etape / total) * 100);
  return (
    <div className="bg-white border-b border-slate-200 px-4 py-3.5">
      <div className="max-w-xl mx-auto flex flex-col gap-2">
        <div className="flex items-center justify-between text-sm">
          <span className="font-bold text-slate-900">
            Étape {etape} sur {total}
          </span>
          <span className="text-slate-500">{TITRES[etape - 1]}</span>
        </div>
        <div
          className="h-2 rounded-full bg-slate-200 overflow-hidden"
          role="progressbar"
          aria-valuenow={pourcentage}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label="Progression de la candidature"
        >
          <div className="h-full bg-blue-700 transition-all" style={{ width: `${pourcentage}%` }} />
        </div>
      </div>
    </div>
  );
};
