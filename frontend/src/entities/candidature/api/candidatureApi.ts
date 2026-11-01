import { apiClient, ApiError } from '../../../shared/api/client';
import type { Brouillon, ErreursChamps, InformationsPersonnelles, MethodePaiement } from '../model/types';

const BASE = '/api/v1/candidatures';

export const candidatureApi = {
  creerBrouillon: (informations: InformationsPersonnelles): Promise<Brouillon> =>
    apiClient<Brouillon>(BASE, { method: 'POST', body: JSON.stringify(informations) }),

  obtenirBrouillon: (id: string): Promise<Brouillon> => apiClient<Brouillon>(`${BASE}/${id}`),

  modifierInformations: (id: string, informations: InformationsPersonnelles): Promise<Brouillon> =>
    apiClient<Brouillon>(`${BASE}/${id}/informations`, { method: 'PUT', body: JSON.stringify(informations) }),

  /** Simule le paiement des frais de dossier : aucun montant réel n'est prélevé. */
  simulerPaiement: (id: string, methode: MethodePaiement, numeroTelephone: string): Promise<Brouillon> =>
    apiClient<Brouillon>(`${BASE}/${id}/paiement`, {
      method: 'POST',
      body: JSON.stringify({ methode, numero_telephone: numeroTelephone }),
    }),

  definirDeplacementPhysique: (id: string, deplacementPhysique: boolean): Promise<Brouillon> =>
    apiClient<Brouillon>(`${BASE}/${id}/deplacement-physique`, {
      method: 'PUT',
      body: JSON.stringify({ deplacement_physique: deplacementPhysique }),
    }),
};

/** Extrait les messages par champ d'une réponse 422 de l'API, ou null si l'erreur est d'un autre type. */
export function extraireErreursChamps(erreur: unknown): ErreursChamps | null {
  if (!(erreur instanceof ApiError) || erreur.status !== 422) return null;
  const detail = (erreur.body as { detail?: { erreurs?: ErreursChamps } } | null)?.detail;
  return detail?.erreurs ?? null;
}
