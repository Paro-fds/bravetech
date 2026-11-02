import React, { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ArrowLeft, ChevronDown, FileText, Plus, Check } from 'lucide-react';
import { cursusApi, type MatiereItem } from '../../../entities/cursus';
import { FRAIS_DOSSIER_PAR_DEFAUT } from '../../../features/candidature-form';
import { useNomPiece, useT } from '../../../shared/i18n/useT';

/** « 120 h + 60 h TP », ou « 90 h » selon les volumes renseignés. */
function formaterHeures(m: MatiereItem): string {
  if (m.heures_theorie != null || m.heures_tp != null) {
    return [m.heures_theorie != null ? `${m.heures_theorie} h` : null, m.heures_tp != null ? `${m.heures_tp} h TP` : null]
      .filter(Boolean)
      .join(' + ');
  }
  return m.heures ? `${m.heures} h` : '';
}

/** « MPC1 » → « MPC 1 » : le nom du niveau vient des données, sans espace. */
const formaterNiveau = (nom: string) => nom.replace(/^([A-Za-z]+)(\d+)$/, '$1 $2');

const BRANCHES = ['Génie Civil', 'Génie Électromécanique', 'Génie Électronique', 'Architecture'];

const Titre: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <h2 className="font-fds-serif text-xl font-bold text-fds-navy-d">{children}</h2>
);

/** Fiche d'un cursus (maquettes « Cursus » mobile et bureau). Le MPC est le cursus d'admission ; les branches viennent après. */
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

  const retour = (
    <Link to="/" className="flex items-center gap-2 min-h-11 font-semibold text-fds-navy">
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
        {retour}
        <h1 className="font-fds-serif text-2xl font-bold text-fds-navy-d">{t('cursus.introuvableTitre')}</h1>
        <p className="text-fds-mute">{t('cursus.introuvableTexte')}</p>
      </div>
    );
  }

  const niveaux = Object.entries(cursus.niveaux ?? {});
  const admission = cursus.est_admission;

  return (
    <>
      <div className="max-w-5xl w-full mx-auto px-4 py-6 flex flex-col gap-6 flex-1">
        {retour}

        <section className="flex flex-col gap-2.5">
          <div className="flex flex-wrap gap-2">
            {admission ? (
              <span className="rounded-full bg-fds-navy-t text-fds-navy px-2.5 py-0.5 text-[13px] font-semibold">{t('cursus.badgeAdmission')}</span>
            ) : (
              <span className="rounded-full bg-fds-navy-t text-fds-navy px-2.5 py-0.5 text-[13px] font-semibold">{t('cursus.badgeBranche')}</span>
            )}
            {admission && cursus.est_ouvert && (
              <span className="rounded-full bg-fds-ok-bg text-fds-ok px-2.5 py-0.5 text-[13px] font-semibold">{t('accueil.badge')}</span>
            )}
          </div>
          <h1 lang="fr" className="font-fds-serif text-[28px] md:text-4xl leading-tight font-bold text-fds-navy-d">{cursus.nom}</h1>
          <p lang="fr" className="text-fds-mute md:text-lg max-w-3xl">{cursus.description_longue || cursus.description_courte}</p>
        </section>

        <section className="rounded-xl border border-fds-line bg-white p-4 grid grid-cols-2 md:grid-cols-4 gap-4" aria-label={t('cursus.infosCles')}>
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
              {/* Dates non confirmées par la Faculté : on ne les affiche pas comme si elles l'étaient */}
              <div>
                <div className="text-xs text-fds-mute">{t('cursus.dateLimite')}</div>
                <div className="font-semibold">{t('cursus.aConfirmer')}</div>
              </div>
              <div>
                <div className="text-xs text-fds-mute">{t('cursus.rentree')}</div>
                <div className="font-semibold">{t('cursus.aConfirmer')}</div>
              </div>
            </>
          ) : (
            <div>
              <div className="text-xs text-fds-mute">{t('cursus.acces')}</div>
              <div className="font-semibold">{t('cursus.apresMpc')}</div>
            </div>
          )}
        </section>

        <div className="grid gap-6 lg:grid-cols-[1fr_340px] items-start">
          <div className="flex flex-col gap-6 min-w-0">
            {admission && (
              <section className="flex flex-col gap-3" aria-labelledby="parcours">
                <h2 id="parcours" className="font-fds-serif text-xl font-bold text-fds-navy-d">
                  {t('cursus.parcoursTitre')}
                </h2>
                <ol className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-4">
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
                    <span className="w-7 h-7 rounded-full border-2 border-fds-line bg-white text-fds-mute flex items-center justify-center shrink-0" aria-hidden="true">
                      <Plus className="w-4 h-4" />
                    </span>
                    <div className="flex flex-col gap-2">
                      <div className="font-semibold">{t('cursus.parcours35Titre')}</div>
                      <div className="text-sm text-fds-mute">{t('cursus.parcours35Texte')}</div>
                      <div className="flex flex-wrap gap-1.5">
                        {BRANCHES.map((b) => (
                          <span key={b} lang="fr" className="rounded-full bg-fds-navy-t text-fds-navy px-2.5 py-0.5 text-[13px] font-semibold">
                            {b}
                          </span>
                        ))}
                      </div>
                    </div>
                  </li>
                </ol>
              </section>
            )}

            {niveaux.length > 0 && (
              <section className="flex flex-col gap-3" aria-labelledby="programme">
                <h2 id="programme" className="font-fds-serif text-xl font-bold text-fds-navy-d">
                  {admission ? t('cursus.programmeMpc') : t('cursus.programme')}
                </h2>
                {niveaux.map(([nom, matieres], index) => {
                  const ouvert = ouverts[nom] ?? index === 0; // le premier niveau est déplié par défaut
                  return (
                    <div key={nom} className="rounded-xl border border-fds-line bg-white">
                      <button
                        type="button"
                        aria-expanded={ouvert}
                        onClick={() => setOuverts({ ...ouverts, [nom]: !ouvert })}
                        className="w-full min-h-14 px-4 flex items-center gap-2 text-left"
                      >
                        <h3 className="flex-1 font-fds-serif text-lg font-bold text-fds-navy-d">{formaterNiveau(nom)}</h3>
                        <span className="rounded-full bg-fds-navy-t text-fds-navy px-2.5 py-0.5 text-[13px] font-semibold">{t('cursus.matieres', { n: matieres.length })}</span>
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
              </section>
            )}
          </div>

          <aside className="flex flex-col gap-3 lg:sticky lg:top-4">
            {admission ? (
              <>
                <Titre>{t('cursus.piecesTitre')}</Titre>
                <ul className="rounded-xl border border-fds-line bg-white px-4">
                  {cursus.documents_requis?.map((doc) => (
                    <li key={doc.id} className="flex gap-3 items-center py-2.5 border-b border-fds-line last:border-b-0">
                      <FileText className="w-5 h-5 shrink-0 text-fds-navy" aria-hidden="true" />
                      <span className="flex-1">{nomPiece(doc.id, doc.nom)}</span>
                    </li>
                  ))}
                </ul>
                <p className="text-xs text-fds-mute">{t('cursus.piecesNote')}</p>
              </>
            ) : (
              <div className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-3">
                <h2 className="font-fds-serif text-lg font-bold text-fds-navy-d">{t('cursus.brancheTitre')}</h2>
                <p className="text-sm text-fds-mute">{t('cursus.brancheTexte')}</p>
                <Link to="/cursus/mpc" className="min-h-12 px-4 rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white font-semibold flex items-center justify-center">
                  {t('cursus.voirMpc')}
                </Link>
              </div>
            )}
          </aside>
        </div>
      </div>

      {admission && (
        <div className="sticky bottom-0 bg-white border-t border-fds-line px-4 py-3">
          <div className="max-w-5xl mx-auto flex flex-col sm:flex-row sm:items-center gap-2">
            <p className="flex-1 text-xs text-fds-mute text-center sm:text-left">{t('cursus.sansDeplacement')}</p>
            <Link to="/postuler" className="min-h-12 px-6 rounded-lg bg-fds-gold text-fds-navy-d font-semibold flex items-center justify-center hover:brightness-95">
              {t('cursus.deposer')}
            </Link>
          </div>
        </div>
      )}
    </>
  );
};
