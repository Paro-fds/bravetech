import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Check, Copy, Info, Mail, TriangleAlert } from 'lucide-react';
import { formaterHorodatage } from '../lib/dates';

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

  const copierReference = async () => {
    setCopie((await copier(reference)) ? 'ok' : 'echec');
    window.setTimeout(() => setCopie('idle'), 3000);
  };

  return (
    <div className="flex flex-col gap-[18px] flex-1 pb-8" aria-live="polite">
      <div className="flex flex-col items-center text-center gap-2.5">
        <span className="w-16 h-16 rounded-full bg-fds-ok text-white flex items-center justify-center">
          <Check className="w-9 h-9" strokeWidth={2.5} aria-hidden="true" />
        </span>
        <h1 className="font-fds-serif text-2xl font-bold text-fds-navy-d">Votre dossier a bien été envoyé</h1>
        <p className="text-fds-mute">Merci, {prenom}. La Faculté va maintenant examiner vos pièces.</p>
      </div>

      <section className="rounded-xl border-2 border-fds-navy bg-white p-4 flex flex-col gap-2 text-center" aria-label="Référence du dossier">
        <div className="text-sm text-fds-mute">Votre référence de dossier</div>
        <div className="font-fds-serif text-[34px] leading-tight font-bold text-fds-navy-d tracking-wide break-all" data-testid="reference-dossier">
          {reference}
        </div>
        <div className="flex gap-2.5 items-start text-left rounded-[10px] border border-[#e6c36b] bg-fds-warn-bg px-3.5 py-3 text-sm text-fds-warn">
          <TriangleAlert className="w-5 h-5 shrink-0" aria-hidden="true" />
          <span>
            <strong>Notez-la ou faites une capture d'écran.</strong> Elle vous permet de suivre votre dossier.
          </span>
        </div>
        <button
          type="button"
          onClick={() => void copierReference()}
          className="min-h-12 rounded-lg border-2 border-fds-navy bg-white text-fds-navy font-semibold flex items-center justify-center gap-2"
        >
          {copie === 'ok' ? <Check className="w-5 h-5" aria-hidden="true" /> : <Copy className="w-5 h-5" aria-hidden="true" />}
          <span>
            {copie === 'ok' ? 'Référence copiée' : copie === 'echec' ? 'Copie impossible : notez-la' : 'Copier la référence'}
          </span>
        </button>
      </section>

      <section className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-2.5 text-sm">
        <div className="flex gap-2.5 items-start">
          <Mail className="w-5 h-5 shrink-0 text-fds-ok" aria-hidden="true" />
          <span>
            Un email de confirmation, avec un lien de suivi, est envoyé à <strong className="break-all">{email}</strong>. Si vous ne
            le recevez pas, votre référence suffit pour suivre votre dossier.
          </span>
        </div>
        <hr className="border-fds-line" />
        <div className="flex gap-3">
          <span className="flex-1 text-fds-mute">Admission</span>
          <strong>Premier cycle MPC</strong>
        </div>
        <div className="flex gap-3">
          <span className="flex-1 text-fds-mute">Frais</span>
          <strong>{montantHtg} HTG (simulation)</strong>
        </div>
        {referencePaiement && (
          <div className="flex gap-3">
            <span className="flex-1 text-fds-mute">Paiement simulé</span>
            <strong>{referencePaiement}</strong>
          </div>
        )}
        <div className="flex gap-3">
          <span className="flex-1 text-fds-mute">Pièces envoyées</span>
          <strong>5 sur 5</strong>
        </div>
        <div className="flex gap-3">
          <span className="flex-1 text-fds-mute">Envoyé le</span>
          <strong className="text-right">{formaterHorodatage(soumiseLe)}</strong>
        </div>
      </section>

      <div className="flex gap-2.5 items-start rounded-[10px] border border-[#b9cbe3] bg-fds-navy-t px-3.5 py-3 text-sm text-fds-navy-d">
        <Info className="w-5 h-5 shrink-0" aria-hidden="true" />
        <span>Le paiement était une simulation : aucun argent n'a été prélevé.</span>
      </div>

      <Link
        to={`/suivi/${reference}`}
        className="min-h-12 rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white font-semibold flex items-center justify-center"
      >
        Suivre mon dossier
      </Link>
      <Link
        to="/"
        className="min-h-12 rounded-lg border-2 border-fds-navy bg-white text-fds-navy font-semibold flex items-center justify-center"
      >
        Retour à l'accueil
      </Link>
      <button type="button" onClick={onNouvelleCandidature} className="min-h-11 text-sm text-fds-mute underline self-center">
        Commencer une nouvelle candidature
      </button>
    </div>
  );
};
