import { apiClient, ApiError } from '../../../shared/api';
import { enteteAuth, useSessionStore, type Session } from '../../../entities/session';

export type RolePersonnel = 'admin' | 'agent';

export interface ComptePersonnel {
  id: string;
  email: string;
  role: RolePersonnel;
  est_actif: boolean;
  created_at: string;
}

export interface CreerComptePayload {
  email: string;
  mot_de_passe: string;
  role: RolePersonnel;
}

export interface ModifierAccesPayload {
  role?: RolePersonnel;
  est_actif?: boolean;
}

const BASE = '/api/v1/admin/utilisateurs';

function surSessionRefusee(erreur: unknown): never {
  if (erreur instanceof ApiError && erreur.status === 401) useSessionStore.getState().fermer();
  throw erreur;
}

export const utilisateursApi = {
  lister: (session: Session): Promise<ComptePersonnel[]> =>
    apiClient<ComptePersonnel[]>(BASE, { headers: enteteAuth(session) }).catch(surSessionRefusee),

  creer: (session: Session, donnees: CreerComptePayload): Promise<ComptePersonnel> =>
    apiClient<ComptePersonnel>(BASE, {
      method: 'POST',
      headers: enteteAuth(session),
      body: JSON.stringify(donnees),
    }).catch(surSessionRefusee),

  modifierAcces: (session: Session, id: string, donnees: ModifierAccesPayload): Promise<ComptePersonnel> =>
    apiClient<ComptePersonnel>(`${BASE}/${encodeURIComponent(id)}`, {
      method: 'PATCH',
      headers: enteteAuth(session),
      body: JSON.stringify(donnees),
    }).catch(surSessionRefusee),

  reinitialiserMotDePasse: (session: Session, id: string, nouveauMotDePasse: string): Promise<ComptePersonnel> =>
    apiClient<ComptePersonnel>(`${BASE}/${encodeURIComponent(id)}/mot-de-passe`, {
      method: 'PUT',
      headers: enteteAuth(session),
      body: JSON.stringify({ nouveau_mot_de_passe: nouveauMotDePasse }),
    }).catch(surSessionRefusee),
};

