import React from 'react';

const TITRES = ['Vos informations', 'Admission et accès', 'Frais de dossier', 'Vos pièces'];

interface StepProgressProps {
  etape: number;
}

/** Barre de progression du tunnel de candidature (4 étapes), comme sur les maquettes. */
export const StepProgress: React.FC<StepProgressProps> = ({ etape }) => {
  const total = TITRES.length;
  const pourcentage = Math.round((etape / total) * 100);
  return (
    <div className="bg-white border-b border-fds-line">
      <div className="max-w-xl mx-auto px-4 py-3.5 flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <span className="font-semibold">
            Étape {etape} sur {total}
          </span>
          <span className="text-sm text-fds-mute">{TITRES[etape - 1]}</span>
        </div>
        <div
          className="h-2 rounded bg-fds-line overflow-hidden"
          role="progressbar"
          aria-valuenow={pourcentage}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label="Progression de la candidature"
        >
          <div className="h-full bg-fds-navy transition-all" style={{ width: `${pourcentage}%` }} />
        </div>
      </div>
    </div>
  );
};
