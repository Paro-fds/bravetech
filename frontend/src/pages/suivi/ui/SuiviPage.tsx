import React, { useEffect, useState } from 'react';
import { Link, Navigate, useNavigate, useParams, useSearchParams } from 'react-router-dom';
import { ArrowLeft, Check, Clock, Search, TriangleAlert, X } from 'lucide-react';
import {
  candidatureApi,
  FORMAT_REFERENCE,
  normaliserReference as normaliser,
  type PieceSuivi,
  type StatutGlobal,
  type SuiviDossier,
} from '../../../entities/candidature';
import { formaterJour } from '../../../features/candidature-form';
import { ApiError } from '../../../shared/api';
import { traduireMaintenant as tr, useT } from '../../../shared/i18n';
import type { Cle } from '../../../shared/i18n';

// Adresse déjà affichée dans le pied de page du site ; à confirmer avec la Faculté.
const EMAIL_FACULTE = 'admission@fds.ueh.edu.ht';

type Resultat = { reference: string; etat: 'ok'; suivi: SuiviDossier } | { reference: string; etat: 'introuvable' | 'limite' | 'erreur' };

const BADGES_GLOBAUX: Record<StatutGlobal, { cle: Cle; classe: string }> = {
  en_examen: { cle: 'suivi.enExamen', classe: 'bg-fds-navy-t text-fds-accent' },
  action_requise: { cle: 'suivi.actionRequise', classe: 'bg-fds-warn-bg text-fds-warn' },
  complet: { cle: 'suivi.complet', classe: 'bg-fds-ok-bg text-fds-ok' },
};

const BADGES_PIECES: Record<PieceSuivi['statut'], { cle: Cle; classe: string }> = {
  manquant: { cle: 'suivi.pieceAFournir', classe: 'bg-fds-warn-bg text-fds-warn' },
  en_attente: { cle: 'suivi.enExamen', classe: 'bg-fds-navy-t text-fds-accent' },
  valide: { cle: 'suivi.pieceValide', classe: 'bg-fds-ok-bg text-fds-ok' },
  rejete: { cle: 'suivi.pieceRefuse', classe: 'bg-fds-bad-bg text-fds-bad' },
};

/** Formulaire de recherche (maquette « Suivi »). */
const RechercheReference: React.FC<{ valeurInitiale?: string; message?: string }> = ({ valeurInitiale = '', message }) => {
  const t = useT();
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
      <section className="flex flex-col gap-2 lg:gap-2.5">
        <h1 className="font-fds-serif text-2xl lg:text-[40px] font-bold text-fds-title">{t('accueil.suivre')}</h1>
        <p className="text-fds-mute lg:text-lg">{t('suivi.intro')}</p>
      </section>

      {/* Sur ordinateur : la recherche à gauche, l'aide « référence perdue » à droite */}
      <div className="flex flex-col gap-[18px] lg:grid lg:grid-cols-[3fr_2fr] lg:gap-8 lg:items-start">
        <div className="flex flex-col gap-[18px] min-w-0">
          <form onSubmit={rechercher} noValidate className="rounded-xl border border-fds-line bg-fds-surface p-4 lg:p-6 flex flex-col gap-3.5">
            <div className="flex flex-col gap-1.5">
              <label htmlFor="reference" className="text-[15px] font-semibold">
                {t('suivi.refLabel')}
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
                className={`w-full min-h-12 rounded-lg border-[1.5px] bg-fds-surface px-3 text-lg tracking-wide text-fds-ink focus:outline-none focus:ring-2 focus:ring-fds-accent ${erreurFormat ? 'border-fds-bad' : 'border-fds-field'}`}
              />
              <p id="reference-aide" role={erreurFormat ? 'alert' : undefined} className={`text-[13px] ${erreurFormat ? 'font-semibold text-fds-bad' : 'text-fds-mute'}`}>
                {erreurFormat ? t('suivi.formatErreur') : t('suivi.formatAide')}
              </p>
            </div>
            <button
              type="submit"
              className="min-h-12 px-4 lg:px-8 lg:self-start rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white font-semibold flex items-center justify-center gap-2 transition-colors"
            >
              <Search className="w-5 h-5" aria-hidden="true" />
              {t('suivi.voir')}
            </button>
          </form>

          {message && (
            <div role="alert" className="flex gap-2.5 items-start rounded-[10px] border border-fds-bad-line bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
              <TriangleAlert className="w-5 h-5 shrink-0" aria-hidden="true" />
              <span>{message}</span>
            </div>
          )}
        </div>

        <section className="rounded-xl border border-fds-accent-line bg-fds-navy-t p-4 lg:p-6 flex flex-col gap-2">
          <h2 className="font-semibold">{t('suivi.perdueTitre')}</h2>
          <p className="text-sm">{t('suivi.perdueTexte')}</p>
          <a
            href={`mailto:${EMAIL_FACULTE}?subject=${encodeURIComponent(t('suivi.mailSujet'))}`}
            className="min-h-12 rounded-lg border-2 border-fds-accent bg-fds-surface text-fds-accent font-semibold flex items-center justify-center"
          >
            {t('suivi.contacter')}
          </a>
        </section>
      </div>
    </>
  );
};

const IconePiece: React.FC<{ statut: PieceSuivi['statut'] }> = ({ statut }) => {
  const style =
    statut === 'valide'
      ? 'bg-fds-ok-solid text-white'
      : statut === 'rejete'
        ? 'bg-fds-bad-solid text-white'
        : 'bg-fds-navy-t text-fds-accent border border-fds-accent-line';
  const Icone = statut === 'valide' ? Check : statut === 'rejete' ? X : Clock;
  return (
    <span className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 ${style}`} aria-hidden="true">
      <Icone className="w-4 h-4" strokeWidth={2.5} />
    </span>
  );
};

function detailPiece(piece: PieceSuivi): string | null {
  if (piece.statut === 'valide' && piece.valide_le) return tr('suivi.valideLe', { date: formaterJour(piece.valide_le) });
  if (piece.statut === 'en_attente' && piece.depose_le) return tr('suivi.recuLe', { date: formaterJour(piece.depose_le) });
  return null;
}

/** Vue d'un dossier (maquette « Dossier »). */
const VueDossier: React.FC<{ suivi: SuiviDossier }> = ({ suivi }) => {
  const t = useT();
  const badge = BADGES_GLOBAUX[suivi.statut_global];
  const pourcentage = suivi.pieces_total ? Math.round((suivi.pieces_validees / suivi.pieces_total) * 100) : 0;
  const refusees = suivi.pieces.filter((p) => p.statut === 'rejete').length;
  const resume =
    suivi.statut_global === 'complet'
      ? t('suivi.resumeComplet')
      : t(suivi.pieces_validees > 1 ? 'suivi.resumePlus' : 'suivi.resumeUn', { n: suivi.pieces_validees, total: suivi.pieces_total }) +
        (refusees ? (refusees > 1 ? t('suivi.aRemplacerPlus', { n: refusees }) : t('suivi.aRemplacerUne')) : '');

  return (
    <>
      <Link to="/suivi" className="flex items-center gap-2 min-h-11 font-semibold text-fds-accent">
        <ArrowLeft className="w-5 h-5" aria-hidden="true" />
        {t('suivi.autre')}
      </Link>

      {/* Sur ordinateur : identité et avancement à gauche, toujours visibles ; les pièces à droite */}
      <div className="flex flex-col gap-[18px] lg:grid lg:grid-cols-[2fr_3fr] lg:gap-8 lg:items-start">
        <div className="flex flex-col gap-[18px] min-w-0 lg:sticky lg:top-4">
          <section className="rounded-xl border border-fds-line bg-fds-surface p-4 lg:p-6 flex flex-col gap-2.5" aria-label={t('suivi.dossier')}>
            <div className="text-sm text-fds-mute">{t('suivi.dossier')}</div>
            <div className="font-fds-serif text-[28px] leading-tight font-bold text-fds-title break-all" data-testid="reference-dossier">
              {suivi.reference_dossier}
            </div>
            <div className="flex gap-3 text-sm">
              <span className="flex-1 text-fds-mute">{t('suivi.candidat')}</span>
              <strong>
                {suivi.prenom} {suivi.initiale_nom}.
              </strong>
            </div>
            <div className="flex gap-3 text-sm">
              <span className="flex-1 text-fds-mute">{t('suivi.admission')}</span>
              <strong>{t('adm.mpc')}</strong>
            </div>
            {suivi.soumise_le && (
              <div className="flex gap-3 text-sm">
                <span className="flex-1 text-fds-mute">{t('suivi.envoyeLe')}</span>
                <strong>{formaterJour(suivi.soumise_le)}</strong>
              </div>
            )}
          </section>

          <section className="flex flex-col gap-2.5" aria-label={t('suivi.avancement')}>
            <div className="flex items-center gap-2">
              <h2 className="font-fds-serif text-xl font-bold text-fds-title flex-1">{t('suivi.avancement')}</h2>
              <span className={`rounded-full px-2.5 py-0.5 text-[13px] font-semibold whitespace-nowrap ${badge.classe}`}>{t(badge.cle)}</span>
            </div>
            <div
              className="h-2.5 rounded bg-fds-line overflow-hidden"
              role="progressbar"
              aria-valuenow={pourcentage}
              aria-valuemin={0}
              aria-valuemax={100}
              aria-label={t('suivi.progAria')}
            >
              <div className="h-full bg-fds-ok" style={{ width: `${pourcentage}%` }} />
            </div>
            <p className="text-sm text-fds-mute">{resume}</p>
          </section>
        </div>

        <div className="flex flex-col gap-[18px] min-w-0">
          {refusees > 0 && (
            <div role="alert" className="flex gap-2.5 items-start rounded-[10px] border border-fds-bad-line bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
              <TriangleAlert className="w-5 h-5 shrink-0" aria-hidden="true" />
              <span>
                <strong>{refusees > 1 ? t('suivi.refuseePlus', { n: refusees }) : t('suivi.refuseeUne')}</strong>
                {refusees > 1 ? t('suivi.remplacezPlus') : t('suivi.remplacezUne')}
              </span>
            </div>
          )}

          <ul className="rounded-xl border border-fds-line bg-fds-surface p-4 lg:p-6 flex flex-col gap-4 lg:gap-5" aria-label={t('suivi.statutPieces')}>
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
                        {t(badgePiece.cle)}
                      </span>
                    </div>
                    {detail && <div className="text-xs text-fds-mute">{detail}</div>}
                    {piece.statut === 'rejete' && piece.motif_rejet && (
                      <p className="rounded-[10px] border border-fds-bad-line bg-fds-bad-bg px-3 py-2 text-sm text-fds-bad">
                        <strong>{t('suivi.motif')}</strong> {piece.motif_rejet}
                      </p>
                    )}
                    {piece.statut === 'rejete' && (
                      <Link
                        to={`/suivi/${suivi.reference_dossier}/remplacer/${piece.id}`}
                        className="min-h-12 px-4 lg:px-6 lg:self-start rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white font-semibold flex items-center justify-center"
                      >
                        {t('suivi.remplacer')}
                      </Link>
                    )}
                  </div>
                </li>
              );
            })}
          </ul>

          <p className="text-xs text-fds-mute">{t('suivi.note')}</p>
        </div>
      </div>
    </>
  );
};

/**
 * Suivi de dossier par référence (maquettes « Suivi » et « Dossier »). `/suivi` propose la recherche,
 * `/suivi/CAN-2026-0089` affiche le dossier ; `/suivi?ref=CAN-2026-0089` redirige vers cette adresse.
 */
export const SuiviPage: React.FC = () => {
  const t = useT();
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
    contenu = <RechercheReference valeurInitiale={reference} message={t('suivi.formatErreur')} />;
  } else if (!resultat || resultat.reference !== reference) {
    contenu = (
      <p className="text-fds-mute" role="status">
        {t('suivi.recherche')}
      </p>
    );
  } else if (resultat.etat === 'ok') {
    contenu = <VueDossier suivi={resultat.suivi} />;
  } else {
    const messages = {
      introuvable: t('suivi.introuvable'),
      limite: t('suivi.limite'),
      erreur: t('suivi.reseau'),
    } as const;
    contenu = <RechercheReference valeurInitiale={reference} message={messages[resultat.etat]} />;
  }

  return <div className="max-w-xl lg:max-w-5xl w-full mx-auto px-4 py-6 lg:pt-10 lg:pb-14 flex-1 flex flex-col gap-[18px] lg:gap-7">{contenu}</div>;
};
