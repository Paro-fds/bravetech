import React, { useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { Lock, TriangleAlert } from 'lucide-react';
import { sessionApi, sessionValide, useSessionStore } from '../../../entities/session';
import { ApiError } from '../../../shared/api/client';

function messageErreur(erreur: unknown): string {
  if (erreur instanceof ApiError) {
    if (erreur.status === 429) return 'Trop de tentatives. Patientez une minute puis réessayez.';
    if (erreur.status === 503) return "La connexion n'est pas disponible pour le moment. Contactez l'administrateur système.";
    if (erreur.status === 401) return 'Email ou mot de passe incorrect.';
  }
  // Message volontairement générique : aucun détail interne n'est montré
  return 'Connexion impossible. Vérifiez votre connexion puis réessayez.';
}

/** Connexion du personnel (maquette « Administration connexion »). */
export const AdminLoginPage: React.FC = () => {
  const navigate = useNavigate();
  const session = useSessionStore((s) => s.session);
  const ouvrir = useSessionStore((s) => s.ouvrir);
  const [email, setEmail] = useState('');
  const [motDePasse, setMotDePasse] = useState('');
  const [erreur, setErreur] = useState<string | null>(null);
  const [enCours, setEnCours] = useState(false);

  if (sessionValide(session)) return <Navigate to="/admin" replace />;

  const soumettre = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !motDePasse) {
      setErreur('Saisissez votre email et votre mot de passe.');
      return;
    }
    setEnCours(true);
    setErreur(null);
    try {
      ouvrir(await sessionApi.connecter(email.trim(), motDePasse));
      navigate('/admin', { replace: true });
    } catch (e) {
      setErreur(messageErreur(e));
      setMotDePasse('');
    } finally {
      setEnCours(false);
    }
  };

  const classeChamp =
    'w-full min-h-12 rounded-lg border-[1.5px] border-fds-field bg-fds-surface px-3 text-base text-fds-ink focus:outline-none focus:ring-2 focus:ring-fds-accent';

  return (
    <div className="min-h-screen bg-fds-navy flex items-center justify-center px-4 py-8 font-fds-sans">
      <main className="w-full max-w-[440px] flex flex-col gap-5">
        <div className="flex flex-col items-center gap-2.5 text-center text-white">
          <img
            src="/logo-fds.png"
            alt="Logo de la Faculté des Sciences"
            width={72}
            height={72}
            className="rounded border border-white/30"
          />
          <h1 className="font-fds-serif text-[26px] font-bold">Espace administration</h1>
          <p className="text-[15px] text-fds-on-navy">Faculté des Sciences · réservé au personnel autorisé</p>
        </div>

        <form onSubmit={soumettre} noValidate className="rounded-xl border border-fds-line bg-fds-surface p-6 flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <label htmlFor="admin-email" className="text-[15px] font-semibold">
              Email professionnel
            </label>
            <input
              id="admin-email"
              type="email"
              inputMode="email"
              autoComplete="username"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={classeChamp}
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <label htmlFor="admin-mdp" className="text-[15px] font-semibold">
              Mot de passe
            </label>
            <input
              id="admin-mdp"
              type="password"
              autoComplete="current-password"
              value={motDePasse}
              onChange={(e) => setMotDePasse(e.target.value)}
              className={classeChamp}
            />
          </div>

          {erreur && (
            <div role="alert" className="flex gap-2.5 items-start rounded-[10px] border border-fds-bad-line bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
              <TriangleAlert className="w-5 h-5 shrink-0" aria-hidden="true" />
              <span>{erreur}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={enCours}
            className="min-h-12 px-4 rounded-lg bg-fds-navy hover:bg-fds-navy-d disabled:opacity-60 text-white font-semibold flex items-center justify-center gap-2 transition-colors"
          >
            <Lock className="w-5 h-5" aria-hidden="true" />
            {enCours ? 'Connexion…' : 'Se connecter'}
          </button>
          <p className="text-xs text-fds-mute text-center">
            Le compte est créé par la Faculté. En cas de problème, contactez l'administrateur système.
          </p>
        </form>

        <p className="text-xs text-fds-on-navy text-center">
          La session se ferme automatiquement après 60 minutes. Toutes vos actions sont enregistrées.
        </p>
      </main>
    </div>
  );
};
