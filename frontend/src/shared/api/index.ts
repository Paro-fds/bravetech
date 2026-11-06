/** API publique du segment (Feature-Sliced Design) : les autres couches importent d'ici, jamais d'un fichier interne. */
export { apiClient, ApiError, urlApi } from './client';
