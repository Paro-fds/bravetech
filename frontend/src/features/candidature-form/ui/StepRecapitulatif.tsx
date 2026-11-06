import React, { useEffect, useState } from 'react';
import { Info, ShieldCheck } from 'lucide-react';
import {
  candidatureApi,
  extraireManques,
  type InformationsPersonnelles,
  type PieceDossier,
} from '../../../entities/candidature';
import { estCandidaturesFermees } from '../../../entities/calendrier';
import { formaterDateNaissance } from '../lib/dates';
import { formaterTaille } from '../lib/fichiers';
import type { PaiementSimule } from '../model/useCandidatureStore';
import { BarreAction, CLASSE_BOUTON_PRIMAIRE } from './BarreAction';
import { useNomDepartement, useNomPiece, useT } from '../../../shared/i18n';

interface StepRecapitulatifProps {
  candidatureId: string;
  informations: InformationsPersonnelles;
  deplacementPhysique: boolean | null;
  paiement: PaiementSimule | null;
  montantHtg: number;
  onRetour: () => void;
  /** Soumet le dossier ; rejette en cas d'erreur (dossier incomplet, réseau). */
  onSoumettre: () => Promise<void>;
}

const Ligne: React.FC<{ libelle: string; children: React.ReactNode }> = ({ libelle, children }) => (
  <div className="flex gap-3 text-sm py-1">
    <dt className="w-32 shrink-0 text-fds-mute">{libelle}</dt>
    <dd className="flex-1 font-semibold break-words">{children}</dd>
  </div>
);

/** Récapitulatif du dossier avant la soumission définitive (US-008). */
export const StepRecapitulatif: React.FC<StepRecapitulatifProps> = ({
  candidatureId,
  informations,
  deplacementPhysique,
  paiement,
  montantHtg,
  onRetour,
  onSoumettre,
}) => {
  const t = useT();
  const nomPiece = useNomPiece();
  const nomDepartement = useNomDepartement();
  const [pieces, setPieces] = useState<PieceDossier[] | null>(null);
  const [erreur, setErreur] = useState<string | null>(null);
  const [manques, setManques] = useState<string[]>([]);
  const [enCours, setEnCours] = useState(false);

  useEffect(() => {
    let annule = false;
    candidatureApi
      .listerPieces(candidatureId)
      .then((liste) => {
        if (!annule) setPieces(liste);
      })
      .catch(() => {
        // Le récapitulatif reste utilisable sans la liste ; le serveur revérifie de toute façon les pièces
      });
    return () => {
      annule = true;
    };
  }, [candidatureId]);

  const soumettre = async () => {
    setErreur(null);
    setManques([]);
    setEnCours(true);
    try {
      await onSoumettre();
    } catch (e) {
      const liste = extraireManques(e);
      if (liste) {
        setManques(liste);
        setErreur(t('recap.incomplet'));
      } else if (estCandidaturesFermees(e)) {
        setErreur(t('cand.fermeeErreur'));
      } else {
        setErreur(t('recap.erreurEnvoi'));
      }
    } finally {
      setEnCours(false);
    }
  };

  return (
    <div className="flex flex-col gap-4 flex-1">
      <h1 className="font-fds-serif text-2xl font-bold text-fds-title">{t('recap.titre')}</h1>
      <p className="text-sm text-fds-mute">{t('recap.consigne')}</p>

      <section className="rounded-xl border border-fds-line bg-fds-surface p-4" aria-label={t('recap.secInfos')}>
        <h2 className="font-fds-serif text-lg font-bold text-fds-title mb-1">{t('recap.secInfos')}</h2>
        <dl>
          <Ligne libelle={t('recap.nom')}>
            {informations.prenom} {informations.nom}
          </Ligne>
          <Ligne libelle={t('recap.naissance')}>{formaterDateNaissance(informations.date_naissance)}</Ligne>
          <Ligne libelle={t('recap.email')}>{informations.email}</Ligne>
          <Ligne libelle={t('recap.tel')}>{informations.telephone}</Ligne>
          <Ligne libelle={t('recap.residence')}>
            {informations.commune}, {nomDepartement(informations.departement)}
          </Ligne>
        </dl>
      </section>

      <section className="rounded-xl border border-fds-line bg-fds-surface p-4" aria-label={t('recap.secAdmissionAria')}>
        <h2 className="font-fds-serif text-lg font-bold text-fds-title mb-1">{t('recap.admTitre')}</h2>
        <dl>
          <Ligne libelle={t('recap.admTitre')}>{t('adm.mpc')}</Ligne>
          <Ligne libelle={t('recap.deplacement')}>
            {deplacementPhysique === null ? '—' : deplacementPhysique ? t('adm.optOui') : t('adm.optNon')}
          </Ligne>
          <Ligne libelle={t('recap.frais')}>
            {t('recap.fraisValeur', { montant: montantHtg })}{paiement ? ` · ${paiement.reference}` : ''}
          </Ligne>
        </dl>
      </section>

      <section className="rounded-xl border border-fds-line bg-fds-surface p-4" aria-label={t('recap.secPieces')}>
        <h2 className="font-fds-serif text-lg font-bold text-fds-title mb-1">{t('recap.secPieces')}</h2>
        {pieces ? (
          <ul className="flex flex-col gap-1.5 text-sm">
            {pieces.map((p) => (
              <li key={p.id} className="flex gap-2">
                <span className="flex-1">{nomPiece(p.id, p.nom)}</span>
                <span className="text-fds-mute text-right break-all">
                  {p.nom_fichier ? `${p.nom_fichier}${p.taille_octets ? ` (${formaterTaille(p.taille_octets)})` : ''}` : t('recap.manquant')}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-fds-mute" role="status">
            {t('recap.chargement')}
          </p>
        )}
      </section>

      <div className="flex gap-2.5 items-start rounded-[10px] border border-fds-accent-line bg-fds-navy-t px-3.5 py-3 text-sm text-fds-title">
        <Info className="w-5 h-5 shrink-0" aria-hidden="true" />
        <span>{t('recap.simulNote')}</span>
      </div>

      {erreur && (
        <div role="alert" className="rounded-[10px] border border-fds-bad-line bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
          <p>{erreur}</p>
          {manques.length > 0 && (
            <ul className="list-disc pl-5 mt-1">
              {manques.map((m) => (
                <li key={m}>{m}</li>
              ))}
            </ul>
          )}
        </div>
      )}

      <BarreAction>
        <button type="button" onClick={() => void soumettre()} disabled={enCours} className={CLASSE_BOUTON_PRIMAIRE}>
          <ShieldCheck className="w-5 h-5" aria-hidden="true" />
          <span>{enCours ? t('recap.enCours') : t('recap.confirmer')}</span>
        </button>
        <button type="button" onClick={onRetour} disabled={enCours} className="min-h-11 text-fds-accent font-semibold underline">
          {t('commun.retour')}
        </button>
      </BarreAction>
    </div>
  );
};
