import { create } from 'zustand';
import { createJSONStorage, persist, type StateStorage } from 'zustand/middleware';
import {
  INFORMATIONS_VIDES,
  STATUT_PAIEMENT_SIMULE,
  STATUT_SOUMISE,
  type Brouillon,
  type InformationsPersonnelles,
  type MethodePaiement,
} from '../../../entities/candidature';

/** 1 informations, 2 admission, 3 paiement, 4 pièces, 5 récapitulatif, 6 confirmation (dossier soumis). */
export type EtapeCandidature = 1 | 2 | 3 | 4 | 5 | 6;

/** Montant des frais de dossier tant que le serveur ne l'a pas renvoyé (la valeur de référence vient de l'API). */
export const FRAIS_DOSSIER_PAR_DEFAUT = 500;

export interface PaiementSimule {
  reference: string;
  methode: MethodePaiement | null;
}

/** Dossier soumis : référence officielle et horodatage UTC. */
export interface Soumission {
  reference: string;
  soumiseLe: string;
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
  /** Renseigné une fois le dossier soumis. */
  soumission: Soumission | null;
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
  soumission: null,
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
          soumission:
            brouillon.statut === STATUT_SOUMISE && brouillon.reference_dossier && brouillon.soumise_le
              ? { reference: brouillon.reference_dossier, soumiseLe: brouillon.soumise_le }
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
