// Vide par défaut : les appels passent par le même domaine (proxy Vite en dev, Nginx en production).
// `??` (et non `||`) pour qu'une valeur vide reste vide au lieu de retomber sur localhost.
const API_BASE_URL = import.meta.env.VITE_API_URL ?? '';

/** Erreur HTTP de l'API, avec le statut et le corps de réponse décodé (JSON si possible). */
export class ApiError extends Error {
  status: number;
  body: unknown;

  constructor(status: number, body: unknown, message: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.body = body;
  }
}

export async function apiClient<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const errorBody = await response.text();
    let decoded: unknown = errorBody;
    try {
      decoded = JSON.parse(errorBody);
    } catch {
      // corps non JSON : on garde le texte brut
    }
    throw new ApiError(
      response.status,
      decoded,
      `Erreur API (${response.status}): ${errorBody || response.statusText}`,
    );
  }

  return response.json();
}
