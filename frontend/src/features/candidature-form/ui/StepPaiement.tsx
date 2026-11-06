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
import { useT } from '../../../shared/i18n';

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
  const t = useT();
  const [erreurs, setErreurs] = useState<ErreursChamps>({});
  const [messageGlobal, setMessageGlobal] = useState<string | null>(null);
  const [enCours, setEnCours] = useState(false);

  const soumettre = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessageGlobal(null);

    const erreursLocales: ErreursChamps = {};
    if (!methode) erreursLocales.methode_paiement = t('pay.erreurMethode');
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
        setMessageGlobal(t('pay.erreurReseau'));
    } finally {
      setEnCours(false);
    }
  };

  return (
    <form onSubmit={soumettre} noValidate className="flex flex-col gap-[18px] flex-1">
      <div role="note" className="bandeau-simulation rounded-[10px] px-3.5 py-3 text-fds-warn font-semibold text-sm">
        <div className="flex items-center gap-2 mb-1 text-base">
          <TriangleAlert className="w-5 h-5" aria-hidden="true" />
          <span>{t('pay.badge')}</span>
        </div>
        {t('pay.bandeau')}
      </div>

      <h1 className="font-fds-serif text-2xl font-bold text-fds-title">{t('pay.titre')}</h1>

      <div className="flex items-center justify-between rounded-xl border border-fds-line bg-fds-surface p-4">
        <div>
          <div className="text-sm text-fds-mute">{t('pay.montant')}</div>
          <div className="font-fds-serif text-3xl font-bold text-fds-title">{montantHtg} HTG</div>
        </div>
        <span className="rounded-full bg-fds-warn-bg text-fds-warn text-[13px] font-semibold px-2.5 py-0.5">{t('pay.tag')}</span>
      </div>

      <fieldset className="flex flex-col gap-2.5" aria-describedby={erreurs.methode_paiement ? 'erreur-methode' : undefined}>
        <legend className="text-[15px] font-semibold mb-1.5">{t('pay.service')}</legend>
        {OPERATEURS.map((op) => {
          const choisi = methode === op.valeur;
          return (
            <label
              key={op.valeur}
              className={`flex items-start gap-3 rounded-[10px] border-2 p-3.5 min-h-12 cursor-pointer ${
                choisi ? 'border-fds-accent bg-fds-navy-t' : 'border-fds-line bg-fds-surface'
              }`}
            >
              <input
                type="radio"
                name="methode_paiement"
                className="w-5 h-5 mt-0.5 accent-fds-accent"
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
                <span className="block text-sm text-fds-mute">{t('pay.simulPar', { nom: op.nom })}</span>
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
        libelle={t('pay.numero')}
        erreur={erreurs.numero_telephone}
        aide={t('pay.numeroAide')}
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

      <div className="flex gap-2.5 items-start rounded-[10px] border border-fds-accent-line bg-fds-navy-t px-3.5 py-3 text-sm text-fds-title">
        <Info className="w-5 h-5 shrink-0" aria-hidden="true" />
        <span>
          {t('pay.refAvant')}<strong>PAY-SIM-2026-XXXX</strong>{t('pay.refApres')}
        </span>
      </div>

      {messageGlobal && (
        <p role="alert" className="rounded-[10px] border border-fds-bad-line bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
          {messageGlobal}
        </p>
      )}

      <BarreAction>
        <button type="submit" disabled={enCours} className={CLASSE_BOUTON_PRIMAIRE}>
          {enCours ? t('pay.enCours') : t('pay.bouton', { montant: montantHtg })}
        </button>
        <button type="button" onClick={onRetour} className="min-h-11 text-fds-accent font-semibold underline">
          {t('commun.retour')}
        </button>
      </BarreAction>
    </form>
  );
};
