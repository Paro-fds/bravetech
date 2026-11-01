import React from 'react';
import { useSessionStore } from '../../../entities/session';

/** Page d'arrivée après connexion. Le tableau de bord des dossiers la remplacera avec US-012. */
export const AdminAccueilPage: React.FC = () => {
  const role = useSessionStore((s) => s.session?.role);
  return (
    <div className="max-w-5xl w-full mx-auto px-4 py-8 flex flex-col gap-3">
      <h1 className="font-fds-serif text-2xl font-bold text-fds-navy-d">Bienvenue</h1>
      <p className="text-fds-mute">
        Vous êtes connecté en tant que <strong>{role === 'admin' ? 'administrateur' : 'agent'}</strong>. La liste des dossiers à
        examiner arrive prochainement.
      </p>
    </div>
  );
};
