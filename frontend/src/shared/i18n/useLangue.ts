import { create } from 'zustand';
import { createJSONStorage, persist, type StateStorage } from 'zustand/middleware';
import { codeHtml, langueValide, type Dictionnaire, type Langue } from './traduire';

interface LangueState {
  langue: Langue;
  /** Dictionnaire créole, chargé à la demande (null tant qu'il n'est pas arrivé, ou en français). */
  kr: Dictionnaire | null;
  setLangue: (langue: Langue) => void;
  chargerKr: () => Promise<void>;
}

/** localStorage peut être absent ou bloqué (navigation privée) : le choix n'est alors pas mémorisé, sans erreur. */
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
      // ignoré : la langue reste active pour la visite en cours
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

function appliquerLangueAuDocument(langue: Langue): void {
  if (typeof document !== 'undefined') document.documentElement.lang = codeHtml(langue);
}

let chargementKr: Promise<void> | null = null;

export const useLangue = create<LangueState>()(
  persist(
    (set, get) => ({
      langue: 'fr',
      kr: null,
      setLangue: (langue) => {
        appliquerLangueAuDocument(langue);
        set({ langue });
        if (langue === 'kr') void get().chargerKr();
      },
      chargerKr: () => {
        if (get().kr) return Promise.resolve();
        // Un seul chargement à la fois ; en cas d'échec réseau on pourra réessayer (le français reste affiché)
        chargementKr ??= import('./kr')
          .then((module) => {
            set({ kr: module.kr as Dictionnaire });
          })
          .catch(() => undefined)
          .finally(() => {
            chargementKr = null;
          });
        return chargementKr as Promise<void>;
      },
    }),
    {
      name: 'fds-langue',
      storage: createJSONStorage(() => stockageSecurise),
      partialize: (etat) => ({ langue: etat.langue }), // le dictionnaire n'est jamais mémorisé
      merge: (sauvegarde, courant) => ({ ...courant, langue: langueValide((sauvegarde as Partial<LangueState> | undefined)?.langue) }),
      onRehydrateStorage: () => (etat) => {
        if (!etat) return;
        appliquerLangueAuDocument(etat.langue);
        if (etat.langue === 'kr') void etat.chargerKr();
      },
    },
  ),
);
