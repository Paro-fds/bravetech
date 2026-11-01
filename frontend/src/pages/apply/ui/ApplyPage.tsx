import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { CheckCircle2 } from 'lucide-react';
import {
  candidatureApi,
  STATUT_PAIEMENT_SIMULE,
  type Brouillon,
  type InformationsPersonnelles,
  type MethodePaiement,
} from '../../../entities/candidature';
import {
  StepAdmission,
  StepInformations,
  StepPaiement,
  StepProgress,
  useCandidatureStore,
  type EtapeCandidature,
} from '../../../features/candidature-form';
import { ApiError } from '../../../shared/api/client';

/** Étape du tunnel que le serveur autorise, d'après l'état du brouillon (le serveur est la source de vérité). */
function etapeAutorisee(brouillon: Brouillon): EtapeCandidature {
  if (brouillon.statut_paiement === STATUT_PAIEMENT_SIMULE) return 4;
  if (brouillon.deplacement_physique !== null) return 3;
  return 2;
}

/**
 * Tunnel de candidature (maquettes) : étapes 1 (informations), 2 (admission MPC + déplacement physique),
 * 3 (paiement simulé) ; l'étape 4 (pièces) arrive avec US-007.
 */
export const ApplyPage: React.FC = () => {
  const {
    candidatureId,
    etape,
    informations,
    deplacementPhysique,
    montantHtg,
    paiement,
    methodePaiementChoisie,
    numeroPaiement,
    setInformations,
    appliquerBrouillon,
    setDeplacementPhysique,
    setSaisiePaiement,
    allerEtape,
    reinitialiser,
  } = useCandidatureStore();

  // Reprise : si un brouillon existe déjà côté serveur, on le recharge.
  const [reprise, setReprise] = useState(Boolean(candidatureId));

  useEffect(() => {
    if (!candidatureId) return;
    let annule = false;
    candidatureApi
      .obtenirBrouillon(candidatureId)
      .then((brouillon) => {
        if (annule) return;
        appliquerBrouillon(brouillon);
        allerEtape(etapeAutorisee(brouillon));
      })
      .catch((erreur) => {
        // Brouillon disparu côté serveur : on repart d'un formulaire vide. Autre erreur : on garde la saisie locale.
        if (!annule && erreur instanceof ApiError && erreur.status === 404) reinitialiser();
      })
      .finally(() => {
        if (!annule) setReprise(false);
      });
    return () => {
      annule = true;
    };
    // Exécuté une seule fois au chargement de la page
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const soumettreInformations = async (valeurs: InformationsPersonnelles) => {
    const brouillon = candidatureId
      ? await candidatureApi.modifierInformations(candidatureId, valeurs)
      : await candidatureApi.creerBrouillon(valeurs);
    appliquerBrouillon(brouillon);
    allerEtape(2);
  };

  const soumettreDeplacement = async (valeur: boolean) => {
    if (!candidatureId) return;
    const brouillon = await candidatureApi.definirDeplacementPhysique(candidatureId, valeur);
    appliquerBrouillon(brouillon);
    allerEtape(3);
  };

  const soumettrePaiement = async (methode: MethodePaiement, numero: string) => {
    if (!candidatureId) return;
    const brouillon = await candidatureApi.simulerPaiement(candidatureId, methode, numero);
    appliquerBrouillon(brouillon);
    allerEtape(4);
  };

  // Garde-fous : on n'affiche jamais une étape dont les préalables ne sont pas remplis
  let etapeAffichee: EtapeCandidature = etape;
  if (etapeAffichee > 1 && !candidatureId) etapeAffichee = 1;
  if (etapeAffichee > 2 && deplacementPhysique === null) etapeAffichee = 2;
  if (etapeAffichee > 3 && !paiement) etapeAffichee = 3;

  return (
    <>
      <StepProgress etape={etapeAffichee} />
      <div className="max-w-xl w-full mx-auto px-4 pt-6 flex-1 flex flex-col">
        {reprise ? (
          <p className="text-fds-mute" role="status">
            Reprise de votre candidature…
          </p>
        ) : etapeAffichee === 1 ? (
          <StepInformations valeurs={informations} onChange={setInformations} onSoumettre={soumettreInformations} />
        ) : etapeAffichee === 2 ? (
          <StepAdmission
            deplacementPhysique={deplacementPhysique}
            onChange={setDeplacementPhysique}
            onSoumettre={soumettreDeplacement}
            onRetour={() => allerEtape(1)}
          />
        ) : etapeAffichee === 3 ? (
          <StepPaiement
            montantHtg={montantHtg}
            methode={methodePaiementChoisie}
            numero={numeroPaiement}
            onChange={setSaisiePaiement}
            onSoumettre={soumettrePaiement}
            onRetour={() => allerEtape(2)}
          />
        ) : (
          <section className="flex flex-col gap-4" aria-live="polite">
            <div className="flex gap-2.5 items-start rounded-[10px] border border-[#9bd3b2] bg-fds-ok-bg px-3.5 py-3 text-sm text-fds-ok">
              <CheckCircle2 className="w-5 h-5 shrink-0" aria-hidden="true" />
              <span>
                Paiement simulé enregistré : <strong>{paiement?.reference}</strong> (aucun argent réel prélevé).
              </span>
            </div>
            <h1 className="font-fds-serif text-2xl font-bold text-fds-navy-d">Déposez vos pièces</h1>
            <p className="text-fds-mute">
              Le dépôt des pièces sera disponible très prochainement. Votre brouillon est conservé : vous pourrez
              reprendre ici.
            </p>
            <Link
              to="/"
              className="min-h-12 rounded-lg border-2 border-fds-navy bg-white text-fds-navy font-semibold flex items-center justify-center"
            >
              Retour à l'accueil
            </Link>
          </section>
        )}
      </div>
    </>
  );
};
