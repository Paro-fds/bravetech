import React from 'react';
import { Link, NavLink, Outlet } from 'react-router-dom';
import { LanguageSwitcher } from '../../shared/i18n/LanguageSwitcher';
import type { Cle } from '../../shared/i18n/fr';
import { useT } from '../../shared/i18n/useT';

const LIENS: { to: string; cle: Cle; cleLongue?: Cle; fin?: boolean }[] = [
  { to: '/', cle: 'nav.accueil', fin: true },
  { to: '/cursus/mpc', cle: 'nav.cursus' },
  { to: '/histoire', cle: 'nav.histoire' },
  { to: '/suivi', cle: 'nav.suivi', cleLongue: 'nav.suiviLong' },
  { to: '/contact', cle: 'nav.contact' },
];

/**
 * Mise en page publique du site (maquettes mobile et bureau) : en-tête marine avec menu et sélecteur de langue, contenu,
 * pied de page. Sur mobile le menu passe sous le logo ; à partir de 768 px il s'aligne dans l'en-tête.
 */
export const SiteLayout: React.FC = () => {
  const t = useT();
  return (
    <div className="flex flex-col min-h-screen bg-[#f4f6fa] font-fds-sans text-fds-ink">
      <header className="bg-fds-navy text-white">
        <div className="max-w-5xl mx-auto px-4 py-2.5 flex flex-wrap items-center gap-x-4 gap-y-0">
          <Link to="/" className="flex items-center gap-3 min-h-11 mr-auto" aria-label={t('marque.accueilLien')}>
            <img src="/logo-fds.png" alt={t('marque.logoAlt')} width={44} height={44} className="rounded" />
            <span className="leading-tight">
              <span className="block font-semibold text-[15px] md:text-lg">{t('marque.faculte')}</span>
              <span className="block text-xs md:text-[13px] text-[#cfe0f5]">{t('marque.universite')}</span>
            </span>
          </Link>
          <LanguageSwitcher />
          <nav aria-label={t('nav.principale')} className="order-last w-full md:order-none md:w-auto border-t border-white/15 md:border-0 -mx-2 md:mx-0">
            <ul className="flex flex-wrap px-2 md:px-0">
              {LIENS.map((lien) => (
                <li key={lien.to}>
                  <NavLink
                    to={lien.to}
                    end={lien.fin}
                    className={({ isActive }) =>
                      `min-h-11 px-2.5 sm:px-3 flex items-center text-sm font-semibold border-b-2 ${isActive ? 'border-fds-gold text-white' : 'border-transparent text-[#cfe0f5] hover:text-white'}`
                    }
                  >
                    {t(lien.cle)}
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>
          {/* Sur mobile la place manque : « Postuler » reste accessible depuis l'accueil, les fiches et la page Histoire */}
          <Link to="/postuler" className="hidden md:flex min-h-11 px-4 rounded-lg bg-fds-gold text-fds-navy-d font-semibold items-center">
            {t('nav.postuler')}
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
            <span className="font-semibold text-white">{t('marque.facuteUeh')}</span>
          </div>
          <p>{t('marque.adresse')}</p>
          <ul className="flex flex-wrap gap-x-5">
            {LIENS.filter((l) => l.to !== '/cursus/mpc').map((lien) => (
              <li key={lien.to}>
                <Link to={lien.to} className="min-h-11 inline-flex items-center underline">
                  {t(lien.cleLongue ?? lien.cle)}
                </Link>
              </li>
            ))}
          </ul>
          <p className="text-xs">{t('pied.simulation')}</p>
          <p className="text-xs">{t('pied.droits')}</p>
        </div>
      </footer>
    </div>
  );
};
