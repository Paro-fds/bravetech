import React from 'react';
import { Link, NavLink, Outlet } from 'react-router-dom';
import { INSTITUTION } from '../../shared/config/institution';

const LIENS = [
  { to: '/', libelle: 'Accueil', fin: true },
  { to: '/cursus/mpc', libelle: 'Cursus' },
  { to: '/histoire', libelle: 'Histoire' },
  { to: '/suivi', libelle: 'Suivi' },
  { to: '/contact', libelle: 'Contact' },
];

/**
 * Mise en page publique du site (maquettes mobile et bureau) : en-tête marine avec menu, contenu, pied de page.
 * Sur mobile le menu passe sous le logo ; à partir de 768 px il s'aligne dans l'en-tête.
 */
export const SiteLayout: React.FC = () => (
  <div className="flex flex-col min-h-screen bg-[#f4f6fa] font-fds-sans text-fds-ink">
    <header className="bg-fds-navy text-white">
      <div className="max-w-5xl mx-auto px-4 py-2.5 flex flex-wrap items-center gap-x-6 gap-y-0">
        <Link to="/" className="flex items-center gap-3 min-h-11 mr-auto" aria-label="Accueil du portail">
          <img src="/logo-fds.png" alt="Logo de la Faculté des Sciences, Université d'État d'Haïti" width={44} height={44} className="rounded" />
          <span className="leading-tight">
            <span className="block font-semibold text-[15px] md:text-lg">Faculté des Sciences</span>
            <span className="block text-xs md:text-[13px] text-[#cfe0f5]">Université d'État d'Haïti</span>
          </span>
        </Link>
        <nav aria-label="Navigation principale" className="order-last w-full md:order-none md:w-auto border-t border-white/15 md:border-0 -mx-2 md:mx-0">
          <ul className="flex flex-wrap px-2 md:px-0">
            {LIENS.map((lien) => (
              <li key={lien.to}>
                <NavLink
                  to={lien.to}
                  end={lien.fin}
                  className={({ isActive }) =>
                    `min-h-11 px-3 flex items-center text-sm font-semibold border-b-2 ${isActive ? 'border-fds-gold text-white' : 'border-transparent text-[#cfe0f5] hover:text-white'}`
                  }
                >
                  {lien.libelle}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        <Link to="/postuler" className="min-h-11 px-4 rounded-lg bg-fds-gold text-fds-navy-d font-semibold flex items-center">
          Postuler
        </Link>
      </div>
    </header>

    <main className="flex-1 flex flex-col">
      <Outlet />
    </main>

    <footer className="bg-fds-navy-d text-[#cfe0f5] text-sm">
      <div className="max-w-5xl mx-auto px-4 py-6 flex flex-col gap-3">
        <div className="flex items-center gap-3">
          <img src="/logo-fds.png" alt="" width={40} height={40} className="rounded" />
          <span className="font-semibold text-white">Faculté des Sciences, UEH</span>
        </div>
        <p>{INSTITUTION.adresse}</p>
        <ul className="flex flex-wrap gap-x-5">
          {LIENS.filter((l) => l.to !== '/cursus/mpc').map((lien) => (
            <li key={lien.to}>
              <Link to={lien.to} className="min-h-11 inline-flex items-center underline">
                {lien.to === '/suivi' ? 'Suivi de dossier' : lien.libelle}
              </Link>
            </li>
          ))}
        </ul>
        <p className="text-xs">Le paiement en ligne est une simulation pendant la phase de lancement.</p>
        <p className="text-xs">© Faculté des Sciences, Université d'État d'Haïti</p>
      </div>
    </footer>
  </div>
);
