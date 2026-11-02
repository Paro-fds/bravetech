import React from 'react';
import { useT } from '../../../shared/i18n/useT';

const TITRES = ['cand.etape1', 'cand.etape2', 'cand.etape3', 'cand.etape4'] as const;

interface StepProgressProps {
  etape: number;
}

/** Barre de progression du tunnel de candidature (4 étapes), comme sur les maquettes. */
export const StepProgress: React.FC<StepProgressProps> = ({ etape }) => {
  const t = useT();
  const total = TITRES.length;
  const pourcentage = Math.round((etape / total) * 100);
  return (
    <div className="bg-fds-surface border-b border-fds-line">
      <div className="max-w-xl mx-auto px-4 py-3.5 flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <span className="font-semibold">
            {t('cand.etapeSur', { n: etape, total })}
          </span>
          <span className="text-sm text-fds-mute">{t(TITRES[etape - 1])}</span>
        </div>
        <div
          className="h-2 rounded bg-fds-line overflow-hidden"
          role="progressbar"
          aria-valuenow={pourcentage}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label={t('cand.progressionAria')}
        >
          <div className="h-full bg-fds-accent transition-all" style={{ width: `${pourcentage}%` }} />
        </div>
      </div>
    </div>
  );
};
