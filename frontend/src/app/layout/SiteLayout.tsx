import React from 'react';
import { Link, NavLink, Outlet } from 'react-router-dom';
import { INSTITUTION } from '../../shared/config/institution';

const LIENS = [
  { to: '/', libelle: 'Accueil', fin: true },
  { to: '/histoire', libelle: 'Histoire' },
  { to: '/contact', libelle: 'Contact' },
  { to: '/suivi', libelle: 'Suivi de dossier' },
];

/** Mise en page des pages institutionnelles (maquettes « Histoire » et « Contact ») : en-tête marine, menu, pied de page. */
export const SiteLayout: React.FC = () => (
  <div className="flex flex-col min-h-screen bg-[#f4f6fa] font-fds-sans text-fds-ink">
    <header className="bg-fds-navy text-white">
      <div className="max-w-3xl mx-auto px-4 py-2.5 flex flex-wrap items-center gap-x-4 gap-y-1">
        <Link to="/" className="flex items-center gap-3 min-h-11 flex-1" aria-label="Accueil du portail">
          <img src="/logo-fds.png" alt="Logo de la Faculté des Sciences, Université d'État d'Haïti" width={40} height={40} className="rounded" />
          <span className="leading-tight">
            <span className="block font-semibold text-[15px]">Faculté des Sciences</span>
            <span className="block text-xs text-[#cfe0f5]">Université d'État d'Haïti</span>
          </span>
        </Link>
        <Link to="/postuler" className="min-h-11 px-4 rounded-lg bg-fds-gold text-fds-navy-d font-semibold flex items-center">
          Postuler
        </Link>
      </div>
      <nav aria-label="Navigation principale" className="border-t border-white/15">
        <ul className="max-w-3xl mx-auto px-2 flex flex-wrap">
          {LIENS.map((lien) => (
            <li key={lien.to}>
              <NavLink
                to={lien.to}
                end={lien.fin}
                className={({ isActive }) =>
                  `min-h-11 px-3 flex items-center text-sm font-semibold border-b-2 ${isActive ? 'border-fds-gold text-white' : 'border-transparent text-[#cfe0f5]'}`
                }
              >
                {lien.libelle}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </header>
    <main className="flex-1 flex flex-col">
      <Outlet />
    </main>
    <footer className="bg-fds-navy-d text-[#cfe0f5] text-sm">
      <div className="max-w-3xl mx-auto px-4 py-6 flex flex-col gap-3">
        <p>{INSTITUTION.adresse}</p>
        <ul className="flex flex-wrap gap-x-5">
          {LIENS.map((lien) => (
            <li key={lien.to}>
              <Link to={lien.to} className="min-h-11 inline-flex items-center underline">
                {lien.libelle}
              </Link>
            </li>
          ))}
        </ul>
        <p className="text-xs">© Faculté des Sciences, Université d'État d'Haïti</p>
      </div>
    </footer>
  </div>
);
