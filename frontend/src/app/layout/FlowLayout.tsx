import React from 'react';
import { Link, Outlet, useMatches } from 'react-router-dom';
import { LanguageSwitcher } from '../../shared/i18n/LanguageSwitcher';
import type { Cle } from '../../shared/i18n/fr';
import { useT } from '../../shared/i18n/useT';
import { ThemeToggle } from '../../shared/theme/ThemeToggle';

/**
 * Mise en page du tunnel de candidature et du suivi (maquettes) : en-tête marine allégé, sans menu ni pied de page.
 * Le titre de l'en-tête vient du `handle.titre` de la route (une clé de traduction).
 */
export const FlowLayout: React.FC = () => {
  const t = useT();
  const cleTitre = useMatches().reduce<Cle>(
    (acc, m) => (m.handle as { titre?: Cle } | undefined)?.titre ?? acc,
    'flux.titreCandidature',
  );
  return (
    <div className="flex flex-col min-h-screen bg-fds-page font-fds-sans text-fds-ink">
      <header className="bg-fds-navy text-white">
        <div className="max-w-xl mx-auto flex items-center gap-3 px-4 py-2.5">
          <Link to="/" className="flex items-center gap-3 min-h-11 mr-auto" aria-label={t('marque.accueilRetour')}>
            <img src="/logo-fds.png" alt={t('marque.logoAlt')} width={40} height={40} className="rounded" />
            <span className="leading-tight">
              <span className="block font-semibold text-[15px]">{t(cleTitre)}</span>
              <span className="block text-xs text-fds-on-navy">{t('marque.facuteUeh')}</span>
            </span>
          </Link>
          <ThemeToggle libelle={t('nav.modeSombre')} />
          <LanguageSwitcher />
        </div>
      </header>
      <main className="flex-1 flex flex-col">
        <Outlet />
      </main>
    </div>
  );
};
