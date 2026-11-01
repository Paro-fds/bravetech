import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { LogOut } from 'lucide-react';
import { sessionValide, useSessionStore } from '../../entities/session';

/**
 * Mise en page de l'espace administration. Barrière d'accès côté navigateur : sans session valide on renvoie vers la
 * connexion. La vraie protection reste côté serveur (`get_current_admin` sur chaque route `/admin/`).
 */
export const AdminLayout: React.FC = () => {
  const session = useSessionStore((s) => s.session);
  const fermer = useSessionStore((s) => s.fermer);

  if (!sessionValide(session)) {
    if (session) fermer(); // session expirée : on la purge
    return <Navigate to="/admin/login" replace />;
  }

  return (
    <div className="flex flex-col min-h-screen bg-[#f4f6fa] font-fds-sans text-fds-ink">
      <header className="bg-fds-navy text-white">
        <div className="max-w-5xl mx-auto flex items-center gap-3 px-4 py-2.5">
          <img src="/logo-fds.png" alt="" width={36} height={36} className="rounded" />
          <span className="flex-1 leading-tight">
            <span className="block font-semibold text-[15px]">Administration</span>
            <span className="block text-xs text-[#cfe0f5] break-all">{session.email}</span>
          </span>
          <button type="button" onClick={fermer} className="min-h-11 px-3 rounded-lg border border-white/40 flex items-center gap-2 text-sm font-semibold">
            <LogOut className="w-4 h-4" aria-hidden="true" />
            Se déconnecter
          </button>
        </div>
      </header>
      <main className="flex-1 flex flex-col">
        <Outlet />
      </main>
    </div>
  );
};
