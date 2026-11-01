import React, { useEffect, useState } from 'react';
import { Link, Navigate, useNavigate, useParams, useSearchParams } from 'react-router-dom';
import { ArrowLeft, Check, Clock, Search, TriangleAlert, X } from 'lucide-react';
import {
  candidatureApi,
  FORMAT_REFERENCE,
  type PieceSuivi,
  type StatutGlobal,
  type SuiviDossier,
} from '../../../entities/candidature';
import { formaterJour } from '../../../features/candidature-form';
import { ApiError } from '../../../shared/api/client';

// Adresse déjà affichée dans le pied de page du site ; à confirmer avec la Faculté.
const EMAIL_FACULTE = 'admission@fds.ueh.edu.ht';

type Resultat = { reference: string; etat: 'ok'; suivi: SuiviDossier } | { reference: string; etat: 'introuvable' | 'limite' | 'erreur' };

const BADGES_GLOBAUX: Record<StatutGlobal, { libelle: string; classe: string }> = {
  en_examen: { libelle: 'En examen', classe: 'bg-fds-navy-t text-fds-navy' },
  action_requise: { libelle: 'Action requise', classe: 'bg-fds-warn-bg text-fds-warn' },
  complet: { libelle: 'Dossier complet', classe: 'bg-fds-ok-bg text-fds-ok' },
};

const BADGES_PIECES: Record<PieceSuivi['statut'], { libelle: string; classe: string }> = {
  manquant: { libelle: 'À fournir', classe: 'bg-fds-warn-bg text-fds-warn' },
  en_attente: { libelle: 'En examen', classe: 'bg-fds-navy-t text-fds-navy' },
  valide: { libelle: 'Validé', classe: 'bg-fds-ok-bg text-fds-ok' },
  rejete: { libelle: 'Refusé', classe: 'bg-fds-bad-bg text-fds-bad' },
};

function normaliser(saisie: string): string {
  return saisie.trim().toUpperCase();
}

/** Formulaire de recherche (maquette « Suivi »). */
const RechercheReference: React.FC<{ valeurInitiale?: string; message?: string }> = ({ valeurInitiale = '', message }) => {
  const navigate = useNavigate();
  const [saisie, setSaisie] = useState(valeurInitiale);
  const [erreurFormat, setErreurFormat] = useState(false);

  const rechercher = (e: React.FormEvent) => {
    e.preventDefault();
    const reference = normaliser(saisie);
    if (!FORMAT_REFERENCE.test(reference)) {
      setErreurFormat(true);
      return;
    }
    setErreurFormat(false);
    navigate(`/suivi/${reference}`);
  };

  return (
    <>
      <section className="flex flex-col gap-2">
        <h1 className="font-fds-serif text-2xl font-bold text-fds-navy-d">Suivre mon dossier</h1>
        <p className="text-fds-mute">Entrez la référence reçue à la fin de votre candidature et dans votre email.</p>
      </section>

      <form onSubmit={rechercher} noValidate className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-3.5">
        <div className="flex flex-col gap-1.5">
          <label htmlFor="reference" className="text-[15px] font-semibold">
            Référence du dossier
          </label>
          <input
            id="reference"
            value={saisie}
            onChange={(e) => setSaisie(e.target.value)}
            placeholder="CAN-2026-0089"
            autoCapitalize="characters"
            autoComplete="off"
            spellCheck={false}
            aria-invalid={erreurFormat}
            aria-describedby="reference-aide"
            className={`w-full min-h-12 rounded-lg border-[1.5px] bg-white px-3 text-lg tracking-wide text-fds-ink focus:outline-none focus:ring-2 focus:ring-fds-navy ${erreurFormat ? 'border-fds-bad' : 'border-fds-field'}`}
          />
          <p id="reference-aide" role={erreurFormat ? 'alert' : undefined} className={`text-[13px] ${erreurFormat ? 'font-semibold text-fds-bad' : 'text-fds-mute'}`}>
            {erreurFormat ? 'Cette référence n’a pas le bon format. Exemple : CAN-2026-0089.' : 'Format : CAN-2026-0000'}
          </p>
        </div>
        <button
          type="submit"
          className="min-h-12 px-4 rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white font-semibold flex items-center justify-center gap-2 transition-colors"
        >
          <Search className="w-5 h-5" aria-hidden="true" />
          Voir mon dossier
        </button>
      </form>

      {message && (
        <div role="alert" className="flex gap-2.5 items-start rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
          <TriangleAlert className="w-5 h-5 shrink-0" aria-hidden="true" />
          <span>{message}</span>
        </div>
      )}

      <section className="rounded-xl border border-[#b9cbe3] bg-fds-navy-t p-4 flex flex-col gap-2">
        <h2 className="font-semibold">Vous avez perdu votre référence ?</h2>
        <p className="text-sm">Écrivez-nous avec votre nom et votre email de candidature. Nous vous la renverrons.</p>
        <a
          href={`mailto:${EMAIL_FACULTE}?subject=${encodeURIComponent('Référence de dossier perdue')}`}
          className="min-h-12 rounded-lg border-2 border-fds-navy bg-white text-fds-navy font-semibold flex items-center justify-center"
        >
          Nous contacter
        </a>
      </section>
    </>
  );
};

const IconePiece: React.FC<{ statut: PieceSuivi['statut'] }> = ({ statut }) => {
  const style =
    statut === 'valide'
      ? 'bg-fds-ok text-white'
      : statut === 'rejete'
        ? 'bg-fds-bad text-white'
        : 'bg-fds-navy-t text-fds-navy border border-[#b9cbe3]';
  const Icone = statut === 'valide' ? Check : statut === 'rejete' ? X : Clock;
  return (
    <span className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 ${style}`} aria-hidden="true">
      <Icone className="w-4 h-4" strokeWidth={2.5} />
    </span>
  );
};

function detailPiece(piece: PieceSuivi): string | null {
  if (piece.statut === 'valide' && piece.valide_le) return `Validé le ${formaterJour(piece.valide_le)}`;
  if (piece.statut === 'en_attente' && piece.depose_le) return `Reçu le ${formaterJour(piece.depose_le)}`;
  return null;
}

/** Vue d'un dossier (maquette « Dossier »). */
const VueDossier: React.FC<{ suivi: SuiviDossier }> = ({ suivi }) => {
  const badge = BADGES_GLOBAUX[suivi.statut_global];
  const pourcentage = suivi.pieces_total ? Math.round((suivi.pieces_validees / suivi.pieces_total) * 100) : 0;
  const refusees = suivi.pieces.filter((p) => p.statut === 'rejete').length;
  const resume =
    suivi.statut_global === 'complet'
      ? 'Toutes vos pièces sont validées.'
      : `${suivi.pieces_validees} pièce${suivi.pieces_validees > 1 ? 's' : ''} validée${suivi.pieces_validees > 1 ? 's' : ''} sur ${suivi.pieces_total}.` +
        (refusees ? ` ${refusees > 1 ? `${refusees} pièces sont à remplacer.` : 'Une pièce est à remplacer.'}` : '');

  return (
    <>
      <Link to="/suivi" className="flex items-center gap-2 min-h-11 font-semibold text-fds-navy">
        <ArrowLeft className="w-5 h-5" aria-hidden="true" />
        Autre dossier
      </Link>

      <section className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-2.5" aria-label="Dossier">
        <div className="text-sm text-fds-mute">Dossier</div>
        <div className="font-fds-serif text-[28px] leading-tight font-bold text-fds-navy-d break-all" data-testid="reference-dossier">
          {suivi.reference_dossier}
        </div>
        <div className="flex gap-3 text-sm">
          <span className="flex-1 text-fds-mute">Candidat</span>
          <strong>
            {suivi.prenom} {suivi.initiale_nom}.
          </strong>
        </div>
        <div className="flex gap-3 text-sm">
          <span className="flex-1 text-fds-mute">Admission</span>
          <strong>{suivi.admission}</strong>
        </div>
        {suivi.soumise_le && (
          <div className="flex gap-3 text-sm">
            <span className="flex-1 text-fds-mute">Envoyé le</span>
            <strong>{formaterJour(suivi.soumise_le)}</strong>
          </div>
        )}
      </section>

      <section className="flex flex-col gap-2.5" aria-label="Avancement">
        <div className="flex items-center gap-2">
          <h2 className="font-fds-serif text-xl font-bold text-fds-navy-d flex-1">Avancement</h2>
          <span className={`rounded-full px-2.5 py-0.5 text-[13px] font-semibold whitespace-nowrap ${badge.classe}`}>{badge.libelle}</span>
        </div>
        <div
          className="h-2.5 rounded bg-fds-line overflow-hidden"
          role="progressbar"
          aria-valuenow={pourcentage}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label="Pièces validées"
        >
          <div className="h-full bg-fds-ok" style={{ width: `${pourcentage}%` }} />
        </div>
        <p className="text-sm text-fds-mute">{resume}</p>
      </section>

      {refusees > 0 && (
        <div role="alert" className="flex gap-2.5 items-start rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
          <TriangleAlert className="w-5 h-5 shrink-0" aria-hidden="true" />
          <span>
            <strong>{refusees > 1 ? `${refusees} pièces ont été refusées.` : 'Une pièce a été refusée.'}</strong> Le motif est indiqué
            ci-dessous. Pour la remplacer,{' '}
            <a
              className="underline font-semibold"
              href={`mailto:${EMAIL_FACULTE}?subject=${encodeURIComponent(`Dossier ${suivi.reference_dossier} : pièce à remplacer`)}`}
            >
              contactez la Faculté
            </a>
            .
          </span>
        </div>
      )}

      <ul className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-4" aria-label="Statut de chaque pièce">
        {suivi.pieces.map((piece) => {
          const badgePiece = BADGES_PIECES[piece.statut];
          const detail = detailPiece(piece);
          return (
            <li key={piece.id} className="flex gap-3 items-start">
              <IconePiece statut={piece.statut} />
              <div className="flex-1 flex flex-col gap-1.5">
                <div className="flex items-center gap-2">
                  <span className="font-semibold flex-1">{piece.nom}</span>
                  <span className={`rounded-full px-2.5 py-0.5 text-[13px] font-semibold whitespace-nowrap ${badgePiece.classe}`}>
                    {badgePiece.libelle}
                  </span>
                </div>
                {detail && <div className="text-xs text-fds-mute">{detail}</div>}
                {piece.statut === 'rejete' && piece.motif_rejet && (
                  <p className="rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3 py-2 text-sm text-fds-bad">
                    <strong>Motif :</strong> {piece.motif_rejet}
                  </p>
                )}
              </div>
            </li>
          );
        })}
      </ul>

      <p className="text-xs text-fds-mute">Cette page affiche toujours l’état le plus récent de votre dossier.</p>
    </>
  );
};

/**
 * Suivi de dossier par référence (maquettes « Suivi » et « Dossier »). `/suivi` propose la recherche,
 * `/suivi/CAN-2026-0089` affiche le dossier ; `/suivi?ref=CAN-2026-0089` redirige vers cette adresse.
 */
export const SuiviPage: React.FC = () => {
  const { reference: paramReference } = useParams();
  const [recherche] = useSearchParams();
  const refDansUrl = recherche.get('ref');

  const reference = paramReference ? normaliser(paramReference) : undefined;
  const [resultat, setResultat] = useState<Resultat | null>(null);

  useEffect(() => {
    if (!reference || !FORMAT_REFERENCE.test(reference)) return;
    let annule = false;
    candidatureApi
      .obtenirSuivi(reference)
      .then((suivi) => {
        if (!annule) setResultat({ reference, etat: 'ok', suivi });
      })
      .catch((erreur) => {
        if (annule) return;
        const etat = erreur instanceof ApiError ? (erreur.status === 404 ? 'introuvable' : erreur.status === 429 ? 'limite' : 'erreur') : 'erreur';
        setResultat({ reference, etat });
      });
    return () => {
      annule = true;
    };
  }, [reference]);

  // Lien `?ref=` (ancien format) : on bascule vers l'adresse canonique
  if (!reference && refDansUrl) return <Navigate to={`/suivi/${encodeURIComponent(normaliser(refDansUrl))}`} replace />;

  let contenu: React.ReactNode;
  if (!reference) {
    contenu = <RechercheReference />;
  } else if (!FORMAT_REFERENCE.test(reference)) {
    contenu = <RechercheReference valeurInitiale={reference} message="Cette référence n’a pas le bon format. Exemple : CAN-2026-0089." />;
  } else if (!resultat || resultat.reference !== reference) {
    contenu = (
      <p className="text-fds-mute" role="status">
        Recherche de votre dossier…
      </p>
    );
  } else if (resultat.etat === 'ok') {
    contenu = <VueDossier suivi={resultat.suivi} />;
  } else {
    const messages = {
      introuvable: 'Aucun dossier trouvé pour cette référence. Vérifiez les chiffres, ou contactez-nous.',
      limite: 'Trop de recherches en peu de temps. Patientez une minute puis réessayez.',
      erreur: 'Impossible de joindre le serveur. Vérifiez votre connexion puis réessayez.',
    } as const;
    contenu = <RechercheReference valeurInitiale={reference} message={messages[resultat.etat]} />;
  }

  return <div className="max-w-xl w-full mx-auto px-4 py-6 flex-1 flex flex-col gap-[18px]">{contenu}</div>;
};
