import { create } from 'zustand';
import { attributTheme, CLE_THEME, themeEffectif, themeValide, type Theme } from './theme';

interface ThemeState {
  /** Choix explicite de l'utilisateur ; null tant qu'il n'a rien choisi (on suit alors le système). */
  preference: Theme | null;
  systemeSombre: boolean;
  theme: Theme;
  basculer: () => void;
}

const REQUETE_SOMBRE = '(prefers-color-scheme: dark)';

/** localStorage peut être absent ou bloqué (navigation privée) : le choix n'est alors pas mémorisé, sans erreur. */
function lirePreference(): Theme | null {
  try {
    return themeValide(localStorage.getItem(CLE_THEME));
  } catch {
    return null;
  }
}

function enregistrerPreference(theme: Theme): void {
  try {
    localStorage.setItem(CLE_THEME, theme);
  } catch {
    // ignoré : le thème reste actif pour la visite en cours
  }
}

function systemeEstSombre(): boolean {
  return typeof window !== 'undefined' && typeof window.matchMedia === 'function' && window.matchMedia(REQUETE_SOMBRE).matches;
}

function appliquerAuDocument(theme: Theme): void {
  if (typeof document !== 'undefined') document.documentElement.dataset.theme = attributTheme(theme);
}

const preferenceInitiale = lirePreference();
const systemeInitial = systemeEstSombre();

export const useTheme = create<ThemeState>()((set, get) => ({
  preference: preferenceInitiale,
  systemeSombre: systemeInitial,
  theme: themeEffectif(preferenceInitiale, systemeInitial),
  basculer: () => {
    const suivant: Theme = get().theme === 'sombre' ? 'clair' : 'sombre';
    enregistrerPreference(suivant);
    set({ preference: suivant, theme: suivant });
  },
}));

appliquerAuDocument(useTheme.getState().theme);
useTheme.subscribe((etat, avant) => {
  if (etat.theme !== avant.theme) appliquerAuDocument(etat.theme);
});

// Sans choix explicite, on suit le système même s'il change pendant la visite (passage auto en mode nuit).
if (typeof window !== 'undefined' && typeof window.matchMedia === 'function') {
  window.matchMedia(REQUETE_SOMBRE).addEventListener('change', (e) => {
    const { preference } = useTheme.getState();
    useTheme.setState({ systemeSombre: e.matches, theme: themeEffectif(preference, e.matches) });
  });
}
