import React from 'react';
import { Navigate, NavLink, Outlet, useLocation } from 'react-router-dom';
import { CalendarDays, FileText, LogOut } from 'lucide-react';
import { sessionValide, useSessionStore } from '../../entities/session';
import { ThemeToggle } from '../../shared/theme';

const lienMenu = (actif: boolean) =>
  `min-h-11 px-3 rounded-lg flex items-center gap-2.5 font-semibold ${actif ? 'bg-white/15' : 'hover:bg-white/10'}`;

/**
 * Mise en page de l'espace administration (maquettes « Administration ») : barre latérale marine, contenu à droite ;
 * sur mobile la barre passe au-dessus. Barrière d'accès côté navigateur : sans session valide on renvoie vers la
 * connexion. La vraie protection reste côté serveur (`get_current_admin` sur chaque route `/admin/`).
 */
export const AdminLayout: React.FC = () => {
  const session = useSessionStore((s) => s.session);
  const fermer = useSessionStore((s) => s.fermer);
  const { pathname } = useLocation();

  if (!sessionValide(session)) {
    if (session) fermer(); // session expirée : on la purge
    return <Navigate to="/admin/login" replace />;
  }

  return (
    <div className="flex flex-wrap min-h-screen bg-fds-page font-fds-sans text-fds-ink">
      <aside className="flex-[1_1_240px] lg:max-w-60 bg-fds-navy-d text-white p-4 flex flex-col gap-1.5">
        <div className="flex items-center gap-2.5 pb-4 px-2">
          <img src="/logo-fds.png" alt="Logo FDS" width={40} height={40} className="rounded" />
          <div className="leading-tight mr-auto">
            <div className="font-semibold">FDS Admin</div>
            <div className="text-xs text-fds-on-navy">{session.role === 'admin' ? 'Administrateur' : 'Agent'}</div>
          </div>
          {/* L'administration reste en français (spec WS-01 §1.6) : libellé fixe, pas de traduction */}
          <ThemeToggle libelle="Mode sombre" />
        </div>
        {/* « Candidatures » couvre /admin et les dossiers, mais pas le calendrier */}
        <NavLink
          to="/admin"
          end={false}
          className={({ isActive }) => lienMenu(isActive && !pathname.startsWith('/admin/calendrier'))}
        >
          <FileText className="w-5 h-5" aria-hidden="true" />
          Candidatures
        </NavLink>
        <NavLink to="/admin/calendrier" className={({ isActive }) => lienMenu(isActive)}>
          <CalendarDays className="w-5 h-5" aria-hidden="true" />
          Calendrier
        </NavLink>
        <div className="flex-1" />
        <div className="px-2 py-2 text-[13px] text-fds-on-navy">
          Connecté : <b className="text-white break-all">{session.email}</b>
        </div>
        <button type="button" onClick={fermer} className="min-h-11 px-3 rounded-lg flex items-center gap-2.5 font-semibold hover:bg-white/10">
          <LogOut className="w-5 h-5" aria-hidden="true" />
          Se déconnecter
        </button>
      </aside>
      <main className="flex-[999_1_640px] min-w-0 p-4 sm:p-8 flex flex-col gap-6">
        <Outlet />
      </main>
    </div>
  );
};
