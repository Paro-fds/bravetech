import React from 'react';

interface ChampTexteProps {
  id: string;
  libelle: string;
  erreur?: string;
  aide?: string;
  children: (props: { id: string; 'aria-invalid': boolean; 'aria-describedby'?: string; className: string }) => React.ReactNode;
}

const CLASSE_BASE =
  'w-full min-h-12 rounded-lg border-[1.5px] bg-fds-surface px-3 text-base text-fds-ink focus:outline-none focus:ring-2 focus:ring-fds-accent';

/** Libellé + champ + message d'aide ou d'erreur, reliés pour les lecteurs d'écran (style des maquettes). */
export const ChampTexte: React.FC<ChampTexteProps> = ({ id, libelle, erreur, aide, children }) => {
  const idMessage = erreur || aide ? `${id}-message` : undefined;
  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={id} className="text-[15px] font-semibold">
        {libelle}
      </label>
      {children({
        id,
        'aria-invalid': Boolean(erreur),
        'aria-describedby': idMessage,
        className: `${CLASSE_BASE} ${erreur ? 'border-fds-bad' : 'border-fds-field'}`,
      })}
      {erreur ? (
        <p id={idMessage} role="alert" className="text-sm font-semibold text-fds-bad">
          {erreur}
        </p>
      ) : (
        aide && (
          <p id={idMessage} className="text-[13px] text-fds-mute">
            {aide}
          </p>
        )
      )}
    </div>
  );
};
