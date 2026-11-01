import { create } from 'zustand';
import { createJSONStorage, persist, type StateStorage } from 'zustand/middleware';

export interface Session {
  /** Jeton JWT à présenter dans `Authorization: Bearer`. */
  jeton: string;
  /** Heure d'expiration (ms depuis 1970), calculée à la connexion : les sessions durent 60 minutes. */
  expireA: number;
  email: string;
  role: string;
}

interface SessionState {
  session: Session | null;
  ouvrir: (session: Session) => void;
  fermer: () => void;
}

/**
 * sessionStorage : la session disparaît à la fermeture de l'onglet (poste de travail partagé à la Faculté).
 * Il peut être bloqué (navigation privée) : on n'échoue jamais pour autant, on perd seulement la reprise après rechargement.
 */
const stockageSecurise: StateStorage = {
  getItem: (nom) => {
    try {
      return sessionStorage.getItem(nom);
    } catch {
      return null;
    }
  },
  setItem: (nom, valeur) => {
    try {
      sessionStorage.setItem(nom, valeur);
    } catch {
      // ignoré
    }
  },
  removeItem: (nom) => {
    try {
      sessionStorage.removeItem(nom);
    } catch {
      // ignoré
    }
  },
};

export const useSessionStore = create<SessionState>()(
  persist(
    (set) => ({
      session: null,
      ouvrir: (session) => set({ session }),
      fermer: () => set({ session: null }),
    }),
    { name: 'fds-session-admin', storage: createJSONStorage(() => stockageSecurise) },
  ),
);

/** Une session expirée est traitée comme absente, sans attendre que le serveur réponde 401. */
export function sessionValide(session: Session | null): session is Session {
  return session !== null && session.expireA > Date.now();
}
