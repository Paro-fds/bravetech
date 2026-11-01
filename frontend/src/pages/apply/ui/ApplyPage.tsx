import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { CheckCircle2 } from 'lucide-react';
import { candidatureApi, type InformationsPersonnelles } from '../../../entities/candidature';
import {
  StepAdmission,
  StepInformations,
  StepProgress,
  useCandidatureStore,
} from '../../../features/candidature-form';
import { ApiError } from '../../../shared/api/client';

/** Tunnel de candidature : étapes 1 (informations) et 2 (admission MPC + déplacement physique) — US-005. */
export const ApplyPage: React.FC = () => {
  const {
    candidatureId,
    etape,
    informations,
    deplacementPhysique,
    setInformations,
    setBrouillon,
    setDeplacementPhysique,
    allerEtape,
    reinitialiser,
  } = useCandidatureStore();

  // Reprise : si un brouillon existe déjà côté serveur, on le recharge (source de vérité = serveur).
  const [reprise, setReprise] = useState(Boolean(candidatureId));

  useEffect(() => {
    if (!candidatureId) return;
    let annule = false;
    candidatureApi
      .obtenirBrouillon(candidatureId)
      .then((brouillon) => {
        if (annule) return;
        setBrouillon(brouillon.candidature_id, brouillon.informations, brouillon.deplacement_physique);
        if (brouillon.deplacement_physique !== null) allerEtape(3);
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
    setBrouillon(brouillon.candidature_id, brouillon.informations, brouillon.deplacement_physique);
    allerEtape(2);
  };

  const soumettreDeplacement = async (valeur: boolean) => {
    if (!candidatureId) return;
    const brouillon = await candidatureApi.definirDeplacementPhysique(candidatureId, valeur);
    setDeplacementPhysique(brouillon.deplacement_physique);
    allerEtape(3);
  };

  // Garde-fou : l'étape 2 suppose un brouillon créé
  const etapeAffichee = etape > 1 && !candidatureId ? 1 : etape;

  return (
    <div className="bg-slate-50 min-h-screen">
      <StepProgress etape={Math.min(etapeAffichee, 4)} />
      <div className="max-w-xl mx-auto px-4 py-8">
        {reprise ? (
          <p className="text-slate-600" role="status">
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
        ) : (
          <section className="flex flex-col gap-4" aria-live="polite">
            <div className="flex items-center gap-3 text-emerald-700">
              <CheckCircle2 className="w-8 h-8" />
              <h1 className="text-2xl font-extrabold text-slate-900">Vos informations sont enregistrées</h1>
            </div>
            <p className="text-slate-600">
              Le paiement simulé des frais de dossier et le dépôt des pièces seront disponibles très prochainement.
              Votre brouillon est conservé : vous pourrez reprendre ici.
            </p>
            <Link to="/" className="min-h-12 rounded-xl border-2 border-blue-700 text-blue-700 font-bold flex items-center justify-center">
              Retour à l'accueil
            </Link>
          </section>
        )}
      </div>
    </div>
  );
};
