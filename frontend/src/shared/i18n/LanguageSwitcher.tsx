import React from 'react';
import type { Langue } from './traduire';
import { useLangue } from './useLangue';

const CHOIX: { langue: Langue; libelle: string; nom: string }[] = [
  { langue: 'fr', libelle: 'FR', nom: 'Français' },
  { langue: 'kr', libelle: 'KR', nom: 'Kreyòl ayisyen' },
];

/** Sélecteur FR / KR de l'en-tête (maquettes). Chaque bouton fait au moins 44 px de haut pour le doigt. */
export const LanguageSwitcher: React.FC<{ className?: string }> = ({ className = '' }) => {
  const langue = useLangue((s) => s.langue);
  const setLangue = useLangue((s) => s.setLangue);
  return (
    <div role="group" aria-label="Langue / Lang" className={`flex rounded-lg border border-white/40 overflow-hidden ${className}`}>
      {CHOIX.map((c) => {
        const actif = c.langue === langue;
        return (
          <button
            key={c.langue}
            type="button"
            lang={c.langue === 'kr' ? 'ht' : 'fr'}
            aria-pressed={actif}
            aria-label={c.nom}
            onClick={() => setLangue(c.langue)}
            className={`min-h-11 min-w-11 px-3 text-sm font-bold ${actif ? 'bg-white text-fds-on-light' : 'text-white hover:bg-white/10'}`}
          >
            {c.libelle}
          </button>
        );
      })}
    </div>
  );
};
