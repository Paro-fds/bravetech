import { create } from 'zustand';
import { createJSONStorage, persist, type StateStorage } from 'zustand/middleware';
import { INFORMATIONS_VIDES, type InformationsPersonnelles } from '../../../entities/candidature';

export type EtapeCandidature = 1 | 2 | 3;

interface CandidatureState {
  /** Identifiant du brouillon côté serveur : permet de reprendre après une coupure de connexion. */
  candidatureId: string | null;
  etape: EtapeCandidature;
  informations: InformationsPersonnelles;
  deplacementPhysique: boolean | null;
  setInformations: (informations: InformationsPersonnelles) => void;
  setBrouillon: (candidatureId: string, informations: InformationsPersonnelles, deplacementPhysique: boolean | null) => void;
  setDeplacementPhysique: (valeur: boolean | null) => void;
  allerEtape: (etape: EtapeCandidature) => void;
  reinitialiser: () => void;
}

const etatInitial = {
  candidatureId: null,
  etape: 1 as EtapeCandidature,
  informations: INFORMATIONS_VIDES,
  deplacementPhysique: null,
};

/** localStorage peut être absent ou bloqué (navigation privée) : on n'échoue jamais pour autant. */
const stockageSecurise: StateStorage = {
  getItem: (nom) => {
    try {
      return localStorage.getItem(nom);
    } catch {
      return null;
    }
  },
  setItem: (nom, valeur) => {
    try {
      localStorage.setItem(nom, valeur);
    } catch {
      // ignoré : le formulaire reste utilisable sans sauvegarde locale
    }
  },
  removeItem: (nom) => {
    try {
      localStorage.removeItem(nom);
    } catch {
      // ignoré
    }
  },
};

export const useCandidatureStore = create<CandidatureState>()(
  persist(
    (set) => ({
      ...etatInitial,
      setInformations: (informations) => set({ informations }),
      setBrouillon: (candidatureId, informations, deplacementPhysique) =>
        set({ candidatureId, informations, deplacementPhysique }),
      setDeplacementPhysique: (deplacementPhysique) => set({ deplacementPhysique }),
      allerEtape: (etape) => set({ etape }),
      reinitialiser: () => set({ ...etatInitial }),
    }),
    { name: 'fds-candidature', storage: createJSONStorage(() => stockageSecurise) },
  ),
);
