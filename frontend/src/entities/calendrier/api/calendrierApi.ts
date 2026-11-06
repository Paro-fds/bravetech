import { apiClient, ApiError } from '../../../shared/api';
import { enteteAuth, useSessionStore, type Session } from '../../session/@x/calendrier';
import type { CalendrierAdmin, CalendrierPublic, DatesCalendrier } from '../model/types';

/** Une réponse 401 signifie que la session a expiré : on la ferme, le garde de l'espace admin renvoie à la connexion. */
function surSessionRefusee(erreur: unknown): never {
  if (erreur instanceof ApiError && erreur.status === 401) useSessionStore.getState().fermer();
  throw erreur;
}

export const calendrierApi = {
  obtenir: (): Promise<CalendrierPublic> => apiClient<CalendrierPublic>('/api/v1/calendrier'),

  obtenirAdmin: (session: Session): Promise<CalendrierAdmin> =>
    apiClient<CalendrierAdmin>('/api/v1/admin/calendrier', { headers: enteteAuth(session) }).catch(surSessionRefusee),

  /** Rejette avec une `ApiError` : 422 (`detail.erreurs`, champ -> message) si les dates manquent ou ne se suivent pas, 403 pour un agent. */
  modifier: (session: Session, dates: DatesCalendrier): Promise<CalendrierAdmin> =>
    apiClient<CalendrierAdmin>('/api/v1/admin/calendrier', {
      method: 'PUT',
      headers: enteteAuth(session),
      body: JSON.stringify(dates),
    }).catch(surSessionRefusee),
};

/** Réponse 403 `candidatures_fermees` du serveur (création ou soumission hors période). */
export function estCandidaturesFermees(erreur: unknown): boolean {
  if (!(erreur instanceof ApiError) || erreur.status !== 403) return false;
  const detail = (erreur.body as { detail?: { code?: string } } | null)?.detail;
  return detail?.code === 'candidatures_fermees';
}
