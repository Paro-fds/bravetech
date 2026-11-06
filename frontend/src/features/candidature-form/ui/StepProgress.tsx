import React from 'react';
import { useT } from '../../../shared/i18n';

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
      <div className="max-w-xl lg:max-w-5xl mx-auto px-4 py-3.5 lg:py-4 flex flex-col gap-2 lg:gap-3">
        {/* Ordinateur : les quatre étapes nommées, l'étape en cours mise en avant */}
        <ol className="hidden lg:grid grid-cols-4 gap-4">
          {TITRES.map((titre, i) => {
            const n = i + 1;
            const etat = n < etape ? 'fait' : n === etape ? 'courant' : 'avenir';
            return (
              <li key={titre} className="flex items-center gap-2.5" aria-current={etat === 'courant' ? 'step' : undefined}>
                <span
                  className={`w-7 h-7 rounded-full flex items-center justify-center text-sm font-bold shrink-0 ${
                    etat === 'avenir' ? 'border-2 border-fds-line text-fds-mute' : 'bg-fds-accent text-white'
                  }`}
                  aria-hidden="true"
                >
                  {n}
                </span>
                <span className={`text-sm ${etat === 'courant' ? 'font-semibold' : 'text-fds-mute'}`}>{t(titre)}</span>
              </li>
            );
          })}
        </ol>
        <div className="flex items-center justify-between lg:hidden">
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
