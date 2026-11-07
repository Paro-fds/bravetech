import React from 'react';
import { Link, Outlet, useMatches, useParams } from 'react-router-dom';
import { LanguageSwitcher } from '../../shared/i18n';
import type { Cle } from '../../shared/i18n';
import { useT } from '../../shared/i18n';
import { ThemeToggle } from '../../shared/theme';

/**
 * Mise en page du tunnel de candidature et du suivi (maquettes) : en-tête marine allégé, sans menu ni pied de page.
 * Le titre de l'en-tête vient du `handle.titre` de la route (une clé de traduction, qui peut citer `{reference}`).
 */
export const FlowLayout: React.FC = () => {
  const t = useT();
  const { reference = '' } = useParams();
  // Référence insécable (traits d'union U+2011) : le titre ne se coupe jamais au milieu de « CAN-2026-0001 »
  const referenceInsecable = reference.replace(/-/g, '‑');
  const cleTitre = useMatches().reduce<Cle>(
    (acc, m) => (m.handle as { titre?: Cle } | undefined)?.titre ?? acc,
    'flux.titreCandidature',
  );
  return (
    <div className="flex flex-col min-h-screen bg-fds-page font-fds-sans text-fds-ink">
      <a
        href="#contenu-principal"
        className="sr-only focus:not-sr-only focus:fixed focus:top-2 focus:left-2 focus:z-50 focus:rounded-lg focus:bg-fds-gold focus:px-4 focus:py-2.5 focus:font-semibold focus:text-fds-on-light focus:shadow-lg"
      >
        {t('nav.allerContenu')}
      </a>
      <header className="bg-fds-navy text-white">
        <div className="max-w-xl lg:max-w-5xl mx-auto flex items-center gap-3 px-4 py-2.5">
          <Link to="/" className="flex items-center gap-3 min-h-11 mr-auto" aria-label={t('marque.accueilRetour')}>
            <img src="/logo-fds.png" alt={t('marque.logoAlt')} width={40} height={40} className="rounded" />
            <span className="leading-tight">
              <span className="block font-semibold text-[15px]">{t(cleTitre, { reference: referenceInsecable })}</span>
              <span className="hidden min-[400px]:block text-xs text-fds-on-navy">{t('marque.facuteUeh')}</span>
            </span>
          </Link>
          <ThemeToggle libelle={t('nav.modeSombre')} />
          <LanguageSwitcher />
        </div>
      </header>
      <main id="contenu-principal" tabIndex={-1} className="flex-1 flex flex-col focus:outline-none">
        <Outlet />
      </main>
    </div>
  );
};
