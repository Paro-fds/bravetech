import { useCallback } from 'react';
import { fr, type Cle } from './fr';
import { traduire, type Variables } from './traduire';
import { useLangue } from './useLangue';

/** Traducteur pour un composant : se met à jour quand la langue change ou quand le dictionnaire créole arrive. */
export function useT() {
  const langue = useLangue((s) => s.langue);
  const kr = useLangue((s) => s.kr);
  return useCallback((cle: Cle, variables?: Variables) => traduire(cle, langue, fr, kr, variables), [langue, kr]);
}

/**
 * Nom d'une pièce à fournir : traduit en créole d'après son identifiant ; en français (ou sans traduction connue),
 * le nom renvoyé par l'API est utilisé tel quel.
 */
export function useNomPiece() {
  const langue = useLangue((s) => s.langue);
  const kr = useLangue((s) => s.kr);
  return useCallback(
    (id: string, nomApi: string) => {
      const cle = `piece.${id}`;
      const traduit = traduire(cle, langue, fr, kr);
      return langue === 'kr' && traduit !== cle ? traduit : nomApi;
    },
    [langue, kr],
  );
}

/** Nom d'un département : traduit en créole s'il est connu, sinon la valeur telle quelle. */
export function useNomDepartement() {
  const langue = useLangue((s) => s.langue);
  const kr = useLangue((s) => s.kr);
  return useCallback(
    (departement: string) => {
      const cle = `dept.${departement}`;
      const traduit = traduire(cle, langue, fr, kr);
      return langue === 'kr' && traduit !== cle ? traduit : departement;
    },
    [langue, kr],
  );
}

/** Traduction hors composant (fonctions utilitaires) : lit la langue courante au moment de l'appel. */
export function traduireMaintenant(cle: Cle, variables?: Variables): string {
  const { langue, kr } = useLangue.getState();
  return traduire(cle, langue, fr, kr, variables);
}
