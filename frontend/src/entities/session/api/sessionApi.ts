import { apiClient } from '../../../shared/api';
import type { Session } from '../model/useSessionStore';

interface JetonReponse {
  access_token: string;
  expires_in: number; // secondes
}

interface UtilisateurCourant {
  id: string;
  email: string;
  role: string;
}

export const sessionApi = {
  /**
   * Connexion du personnel. Rejette avec une `ApiError` : 401 identifiants incorrects, 429 trop de tentatives,
   * 503 connexion non configurée côté serveur.
   */
  connecter: async (email: string, motDePasse: string): Promise<Session> => {
    const jeton = await apiClient<JetonReponse>('/api/v1/auth/token', {
      method: 'POST',
      body: JSON.stringify({ email, password: motDePasse }),
    });
    const moi = await apiClient<UtilisateurCourant>('/api/v1/admin/moi', {
      headers: { Authorization: `Bearer ${jeton.access_token}` },
    });
    return {
      jeton: jeton.access_token,
      expireA: Date.now() + jeton.expires_in * 1000,
      email: moi.email,
      role: moi.role,
    };
  },
};

/** En-tête d'authentification des appels admin. */
export function enteteAuth(session: Session): Record<string, string> {
  return { Authorization: `Bearer ${session.jeton}` };
}
