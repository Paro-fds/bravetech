import React from 'react';

interface ChampTexteProps {
  id: string;
  libelle: string;
  erreur?: string;
  aide?: string;
  children: (props: { id: string; 'aria-invalid': boolean; 'aria-describedby'?: string; className: string }) => React.ReactNode;
}

const CLASSE_BASE =
  'w-full min-h-12 rounded-xl border bg-white px-3.5 text-base text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500';

/** Libellé + champ + message d'aide ou d'erreur, reliés pour les lecteurs d'écran. */
export const ChampTexte: React.FC<ChampTexteProps> = ({ id, libelle, erreur, aide, children }) => {
  const idMessage = erreur || aide ? `${id}-message` : undefined;
  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={id} className="text-sm font-semibold text-slate-800">
        {libelle}
      </label>
      {children({
        id,
        'aria-invalid': Boolean(erreur),
        'aria-describedby': idMessage,
        className: `${CLASSE_BASE} ${erreur ? 'border-rose-500' : 'border-slate-400'}`,
      })}
      {erreur ? (
        <p id={idMessage} role="alert" className="text-sm font-medium text-rose-700">
          {erreur}
        </p>
      ) : (
        aide && (
          <p id={idMessage} className="text-xs text-slate-500">
            {aide}
          </p>
        )
      )}
    </div>
  );
};
