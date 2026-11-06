import { apiClient, ApiError } from '../../../shared/api';

export interface MessageContact {
  nom: string;
  email: string;
  message: string;
  /** Piège à robots : toujours vide pour un visiteur humain. */
  site_web?: string;
}

export type ErreursContact = Partial<Record<'nom' | 'email' | 'message', string>>;

export const contactApi = {
  /**
   * Envoie un message au secrétariat. Rejette avec une `ApiError` : 422 (`detail.erreurs`), 429 trop de messages,
   * 503 envoi impossible pour le moment (le visiteur garde son texte et peut réessayer).
   */
  envoyer: (message: MessageContact): Promise<{ envoye: boolean }> =>
    apiClient<{ envoye: boolean }>('/api/v1/contact', { method: 'POST', body: JSON.stringify(message) }),
};

/** Messages par champ d'une réponse 422, ou null si l'erreur est d'un autre type. */
export function extraireErreursContact(erreur: unknown): ErreursContact | null {
  if (!(erreur instanceof ApiError) || erreur.status !== 422) return null;
  const detail = (erreur.body as { detail?: { erreurs?: ErreursContact } } | null)?.detail;
  return detail?.erreurs ?? null;
}
