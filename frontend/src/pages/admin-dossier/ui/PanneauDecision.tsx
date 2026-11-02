import React, { useState } from 'react';
import { Check } from 'lucide-react';
import { MOTIF_MAX, MOTIF_MIN } from '../../../entities/dossier-admin';
import { ApiError } from '../../../shared/api/client';

interface PanneauDecisionProps {
  nomPiece: string;
  /** Envoie la décision ; rejette avec une `ApiError` si le serveur la refuse. */
  onDecider: (statut: 'valide' | 'rejete', motif?: string) => Promise<void>;
}

type Mode = 'repos' | 'confirmer-validation' | 'refus';

function messageErreur(erreur: unknown): string {
  if (erreur instanceof ApiError) {
    if (erreur.status === 409) return "Cette pièce a déjà reçu une décision (peut-être d'un autre agent). La page a été actualisée.";
    if (erreur.status === 422) {
      const motif = (erreur.body as { detail?: { erreurs?: { motif?: string } } } | null)?.detail?.erreurs?.motif;
      if (motif) return motif;
    }
  }
  return "La décision n'a pas pu être enregistrée. Vérifiez votre connexion puis réessayez.";
}

/** Boutons de décision d'une pièce « à examiner » (maquette « Administration validation d'un dossier »). */
export const PanneauDecision: React.FC<PanneauDecisionProps> = ({ nomPiece, onDecider }) => {
  const [mode, setMode] = useState<Mode>('repos');
  const [motif, setMotif] = useState('');
  const [enCours, setEnCours] = useState(false);
  const [erreur, setErreur] = useState<string | null>(null);

  const envoyer = async (statut: 'valide' | 'rejete') => {
    if (statut === 'rejete' && motif.trim().length < MOTIF_MIN) {
      setErreur(`Indiquez le motif du refus (${MOTIF_MIN} caractères minimum) : le candidat le verra.`);
      return;
    }
    setEnCours(true);
    setErreur(null);
    try {
      await onDecider(statut, statut === 'rejete' ? motif.trim() : undefined);
      setMode('repos');
      setMotif('');
    } catch (e) {
      setErreur(messageErreur(e));
    } finally {
      setEnCours(false);
    }
  };

  return (
    <div className="flex flex-col gap-4">
      {mode === 'refus' && (
        <div className="rounded-xl border-2 border-fds-bad bg-fds-surface p-4 flex flex-col gap-3.5">
          <h3 className="font-semibold text-lg">Refuser cette pièce</h3>
          <div className="flex flex-col gap-1.5">
            <label htmlFor="motif-refus" className="text-[15px] font-semibold">
              Motif du refus (visible par le candidat)
            </label>
            <textarea
              id="motif-refus"
              rows={3}
              maxLength={MOTIF_MAX}
              value={motif}
              onChange={(e) => setMotif(e.target.value)}
              className="w-full rounded-lg border-[1.5px] border-fds-field bg-fds-surface px-3 py-2.5 text-base text-fds-ink focus:outline-none focus:ring-2 focus:ring-fds-accent"
            />
            <p className="text-[13px] text-fds-mute">
              Soyez précis : le candidat verra ce message et pourra remplacer la pièce. Une décision enregistrée ne peut plus être modifiée.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <button
              type="button"
              disabled={enCours}
              onClick={() => void envoyer('rejete')}
              className="min-h-12 px-4 rounded-lg bg-fds-bad-solid text-white font-semibold disabled:opacity-60"
            >
              {enCours ? 'Enregistrement…' : 'Confirmer le refus'}
            </button>
            <button
              type="button"
              disabled={enCours}
              onClick={() => {
                setMode('repos');
                setErreur(null);
              }}
              className="min-h-12 px-4 rounded-lg border-2 border-fds-accent bg-fds-surface text-fds-accent font-semibold"
            >
              Annuler
            </button>
          </div>
        </div>
      )}

      {mode === 'confirmer-validation' && (
        <div className="rounded-xl border-2 border-fds-ok bg-fds-surface p-4 flex flex-col gap-3">
          <p className="font-semibold">Valider « {nomPiece} » ?</p>
          <p className="text-sm text-fds-mute">Cette décision est définitive : elle sera enregistrée avec votre nom et l'heure.</p>
          <div className="flex flex-wrap gap-3">
            <button
              type="button"
              disabled={enCours}
              onClick={() => void envoyer('valide')}
              className="min-h-12 px-4 rounded-lg bg-fds-ok-solid text-white font-semibold disabled:opacity-60"
            >
              {enCours ? 'Enregistrement…' : 'Confirmer la validation'}
            </button>
            <button
              type="button"
              disabled={enCours}
              onClick={() => setMode('repos')}
              className="min-h-12 px-4 rounded-lg border-2 border-fds-accent bg-fds-surface text-fds-accent font-semibold"
            >
              Annuler
            </button>
          </div>
        </div>
      )}

      {erreur && (
        <p role="alert" className="rounded-[10px] border border-fds-bad-line bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
          {erreur}
        </p>
      )}

      {mode === 'repos' && (
        <div className="flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={() => setMode('confirmer-validation')}
            className="min-h-12 px-4 rounded-lg bg-fds-ok-solid text-white font-semibold flex items-center gap-2"
          >
            <Check className="w-5 h-5" aria-hidden="true" />
            Valider cette pièce
          </button>
          <button
            type="button"
            onClick={() => setMode('refus')}
            className="min-h-12 px-4 rounded-lg border-2 border-fds-bad bg-fds-surface text-fds-bad font-semibold"
          >
            Refuser cette pièce…
          </button>
          <span className="flex-1 basis-60 text-xs text-fds-mute">
            Un email part au candidat après chaque décision. S'il échoue, la décision reste enregistrée.
          </span>
        </div>
      )}
    </div>
  );
};
