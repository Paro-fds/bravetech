import React from 'react';
import { Link, Outlet, useMatches } from 'react-router-dom';

/**
 * Mise en page du tunnel de candidature et du suivi (maquettes) : en-tête marine allégé, sans menu ni pied de page.
 * Le titre de l'en-tête vient du `handle.titre` de la route.
 */
export const FlowLayout: React.FC = () => {
  const titre = useMatches().reduce<string>((acc, m) => (m.handle as { titre?: string } | undefined)?.titre ?? acc, 'Candidature');
  return (
    <div className="flex flex-col min-h-screen bg-[#f4f6fa] font-fds-sans text-fds-ink">
      <header className="bg-fds-navy text-white">
        <div className="max-w-xl mx-auto flex items-center gap-3 px-4 py-2.5">
          <Link to="/" className="flex items-center gap-3 min-h-11" aria-label="Retour à l'accueil du portail">
            <img
              src="/logo-fds.png"
              alt="Logo de la Faculté des Sciences, Université d'État d'Haïti"
              width={40}
              height={40}
              className="rounded"
            />
            <span className="leading-tight">
              <span className="block font-semibold text-[15px]">{titre}</span>
              <span className="block text-xs text-[#cfe0f5]">Faculté des Sciences, UEH</span>
            </span>
          </Link>
        </div>
      </header>
      <main className="flex-1 flex flex-col">
        <Outlet />
      </main>
    </div>
  );
};
