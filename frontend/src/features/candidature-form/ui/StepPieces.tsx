import React, { useCallback, useEffect, useState } from 'react';
import { CheckCircle2, FileText, TriangleAlert, Upload } from 'lucide-react';
import { candidatureApi, extraireErreursChamps, type PieceDossier } from '../../../entities/candidature';
import { ApiError } from '../../../shared/api/client';
import { attributAccept, formaterTaille, validerFichierLocal } from '../lib/fichiers';
import { BarreAction, CLASSE_BOUTON_PRIMAIRE } from './BarreAction';

interface StepPiecesProps {
  candidatureId: string;
  referencePaiement: string | null;
  onRetour: () => void;
  /** Passe au récapitulatif, une fois les 5 pièces reçues. */
  onContinuer: () => void;
}

/** État d'un envoi en cours ou en échec pour une pièce (les pièces reçues viennent du serveur). */
type Envoi = { progression: number } | { erreur: string };

function messageErreur(erreur: unknown): string {
  if (erreur instanceof ApiError) {
    if (erreur.status === 413) return 'Ce fichier dépasse la limite de 5 Mo. Choisissez un fichier plus léger ou reprenez une photo.';
    if (erreur.status === 429) return "Trop d'envois en peu de temps. Patientez une minute puis réessayez.";
    const champs = extraireErreursChamps(erreur);
    if (champs?.fichier) return champs.fichier;
    if (erreur.status === 409) return 'Ce document ne peut plus être remplacé.';
  }
  return 'Envoi interrompu. Vérifiez votre connexion puis réessayez.';
}

const BADGES: Record<PieceDossier['statut'], { libelle: string; classe: string }> = {
  manquant: { libelle: 'À fournir', classe: 'bg-fds-warn-bg text-fds-warn' },
  en_attente: { libelle: 'Reçu', classe: 'bg-fds-ok-bg text-fds-ok' },
  valide: { libelle: 'Validé', classe: 'bg-fds-ok-bg text-fds-ok' },
  rejete: { libelle: 'Refusé', classe: 'bg-fds-bad-bg text-fds-bad' },
};

/** Étape 4 : dépôt des pièces justificatives (maquette « Candidature 4/4 - Pièces »). */
export const StepPieces: React.FC<StepPiecesProps> = ({ candidatureId, referencePaiement, onRetour, onContinuer }) => {
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
      definirEnvoi(piece.id, { erreur: messageErreur(erreur) });
    }
  };

  const recues = pieces?.filter((p) => p.statut !== 'manquant').length ?? 0;
  const total = pieces?.length ?? 5;
  const complet = pieces !== null && recues === total;

  return (
    <div className="flex flex-col gap-4 flex-1">
      {referencePaiement && (
        <div className="flex gap-2.5 items-start rounded-[10px] border border-[#9bd3b2] bg-fds-ok-bg px-3.5 py-3 text-sm text-fds-ok">
          <CheckCircle2 className="w-5 h-5 shrink-0" aria-hidden="true" />
          <span>
            Paiement simulé enregistré : <strong>{referencePaiement}</strong> (aucun argent réel prélevé).
          </span>
        </div>
      )}

      <h1 className="font-fds-serif text-2xl font-bold text-fds-navy-d">Déposez vos pièces</h1>
      <p className="text-sm text-fds-mute">
        PDF ou JPG, 5 Mo maximum par fichier. Vous pouvez photographier un document avec votre téléphone.
      </p>

      {erreurChargement && (
        <div role="alert" className="rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad flex flex-col gap-2">
          <span>Impossible de charger la liste des pièces. Vérifiez votre connexion.</span>
          <button type="button" onClick={recharger} className="self-start font-semibold underline min-h-11">
            Réessayer
          </button>
        </div>
      )}

      {!pieces && !erreurChargement && (
        <p className="text-fds-mute" role="status">
          Chargement des pièces…
        </p>
      )}

      {pieces?.map((piece) => {
        const envoi = envois[piece.id];
        const enCours = envoi && 'progression' in envoi;
        const erreur = envoi && 'erreur' in envoi ? envoi.erreur : undefined;
        const badge = enCours
          ? { libelle: 'En cours', classe: 'bg-fds-navy-t text-fds-navy' }
          : erreur
            ? { libelle: 'Erreur', classe: 'bg-fds-bad-bg text-fds-bad' }
            : BADGES[piece.statut];
        const aUnFichier = piece.statut !== 'manquant';

        return (
          <section
            key={piece.id}
            className={`rounded-xl border bg-white p-4 flex flex-col gap-2.5 ${erreur ? 'border-[#efb1ab]' : 'border-fds-line'}`}
            aria-label={piece.nom}
          >
            <div className="flex items-center gap-2">
              <h2 className="font-semibold flex-1">{piece.nom}</h2>
              <span className={`rounded-full px-2.5 py-0.5 text-[13px] font-semibold whitespace-nowrap ${badge.classe}`}>
                {badge.libelle}
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
              <p className="rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3 py-2.5 text-sm text-fds-bad">
                <strong>Motif :</strong> {piece.motif_rejet}
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
                  aria-label={`Envoi de ${piece.nom}`}
                >
                  <div
                    className="h-full bg-fds-navy"
                    style={{ width: `${(envoi as { progression: number }).progression}%` }}
                  />
                </div>
                <span className="text-xs text-fds-mute">
                  Envoi en cours, {(envoi as { progression: number }).progression} %
                </span>
              </>
            )}

            {erreur && (
              <p role="alert" className="flex gap-2 items-start rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3 py-2.5 text-sm text-fds-bad">
                <TriangleAlert className="w-5 h-5 shrink-0" aria-hidden="true" />
                <span>{erreur}</span>
              </p>
            )}

            {!enCours && piece.statut !== 'valide' && (
              <label className="min-h-12 rounded-lg border-2 border-fds-navy bg-white text-fds-navy font-semibold flex items-center justify-center gap-2 cursor-pointer focus-within:ring-2 focus-within:ring-fds-navy focus-within:ring-offset-2">
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
                  {erreur ? 'Choisir un autre fichier' : aUnFichier ? 'Remplacer le fichier' : 'Choisir un fichier'}
                </span>
              </label>
            )}
          </section>
        );
      })}

      <BarreAction>
        <p className="text-xs text-fds-mute text-center" aria-live="polite">
          {complet
            ? 'Toutes vos pièces sont reçues. Vous pouvez vérifier votre dossier.'
            : `${recues} pièce${recues > 1 ? 's' : ''} reçue${recues > 1 ? 's' : ''} sur ${total} obligatoires`}
        </p>
        <button type="button" disabled={!complet} onClick={onContinuer} className={CLASSE_BOUTON_PRIMAIRE}>
          Vérifier mon dossier
        </button>
        <button type="button" onClick={onRetour} className="min-h-11 text-fds-navy font-semibold underline">
          Retour
        </button>
      </BarreAction>
    </div>
  );
};
