import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, ExternalLink } from 'lucide-react';
import { ApiError } from '../../../shared/api/client';
import { BADGES_DOSSIER, dossierAdminApi, type DossierAdmin, type PieceAdmin } from '../../../entities/dossier-admin';
import { useSessionStore, type Session } from '../../../entities/session';
import { formaterHorodatage, formaterJourCourt, formaterTaille } from '../../../features/candidature-form';

type Resultat = { reference: string; etat: 'ok'; dossier: DossierAdmin } | { reference: string; etat: 'introuvable' | 'erreur' };
type Apercu = { documentId: string; url: string; type: string } | { documentId: string; erreur: true };

const BADGES_PIECE: Record<PieceAdmin['statut'], { libelle: string; classe: string }> = {
  manquant: { libelle: 'Manquante', classe: 'bg-fds-warn-bg text-fds-warn' },
  en_attente: { libelle: 'À examiner', classe: 'bg-fds-warn-bg text-fds-warn' },
  valide: { libelle: 'Validé', classe: 'bg-fds-ok-bg text-fds-ok' },
  rejete: { libelle: 'Refusé', classe: 'bg-fds-bad-bg text-fds-bad' },
};

const Info: React.FC<{ libelle: string; children: React.ReactNode }> = ({ libelle, children }) => (
  <div className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-1">
    <div className="text-xs text-fds-mute">{libelle}</div>
    <div className="font-semibold break-words">{children}</div>
  </div>
);

/** Aperçu d'une pièce, récupérée avec la session du personnel puis affichée depuis une URL locale. */
const ApercuPiece: React.FC<{ session: Session; piece: PieceAdmin }> = ({ session, piece }) => {
  const [apercu, setApercu] = useState<Apercu | null>(null);
  const documentId = piece.document_id;

  useEffect(() => {
    if (!documentId) return;
    let annule = false;
    let url: string | null = null;
    dossierAdminApi
      .telechargerDocument(session, documentId)
      .then((blob) => {
        if (annule) return;
        url = URL.createObjectURL(blob);
        setApercu({ documentId, url, type: blob.type });
      })
      .catch(() => {
        if (!annule) setApercu({ documentId, erreur: true });
      });
    return () => {
      annule = true;
      if (url) URL.revokeObjectURL(url); // libère la mémoire quand on change de pièce
    };
  }, [session, documentId]);

  if (!documentId) {
    return <div className="h-40 rounded-[10px] bg-[#e9edf4] border border-dashed border-fds-field flex items-center justify-center text-fds-mute font-semibold">Aucun fichier déposé</div>;
  }
  const courant = apercu && apercu.documentId === documentId ? apercu : null;
  if (!courant) return <p className="text-fds-mute" role="status">Chargement du document…</p>;
  if ('erreur' in courant) {
    return (
      <p role="alert" className="rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
        Impossible d'afficher ce document.
      </p>
    );
  }
  return (
    <>
      <div className="h-80 sm:h-[480px] rounded-[10px] bg-[#e9edf4] border border-fds-line overflow-hidden">
        {courant.type.startsWith('image/') ? (
          <img src={courant.url} alt={`Aperçu : ${piece.nom}`} className="w-full h-full object-contain" />
        ) : (
          <iframe src={courant.url} title={`Aperçu : ${piece.nom}`} className="w-full h-full" />
        )}
      </div>
      <a
        href={courant.url}
        target="_blank"
        rel="noreferrer"
        className="self-start min-h-12 px-4 rounded-lg border-2 border-fds-navy bg-white text-fds-navy font-semibold flex items-center gap-2"
      >
        <ExternalLink className="w-5 h-5" aria-hidden="true" />
        Ouvrir en grand
      </a>
    </>
  );
};

/** Détail d'un dossier (maquette « Administration validation d'un dossier », sans les boutons de décision : US-013). */
export const AdminDossierPage: React.FC = () => {
  const { reference = '' } = useParams();
  const session = useSessionStore((s) => s.session);
  const [resultat, setResultat] = useState<Resultat | null>(null);
  const [choisie, setChoisie] = useState<string | null>(null);

  useEffect(() => {
    if (!session) return;
    let annule = false;
    dossierAdminApi
      .obtenir(session, reference)
      .then((dossier) => {
        if (!annule) setResultat({ reference, etat: 'ok', dossier });
      })
      .catch((erreur) => {
        if (!annule) setResultat({ reference, etat: erreur instanceof ApiError && erreur.status === 404 ? 'introuvable' : 'erreur' });
      });
    return () => {
      annule = true;
    };
  }, [session, reference]);

  const retour = (
    <Link to="/admin" className="flex items-center gap-2 min-h-11 font-semibold text-fds-navy">
      <ArrowLeft className="w-5 h-5" aria-hidden="true" />
      Toutes les candidatures
    </Link>
  );

  if (!session) return null;
  if (!resultat || resultat.reference !== reference) {
    return (
      <>
        {retour}
        <p className="text-fds-mute" role="status">
          Chargement du dossier…
        </p>
      </>
    );
  }
  if (resultat.etat !== 'ok') {
    return (
      <>
        {retour}
        <p role="alert" className="rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
          {resultat.etat === 'introuvable' ? 'Aucun dossier ne porte cette référence.' : 'Impossible de charger le dossier. Vérifiez votre connexion.'}
        </p>
      </>
    );
  }

  const d = resultat.dossier;
  const badge = BADGES_DOSSIER[d.statut];
  // Par défaut : première pièce à examiner, sinon la première
  const pieceParDefaut = d.pieces.find((p) => p.statut === 'en_attente') ?? d.pieces[0];
  const piece = d.pieces.find((p) => p.id === choisie) ?? pieceParDefaut;
  const badgePiece = BADGES_PIECE[piece.statut];

  return (
    <>
      {retour}

      <div className="flex flex-wrap items-start gap-4">
        <div className="flex-1">
          <h1 className="font-fds-serif text-[28px] font-bold text-fds-navy-d">{d.reference_dossier}</h1>
          <p className="text-fds-mute">
            {d.nom} {d.prenom} · Admission MPC · reçu le {d.soumise_le ? formaterJourCourt(d.soumise_le) : '–'}
          </p>
        </div>
        <span className={`rounded-full px-3 py-1 text-sm font-semibold ${badge.classe}`}>{badge.libelle}</span>
      </div>

      <div className="grid gap-4 grid-cols-[repeat(auto-fit,minmax(220px,1fr))]">
        <Info libelle="Déplacement physique">{d.deplacement_physique === null ? '–' : d.deplacement_physique ? 'Oui' : 'Non'}</Info>
        <Info libelle="Paiement (simulé)">
          {d.reference_paiement ?? '–'} · {d.montant_htg} HTG
        </Info>
        <Info libelle="Contact">
          <span className="block">{d.email}</span>
          <span className="block font-normal text-sm">{d.telephone}</span>
          <span className="block font-normal text-sm text-fds-mute">
            {d.commune}, {d.departement}
          </span>
        </Info>
      </div>

      <div className="flex flex-wrap gap-6 items-start">
        <section className="flex-[1_1_320px] rounded-xl border border-fds-line bg-white px-4 py-2" aria-label="Pièces du dossier">
          <h2 className="font-fds-serif text-lg font-bold text-fds-navy-d py-2">Pièces</h2>
          <ul>
            {d.pieces.map((p) => {
              const b = BADGES_PIECE[p.statut];
              const active = p.id === piece.id;
              return (
                <li key={p.id} className="border-t border-fds-line">
                  <button
                    type="button"
                    onClick={() => setChoisie(p.id)}
                    aria-current={active}
                    className={`w-full min-h-12 py-3 flex items-center gap-2 text-left ${active ? 'bg-fds-navy-t -mx-2 px-2 rounded-lg font-semibold' : ''}`}
                  >
                    <span className="flex-1">{p.nom}</span>
                    <span className={`rounded-full px-2.5 py-0.5 text-[13px] font-semibold whitespace-nowrap ${b.classe}`}>{b.libelle}</span>
                  </button>
                </li>
              );
            })}
          </ul>
        </section>

        <section className="flex-[2_1_460px] rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-3.5" aria-label="Pièce sélectionnée">
          <div className="flex flex-wrap items-baseline gap-2">
            <h2 className="font-fds-serif text-xl font-bold text-fds-navy-d flex-1">{piece.nom}</h2>
            <span className={`rounded-full px-2.5 py-0.5 text-[13px] font-semibold ${badgePiece.classe}`}>{badgePiece.libelle}</span>
          </div>
          {piece.nom_fichier && (
            <p className="text-sm text-fds-mute break-all">
              {piece.nom_fichier}
              {piece.taille_octets !== null && ` · ${formaterTaille(piece.taille_octets)}`}
              {piece.depose_le && ` · déposé le ${formaterHorodatage(piece.depose_le)}`}
            </p>
          )}
          {piece.statut === 'rejete' && piece.motif_rejet && (
            <p className="rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3 py-2.5 text-sm text-fds-bad">
              <strong>Motif du refus :</strong> {piece.motif_rejet}
            </p>
          )}
          <ApercuPiece session={session} piece={piece} />
        </section>
      </div>
    </>
  );
};
