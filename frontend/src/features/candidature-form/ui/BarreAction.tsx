import React from 'react';

/** Barre d'actions fixée en bas de l'écran (boutons Continuer / Retour), comme sur les maquettes mobiles. */
export const BarreAction: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="sticky bottom-0 -mx-4 mt-auto bg-white border-t border-fds-line px-4 py-3 flex flex-col gap-2">
    {children}
  </div>
);

export const CLASSE_BOUTON_PRIMAIRE =
  'min-h-12 px-4 rounded-lg bg-fds-navy hover:bg-fds-navy-d disabled:opacity-60 text-white font-semibold flex items-center justify-center gap-2 transition-colors';

export const CLASSE_BOUTON_SECONDAIRE =
  'min-h-12 px-4 rounded-lg border-2 border-fds-navy bg-white text-fds-navy font-semibold flex items-center justify-center gap-2';
