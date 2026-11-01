import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  BADGES_DOSSIER,
  dossierAdminApi,
  TAILLE_PAGE,
  type FiltresDossiers,
  type PageDossiers,
} from '../../../entities/dossier-admin';
import { useSessionStore } from '../../../entities/session';
import { formaterJourCourt } from '../../../features/candidature-form';

type Resultat = { cle: string; page: PageDossiers } | { cle: string; erreur: true };

const CLASSE_CHAMP =
  'w-full min-h-12 rounded-lg border-[1.5px] border-fds-field bg-white px-3 text-base text-fds-ink focus:outline-none focus:ring-2 focus:ring-fds-navy';

function pourcentage(partie: number, total: number): string {
  return total === 0 ? '–' : `${Math.round((partie / total) * 100)} %`;
}

const Indicateur: React.FC<{ libelle: string; valeur: string | number; aide?: string }> = ({ libelle, valeur, aide }) => (
  <div className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-1">
    <div className="text-sm text-fds-mute">{libelle}</div>
    <div className="font-fds-serif text-[32px] leading-tight font-bold text-fds-navy-d">{valeur}</div>
    {aide && <div className="text-xs text-fds-mute">{aide}</div>}
  </div>
);

/** Liste des dossiers soumis (maquette « Administration liste des dossiers »). */
export const AdminCandidaturesPage: React.FC = () => {
  const session = useSessionStore((s) => s.session);
  const [saisie, setSaisie] = useState('');
  const [filtres, setFiltres] = useState<FiltresDossiers>({ page: 1, q: '', statut: '', deplacement: '' });
  const [resultat, setResultat] = useState<Resultat | null>(null);
  const [rechargement, setRechargement] = useState(0);

  // La recherche part 300 ms après la dernière frappe
  useEffect(() => {
    const minuterie = window.setTimeout(() => setFiltres((f) => (f.q === saisie ? f : { ...f, q: saisie, page: 1 })), 300);
    return () => window.clearTimeout(minuterie);
  }, [saisie]);

  const cle = JSON.stringify([filtres, rechargement]);
  useEffect(() => {
    if (!session) return;
    let annule = false;
    dossierAdminApi
      .lister(session, filtres)
      .then((page) => {
        if (!annule) setResultat({ cle, page });
      })
      .catch(() => {
        if (!annule) setResultat({ cle, erreur: true });
      });
    return () => {
      annule = true;
    };
    // `cle` résume `filtres` et `rechargement`
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cle, session]);

  const enChargement = !resultat || resultat.cle !== cle;
  const page = resultat && 'page' in resultat ? resultat.page : null;
  const stats = page?.statistiques;
  const debut = page && page.total > 0 ? (page.page - 1) * TAILLE_PAGE + 1 : 0;
  const fin = page ? (page.page - 1) * TAILLE_PAGE + page.items.length : 0;
  const derniere = page ? Math.max(1, Math.ceil(page.total / TAILLE_PAGE)) : 1;

  return (
    <>
      <div className="flex flex-wrap items-baseline gap-2">
        <h1 className="font-fds-serif text-[28px] font-bold text-fds-navy-d flex-1">Candidatures</h1>
        <button type="button" onClick={() => setRechargement((n) => n + 1)} className="min-h-11 px-2 text-sm font-semibold text-fds-navy underline">
          Actualiser
        </button>
      </div>

      <div className="grid gap-4 grid-cols-[repeat(auto-fit,minmax(200px,1fr))]">
        <Indicateur libelle="Dossiers soumis" valeur={stats?.dossiers_soumis ?? '–'} />
        <Indicateur
          libelle="Sans déplacement physique"
          valeur={stats ? pourcentage(stats.sans_deplacement, stats.dossiers_soumis) : '–'}
          aide="Objectif : 70 % ou plus"
        />
        <Indicateur libelle="Pièces à examiner" valeur={stats?.pieces_a_examiner ?? '–'} />
        <Indicateur
          libelle="Pièces refusées"
          valeur={stats ? pourcentage(stats.pieces_refusees, stats.pieces_deposees) : '–'}
          aide="Seuil d'alerte : 20 %"
        />
      </div>

      <section className="rounded-xl border border-fds-line bg-white flex flex-col gap-4" aria-label="Liste des dossiers">
        <div className="flex flex-wrap gap-4 p-4 pb-0">
          <div className="flex flex-col gap-1.5 flex-[2_1_260px]">
            <label htmlFor="recherche" className="text-[15px] font-semibold">
              Rechercher
            </label>
            <input
              id="recherche"
              type="search"
              value={saisie}
              onChange={(e) => setSaisie(e.target.value)}
              placeholder="Référence ou nom du candidat"
              className={CLASSE_CHAMP}
            />
          </div>
          <div className="flex flex-col gap-1.5 flex-[1_1_180px]">
            <label htmlFor="filtre-statut" className="text-[15px] font-semibold">
              Statut
            </label>
            <select
              id="filtre-statut"
              value={filtres.statut}
              onChange={(e) => setFiltres({ ...filtres, statut: e.target.value as FiltresDossiers['statut'], page: 1 })}
              className={CLASSE_CHAMP}
            >
              <option value="">Tous</option>
              <option value="en_examen">À examiner</option>
              <option value="action_requise">Action du candidat</option>
              <option value="complet">Complet</option>
            </select>
          </div>
          <div className="flex flex-col gap-1.5 flex-[1_1_180px]">
            <label htmlFor="filtre-deplacement" className="text-[15px] font-semibold">
              Déplacement physique
            </label>
            <select
              id="filtre-deplacement"
              value={filtres.deplacement}
              onChange={(e) => setFiltres({ ...filtres, deplacement: e.target.value as FiltresDossiers['deplacement'], page: 1 })}
              className={CLASSE_CHAMP}
            >
              <option value="">Tous</option>
              <option value="non">Non</option>
              <option value="oui">Oui</option>
            </select>
          </div>
        </div>

        {resultat && 'erreur' in resultat && resultat.cle === cle && (
          <p role="alert" className="mx-4 rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
            Impossible de charger les dossiers. Vérifiez votre connexion puis cliquez sur « Actualiser ».
          </p>
        )}

        <div className="overflow-x-auto" aria-busy={enChargement}>
          <table className="w-full text-left text-[15px]">
            <thead>
              <tr className="border-y border-fds-line bg-[#f8fafd] text-sm text-fds-mute">
                <th className="px-4 py-3 font-semibold">Référence</th>
                <th className="px-4 py-3 font-semibold">Candidat</th>
                <th className="px-4 py-3 font-semibold">Déplacement</th>
                <th className="px-4 py-3 font-semibold">Pièces validées</th>
                <th className="px-4 py-3 font-semibold">Statut</th>
                <th className="px-4 py-3 font-semibold">Reçu le</th>
                <th className="px-4 py-3">
                  <span className="sr-only">Action</span>
                </th>
              </tr>
            </thead>
            <tbody>
              {page?.items.map((d) => {
                const badge = BADGES_DOSSIER[d.statut];
                return (
                  <tr key={d.reference_dossier} className="border-b border-fds-line last:border-b-0">
                    <td className="px-4 py-3 font-semibold whitespace-nowrap">{d.reference_dossier}</td>
                    <td className="px-4 py-3">
                      {d.nom} {d.prenom}
                    </td>
                    <td className="px-4 py-3">{d.deplacement_physique === null ? '–' : d.deplacement_physique ? 'Oui' : 'Non'}</td>
                    <td className="px-4 py-3 whitespace-nowrap">
                      {d.pieces_validees} / {d.pieces_total}
                    </td>
                    <td className="px-4 py-3">
                      <span className={`rounded-full px-2.5 py-0.5 text-[13px] font-semibold whitespace-nowrap ${badge.classe}`}>{badge.libelle}</span>
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap">{d.soumise_le ? formaterJourCourt(d.soumise_le) : '–'}</td>
                    <td className="px-4 py-3">
                      <Link
                        to={`/admin/candidatures/${d.reference_dossier}`}
                        className="min-h-10 px-4 rounded-lg border-2 border-fds-navy text-fds-navy font-semibold inline-flex items-center"
                      >
                        Ouvrir<span className="sr-only"> le dossier {d.reference_dossier}</span>
                      </Link>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          {!enChargement && page && page.items.length === 0 && (
            <p className="px-4 py-8 text-center text-fds-mute">
              {page.total === 0 && !filtres.q && !filtres.statut && !filtres.deplacement
                ? 'Aucun dossier soumis pour le moment.'
                : 'Aucun dossier ne correspond à ces critères.'}
            </p>
          )}
          {enChargement && !page && (
            <p className="px-4 py-8 text-center text-fds-mute" role="status">
              Chargement des dossiers…
            </p>
          )}
        </div>

        <div className="flex flex-wrap items-center gap-2 px-4 pb-4">
          <span className="flex-1 text-sm text-fds-mute" aria-live="polite">
            {page ? `Dossiers ${debut} à ${fin} sur ${page.total}` : ''}
          </span>
          <button
            type="button"
            disabled={!page || page.page <= 1}
            onClick={() => setFiltres({ ...filtres, page: filtres.page - 1 })}
            className="min-h-11 px-4 rounded-lg border-2 border-fds-navy bg-white text-fds-navy font-semibold disabled:opacity-40"
          >
            Précédent
          </button>
          <button
            type="button"
            disabled={!page || page.page >= derniere}
            onClick={() => setFiltres({ ...filtres, page: filtres.page + 1 })}
            className="min-h-11 px-4 rounded-lg border-2 border-fds-navy bg-white text-fds-navy font-semibold disabled:opacity-40"
          >
            Suivant
          </button>
        </div>
      </section>
    </>
  );
};
