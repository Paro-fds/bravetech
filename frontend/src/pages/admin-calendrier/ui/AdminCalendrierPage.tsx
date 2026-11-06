import React, { useEffect, useState } from 'react';
import { CalendarCheck, Check, TriangleAlert } from 'lucide-react';
import {
  calendrierApi,
  CHAMPS_DATES,
  type CalendrierAdmin,
  type DatesCalendrier,
  type EtatPeriode,
} from '../../../entities/calendrier';
import { useSessionStore } from '../../../entities/session';
import { formaterDateCivile, formaterHorodatage } from '../../../features/candidature-form';
import { ApiError } from '../../../shared/api';

// L'administration reste en français (spec WS-01 §1.6) : libellés fixes, sans traduction
const CHAMPS: Record<keyof DatesCalendrier, { libelle: string; aide: string; obligatoire?: boolean }> = {
  date_ouverture: { libelle: 'Ouverture des candidatures', aide: 'Premier jour où le formulaire est ouvert.', obligatoire: true },
  date_limite: { libelle: 'Date limite de dépôt', aide: 'Dernier jour inclus (jusqu’à 23 h 59, heure d’Haïti).', obligatoire: true },
  date_concours: { libelle: 'Concours d’admission', aide: 'Facultatif : « À confirmer » sur le site tant qu’il est vide.' },
  date_resultats: { libelle: 'Publication des résultats', aide: 'Facultatif.' },
  date_rentree: { libelle: 'Rentrée', aide: 'Facultatif.' },
};

const ETATS: Record<EtatPeriode, { libelle: string; classe: string }> = {
  non_definie: { libelle: 'Aucun calendrier : candidatures ouvertes', classe: 'bg-fds-warn-bg text-fds-warn' },
  a_venir: { libelle: 'Candidatures pas encore ouvertes', classe: 'bg-fds-navy-t text-fds-accent' },
  ouverte: { libelle: 'Candidatures ouvertes', classe: 'bg-fds-ok-bg text-fds-ok' },
  fermee: { libelle: 'Candidatures fermées', classe: 'bg-fds-bad-bg text-fds-bad' },
};

const VIDE: DatesCalendrier = { date_ouverture: null, date_limite: null, date_concours: null, date_resultats: null, date_rentree: null };

const CLASSE_CHAMP =
  'w-full min-h-12 rounded-lg border-[1.5px] bg-fds-surface px-3 text-base text-fds-ink focus:outline-none focus:ring-2 focus:ring-fds-accent disabled:opacity-70';

function extraireErreurs(erreur: unknown): Partial<Record<keyof DatesCalendrier, string>> | null {
  if (!(erreur instanceof ApiError) || erreur.status !== 422) return null;
  return (erreur.body as { detail?: { erreurs?: Partial<Record<keyof DatesCalendrier, string>> } } | null)?.detail?.erreurs ?? null;
}

/** Calendrier d'admission (US-028) : l'admin règle les dates, le site public et le formulaire suivent sans redéploiement. */
export const AdminCalendrierPage: React.FC = () => {
  const session = useSessionStore((s) => s.session);
  const peutModifier = session?.role === 'admin';

  const [calendrier, setCalendrier] = useState<CalendrierAdmin | null>(null);
  const [saisie, setSaisie] = useState<DatesCalendrier>(VIDE);
  const [erreurs, setErreurs] = useState<Partial<Record<keyof DatesCalendrier, string>>>({});
  const [message, setMessage] = useState<{ type: 'ok' | 'erreur'; texte: string } | null>(null);
  const [enCours, setEnCours] = useState(false);
  const [echecChargement, setEchecChargement] = useState(false);

  const appliquer = (reponse: CalendrierAdmin) => {
    setCalendrier(reponse);
    setSaisie(Object.fromEntries(CHAMPS_DATES.map((c) => [c, reponse[c]])) as unknown as DatesCalendrier);
  };

  useEffect(() => {
    if (!session) return;
    let annule = false;
    calendrierApi
      .obtenirAdmin(session)
      .then((reponse) => {
        if (!annule) appliquer(reponse);
      })
      .catch(() => {
        if (!annule) setEchecChargement(true);
      });
    return () => {
      annule = true;
    };
  }, [session]);

  const enregistrer = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!session) return;
    setErreurs({});
    setMessage(null);
    setEnCours(true);
    try {
      appliquer(await calendrierApi.modifier(session, saisie));
      setMessage({ type: 'ok', texte: 'Calendrier enregistré. Le site public affiche déjà les nouvelles dates.' });
    } catch (erreur) {
      const parChamp = extraireErreurs(erreur);
      if (parChamp) {
        setErreurs(parChamp);
        setMessage({ type: 'erreur', texte: 'Corrigez les dates signalées.' });
      } else if (erreur instanceof ApiError && erreur.status === 403) {
        setMessage({ type: 'erreur', texte: 'Seul un administrateur peut modifier le calendrier.' });
      } else {
        setMessage({ type: 'erreur', texte: 'Enregistrement impossible. Vérifiez la connexion puis réessayez.' });
      }
    } finally {
      setEnCours(false);
    }
  };

  if (echecChargement) {
    return (
      <p role="alert" className="text-fds-bad">
        Le calendrier n’a pas pu être chargé. Rechargez la page.
      </p>
    );
  }
  if (!calendrier) {
    return (
      <p role="status" className="text-fds-mute">
        Chargement du calendrier…
      </p>
    );
  }

  const etat = ETATS[calendrier.etat];

  return (
    <div className="max-w-3xl w-full flex flex-col gap-6">
      <section className="flex flex-col gap-2">
        <h1 className="font-fds-serif text-[28px] font-bold text-fds-title">Calendrier d’admission</h1>
        <p className="text-fds-mute">
          Ces dates s’affichent sur la fiche MPC. Le formulaire de candidature n’est ouvert qu’entre l’ouverture et la date limite ;
          après la date limite, les candidats peuvent toujours suivre leur dossier et remplacer une pièce refusée.
        </p>
        <div className="flex flex-wrap items-center gap-3 text-sm">
          <span className={`rounded-full px-2.5 py-0.5 font-semibold ${etat.classe}`}>{etat.libelle}</span>
          {calendrier.modifie_le && (
            <span className="text-fds-mute">
              Dernière modification : {formaterHorodatage(calendrier.modifie_le)}
              {calendrier.modifie_par && <> par <b className="text-fds-ink">{calendrier.modifie_par}</b></>}
            </span>
          )}
        </div>
      </section>

      {!peutModifier && (
        <p className="flex gap-2.5 items-start rounded-[10px] border border-fds-accent-line bg-fds-navy-t px-3.5 py-3 text-sm">
          <TriangleAlert className="w-5 h-5 shrink-0 text-fds-accent" aria-hidden="true" />
          Votre compte agent peut consulter le calendrier. Seul un administrateur peut le modifier.
        </p>
      )}

      <form onSubmit={enregistrer} noValidate className="rounded-xl border border-fds-line bg-fds-surface p-4 sm:p-6 flex flex-col gap-5">
        <div className="grid gap-5 sm:grid-cols-2">
          {CHAMPS_DATES.map((champ) => {
            const { libelle, aide, obligatoire } = CHAMPS[champ];
            const erreur = erreurs[champ];
            return (
              <div key={champ} className="flex flex-col gap-1.5">
                <label htmlFor={champ} className="text-[15px] font-semibold">
                  {libelle}
                  {obligatoire && <span className="text-fds-bad"> *</span>}
                </label>
                <input
                  id={champ}
                  type="date"
                  value={saisie[champ] ?? ''}
                  onChange={(e) => {
                    setSaisie((prec) => ({ ...prec, [champ]: e.target.value || null }));
                    if (erreur) setErreurs((prec) => ({ ...prec, [champ]: undefined }));
                  }}
                  disabled={!peutModifier || enCours}
                  required={obligatoire}
                  aria-invalid={Boolean(erreur)}
                  aria-describedby={`${champ}-aide`}
                  className={`${CLASSE_CHAMP} ${erreur ? 'border-fds-bad' : 'border-fds-field'}`}
                />
                <p id={`${champ}-aide`} role={erreur ? 'alert' : undefined} className={`text-[13px] ${erreur ? 'font-semibold text-fds-bad' : 'text-fds-mute'}`}>
                  {erreur ?? (saisie[champ] ? `${formaterDateCivile(saisie[champ]!)} — ${aide}` : aide)}
                </p>
              </div>
            );
          })}
        </div>

        {message && (
          <div
            role={message.type === 'erreur' ? 'alert' : 'status'}
            className={`flex gap-2.5 items-start rounded-[10px] border px-3.5 py-3 text-sm ${
              message.type === 'ok' ? 'border-fds-ok-line bg-fds-ok-bg text-fds-ok' : 'border-fds-bad-line bg-fds-bad-bg text-fds-bad'
            }`}
          >
            {message.type === 'ok' ? <Check className="w-5 h-5 shrink-0" aria-hidden="true" /> : <TriangleAlert className="w-5 h-5 shrink-0" aria-hidden="true" />}
            <span>{message.texte}</span>
          </div>
        )}

        {peutModifier && (
          <button
            type="submit"
            disabled={enCours}
            className="min-h-12 px-6 self-start rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white font-semibold flex items-center justify-center gap-2 transition-colors disabled:opacity-70"
          >
            <CalendarCheck className="w-5 h-5" aria-hidden="true" />
            {enCours ? 'Enregistrement…' : 'Enregistrer le calendrier'}
          </button>
        )}
      </form>
    </div>
  );
};
