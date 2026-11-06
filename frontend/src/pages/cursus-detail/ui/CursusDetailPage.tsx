import React, { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ArrowLeft, ChevronDown, FileText, Info, Plus, Check } from 'lucide-react';
import { calendrierApi, candidaturesAcceptees } from '../../../entities/calendrier';
import { cursusApi, IllustrationCursus, trierBranches, type MatiereItem } from '../../../entities/cursus';
import { FRAIS_DOSSIER_PAR_DEFAUT, formaterDateCivile } from '../../../features/candidature-form';
import { useNomPiece, useT } from '../../../shared/i18n';

/** « 120 h + 60 h TP », ou « 90 h » selon les volumes renseignés (programme replié, mobile). */
function formaterHeures(m: MatiereItem): string {
  if (m.heures_theorie != null || m.heures_tp != null) {
    return [m.heures_theorie != null ? `${m.heures_theorie} h` : null, m.heures_tp != null ? `${m.heures_tp} h TP` : null]
      .filter(Boolean)
      .join(' + ');
  }
  return m.heures ? `${m.heures} h` : '';
}

/** Colonnes Cours / TP du tableau de programme (bureau) ; « - » quand le volume n'est pas renseigné. */
function heuresCours(m: MatiereItem): string {
  const h = m.heures_theorie ?? (m.heures_tp == null ? m.heures : null);
  return h != null ? `${h} h` : '-';
}
const heuresTp = (m: MatiereItem) => (m.heures_tp != null ? `${m.heures_tp} h` : '-');

/** « MPC1 » → « MPC 1 » : le nom du niveau vient des données, sans espace. */
const formaterNiveau = (nom: string) => nom.replace(/^([A-Za-z]+)(\d+)$/, '$1 $2');

const BRANCHES = ['Génie Civil', 'Génie Électromécanique', 'Génie Électronique', 'Architecture'];

const TITRE_SECTION = 'font-fds-serif text-xl lg:text-3xl font-bold text-fds-title';
const PASTILLE = 'rounded-full bg-fds-navy-t text-fds-accent px-2.5 py-0.5 text-[13px] font-semibold';

const Ligne: React.FC<{ libelle: string; valeur: string }> = ({ libelle, valeur }) => (
  <div className="flex gap-3 text-sm">
    <span className="flex-1 text-fds-mute">{libelle}</span>
    <span className="font-semibold text-right">{valeur}</span>
  </div>
);

/**
 * Fiche d'un cursus (maquettes « Cursus » mobile et bureau). Le MPC est le cursus d'admission ; les branches viennent après.
 * Sur ordinateur (≥ 1024 px) : bandeau marine illustré, colonne fixe « Candidater à l'admission », programme en tableaux,
 * cartes des branches. Sur mobile : infos clés en grille, programme dépliable, barre fixe « Déposer ma candidature ».
 */
export const CursusDetailPage: React.FC = () => {
  const t = useT();
  const nomPiece = useNomPiece();
  const { id } = useParams<{ id: string }>();
  const [ouverts, setOuverts] = useState<Record<string, boolean>>({});

  const { data: cursus, isLoading, isError } = useQuery({
    queryKey: ['cursus', id],
    queryFn: () => cursusApi.getById(id || ''),
    enabled: Boolean(id),
  });
  // Cartes « Après le MPC » : même requête que l'accueil (souvent déjà en cache)
  const { data: liste = [] } = useQuery({ queryKey: ['cursus'], queryFn: cursusApi.getList, enabled: Boolean(cursus?.est_admission) });
  // Dates réglées par l'administration (US-028) ; une date absente reste « À confirmer »
  const { data: calendrier } = useQuery({ queryKey: ['calendrier'], queryFn: calendrierApi.obtenir, enabled: Boolean(cursus?.est_admission) });
  const dateOu = (iso: string | null | undefined) => (iso ? formaterDateCivile(iso) : t('cursus.aConfirmer'));
  const ouvertes = candidaturesAcceptees(calendrier?.etat);

  const retour = (
    <Link to="/" className="self-start flex items-center gap-2 min-h-11 font-semibold text-fds-accent lg:text-white">
      <ArrowLeft className="w-5 h-5" aria-hidden="true" />
      {t('nav.accueil')}
    </Link>
  );

  if (isLoading) {
    return (
      <div className="max-w-5xl w-full mx-auto px-4 py-6">
        <p className="text-fds-mute" role="status">
          {t('cursus.chargement')}
        </p>
      </div>
    );
  }

  if (isError || !cursus) {
    return (
      <div className="max-w-5xl w-full mx-auto px-4 py-6 flex flex-col gap-4">
        <Link to="/" className="self-start flex items-center gap-2 min-h-11 font-semibold text-fds-accent">
          <ArrowLeft className="w-5 h-5" aria-hidden="true" />
          {t('nav.accueil')}
        </Link>
        <h1 className="font-fds-serif text-2xl font-bold text-fds-title">{t('cursus.introuvableTitre')}</h1>
        <p className="text-fds-mute">{t('cursus.introuvableTexte')}</p>
      </div>
    );
  }

  const niveaux = Object.entries(cursus.niveaux ?? {});
  const admission = cursus.est_admission;
  const branches = trierBranches(liste.filter((c) => !c.est_admission));

  return (
    <>
      <section className="lg:bg-fds-navy lg:text-white">
        <div className="max-w-5xl mx-auto px-4 pt-6 lg:pt-7 lg:pb-10 flex flex-col gap-4">
          {retour}
          <div className="flex items-center gap-8">
            <div className="flex-1 min-w-0 flex flex-col gap-2.5">
              <div className="flex flex-wrap gap-2">
                <span className={`${PASTILLE} lg:bg-white/15 lg:text-white`}>{admission ? t('cursus.badgeAdmission') : t('cursus.badgeBranche')}</span>
                {admission && cursus.est_ouvert && ouvertes && (
                  <span className="rounded-full bg-fds-ok-bg text-fds-ok px-2.5 py-0.5 text-[13px] font-semibold">{t('accueil.badge')}</span>
                )}
              </div>
              <h1 lang="fr" className="font-fds-serif text-[28px] md:text-4xl lg:text-[40px] leading-tight font-bold text-fds-title lg:text-white">
                {cursus.nom}
              </h1>
              <p lang="fr" className="text-fds-mute lg:text-fds-on-navy md:text-lg max-w-3xl">
                {cursus.description_longue || cursus.description_courte}
              </p>
            </div>
            <IllustrationCursus id={cursus.id} className="hidden lg:block lg:w-96 shrink-0 rounded-xl" />
          </div>
        </div>
      </section>

      <div className="max-w-5xl w-full mx-auto px-4 py-6 lg:py-10 flex-1 grid gap-6 lg:gap-10 lg:grid-cols-[minmax(0,1fr)_300px] items-start">
        <div className="flex flex-col gap-6 lg:gap-11 min-w-0">
          <section
            className={`rounded-xl border border-fds-line bg-fds-surface p-4 grid grid-cols-2 md:grid-cols-4 gap-4 ${admission ? 'lg:hidden' : ''}`}
            aria-label={t('cursus.infosCles')}
          >
            <div>
              <div className="text-xs text-fds-mute">{admission ? t('cursus.dureeMpc') : t('cursus.duree')}</div>
              <div className="font-semibold">{t('carte.ans', { n: cursus.duree_annees })}</div>
            </div>
            {admission ? (
              <>
                <div>
                  <div className="text-xs text-fds-mute">{t('cursus.frais')}</div>
                  <div className="font-semibold">{FRAIS_DOSSIER_PAR_DEFAUT} HTG</div>
                </div>
                <div>
                  <div className="text-xs text-fds-mute">{t('cursus.dateLimite')}</div>
                  <div className="font-semibold">{dateOu(calendrier?.date_limite)}</div>
                </div>
                <div>
                  <div className="text-xs text-fds-mute">{t('cursus.rentree')}</div>
                  <div className="font-semibold">{dateOu(calendrier?.date_rentree)}</div>
                </div>
              </>
            ) : (
              <div>
                <div className="text-xs text-fds-mute">{t('cursus.acces')}</div>
                <div className="font-semibold">{t('cursus.apresMpc')}</div>
              </div>
            )}
          </section>

          {admission && (
            <section className="lg:hidden rounded-xl border border-fds-line bg-fds-surface p-4 flex flex-col gap-2.5" aria-labelledby="dates-cles">
              <h2 id="dates-cles" className="font-fds-serif text-lg font-bold text-fds-title">
                {t('cursus.datesCles')}
              </h2>
              <Ligne libelle={t('cursus.ouverture')} valeur={dateOu(calendrier?.date_ouverture)} />
              <Ligne libelle={t('cursus.dateLimite')} valeur={dateOu(calendrier?.date_limite)} />
              <Ligne libelle={t('cursus.concours')} valeur={dateOu(calendrier?.date_concours)} />
              <Ligne libelle={t('cursus.resultats')} valeur={dateOu(calendrier?.date_resultats)} />
              <Ligne libelle={t('cursus.rentree')} valeur={dateOu(calendrier?.date_rentree)} />
              {!ouvertes && <p className="text-sm font-semibold text-fds-bad">{t('cursus.fermees')}</p>}
            </section>
          )}

          {admission && (
            <section className="flex flex-col gap-3 lg:gap-4" aria-labelledby="parcours">
              <h2 id="parcours" className={TITRE_SECTION}>
                {t('cursus.parcoursTitre')}
              </h2>
              {/* Mobile : frise verticale (maquette « Cursus ») */}
              <ol className="md:hidden rounded-xl border border-fds-line bg-fds-surface p-4 flex flex-col gap-4">
                <li className="flex gap-3 items-start">
                  <span className="w-7 h-7 rounded-full bg-fds-navy text-white flex items-center justify-center shrink-0" aria-hidden="true">
                    <Check className="w-4 h-4" strokeWidth={3} />
                  </span>
                  <div>
                    <div className="font-semibold">{t('cursus.parcours12Titre')}</div>
                    <div className="text-sm text-fds-mute">{t('cursus.parcours12Texte')}</div>
                  </div>
                </li>
                <li className="flex gap-3 items-start">
                  <span className="w-7 h-7 rounded-full border-2 border-fds-line bg-fds-surface text-fds-mute flex items-center justify-center shrink-0" aria-hidden="true">
                    <Plus className="w-4 h-4" />
                  </span>
                  <div className="flex flex-col gap-2">
                    <div className="font-semibold">{t('cursus.parcours35Titre')}</div>
                    <div className="text-sm text-fds-mute">{t('cursus.parcours35Texte')}</div>
                    <div className="flex flex-wrap gap-1.5">
                      {BRANCHES.map((b) => (
                        <span key={b} lang="fr" className={PASTILLE}>
                          {b}
                        </span>
                      ))}
                    </div>
                  </div>
                </li>
              </ol>
              {/* Bureau : deux cartes côte à côte (maquette « Cursus » bureau) */}
              <ol className="hidden md:flex gap-4 items-stretch">
                <li className="flex-[1_1_220px] rounded-xl border-2 border-fds-accent bg-fds-navy-t p-4 flex flex-col gap-2">
                  <span className="self-start rounded-full bg-fds-ok-bg text-fds-ok px-2.5 py-0.5 text-[13px] font-semibold">{t('carte.candidatezIci')}</span>
                  <h3 className="font-fds-serif text-lg font-bold text-fds-title">{t('cursus.parcours12Titre')}</h3>
                  <p className="text-sm text-fds-mute">{t('cursus.parcours12Texte')}</p>
                </li>
                <li className="flex-[2_1_360px] rounded-xl border border-fds-line bg-fds-surface p-4 flex flex-col gap-2">
                  <span className={`self-start ${PASTILLE}`}>{t('cursus.ensuiteChoix')}</span>
                  <h3 className="font-fds-serif text-lg font-bold text-fds-title">{t('cursus.parcours35Titre')}</h3>
                  <p className="text-sm text-fds-mute">{t('cursus.parcours35Texte')}</p>
                  <div className="flex flex-wrap gap-1.5">
                    {BRANCHES.map((b) => (
                      <span key={b} lang="fr" className={PASTILLE}>
                        {b}
                      </span>
                    ))}
                  </div>
                </li>
              </ol>
            </section>
          )}

          {niveaux.length > 0 && (
            <section className="flex flex-col gap-3 lg:gap-4" aria-labelledby="programme">
              <h2 id="programme" className={TITRE_SECTION}>
                {admission ? t('cursus.programmeMpc') : t('cursus.programme')}
              </h2>
              {/* Mobile : niveaux dépliables */}
              <div className="lg:hidden flex flex-col gap-3">
                {niveaux.map(([nom, matieres], index) => {
                  const ouvert = ouverts[nom] ?? index === 0; // le premier niveau est déplié par défaut
                  return (
                    <div key={nom} className="rounded-xl border border-fds-line bg-fds-surface">
                      <button
                        type="button"
                        aria-expanded={ouvert}
                        onClick={() => setOuverts({ ...ouverts, [nom]: !ouvert })}
                        className="w-full min-h-14 px-4 flex items-center gap-2 text-left"
                      >
                        <h3 className="flex-1 font-fds-serif text-lg font-bold text-fds-title">{formaterNiveau(nom)}</h3>
                        <span className={PASTILLE}>{t('cursus.matieres', { n: matieres.length })}</span>
                        <ChevronDown className={`w-5 h-5 transition-transform ${ouvert ? 'rotate-180' : ''}`} aria-hidden="true" />
                      </button>
                      {ouvert && (
                        <ul className="px-4 pb-3 border-t border-fds-line">
                          {matieres.map((m, i) => (
                            <li key={`${m.item}-${i}`} className="flex gap-3 py-2 text-sm border-b border-fds-line last:border-b-0">
                              <span lang="fr" className="flex-1">{m.titre}</span>
                              <span className="text-fds-mute whitespace-nowrap">{formaterHeures(m)}</span>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  );
                })}
              </div>
              {/* Bureau : un tableau par niveau, côte à côte */}
              <div className="hidden lg:grid grid-cols-2 gap-4 items-start">
                {niveaux.map(([nom, matieres]) => (
                  <div key={nom} className="rounded-xl border border-fds-line bg-fds-surface overflow-hidden">
                    <div className="flex items-center gap-2 px-4 pt-4 pb-2">
                      <h3 className="flex-1 font-fds-serif text-lg font-bold text-fds-title">{formaterNiveau(nom)}</h3>
                      <span className={PASTILLE}>{t('cursus.matieres', { n: matieres.length })}</span>
                    </div>
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="bg-fds-surface-alt border-b border-fds-line text-[13px] text-fds-mute text-left">
                          <th scope="col" className="font-semibold px-4 py-2">{t('cursus.colMatiere')}</th>
                          <th scope="col" className="font-semibold px-2 py-2 whitespace-nowrap">{t('cursus.colCours')}</th>
                          <th scope="col" className="font-semibold pl-2 pr-4 py-2 whitespace-nowrap">{t('cursus.colTp')}</th>
                        </tr>
                      </thead>
                      <tbody>
                        {matieres.map((m, i) => (
                          <tr key={`${m.item}-${i}`} className="border-b border-fds-line last:border-b-0">
                            <td lang="fr" className="px-4 py-2.5">{m.titre}</td>
                            <td className="px-2 py-2.5 whitespace-nowrap">{heuresCours(m)}</td>
                            <td className="pl-2 pr-4 py-2.5 whitespace-nowrap text-fds-mute">{heuresTp(m)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ))}
              </div>
            </section>
          )}

          {admission && branches.length > 0 && (
            <section className="hidden lg:flex flex-col gap-4" aria-labelledby="apres-mpc">
              <h2 id="apres-mpc" className={TITRE_SECTION}>
                {t('cursus.apresMpcTitre')}
              </h2>
              <div className="grid grid-cols-2 gap-4">
                {branches.map((b) => (
                  <Link
                    key={b.id}
                    to={`/cursus/${b.id}`}
                    className="rounded-xl border border-fds-line bg-fds-surface overflow-hidden no-underline text-inherit hover:shadow-md transition-shadow"
                  >
                    <IllustrationCursus id={b.id} />
                    <div className="p-3.5 flex flex-col gap-1">
                      <h3 lang="fr" className="font-fds-serif text-lg font-bold text-fds-title">{b.nom}</h3>
                      <p className="text-sm text-fds-mute">
                        {t('carte.ans', { n: b.duree_annees })}. <span lang="fr">{b.description_courte}</span>
                      </p>
                    </div>
                  </Link>
                ))}
              </div>
              <p className="text-sm text-fds-mute">{t('cursus.apresMpcNote')}</p>
            </section>
          )}

          {admission && (
            <section className="flex flex-col gap-3 lg:gap-4" aria-labelledby="pieces">
              <h2 id="pieces" className={TITRE_SECTION}>
                {t('cursus.piecesTitre')}
              </h2>
              <ul className="rounded-xl border border-fds-line bg-fds-surface px-4 md:px-5 md:py-2 grid md:grid-cols-2 md:gap-x-8">
                {cursus.documents_requis?.map((doc) => (
                  <li key={doc.id} className="flex gap-3 items-center py-2.5 md:py-3 border-b border-fds-line last:border-b-0">
                    <FileText className="w-5 h-5 shrink-0 text-fds-accent" aria-hidden="true" />
                    <span className="flex-1">{nomPiece(doc.id, doc.nom)}</span>
                  </li>
                ))}
              </ul>
              <p className="text-xs md:text-sm text-fds-mute">{t('cursus.piecesNote')}</p>
            </section>
          )}
        </div>

        {admission ? (
          <aside className="hidden lg:flex sticky top-4 rounded-xl border border-fds-line bg-fds-surface p-4 flex-col gap-4" aria-labelledby="candidater">
            <h2 id="candidater" className="font-fds-serif text-lg font-bold text-fds-title">
              {t('cursus.candidaterTitre')}
            </h2>
            <div className="flex flex-col gap-2.5">
              <Ligne libelle={t('cursus.dureeMpc')} valeur={t('carte.ans', { n: cursus.duree_annees })} />
              <Ligne libelle={t('cursus.dureeTotale')} valeur={t('carte.ans', { n: 5 })} />
              <Ligne libelle={t('cursus.frais')} valeur={`${FRAIS_DOSSIER_PAR_DEFAUT} HTG`} />
            </div>
            <div className="flex flex-col gap-2.5 border-t border-fds-line pt-3">
              <h3 className="text-sm font-semibold">{t('cursus.datesCles')}</h3>
              <Ligne libelle={t('cursus.ouverture')} valeur={dateOu(calendrier?.date_ouverture)} />
              <Ligne libelle={t('cursus.dateLimite')} valeur={dateOu(calendrier?.date_limite)} />
              <Ligne libelle={t('cursus.concours')} valeur={dateOu(calendrier?.date_concours)} />
              <Ligne libelle={t('cursus.resultats')} valeur={dateOu(calendrier?.date_resultats)} />
              <Ligne libelle={t('cursus.rentree')} valeur={dateOu(calendrier?.date_rentree)} />
            </div>
            {!ouvertes && <p className="text-sm font-semibold text-fds-bad">{t('cursus.fermees')}</p>}
            <Link to="/postuler" className="min-h-12 px-4 rounded-lg bg-fds-gold text-fds-on-light font-semibold flex items-center justify-center hover:brightness-95">
              {t('cursus.deposer')}
            </Link>
            <p className="text-[13px] text-fds-mute text-center">{t('cursus.sansDeplacement')}</p>
            <p className="flex gap-2 items-start rounded-[10px] border border-fds-accent-line bg-fds-navy-t px-3 py-2.5 text-[13px]">
              <Info className="w-4 h-4 shrink-0 mt-0.5 text-fds-accent" aria-hidden="true" />
              {t('cursus.simulationNote')}
            </p>
          </aside>
        ) : (
          <aside className="lg:sticky lg:top-4 rounded-xl border border-fds-line bg-fds-surface p-4 flex flex-col gap-3">
            <h2 className="font-fds-serif text-lg font-bold text-fds-title">{t('cursus.brancheTitre')}</h2>
            <p className="text-sm text-fds-mute">{t('cursus.brancheTexte')}</p>
            <Link to="/cursus/mpc" className="min-h-12 px-4 rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white font-semibold flex items-center justify-center">
              {t('cursus.voirMpc')}
            </Link>
          </aside>
        )}
      </div>

      {admission && (
        <div className="lg:hidden sticky bottom-0 bg-fds-surface border-t border-fds-line px-4 py-3">
          <div className="max-w-5xl mx-auto flex flex-col sm:flex-row sm:items-center gap-2">
            <p className="flex-1 text-xs text-fds-mute text-center sm:text-left">{t('cursus.sansDeplacement')}</p>
            <Link to="/postuler" className="min-h-12 px-6 rounded-lg bg-fds-gold text-fds-on-light font-semibold flex items-center justify-center hover:brightness-95">
              {t('cursus.deposer')}
            </Link>
          </div>
        </div>
      )}
    </>
  );
};
