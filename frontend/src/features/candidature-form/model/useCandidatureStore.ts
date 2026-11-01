import { create } from 'zustand';
import { createJSONStorage, persist, type StateStorage } from 'zustand/middleware';
import {
  INFORMATIONS_VIDES,
  STATUT_PAIEMENT_SIMULE,
  type Brouillon,
  type InformationsPersonnelles,
  type MethodePaiement,
} from '../../../entities/candidature';

export type EtapeCandidature = 1 | 2 | 3 | 4;

/** Montant des frais de dossier tant que le serveur ne l'a pas renvoyé (la valeur de référence vient de l'API). */
export const FRAIS_DOSSIER_PAR_DEFAUT = 500;

export interface PaiementSimule {
  reference: string;
  methode: MethodePaiement | null;
}

interface CandidatureState {
  /** Identifiant du brouillon côté serveur : permet de reprendre après une coupure de connexion. */
  candidatureId: string | null;
  etape: EtapeCandidature;
  informations: InformationsPersonnelles;
  deplacementPhysique: boolean | null;
  montantHtg: number;
  /** Renseigné une fois le paiement simulé enregistré. */
  paiement: PaiementSimule | null;
  /** Saisie en cours de l'étape 3, conservée si l'on change d'écran. */
  methodePaiementChoisie: MethodePaiement | null;
  numeroPaiement: string;
  setInformations: (informations: InformationsPersonnelles) => void;
  /** Aligne l'état local sur le brouillon renvoyé par le serveur (source de vérité). */
  appliquerBrouillon: (brouillon: Brouillon) => void;
  setDeplacementPhysique: (valeur: boolean | null) => void;
  setSaisiePaiement: (methode: MethodePaiement | null, numero: string) => void;
  allerEtape: (etape: EtapeCandidature) => void;
  reinitialiser: () => void;
}

const etatInitial = {
  candidatureId: null,
  etape: 1 as EtapeCandidature,
  informations: INFORMATIONS_VIDES,
  deplacementPhysique: null,
  montantHtg: FRAIS_DOSSIER_PAR_DEFAUT,
  paiement: null,
  methodePaiementChoisie: null,
  numeroPaiement: '',
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
      appliquerBrouillon: (brouillon) =>
        set({
          candidatureId: brouillon.candidature_id,
          informations: brouillon.informations,
          deplacementPhysique: brouillon.deplacement_physique,
          montantHtg: brouillon.montant_htg,
          paiement:
            brouillon.statut_paiement === STATUT_PAIEMENT_SIMULE && brouillon.reference_paiement
              ? { reference: brouillon.reference_paiement, methode: brouillon.methode_paiement }
              : null,
        }),
      setDeplacementPhysique: (deplacementPhysique) => set({ deplacementPhysique }),
      setSaisiePaiement: (methodePaiementChoisie, numeroPaiement) => set({ methodePaiementChoisie, numeroPaiement }),
      allerEtape: (etape) => set({ etape }),
      reinitialiser: () => set({ ...etatInitial }),
    }),
    { name: 'fds-candidature', storage: createJSONStorage(() => stockageSecurise) },
  ),
);
