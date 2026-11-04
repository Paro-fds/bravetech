import React, { useEffect, useRef, useState } from 'react';
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { LanguageSwitcher } from '../../shared/i18n/LanguageSwitcher';
import type { Cle } from '../../shared/i18n/fr';
import { useT } from '../../shared/i18n/useT';
import { ThemeToggle } from '../../shared/theme/ThemeToggle';

const LIENS: { to: string; cle: Cle; clePied?: Cle; fin?: boolean }[] = [
  { to: '/', cle: 'nav.accueil', fin: true },
  { to: '/cursus/mpc', cle: 'nav.cursus' },
  { to: '/histoire', cle: 'nav.histoire' },
  { to: '/suivi', cle: 'nav.suivre', clePied: 'nav.suiviLong' },
  { to: '/contact', cle: 'nav.contact' },
];

const classeLien = ({ isActive }: { isActive: boolean }) =>
  `min-h-11 px-3 rounded-lg flex items-center font-semibold ${isActive ? 'bg-white/15 text-white' : 'text-fds-on-navy hover:text-white hover:bg-white/10'}`;

/**
 * Mise en page publique du site (maquettes mobile et bureau) : en-tête marine, contenu, pied de page.
 * Sous 1024 px l'en-tête tient sur une ligne (logo, langue, bouton menu) et le menu se déplie dessous (US-022) ;
 * au-delà, les liens, le mode sombre et la langue s'alignent dans l'en-tête.
 */
export const SiteLayout: React.FC = () => {
  const t = useT();
  const { pathname } = useLocation();
  // Le menu est ouvert pour une page donnée : changer de page le referme sans effet supplémentaire
  const [ouvertSur, setOuvertSur] = useState<string | null>(null);
  const menuOuvert = ouvertSur === pathname;
  const setMenuOuvert = (ouvert: boolean) => setOuvertSur(ouvert ? pathname : null);
  const boutonMenu = useRef<HTMLButtonElement>(null);

  // Échap ferme le menu et rend le focus au bouton
  useEffect(() => {
    if (!menuOuvert) return;
    const surTouche = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setOuvertSur(null);
        boutonMenu.current?.focus();
      }
    };
    document.addEventListener('keydown', surTouche);
    return () => document.removeEventListener('keydown', surTouche);
  }, [menuOuvert]);

  return (
    <div className="flex flex-col min-h-screen bg-fds-page font-fds-sans text-fds-ink">
      <header className="bg-fds-navy text-white">
        <div className="max-w-5xl mx-auto px-4 py-2.5 flex items-center gap-3 lg:gap-4">
          {/* Sur petit écran le nom passe sur deux lignes (et l'université se masque sous 400 px) */}
          <Link to="/" className="flex flex-1 min-w-0 items-center gap-3 min-h-11 lg:flex-none lg:mr-auto" aria-label={t('marque.accueilLien')}>
            <img src="/logo-fds.png" alt={t('marque.logoAlt')} width={44} height={44} className="rounded shrink-0" />
            <span className="leading-tight min-w-0">
              <span className="block font-semibold text-[15px] lg:text-lg">{t('marque.faculte')}</span>
              <span className="hidden min-[400px]:block text-xs lg:text-[13px] text-fds-on-navy">{t('marque.universite')}</span>
            </span>
          </Link>
          <nav aria-label={t('nav.principale')} className="hidden lg:block">
            <ul className="flex gap-1">
              {LIENS.map((lien) => (
                <li key={lien.to}>
                  <NavLink to={lien.to} end={lien.fin} className={classeLien}>
                    {t(lien.cle)}
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>
          <ThemeToggle libelle={t('nav.modeSombre')} className="hidden lg:flex" />
          <LanguageSwitcher />
          <button
            ref={boutonMenu}
            type="button"
            aria-expanded={menuOuvert}
            aria-controls="menu-mobile"
            aria-label={menuOuvert ? t('nav.fermerMenu') : t('nav.ouvrirMenu')}
            onClick={() => setMenuOuvert(!menuOuvert)}
            className="lg:hidden w-11 h-11 shrink-0 rounded-lg flex items-center justify-center hover:bg-white/10"
          >
            {menuOuvert ? <X className="w-6 h-6" aria-hidden="true" /> : <Menu className="w-6 h-6" aria-hidden="true" />}
          </button>
        </div>
        {menuOuvert && (
          <nav id="menu-mobile" aria-label={t('nav.principale')} className="lg:hidden border-t border-white/15">
            <div className="max-w-5xl mx-auto px-4 py-3 flex flex-col gap-1">
              <ul className="flex flex-col gap-1">
                {LIENS.map((lien) => (
                  <li key={lien.to}>
                    <NavLink to={lien.to} end={lien.fin} className={classeLien}>
                      {t(lien.cle)}
                    </NavLink>
                  </li>
                ))}
              </ul>
              <div className="flex flex-wrap items-center gap-3 pt-2 mt-1 border-t border-white/15">
                <ThemeToggle libelle={t('nav.modeSombre')} avecLibelle />
                <Link to="/postuler" className="ml-auto min-h-11 px-4 rounded-lg bg-fds-gold text-fds-on-light font-semibold flex items-center">
                  {t('nav.postuler')}
                </Link>
              </div>
            </div>
          </nav>
        )}
      </header>

      <main className="flex-1 flex flex-col">
        <Outlet />
      </main>

      <footer className="bg-fds-navy-d text-fds-on-navy text-sm">
        {/* Sur ordinateur (maquette bureau) : identité à gauche, liens à droite, mentions sur toute la largeur */}
        <div className="max-w-5xl mx-auto px-4 py-6 lg:py-8 flex flex-col lg:flex-row lg:flex-wrap lg:items-center lg:justify-between gap-3 lg:gap-x-8">
          <div className="flex flex-col gap-3 lg:gap-2">
            <div className="flex items-center gap-3">
              <img src="/logo-fds.png" alt="" width={40} height={40} className="rounded" />
              <span className="font-semibold text-white">{t('marque.facuteUeh')}</span>
            </div>
            <p>{t('marque.adresse')}</p>
          </div>
          <ul className="flex flex-wrap gap-x-5 lg:gap-x-6">
            {LIENS.filter((l) => l.to !== '/cursus/mpc').map((lien) => (
              <li key={lien.to}>
                <Link to={lien.to} className="min-h-11 inline-flex items-center underline">
                  {t(lien.clePied ?? lien.cle)}
                </Link>
              </li>
            ))}
          </ul>
          <div className="flex flex-col gap-3 lg:basis-full lg:gap-1.5 lg:border-t lg:border-white/15 lg:pt-4">
            <p className="text-xs">{t('pied.simulation')}</p>
            <p className="text-xs">{t('pied.droits')}</p>
          </div>
        </div>
      </footer>
    </div>
  );
};
