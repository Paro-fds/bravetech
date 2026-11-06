import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { CalendarX, Info } from 'lucide-react';
import { calendrierApi, candidaturesAcceptees, type CalendrierPublic } from '../../../entities/calendrier';
import {
  candidatureApi,
  STATUT_PAIEMENT_SIMULE,
  STATUT_SOUMISE,
  type Brouillon,
  type InformationsPersonnelles,
  type MethodePaiement,
} from '../../../entities/candidature';
import {
  EcranConfirmation,
  formaterDateCivile,
  StepAdmission,
  StepInformations,
  StepPaiement,
  StepPieces,
  StepProgress,
  StepRecapitulatif,
  useCandidatureStore,
  type EtapeCandidature,
} from '../../../features/candidature-form';
import { ApiError } from '../../../shared/api';
import { useT } from '../../../shared/i18n';

/** Étape du tunnel que le serveur autorise, d'après l'état du brouillon (le serveur est la source de vérité). */
function etapeAutorisee(brouillon: Brouillon): EtapeCandidature {
  if (brouillon.statut === STATUT_SOUMISE) return 6;
  if (brouillon.statut_paiement === STATUT_PAIEMENT_SIMULE) return 4;
  if (brouillon.deplacement_physique !== null) return 3;
  return 2;
}

/** Hors période (US-028) : on le dit avant que le candidat ne remplisse le formulaire, avec les dates. */
const EcranFerme: React.FC<{ calendrier: CalendrierPublic }> = ({ calendrier }) => {
  const t = useT();
  let detail = t('cand.fermeeSansDate');
  if (calendrier.etat === 'a_venir' && calendrier.date_ouverture) detail = t('cand.aVenir', { date: formaterDateCivile(calendrier.date_ouverture) });
  if (calendrier.etat === 'fermee' && calendrier.date_limite) detail = t('cand.fermee', { date: formaterDateCivile(calendrier.date_limite) });
  return (
    <section className="flex flex-col gap-4 items-start" role="status">
      <span className="w-12 h-12 rounded-full bg-fds-warn-bg text-fds-warn flex items-center justify-center" aria-hidden="true">
        <CalendarX className="w-6 h-6" />
      </span>
      <h1 className="font-fds-serif text-2xl font-bold text-fds-title">{t('cand.fermeeTitre')}</h1>
      <p>{detail}</p>
      <p className="text-sm text-fds-mute">{t('cand.fermeeSuivi')}</p>
      <div className="flex flex-col sm:flex-row gap-3 w-full">
        <Link to="/suivi" className="min-h-12 px-5 rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white font-semibold flex items-center justify-center">
          {t('accueil.suivre')}
        </Link>
        <Link to="/cursus/mpc" className="min-h-12 px-5 rounded-lg border-2 border-fds-accent text-fds-accent font-semibold flex items-center justify-center">
          {t('cand.voirDates')}
        </Link>
      </div>
    </section>
  );
};

/** Ordinateur : rappels à côté du formulaire (frais simulés, date limite, reprise, contact). */
const BonASavoir: React.FC<{ montantHtg: number; calendrier: CalendrierPublic | undefined }> = ({ montantHtg, calendrier }) => {
  const t = useT();
  return (
    <aside className="hidden lg:flex sticky top-4 rounded-xl border border-fds-line bg-fds-surface p-5 flex-col gap-4" aria-labelledby="bon-a-savoir">
      <h2 id="bon-a-savoir" className="font-fds-serif text-lg font-bold text-fds-title">
        {t('cand.aideTitre')}
      </h2>
      <div className="flex flex-col gap-2.5 text-sm">
        <div className="flex gap-3">
          <span className="flex-1 text-fds-mute">{t('cursus.frais')}</span>
          <span className="font-semibold">{montantHtg} HTG</span>
        </div>
        <div className="flex gap-3">
          <span className="flex-1 text-fds-mute">{t('cursus.dateLimite')}</span>
          <span className="font-semibold text-right">
            {calendrier?.date_limite ? formaterDateCivile(calendrier.date_limite) : t('cursus.aConfirmer')}
          </span>
        </div>
      </div>
      <p className="flex gap-2 items-start rounded-[10px] border border-fds-accent-line bg-fds-navy-t px-3 py-2.5 text-[13px]">
        <Info className="w-4 h-4 shrink-0 mt-0.5 text-fds-accent" aria-hidden="true" />
        {t('cursus.simulationNote')}
      </p>
      <p className="text-sm text-fds-mute">{t('cand.aideBrouillon')}</p>
      <p className="text-sm">
        {t('cand.aideQuestion')}{' '}
        <Link to="/contact" className="font-semibold text-fds-accent underline">
          {t('nav.contact')}
        </Link>
      </p>
    </aside>
  );
};

/**
 * Tunnel de candidature (maquettes) : 1 informations, 2 admission MPC + déplacement physique, 3 paiement simulé,
 * 4 dépôt des pièces, 5 récapitulatif, 6 confirmation avec la référence officielle (dossier soumis).
 */
export const ApplyPage: React.FC = () => {
  const t = useT();
  const {
    candidatureId,
    etape,
    informations,
    deplacementPhysique,
    montantHtg,
    paiement,
    soumission,
    methodePaiementChoisie,
    numeroPaiement,
    setInformations,
    appliquerBrouillon,
    setDeplacementPhysique,
    setSaisiePaiement,
    allerEtape,
    reinitialiser,
  } = useCandidatureStore();

  // Période de candidature (US-028). Un brouillon déjà commencé reste affiché : le serveur refusera sa soumission
  // après la date limite, avec un message clair au récapitulatif.
  const { data: calendrier } = useQuery({ queryKey: ['calendrier'], queryFn: calendrierApi.obtenir });
  const ferme = Boolean(calendrier) && !candidaturesAcceptees(calendrier?.etat) && !candidatureId && !soumission;

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
        // On ne ramène jamais en arrière quelqu'un qui était déjà au récapitulatif
        const autorisee = etapeAutorisee(brouillon);
        allerEtape(autorisee === 4 && etape === 5 ? 5 : autorisee);
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

  const soumettreDossier = async () => {
    if (!candidatureId) return;
    // Le serveur enregistre le dossier AVANT d'envoyer l'email : la référence est toujours renvoyée
    const brouillon = await candidatureApi.soumettre(candidatureId);
    appliquerBrouillon(brouillon);
    allerEtape(6);
  };

  // Garde-fous : on n'affiche jamais une étape dont les préalables ne sont pas remplis
  let etapeAffichee: EtapeCandidature = etape;
  if (etapeAffichee > 1 && !candidatureId) etapeAffichee = 1;
  if (etapeAffichee > 2 && deplacementPhysique === null) etapeAffichee = 2;
  if (etapeAffichee > 3 && !paiement) etapeAffichee = 3;
  if (etapeAffichee > 4 && etapeAffichee < 6 && !paiement) etapeAffichee = 3;
  if (soumission) etapeAffichee = 6; // un dossier soumis n'est plus modifiable : on ne montre que la confirmation
  if (etapeAffichee === 6 && !soumission) etapeAffichee = 5;

  return (
    <>
      {etapeAffichee !== 6 && !ferme && <StepProgress etape={Math.min(etapeAffichee, 4)} />}
      <div className="max-w-xl lg:max-w-5xl w-full mx-auto px-4 pt-6 lg:py-10 flex-1 flex flex-col lg:grid lg:grid-cols-[minmax(0,1fr)_300px] lg:gap-10 lg:items-start">
        <div className="flex-1 flex flex-col min-w-0 lg:rounded-xl lg:border lg:border-fds-line lg:bg-fds-surface lg:p-8">
        {reprise ? (
          <p className="text-fds-mute" role="status">
            {t('cand.reprise')}
          </p>
        ) : ferme ? (
          <EcranFerme calendrier={calendrier!} />
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
        ) : etapeAffichee === 4 ? (
          <StepPieces
            candidatureId={candidatureId!}
            referencePaiement={paiement?.reference ?? null}
            onRetour={() => allerEtape(3)}
            onContinuer={() => allerEtape(5)}
          />
        ) : etapeAffichee === 5 ? (
          <StepRecapitulatif
            candidatureId={candidatureId!}
            informations={informations}
            deplacementPhysique={deplacementPhysique}
            paiement={paiement}
            montantHtg={montantHtg}
            onRetour={() => allerEtape(4)}
            onSoumettre={soumettreDossier}
          />
        ) : (
          <EcranConfirmation
            prenom={informations.prenom}
            email={informations.email}
            reference={soumission!.reference}
            soumiseLe={soumission!.soumiseLe}
            montantHtg={montantHtg}
            referencePaiement={paiement?.reference ?? null}
            onNouvelleCandidature={reinitialiser}
          />
        )}
        </div>
        {etapeAffichee !== 6 && !ferme && <BonASavoir montantHtg={montantHtg} calendrier={calendrier} />}
      </div>
    </>
  );
};
