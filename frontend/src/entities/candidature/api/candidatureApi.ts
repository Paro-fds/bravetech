import { apiClient, ApiError, urlApi } from '../../../shared/api/client';
import type {
  Brouillon,
  ErreursChamps,
  InformationsPersonnelles,
  MethodePaiement,
  PieceDossier,
  SuiviDossier,
} from '../model/types';

const BASE = '/api/v1/candidatures';

export const candidatureApi = {
  creerBrouillon: (informations: InformationsPersonnelles): Promise<Brouillon> =>
    apiClient<Brouillon>(BASE, { method: 'POST', body: JSON.stringify(informations) }),

  obtenirBrouillon: (id: string): Promise<Brouillon> => apiClient<Brouillon>(`${BASE}/${id}`),

  modifierInformations: (id: string, informations: InformationsPersonnelles): Promise<Brouillon> =>
    apiClient<Brouillon>(`${BASE}/${id}/informations`, { method: 'PUT', body: JSON.stringify(informations) }),

  /**
   * Soumet définitivement le dossier et renvoie la référence officielle. Idempotent : soumettre deux fois
   * renvoie la même référence. Rejette avec une `ApiError` 409 (`detail.manques`) si le dossier est incomplet.
   */
  soumettre: (id: string): Promise<Brouillon> => apiClient<Brouillon>(`${BASE}/${id}/soumission`, { method: 'POST' }),

  /** Liste les pièces requises avec l'état de chaque dépôt. */
  listerPieces: (id: string): Promise<PieceDossier[]> => apiClient<PieceDossier[]>(`${BASE}/${id}/documents`),

  /**
   * Téléverse (ou remplace) une pièce. XMLHttpRequest plutôt que fetch : seul moyen de suivre la progression
   * de l'envoi, utile sur une connexion 3G lente. Rejette avec une `ApiError` si le serveur refuse le fichier.
   */
  televerserPiece: (
    id: string,
    pieceId: string,
    fichier: File,
    onProgression?: (pourcentage: number) => void,
  ): Promise<PieceDossier> =>
    new Promise((resolve, reject) => {
      const corps = new FormData();
      corps.append('fichier', fichier);

      const xhr = new XMLHttpRequest();
      xhr.open('POST', urlApi(`${BASE}/${id}/documents/${pieceId}`));
      xhr.upload.onprogress = (e) => {
        if (e.lengthComputable && onProgression) onProgression(Math.round((e.loaded / e.total) * 100));
      };
      xhr.onload = () => {
        let decode: unknown = xhr.responseText;
        try {
          decode = JSON.parse(xhr.responseText);
        } catch {
          // corps non JSON : on garde le texte brut
        }
        if (xhr.status >= 200 && xhr.status < 300) resolve(decode as PieceDossier);
        else reject(new ApiError(xhr.status, decode, `Erreur API (${xhr.status}): ${xhr.responseText}`));
      };
      xhr.onerror = () => reject(new TypeError('Envoi interrompu'));
      xhr.ontimeout = () => reject(new TypeError('Envoi interrompu'));
      xhr.send(corps);
    }),

  /**
   * Suivi public d'un dossier soumis. Rejette avec une `ApiError` 404 si la référence est inconnue,
   * 429 si trop de recherches ont été faites en une minute.
   */
  obtenirSuivi: (reference: string): Promise<SuiviDossier> =>
    apiClient<SuiviDossier>(`${BASE}/${encodeURIComponent(reference)}/statut`),

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

/** Liste des éléments manquants d'un dossier incomplet (réponse 409 de la soumission), ou null. */
export function extraireManques(erreur: unknown): string[] | null {
  if (!(erreur instanceof ApiError) || erreur.status !== 409) return null;
  const detail = (erreur.body as { detail?: { manques?: string[] } } | null)?.detail;
  return Array.isArray(detail?.manques) ? detail.manques : null;
}
