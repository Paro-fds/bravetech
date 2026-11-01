import { apiClient, ApiError, urlApi } from '../../../shared/api/client';
import { enteteAuth, useSessionStore, type Session } from '../../session';
import { TAILLE_PAGE, type DossierAdmin, type FiltresDossiers, type PageDossiers } from '../model/types';

const BASE = '/api/v1/admin';

/** Une réponse 401 signifie que la session a expiré ou n'est plus valide : on la ferme, le garde renvoie à la connexion. */
function surSessionRefusee(erreur: unknown): never {
  if (erreur instanceof ApiError && erreur.status === 401) useSessionStore.getState().fermer();
  throw erreur;
}

export const dossierAdminApi = {
  lister: (session: Session, filtres: FiltresDossiers): Promise<PageDossiers> => {
    const params = new URLSearchParams({ page: String(filtres.page), limit: String(TAILLE_PAGE) });
    if (filtres.q.trim()) params.set('q', filtres.q.trim());
    if (filtres.statut) params.set('statut', filtres.statut);
    if (filtres.deplacement) params.set('deplacement_physique', filtres.deplacement === 'oui' ? 'true' : 'false');
    return apiClient<PageDossiers>(`${BASE}/candidatures?${params}`, { headers: enteteAuth(session) }).catch(surSessionRefusee);
  },

  obtenir: (session: Session, reference: string): Promise<DossierAdmin> =>
    apiClient<DossierAdmin>(`${BASE}/candidatures/${encodeURIComponent(reference)}`, { headers: enteteAuth(session) }).catch(
      surSessionRefusee,
    ),

  /**
   * Télécharge une pièce déposée. Un <img> ou <iframe> ne peut pas envoyer l'en-tête d'authentification : on récupère
   * le fichier avec fetch puis on l'affiche depuis une URL locale (à libérer avec `URL.revokeObjectURL`).
   */
  telechargerDocument: async (session: Session, documentId: string): Promise<Blob> => {
    const reponse = await fetch(urlApi(`${BASE}/proxy-document/${encodeURIComponent(documentId)}`), {
      headers: enteteAuth(session),
    });
    if (!reponse.ok) return surSessionRefusee(new ApiError(reponse.status, null, `Erreur API (${reponse.status})`));
    return reponse.blob();
  },
};
