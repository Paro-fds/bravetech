import React, { useCallback, useEffect, useState } from 'react';
import { CheckCircle2, FileText, TriangleAlert, Upload } from 'lucide-react';
import { candidatureApi, extraireErreursChamps, type PieceDossier } from '../../../entities/candidature';
import { ApiError } from '../../../shared/api';
import { attributAccept, formaterTaille, validerFichierLocal } from '../lib/fichiers';
import { BarreAction, CLASSE_BOUTON_PRIMAIRE } from './BarreAction';
import { useNomPiece, useT } from '../../../shared/i18n';
import type { Cle } from '../../../shared/i18n';

interface StepPiecesProps {
  candidatureId: string;
  referencePaiement: string | null;
  onRetour: () => void;
  /** Passe au récapitulatif, une fois les 5 pièces reçues. */
  onContinuer: () => void;
}

/** État d'un envoi en cours ou en échec pour une pièce (les pièces reçues viennent du serveur). */
type Envoi = { progression: number } | { erreur: string };

function messageErreur(erreur: unknown, t: ReturnType<typeof useT>): string {
  if (erreur instanceof ApiError) {
    if (erreur.status === 413) return t('pieces.e413');
    if (erreur.status === 429) return t('pieces.e429');
    const champs = extraireErreursChamps(erreur);
    if (champs?.fichier) return champs.fichier;
    if (erreur.status === 409) return t('pieces.e409');
  }
  return t('pieces.eReseau');
}

const BADGES: Record<PieceDossier['statut'], { cle: Cle; classe: string }> = {
  manquant: { cle: 'pieces.aFournir', classe: 'bg-fds-warn-bg text-fds-warn' },
  en_attente: { cle: 'pieces.recu', classe: 'bg-fds-ok-bg text-fds-ok' },
  valide: { cle: 'pieces.valide', classe: 'bg-fds-ok-bg text-fds-ok' },
  rejete: { cle: 'pieces.refuse', classe: 'bg-fds-bad-bg text-fds-bad' },
};

/** Étape 4 : dépôt des pièces justificatives (maquette « Candidature 4/4 - Pièces »). */
export const StepPieces: React.FC<StepPiecesProps> = ({ candidatureId, referencePaiement, onRetour, onContinuer }) => {
  const t = useT();
  const nomPiece = useNomPiece();
  const [pieces, setPieces] = useState<PieceDossier[] | null>(null);
  const [erreurChargement, setErreurChargement] = useState(false);
  const [envois, setEnvois] = useState<Record<string, Envoi>>({});

  useEffect(() => {
    let annule = false;
    candidatureApi
      .listerPieces(candidatureId)
      .then((liste) => {
        if (!annule) setPieces(liste);
      })
      .catch(() => {
        if (!annule) setErreurChargement(true);
      });
    return () => {
      annule = true;
    };
  }, [candidatureId]);

  const recharger = useCallback(() => {
    setErreurChargement(false);
    candidatureApi
      .listerPieces(candidatureId)
      .then(setPieces)
      .catch(() => setErreurChargement(true));
  }, [candidatureId]);

  const definirEnvoi = (id: string, envoi: Envoi | undefined) =>
    setEnvois((prec) => {
      const suivant = { ...prec };
      if (envoi) suivant[id] = envoi;
      else delete suivant[id];
      return suivant;
    });

  const envoyer = async (piece: PieceDossier, fichier: File) => {
    const erreurLocale = validerFichierLocal(fichier, piece);
    if (erreurLocale) {
      definirEnvoi(piece.id, { erreur: erreurLocale });
      return;
    }
    definirEnvoi(piece.id, { progression: 0 });
    try {
      const misAJour = await candidatureApi.televerserPiece(candidatureId, piece.id, fichier, (progression) =>
        definirEnvoi(piece.id, { progression }),
      );
      setPieces((prec) => prec?.map((p) => (p.id === misAJour.id ? misAJour : p)) ?? prec);
      definirEnvoi(piece.id, undefined);
    } catch (erreur) {
      definirEnvoi(piece.id, { erreur: messageErreur(erreur, t) });
    }
  };

  const recues = pieces?.filter((p) => p.statut !== 'manquant').length ?? 0;
  const total = pieces?.length ?? 5;
  const complet = pieces !== null && recues === total;

  return (
    <div className="flex flex-col gap-4 flex-1">
      {referencePaiement && (
        <div className="flex gap-2.5 items-start rounded-[10px] border border-fds-ok-line bg-fds-ok-bg px-3.5 py-3 text-sm text-fds-ok">
          <CheckCircle2 className="w-5 h-5 shrink-0" aria-hidden="true" />
          <span>
            {t('pieces.payeAvant')} <strong>{referencePaiement}</strong> {t('pieces.payeApres')}
          </span>
        </div>
      )}

      <h1 className="font-fds-serif text-2xl font-bold text-fds-title">{t('pieces.titre')}</h1>
      <p className="text-sm text-fds-mute">
        {t('pieces.consigne')}
      </p>

      {erreurChargement && (
        <div role="alert" className="rounded-[10px] border border-fds-bad-line bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad flex flex-col gap-2">
          <span>{t('pieces.errChargement')}</span>
          <button type="button" onClick={recharger} className="self-start font-semibold underline min-h-11">
            {t('commun.reessayer')}
          </button>
        </div>
      )}

      {!pieces && !erreurChargement && (
        <p className="text-fds-mute" role="status">
          {t('pieces.chargement')}
        </p>
      )}

      {pieces?.map((piece) => {
        const envoi = envois[piece.id];
        const enCours = envoi && 'progression' in envoi;
        const erreur = envoi && 'erreur' in envoi ? envoi.erreur : undefined;
        const badge = enCours
          ? { cle: 'pieces.encours' as Cle, classe: 'bg-fds-navy-t text-fds-accent' }
          : erreur
            ? { cle: 'pieces.erreur' as Cle, classe: 'bg-fds-bad-bg text-fds-bad' }
            : BADGES[piece.statut];
        const aUnFichier = piece.statut !== 'manquant';

        return (
          <section
            key={piece.id}
            className={`rounded-xl border bg-fds-surface p-4 flex flex-col gap-2.5 ${erreur ? 'border-fds-bad-line' : 'border-fds-line'}`}
            aria-label={nomPiece(piece.id, piece.nom)}
          >
            <div className="flex items-center gap-2">
              <h2 className="font-semibold flex-1">{nomPiece(piece.id, piece.nom)}</h2>
              <span className={`rounded-full px-2.5 py-0.5 text-[13px] font-semibold whitespace-nowrap ${badge.classe}`}>
                {t(badge.cle)}
              </span>
            </div>

            {aUnFichier && !enCours && (
              <div className="flex items-center gap-2 text-sm text-fds-mute">
                <FileText className="w-5 h-5 shrink-0" aria-hidden="true" />
                <span className="flex-1 truncate">{piece.nom_fichier}</span>
                {piece.taille_octets !== null && <span>{formaterTaille(piece.taille_octets)}</span>}
              </div>
            )}

            {piece.statut === 'rejete' && piece.motif_rejet && (
              <p className="rounded-[10px] border border-fds-bad-line bg-fds-bad-bg px-3 py-2.5 text-sm text-fds-bad">
                <strong>{t('pieces.motif')}</strong> {piece.motif_rejet}
              </p>
            )}

            {enCours && (
              <>
                <div
                  className="h-2 rounded bg-fds-line overflow-hidden"
                  role="progressbar"
                  aria-valuenow={(envoi as { progression: number }).progression}
                  aria-valuemin={0}
                  aria-valuemax={100}
                  aria-label={t('pieces.envoiAria', { nom: nomPiece(piece.id, piece.nom) })}
                >
                  <div
                    className="h-full bg-fds-accent"
                    style={{ width: `${(envoi as { progression: number }).progression}%` }}
                  />
                </div>
                <span className="text-xs text-fds-mute">
                  {t('pieces.envoiCours', { n: (envoi as { progression: number }).progression })}
                </span>
              </>
            )}

            {erreur && (
              <p role="alert" className="flex gap-2 items-start rounded-[10px] border border-fds-bad-line bg-fds-bad-bg px-3 py-2.5 text-sm text-fds-bad">
                <TriangleAlert className="w-5 h-5 shrink-0" aria-hidden="true" />
                <span>{erreur}</span>
              </p>
            )}

            {!enCours && piece.statut !== 'valide' && (
              <label className="min-h-12 rounded-lg border-2 border-fds-accent bg-fds-surface text-fds-accent font-semibold flex items-center justify-center gap-2 cursor-pointer focus-within:ring-2 focus-within:ring-fds-accent focus-within:ring-offset-2 focus-within:ring-offset-fds-surface">
                <input
                  type="file"
                  className="sr-only"
                  accept={attributAccept(piece.format_accepte)}
                  onChange={(e) => {
                    const fichier = e.target.files?.[0];
                    e.target.value = ''; // permet de rechoisir le même fichier après une erreur
                    if (fichier) void envoyer(piece, fichier);
                  }}
                />
                <Upload className="w-5 h-5" aria-hidden="true" />
                <span>
                  {erreur ? t('pieces.autre') : aUnFichier ? t('pieces.remplacer') : t('pieces.choisir')}
                </span>
              </label>
            )}
          </section>
        );
      })}

      <BarreAction>
        <p className="text-xs text-fds-mute text-center" aria-live="polite">
          {complet ? t('pieces.complet') : t(recues > 1 ? 'pieces.compteurPlus' : 'pieces.compteurUn', { n: recues, total })}
        </p>
        <button type="button" disabled={!complet} onClick={onContinuer} className={CLASSE_BOUTON_PRIMAIRE}>
          {t('pieces.verifier')}
        </button>
        <button type="button" onClick={onRetour} className="min-h-11 text-fds-accent font-semibold underline">
          {t('commun.retour')}
        </button>
      </BarreAction>
    </div>
  );
};
