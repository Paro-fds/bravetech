import React, { useState } from 'react';
import { TriangleAlert, Info } from 'lucide-react';
import {
  extraireErreursChamps,
  type ErreursChamps,
  type MethodePaiement,
} from '../../../entities/candidature';
import { validerNumeroHaitien } from '../lib/validation';
import { BarreAction, CLASSE_BOUTON_PRIMAIRE } from './BarreAction';
import { ChampTexte } from './ChampTexte';

interface StepPaiementProps {
  montantHtg: number;
  methode: MethodePaiement | null;
  numero: string;
  onChange: (methode: MethodePaiement | null, numero: string) => void;
  /** Envoie la simulation au serveur ; rejette en cas d'erreur. */
  onSoumettre: (methode: MethodePaiement, numero: string) => Promise<void>;
  onRetour: () => void;
}

const OPERATEURS: { valeur: MethodePaiement; nom: string; operateur: string }[] = [
  { valeur: 'MONCASH', nom: 'MonCash', operateur: 'Digicel' },
  { valeur: 'NATCASH', nom: 'NatCash', operateur: 'Natcom' },
];

/**
 * Étape 3 : paiement SIMULÉ des frais de dossier (maquette « Candidature 3/4 »).
 * Le candidat ne doit jamais croire qu'il paye réellement (AGENTS.md, fait critique 8).
 */
export const StepPaiement: React.FC<StepPaiementProps> = ({ montantHtg, methode, numero, onChange, onSoumettre, onRetour }) => {
  const [erreurs, setErreurs] = useState<ErreursChamps>({});
  const [messageGlobal, setMessageGlobal] = useState<string | null>(null);
  const [enCours, setEnCours] = useState(false);

  const soumettre = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessageGlobal(null);

    const erreursLocales: ErreursChamps = {};
    if (!methode) erreursLocales.methode_paiement = 'Choisissez MonCash ou NatCash.';
    const erreurNumero = validerNumeroHaitien(numero);
    if (erreurNumero) erreursLocales.numero_telephone = erreurNumero;
    if (Object.keys(erreursLocales).length > 0 || !methode) {
      setErreurs(erreursLocales);
      return;
    }

    setErreurs({});
    setEnCours(true);
    try {
      await onSoumettre(methode, numero);
    } catch (erreur) {
      const erreursServeur = extraireErreursChamps(erreur);
      if (erreursServeur) setErreurs(erreursServeur);
      else
        setMessageGlobal(
          "Impossible d'enregistrer la simulation pour le moment. Vérifiez votre connexion et réessayez : aucun argent n'a été prélevé.",
        );
    } finally {
      setEnCours(false);
    }
  };

  return (
    <form onSubmit={soumettre} noValidate className="flex flex-col gap-[18px] flex-1">
      <div role="note" className="bandeau-simulation rounded-[10px] px-3.5 py-3 text-fds-warn font-semibold text-sm">
        <div className="flex items-center gap-2 mb-1 text-base">
          <TriangleAlert className="w-5 h-5" aria-hidden="true" />
          <span>PAIEMENT SIMULÉ</span>
        </div>
        Simulation de paiement : aucun montant réel ne sera prélevé lors de cette phase de test.
      </div>

      <h1 className="font-fds-serif text-2xl font-bold text-fds-navy-d">Frais de dossier</h1>

      <div className="flex items-center justify-between rounded-xl border border-fds-line bg-white p-4">
        <div>
          <div className="text-sm text-fds-mute">Montant à régler</div>
          <div className="font-fds-serif text-3xl font-bold text-fds-navy-d">{montantHtg} HTG</div>
        </div>
        <span className="rounded-full bg-fds-warn-bg text-fds-warn text-[13px] font-semibold px-2.5 py-0.5">Simulation</span>
      </div>

      <fieldset className="flex flex-col gap-2.5" aria-describedby={erreurs.methode_paiement ? 'erreur-methode' : undefined}>
        <legend className="text-[15px] font-semibold mb-1.5">Choisissez un service</legend>
        {OPERATEURS.map((op) => {
          const choisi = methode === op.valeur;
          return (
            <label
              key={op.valeur}
              className={`flex items-start gap-3 rounded-[10px] border-2 p-3.5 min-h-12 cursor-pointer ${
                choisi ? 'border-fds-navy bg-fds-navy-t' : 'border-fds-line bg-white'
              }`}
            >
              <input
                type="radio"
                name="methode_paiement"
                className="w-5 h-5 mt-0.5 accent-[#01346d]"
                checked={choisi}
                onChange={() => {
                  onChange(op.valeur, numero);
                  setErreurs((prec) => ({ ...prec, methode_paiement: undefined }));
                }}
              />
              <span>
                <span className="block font-semibold">
                  {op.nom} <span className="font-normal text-fds-mute">({op.operateur})</span>
                </span>
                <span className="block text-sm text-fds-mute">Simulation du paiement par {op.nom}</span>
              </span>
            </label>
          );
        })}
        {erreurs.methode_paiement && (
          <p id="erreur-methode" role="alert" className="text-sm font-semibold text-fds-bad">
            {erreurs.methode_paiement}
          </p>
        )}
      </fieldset>

      <ChampTexte
        id="numero_telephone"
        libelle="Numéro de téléphone du compte"
        erreur={erreurs.numero_telephone}
        aide="Numéro haïtien à 8 chiffres."
      >
        {(p) => (
          <input
            {...p}
            type="tel"
            inputMode="tel"
            autoComplete="tel"
            placeholder="37 12 34 56"
            value={numero}
            onChange={(e) => {
              onChange(methode, e.target.value);
              if (erreurs.numero_telephone) setErreurs((prec) => ({ ...prec, numero_telephone: undefined }));
            }}
          />
        )}
      </ChampTexte>

      <div className="flex gap-2.5 items-start rounded-[10px] border border-[#b9cbe3] bg-fds-navy-t px-3.5 py-3 text-sm text-fds-navy-d">
        <Info className="w-5 h-5 shrink-0" aria-hidden="true" />
        <span>
          Après validation, une référence de simulation de type <strong>PAY-SIM-2026-XXXX</strong> vous sera donnée. Elle
          ne correspond à aucun vrai paiement.
        </span>
      </div>

      {messageGlobal && (
        <p role="alert" className="rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
          {messageGlobal}
        </p>
      )}

      <BarreAction>
        <button type="submit" disabled={enCours} className={CLASSE_BOUTON_PRIMAIRE}>
          {enCours ? 'Simulation en cours…' : `Simuler le paiement de ${montantHtg} HTG`}
        </button>
        <button type="button" onClick={onRetour} className="min-h-11 text-fds-navy font-semibold underline">
          Retour
        </button>
      </BarreAction>
    </form>
  );
};
