import React from 'react';
import { Moon, Sun } from 'lucide-react';
import { useTheme } from './useTheme';

/**
 * Bouton soleil / lune des en-têtes marine (US-017). Interrupteur « Mode sombre » (aria-pressed) : la lune propose
 * de passer au sombre, le soleil de revenir au clair. 44 px pour le doigt, comme le sélecteur de langue.
 * `avecLibelle` : version large avec le texte visible, pour le menu mobile (US-022).
 */
export const ThemeToggle: React.FC<{ libelle: string; avecLibelle?: boolean; className?: string }> = ({
  libelle,
  avecLibelle = false,
  className = '',
}) => {
  const theme = useTheme((s) => s.theme);
  const basculer = useTheme((s) => s.basculer);
  const sombre = theme === 'sombre';
  const Icone = sombre ? Sun : Moon;
  return (
    <button
      type="button"
      aria-pressed={sombre}
      aria-label={avecLibelle ? undefined : libelle}
      title={avecLibelle ? undefined : libelle}
      onClick={basculer}
      className={`${avecLibelle ? 'min-h-11 px-3 gap-2.5 font-semibold justify-start' : 'w-11 h-11 justify-center'} shrink-0 rounded-lg border border-white/40 text-white hover:bg-white/10 flex items-center ${className}`}
    >
      <Icone className="w-5 h-5" aria-hidden="true" />
      {avecLibelle && libelle}
    </button>
  );
};
