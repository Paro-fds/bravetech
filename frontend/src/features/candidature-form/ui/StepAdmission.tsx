import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, ArrowRight } from 'lucide-react';

interface StepAdmissionProps {
  deplacementPhysique: boolean | null;
  onChange: (valeur: boolean) => void;
  /** Envoie la réponse au serveur ; rejette en cas d'erreur. */
  onSoumettre: (valeur: boolean) => Promise<void>;
  onRetour: () => void;
}

const OPTIONS: { valeur: boolean; libelle: string }[] = [
  { valeur: false, libelle: 'Non, tout a été fait en ligne' },
  { valeur: true, libelle: "Oui, j'ai dû me déplacer" },
];

/** Étape 2 : rappel de l'admission unique au MPC et question obligatoire sur le déplacement physique. */
export const StepAdmission: React.FC<StepAdmissionProps> = ({ deplacementPhysique, onChange, onSoumettre, onRetour }) => {
  const [erreur, setErreur] = useState<string | null>(null);
  const [enCours, setEnCours] = useState(false);

  const soumettre = async (e: React.FormEvent) => {
    e.preventDefault();
    if (deplacementPhysique === null) {
      setErreur('Merci de répondre à cette question pour continuer.');
      return;
    }
    setErreur(null);
    setEnCours(true);
    try {
      await onSoumettre(deplacementPhysique);
    } catch {
      setErreur("Impossible d'enregistrer votre réponse pour le moment. Vérifiez votre connexion et réessayez.");
    } finally {
      setEnCours(false);
    }
  };

  return (
    <form onSubmit={soumettre} noValidate className="flex flex-col gap-6">
      <section className="flex flex-col gap-3">
        <h1 className="text-2xl font-extrabold text-slate-900">Votre admission</h1>
        <div className="rounded-2xl border-2 border-blue-700 bg-blue-50 p-4 flex flex-col gap-2">
          <span className="self-start text-[11px] font-bold uppercase tracking-wide bg-emerald-100 text-emerald-800 px-2.5 py-0.5 rounded-full">
            Admission unique
          </span>
          <h2 className="text-lg font-bold text-slate-900">Premier cycle MPC</h2>
          <p className="text-sm text-slate-700">
            Vous candidatez à l'entrée de la Faculté. Après 2 ans de MPC, vous choisirez votre branche : Génie Civil,
            Génie Électromécanique, Génie Électronique ou Architecture.
          </p>
        </div>
        <Link to="/cursus/mpc" className="text-sm font-semibold text-blue-700 underline min-h-11 inline-flex items-center">
          Voir la fiche MPC et le parcours en 5 ans
        </Link>
      </section>

      <fieldset className="flex flex-col gap-3" aria-describedby={erreur ? 'erreur-deplacement' : undefined}>
        <legend className="text-lg font-bold text-slate-900 mb-1">Un dernier point</legend>
        <p className="text-sm text-slate-600">
          Cette question nous aide à améliorer le service. Elle n'a aucun effet sur l'examen de votre dossier.{' '}
          <strong className="text-slate-900">Réponse obligatoire.</strong>
        </p>
        <p className="font-semibold text-slate-900">
          Avez-vous dû vous déplacer physiquement pour obtenir des informations ou préparer ce dossier ?
        </p>
        {OPTIONS.map((option) => {
          const choisi = deplacementPhysique === option.valeur;
          return (
            <label
              key={String(option.valeur)}
              className={`flex items-center gap-3 rounded-xl border-2 p-3.5 min-h-12 cursor-pointer ${
                choisi ? 'border-blue-700 bg-blue-50' : 'border-slate-300 bg-white'
              }`}
            >
              <input
                type="radio"
                name="deplacement_physique"
                className="w-5 h-5 accent-blue-700"
                checked={choisi}
                onChange={() => {
                  onChange(option.valeur);
                  setErreur(null);
                }}
              />
              <span className="font-medium text-slate-900">{option.libelle}</span>
            </label>
          );
        })}
        {erreur && (
          <p id="erreur-deplacement" role="alert" className="text-sm font-medium text-rose-700">
            {erreur}
          </p>
        )}
      </fieldset>

      <div className="flex gap-3">
        <button
          type="button"
          onClick={onRetour}
          className="min-h-12 px-4 rounded-xl border-2 border-blue-700 text-blue-700 font-bold flex items-center gap-2"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Retour</span>
        </button>
        <button
          type="submit"
          disabled={enCours}
          className="flex-1 min-h-12 rounded-xl bg-blue-700 hover:bg-blue-600 disabled:opacity-60 text-white font-bold flex items-center justify-center gap-2 transition-colors"
        >
          <span>{enCours ? 'Enregistrement…' : 'Continuer'}</span>
          {!enCours && <ArrowRight className="w-4 h-4" />}
        </button>
      </div>
    </form>
  );
};
