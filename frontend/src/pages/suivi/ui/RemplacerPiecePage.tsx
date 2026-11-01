import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, Check, FileText, TriangleAlert, Upload, X } from 'lucide-react';
import { candidatureApi, extraireErreursChamps, type PieceSuivi } from '../../../entities/candidature';
import { attributAccept, formaterTaille, validerFichierLocal } from '../../../features/candidature-form';
import { ApiError } from '../../../shared/api/client';
import { traduireMaintenant as tr, useNomPiece, useT } from '../../../shared/i18n/useT';

type Chargement = { reference: string; etat: 'ok'; piece: PieceSuivi } | { reference: string; etat: 'introuvable' | 'erreur' };

function messageErreur(erreur: unknown): string {
  if (erreur instanceof ApiError) {
    if (erreur.status === 403) return tr('rempl.e403');
    if (erreur.status === 409) return tr('rempl.e409');
    if (erreur.status === 413) return tr('pieces.e413');
    if (erreur.status === 429) return tr('rempl.e429');
    const champs = extraireErreursChamps(erreur);
    if (champs?.fichier) return champs.fichier;
  }
  return tr('pieces.eReseau');
}

/** Remplacement d'une pièce refusée (maquette « Remplacement »), sans compte : référence dans l'adresse + email du dossier. */
export const RemplacerPiecePage: React.FC = () => {
  const t = useT();
  const nomPiece = useNomPiece();
  const { reference = '', piece: pieceId = '' } = useParams();
  const [chargement, setChargement] = useState<Chargement | null>(null);
  const [email, setEmail] = useState('');
  const [fichier, setFichier] = useState<File | null>(null);
  const [erreur, setErreur] = useState<string | null>(null);
  const [progression, setProgression] = useState<number | null>(null);
  const [envoye, setEnvoye] = useState(false);

  useEffect(() => {
    let annule = false;
    candidatureApi
      .obtenirSuivi(reference)
      .then((suivi) => {
        if (annule) return;
        const piece = suivi.pieces.find((p) => p.id === pieceId);
        setChargement(piece ? { reference, etat: 'ok', piece } : { reference, etat: 'introuvable' });
      })
      .catch((e) => {
        if (!annule) setChargement({ reference, etat: e instanceof ApiError && e.status === 404 ? 'introuvable' : 'erreur' });
      });
    return () => {
      annule = true;
    };
  }, [reference, pieceId]);

  const retour = (
    <Link to={`/suivi/${reference}`} className="flex items-center gap-2 min-h-11 font-semibold text-fds-navy">
      <ArrowLeft className="w-5 h-5" aria-hidden="true" />
      {t('rempl.retour')}
    </Link>
  );

  let contenu: React.ReactNode;
  if (!chargement || chargement.reference !== reference) {
    contenu = (
      <p className="text-fds-mute" role="status">
        {t('rempl.chargement')}
      </p>
    );
  } else if (chargement.etat !== 'ok') {
    contenu = (
      <p role="alert" className="rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
        {chargement.etat === 'introuvable' ? t('rempl.introuvable') : t('rempl.reseau')}
      </p>
    );
  } else if (envoye) {
    contenu = (
      <div className="flex flex-col gap-4" aria-live="polite">
        <div className="flex flex-col items-center text-center gap-2.5">
          <span className="w-16 h-16 rounded-full bg-fds-ok text-white flex items-center justify-center">
            <Check className="w-9 h-9" strokeWidth={2.5} aria-hidden="true" />
          </span>
          <h1 className="font-fds-serif text-2xl font-bold text-fds-navy-d">{t('rempl.envoyeTitre')}</h1>
          <p className="text-fds-mute">
            {t('rempl.envoyeTexte', { nom: nomPiece(chargement.piece.id, chargement.piece.nom) })}
          </p>
        </div>
        <Link to={`/suivi/${reference}`} className="min-h-12 rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white font-semibold flex items-center justify-center">
          {t('rempl.voirDossier')}
        </Link>
      </div>
    );
  } else if (chargement.piece.statut !== 'rejete') {
    contenu = (
      <>
        <h1 className="font-fds-serif text-2xl font-bold text-fds-navy-d">{t('rempl.rienTitre')}</h1>
        <p className="text-fds-mute">{t('rempl.rienTexte', { nom: nomPiece(chargement.piece.id, chargement.piece.nom) })}</p>
      </>
    );
  } else {
    const piece = chargement.piece;
    const envoyer = async (e: React.FormEvent) => {
      e.preventDefault();
      if (!email.trim()) return setErreur(t('rempl.errEmail'));
      if (!fichier) return setErreur(t('rempl.errFichier'));
      const locale = validerFichierLocal(fichier, piece);
      if (locale) return setErreur(locale);
      setErreur(null);
      setProgression(0);
      try {
        await candidatureApi.remplacerPiece(reference, piece.id, email.trim(), fichier, setProgression);
        setEnvoye(true);
      } catch (e) {
        setErreur(messageErreur(e));
      } finally {
        setProgression(null);
      }
    };
    const enCours = progression !== null;

    contenu = (
      <form onSubmit={envoyer} noValidate className="flex flex-col gap-[18px]">
        <section className="flex flex-col gap-2">
          <h1 className="font-fds-serif text-2xl font-bold text-fds-navy-d">{t('rempl.titre', { nom: nomPiece(piece.id, piece.nom) })}</h1>
          <p className="text-fds-mute">{t('rempl.intro')}</p>
        </section>

        {piece.motif_rejet && (
          <div className="flex gap-2.5 items-start rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
            <TriangleAlert className="w-5 h-5 shrink-0" aria-hidden="true" />
            <span>
              <strong>{t('rempl.motif')}</strong> {piece.motif_rejet}
            </span>
          </div>
        )}

        <section className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-2.5">
          <h2 className="font-semibold">{t('rempl.conseilsTitre')}</h2>
          {[
            t('rempl.conseil1'),
            t('rempl.conseil2'),
            t('rempl.conseil3', { formats: piece.format_accepte, max: piece.taille_max_mo }),
          ].map((conseil) => (
            <div key={conseil} className="flex gap-2 items-start text-sm">
              <Check className="w-5 h-5 shrink-0 text-fds-ok" aria-hidden="true" />
              <span>{conseil}</span>
            </div>
          ))}
        </section>

        <div className="flex flex-col gap-1.5">
          <label htmlFor="email-dossier" className="text-[15px] font-semibold">
            {t('rempl.email')}
          </label>
          <input
            id="email-dossier"
            type="email"
            inputMode="email"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            aria-describedby="email-aide"
            className="w-full min-h-12 rounded-lg border-[1.5px] border-fds-field bg-white px-3 text-base text-fds-ink focus:outline-none focus:ring-2 focus:ring-fds-navy"
          />
          <p id="email-aide" className="text-[13px] text-fds-mute">
            {t('rempl.emailAide')}
          </p>
        </div>

        <label className="min-h-16 rounded-lg border-2 border-dashed border-fds-navy bg-white text-fds-navy font-semibold flex items-center justify-center gap-2 cursor-pointer text-center px-3 focus-within:ring-2 focus-within:ring-fds-navy focus-within:ring-offset-2">
          <input
            type="file"
            className="sr-only"
            accept={attributAccept(piece.format_accepte)}
            disabled={enCours}
            onChange={(e) => {
              setFichier(e.target.files?.[0] ?? null);
              setErreur(null);
              e.target.value = '';
            }}
          />
          <Upload className="w-5 h-5 shrink-0" aria-hidden="true" />
          <span>{fichier ? t('pieces.autre') : t('rempl.choisir')}</span>
        </label>

        {fichier && (
          <div className="rounded-xl border border-fds-line bg-white p-3 flex items-center gap-2.5">
            <FileText className="w-6 h-6 shrink-0 text-fds-navy" aria-hidden="true" />
            <div className="flex-1 min-w-0">
              <div className="text-sm font-semibold truncate">{fichier.name}</div>
              <div className="text-xs text-fds-mute">{t('rempl.pret', { taille: formaterTaille(fichier.size) })}</div>
            </div>
            <button type="button" disabled={enCours} onClick={() => setFichier(null)} aria-label={t('rempl.retirer')} className="w-11 h-11 flex items-center justify-center">
              <X className="w-5 h-5" aria-hidden="true" />
            </button>
          </div>
        )}

        {progression !== null && (
          <div className="flex flex-col gap-1">
            <div className="h-2 rounded bg-fds-line overflow-hidden" role="progressbar" aria-valuenow={progression} aria-valuemin={0} aria-valuemax={100} aria-label={t('rempl.progAria')}>
              <div className="h-full bg-fds-navy" style={{ width: `${progression}%` }} />
            </div>
            <span className="text-xs text-fds-mute">{t('pieces.envoiCours', { n: progression })}</span>
          </div>
        )}

        {erreur && (
          <div role="alert" className="flex gap-2.5 items-start rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
            <TriangleAlert className="w-5 h-5 shrink-0" aria-hidden="true" />
            <span>{erreur}</span>
          </div>
        )}

        <button
          type="submit"
          disabled={enCours}
          className="min-h-12 px-4 rounded-lg bg-fds-navy hover:bg-fds-navy-d disabled:opacity-60 text-white font-semibold flex items-center justify-center transition-colors"
        >
          {enCours ? t('rempl.envoi') : t('rempl.envoyer')}
        </button>
        <p className="text-xs text-fds-mute text-center">{t('rempl.note')}</p>
      </form>
    );
  }

  return (
    <div className="max-w-xl w-full mx-auto px-4 py-6 flex-1 flex flex-col gap-[18px]">
      {!envoye && retour}
      {contenu}
    </div>
  );
};
