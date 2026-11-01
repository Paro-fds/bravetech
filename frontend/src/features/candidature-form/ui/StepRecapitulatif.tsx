import React, { useEffect, useState } from 'react';
import { Info, ShieldCheck } from 'lucide-react';
import {
  candidatureApi,
  extraireManques,
  type InformationsPersonnelles,
  type PieceDossier,
} from '../../../entities/candidature';
import { formaterDateNaissance } from '../lib/dates';
import { formaterTaille } from '../lib/fichiers';
import type { PaiementSimule } from '../model/useCandidatureStore';
import { BarreAction, CLASSE_BOUTON_PRIMAIRE } from './BarreAction';

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
        setErreur('Votre dossier est incomplet. Il manque :');
      } else {
        setErreur(
          "Impossible d'envoyer votre dossier pour le moment. Vérifiez votre connexion et réessayez : vos informations sont conservées.",
        );
      }
    } finally {
      setEnCours(false);
    }
  };

  return (
    <div className="flex flex-col gap-4 flex-1">
      <h1 className="font-fds-serif text-2xl font-bold text-fds-navy-d">Vérifiez votre dossier</h1>
      <p className="text-sm text-fds-mute">Relisez ces informations : après l'envoi, votre dossier ne sera plus modifiable.</p>

      <section className="rounded-xl border border-fds-line bg-white p-4" aria-label="Vos informations">
        <h2 className="font-fds-serif text-lg font-bold text-fds-navy-d mb-1">Vos informations</h2>
        <dl>
          <Ligne libelle="Nom">
            {informations.prenom} {informations.nom}
          </Ligne>
          <Ligne libelle="Naissance">{formaterDateNaissance(informations.date_naissance)}</Ligne>
          <Ligne libelle="Email">{informations.email}</Ligne>
          <Ligne libelle="Téléphone">{informations.telephone}</Ligne>
          <Ligne libelle="Résidence">
            {informations.commune}, {informations.departement}
          </Ligne>
        </dl>
      </section>

      <section className="rounded-xl border border-fds-line bg-white p-4" aria-label="Admission et paiement">
        <h2 className="font-fds-serif text-lg font-bold text-fds-navy-d mb-1">Admission</h2>
        <dl>
          <Ligne libelle="Admission">Premier cycle MPC</Ligne>
          <Ligne libelle="Déplacement">
            {deplacementPhysique === null ? '—' : deplacementPhysique ? "Oui, j'ai dû me déplacer" : 'Non, tout a été fait en ligne'}
          </Ligne>
          <Ligne libelle="Frais">
            {montantHtg} HTG (simulation){paiement ? ` · ${paiement.reference}` : ''}
          </Ligne>
        </dl>
      </section>

      <section className="rounded-xl border border-fds-line bg-white p-4" aria-label="Vos pièces">
        <h2 className="font-fds-serif text-lg font-bold text-fds-navy-d mb-1">Vos pièces</h2>
        {pieces ? (
          <ul className="flex flex-col gap-1.5 text-sm">
            {pieces.map((p) => (
              <li key={p.id} className="flex gap-2">
                <span className="flex-1">{p.nom}</span>
                <span className="text-fds-mute text-right break-all">
                  {p.nom_fichier ? `${p.nom_fichier}${p.taille_octets ? ` (${formaterTaille(p.taille_octets)})` : ''}` : 'Manquant'}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-fds-mute" role="status">
            Chargement…
          </p>
        )}
      </section>

      <div className="flex gap-2.5 items-start rounded-[10px] border border-[#b9cbe3] bg-fds-navy-t px-3.5 py-3 text-sm text-fds-navy-d">
        <Info className="w-5 h-5 shrink-0" aria-hidden="true" />
        <span>Le paiement est une simulation : aucun argent n'a été prélevé.</span>
      </div>

      {erreur && (
        <div role="alert" className="rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
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
          <span>{enCours ? 'Envoi en cours…' : 'Confirmer et soumettre mon dossier'}</span>
        </button>
        <button type="button" onClick={onRetour} disabled={enCours} className="min-h-11 text-fds-navy font-semibold underline">
          Retour
        </button>
      </BarreAction>
    </div>
  );
};
