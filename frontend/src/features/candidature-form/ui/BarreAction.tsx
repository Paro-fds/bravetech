import React from 'react';

/** Barre d'actions fixée en bas de l'écran sur mobile (maquettes) ; sur ordinateur, une ligne en bas du formulaire. */
export const BarreAction: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="sticky bottom-0 -mx-4 mt-auto bg-fds-surface border-t border-fds-line px-4 py-3 flex flex-col gap-2 lg:static lg:mx-0 lg:mt-8 lg:px-0 lg:pb-0 lg:pt-6">
    {children}
  </div>
);

export const CLASSE_BOUTON_PRIMAIRE =
  'min-h-12 px-4 rounded-lg bg-fds-navy hover:bg-fds-navy-d disabled:opacity-60 text-white font-semibold flex items-center justify-center gap-2 transition-colors';

export const CLASSE_BOUTON_SECONDAIRE =
  'min-h-12 px-4 rounded-lg border-2 border-fds-accent bg-fds-surface text-fds-accent font-semibold flex items-center justify-center gap-2';
