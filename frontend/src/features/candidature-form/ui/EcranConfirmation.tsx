import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Check, Copy, Info, Mail, TriangleAlert } from 'lucide-react';
import { formaterHorodatage } from '../lib/dates';
import { useT } from '../../../shared/i18n/useT';

interface EcranConfirmationProps {
  prenom: string;
  email: string;
  reference: string;
  soumiseLe: string;
  montantHtg: number;
  referencePaiement: string | null;
  onNouvelleCandidature: () => void;
}

/** Copie dans le presse-papiers ; retombe sur une sélection manuelle si l'API moderne est indisponible. */
async function copier(texte: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(texte);
    return true;
  } catch {
    try {
      const zone = document.createElement('textarea');
      zone.value = texte;
      zone.setAttribute('readonly', '');
      zone.style.position = 'fixed';
      zone.style.opacity = '0';
      document.body.appendChild(zone);
      zone.select();
      const ok = document.execCommand('copy');
      document.body.removeChild(zone);
      return ok;
    } catch {
      return false;
    }
  }
}

/**
 * Écran de succès (maquette « Confirmation »). La référence est TOUJOURS affichée, même si l'email échoue :
 * l'email est une notification, pas la source de vérité (AGENTS.md, fait critique 2).
 */
export const EcranConfirmation: React.FC<EcranConfirmationProps> = ({
  prenom,
  email,
  reference,
  soumiseLe,
  montantHtg,
  referencePaiement,
  onNouvelleCandidature,
}) => {
  const [copie, setCopie] = useState<'idle' | 'ok' | 'echec'>('idle');
  const t = useT();

  const copierReference = async () => {
    setCopie((await copier(reference)) ? 'ok' : 'echec');
    window.setTimeout(() => setCopie('idle'), 3000);
  };

  return (
    <div className="flex flex-col gap-[18px] flex-1 pb-8" aria-live="polite">
      <div className="flex flex-col items-center text-center gap-2.5">
        <span className="w-16 h-16 rounded-full bg-fds-ok-solid text-white flex items-center justify-center">
          <Check className="w-9 h-9" strokeWidth={2.5} aria-hidden="true" />
        </span>
        <h1 className="font-fds-serif text-2xl font-bold text-fds-title">{t('conf.titre')}</h1>
        <p className="text-fds-mute">{t('conf.merci', { prenom })}</p>
      </div>

      <section className="rounded-xl border-2 border-fds-accent bg-fds-surface p-4 flex flex-col gap-2 text-center" aria-label={t('conf.refAria')}>
        <div className="text-sm text-fds-mute">{t('conf.refLabel')}</div>
        <div className="font-fds-serif text-[34px] leading-tight font-bold text-fds-title tracking-wide break-all" data-testid="reference-dossier">
          {reference}
        </div>
        <div className="flex gap-2.5 items-start text-left rounded-[10px] border border-fds-warn-line bg-fds-warn-bg px-3.5 py-3 text-sm text-fds-warn">
          <TriangleAlert className="w-5 h-5 shrink-0" aria-hidden="true" />
          <span>
            <strong>{t('conf.notez')}</strong>{t('conf.notezSuite')}
          </span>
        </div>
        <button
          type="button"
          onClick={() => void copierReference()}
          className="min-h-12 rounded-lg border-2 border-fds-accent bg-fds-surface text-fds-accent font-semibold flex items-center justify-center gap-2"
        >
          {copie === 'ok' ? <Check className="w-5 h-5" aria-hidden="true" /> : <Copy className="w-5 h-5" aria-hidden="true" />}
          <span>
            {copie === 'ok' ? t('conf.copie') : copie === 'echec' ? t('conf.copieEchec') : t('conf.copier')}
          </span>
        </button>
      </section>

      <section className="rounded-xl border border-fds-line bg-fds-surface p-4 flex flex-col gap-2.5 text-sm">
        <div className="flex gap-2.5 items-start">
          <Mail className="w-5 h-5 shrink-0 text-fds-ok" aria-hidden="true" />
          <span>
            {t('conf.emailAvant')}<strong className="break-all">{email}</strong>{t('conf.emailApres')}
          </span>
        </div>
        <hr className="border-fds-line" />
        <div className="flex gap-3">
          <span className="flex-1 text-fds-mute">{t('conf.admission')}</span>
          <strong>{t('adm.mpc')}</strong>
        </div>
        <div className="flex gap-3">
          <span className="flex-1 text-fds-mute">{t('conf.frais')}</span>
          <strong>{t('recap.fraisValeur', { montant: montantHtg })}</strong>
        </div>
        {referencePaiement && (
          <div className="flex gap-3">
            <span className="flex-1 text-fds-mute">{t('conf.paiementSimule')}</span>
            <strong>{referencePaiement}</strong>
          </div>
        )}
        <div className="flex gap-3">
          <span className="flex-1 text-fds-mute">{t('conf.piecesEnvoyees')}</span>
          <strong>{t('conf.cinqSurCinq')}</strong>
        </div>
        <div className="flex gap-3">
          <span className="flex-1 text-fds-mute">{t('conf.envoyeLe')}</span>
          <strong className="text-right">{formaterHorodatage(soumiseLe)}</strong>
        </div>
      </section>

      <div className="flex gap-2.5 items-start rounded-[10px] border border-fds-accent-line bg-fds-navy-t px-3.5 py-3 text-sm text-fds-title">
        <Info className="w-5 h-5 shrink-0" aria-hidden="true" />
        <span>{t('conf.noteSimul')}</span>
      </div>

      <Link
        to={`/suivi/${reference}`}
        className="min-h-12 rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white font-semibold flex items-center justify-center"
      >
        {t('accueil.suivre')}
      </Link>
      <Link
        to="/"
        className="min-h-12 rounded-lg border-2 border-fds-accent bg-fds-surface text-fds-accent font-semibold flex items-center justify-center"
      >
        {t('conf.retourAccueil')}
      </Link>
      <button type="button" onClick={onNouvelleCandidature} className="min-h-11 text-sm text-fds-mute underline self-center">
        {t('conf.nouvelle')}
      </button>
    </div>
  );
};
