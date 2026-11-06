import React, { useEffect, useState } from 'react';
import { Check, KeyRound, ShieldCheck, TriangleAlert, UserCheck, UserPlus, UserX } from 'lucide-react';
import { useSessionStore } from '../../../entities/session';
import { formaterJourCourt } from '../../../features/candidature-form';
import { ApiError } from '../../../shared/api';
import {
  utilisateursApi,
  type ComptePersonnel,
  type CreerComptePayload,
  type RolePersonnel,
} from '../api/utilisateursApi';

const CLASSE_CHAMP =
  'w-full min-h-12 rounded-lg border-[1.5px] bg-fds-surface px-3 text-base text-fds-ink focus:outline-none focus:ring-2 focus:ring-fds-accent disabled:opacity-70';

type ErreursChamps = Partial<Record<'email' | 'mot_de_passe' | 'role' | 'nouveau_mot_de_passe', string>>;

function extraireErreurs422(erreur: unknown): ErreursChamps | null {
  if (!(erreur instanceof ApiError) || erreur.status !== 422) return null;
  return (erreur.body as { detail?: { erreurs?: ErreursChamps } } | null)?.detail?.erreurs ?? null;
}

function extraireDetail(erreur: unknown, repli: string): string {
  if (erreur instanceof ApiError) {
    const detail = (erreur.body as { detail?: unknown } | null)?.detail;
    if (typeof detail === 'string' && detail.trim()) return detail;
  }
  return repli;
}

/** Gestion des accès du personnel (administrateurs et agents du secrétariat). Réservée au rôle `admin`. */
export const AdminUtilisateursPage: React.FC = () => {
  const session = useSessionStore((s) => s.session);
  const estAdmin = session?.role === 'admin';

  const [comptes, setComptes] = useState<ComptePersonnel[] | null>(null);
  const [echecChargement, setEchecChargement] = useState(false);

  // Formulaire de création
  const [email, setEmail] = useState('');
  const [role, setRole] = useState<RolePersonnel>('agent');
  const [motDePasse, setMotDePasse] = useState('');
  const [erreursCreation, setErreursCreation] = useState<ErreursChamps>({});
  const [creationEnCours, setCreationEnCours] = useState(false);

  // Actions sur une ligne existante
  const [actionId, setActionId] = useState<string | null>(null);
  const [cibleMdpId, setCibleMdpId] = useState<string | null>(null);
  const [nouveauMdp, setNouveauMdp] = useState('');
  const [erreurMdp, setErreurMdp] = useState<string | null>(null);

  // Message global (succès ou erreur d'action)
  const [message, setMessage] = useState<{ type: 'ok' | 'erreur'; texte: string } | null>(null);

  useEffect(() => {
    if (!session || !estAdmin) return;
    let annule = false;
    utilisateursApi
      .lister(session)
      .then((liste) => {
        if (!annule) setComptes(liste);
      })
      .catch(() => {
        if (!annule) setEchecChargement(true);
      });
    return () => {
      annule = true;
    };
  }, [session, estAdmin]);

  if (!estAdmin) {
    return (
      <p role="alert" className="flex gap-2.5 items-start rounded-[10px] border border-fds-bad-line bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
        <TriangleAlert className="w-5 h-5 shrink-0" aria-hidden="true" />
        Seul un administrateur peut gérer les comptes du personnel.
      </p>
    );
  }

  if (echecChargement) {
    return (
      <p role="alert" className="text-fds-bad">
        Les comptes du personnel n’ont pas pu être chargés. Rechargez la page.
      </p>
    );
  }

  if (!comptes) {
    return (
      <p role="status" className="text-fds-mute">
        Chargement des comptes du personnel…
      </p>
    );
  }

  const remplacerDansListe = (maj: ComptePersonnel) => {
    setComptes((prec) => (prec ? prec.map((c) => (c.id === maj.id ? maj : c)) : [maj]));
  };

  const creerCompte = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!session) return;
    setErreursCreation({});
    setMessage(null);
    setCreationEnCours(true);
    const payload: CreerComptePayload = { email, mot_de_passe: motDePasse, role };
    try {
      const cree = await utilisateursApi.creer(session, payload);
      setComptes((prec) => (prec ? [...prec, cree].sort((a, b) => a.email.localeCompare(b.email)) : [cree]));
      setEmail('');
      setMotDePasse('');
      setRole('agent');
      setMessage({
        type: 'ok',
        texte: `Compte créé pour ${cree.email} (${cree.role === 'admin' ? 'Administrateur' : 'Agent du secrétariat'}). Communiquez-lui son mot de passe temporaire.`,
      });
    } catch (erreur) {
      const parChamp = extraireErreurs422(erreur);
      if (parChamp) {
        setErreursCreation(parChamp);
      } else {
        setMessage({
          type: 'erreur',
          texte: extraireDetail(erreur, 'Création impossible. Vérifiez la connexion puis réessayez.'),
        });
      }
    } finally {
      setCreationEnCours(false);
    }
  };

  const basculerRole = async (compte: ComptePersonnel) => {
    if (!session) return;
    const nouveauRole: RolePersonnel = compte.role === 'admin' ? 'agent' : 'admin';
    setMessage(null);
    setActionId(compte.id);
    try {
      const maj = await utilisateursApi.modifierAcces(session, compte.id, { role: nouveauRole });
      remplacerDansListe(maj);
      setMessage({
        type: 'ok',
        texte: `Le rôle de ${maj.email} est désormais « ${maj.role === 'admin' ? 'Administrateur' : 'Agent du secrétariat'} ».`,
      });
    } catch (erreur) {
      setMessage({
        type: 'erreur',
        texte: extraireDetail(erreur, 'Modification du rôle impossible.'),
      });
    } finally {
      setActionId(null);
    }
  };

  const basculerStatut = async (compte: ComptePersonnel) => {
    if (!session) return;
    const nouvelEtat = !compte.est_actif;
    setMessage(null);
    setActionId(compte.id);
    try {
      const maj = await utilisateursApi.modifierAcces(session, compte.id, { est_actif: nouvelEtat });
      remplacerDansListe(maj);
      setMessage({
        type: 'ok',
        texte: nouvelEtat
          ? `Le compte ${maj.email} est réactivé.`
          : `Le compte ${maj.email} est désactivé. Ses décisions passées restent tracées dans l’historique.`,
      });
    } catch (erreur) {
      setMessage({
        type: 'erreur',
        texte: extraireDetail(erreur, 'Modification du statut impossible.'),
      });
    } finally {
      setActionId(null);
    }
  };

  const enregistrerNouveauMdp = async (e: React.FormEvent, compte: ComptePersonnel) => {
    e.preventDefault();
    if (!session) return;
    setErreurMdp(null);
    setMessage(null);
    setActionId(compte.id);
    try {
      await utilisateursApi.reinitialiserMotDePasse(session, compte.id, nouveauMdp);
      setCibleMdpId(null);
      setNouveauMdp('');
      setMessage({
        type: 'ok',
        texte: `Mot de passe temporaire mis à jour pour ${compte.email}. Communiquez-lui ce nouveau mot de passe.`,
      });
    } catch (erreur) {
      const parChamp = extraireErreurs422(erreur);
      if (parChamp?.nouveau_mot_de_passe) {
        setErreurMdp(parChamp.nouveau_mot_de_passe);
      } else {
        setErreurMdp(extraireDetail(erreur, 'Réinitialisation impossible.'));
      }
    } finally {
      setActionId(null);
    }
  };

  return (
    <div className="max-w-4xl w-full flex flex-col gap-6">
      <section className="flex flex-col gap-2">
        <h1 className="font-fds-serif text-[28px] font-bold text-fds-title">Gestion des accès</h1>
        <p className="text-fds-mute">
          Créez et gérez les comptes du personnel de la Faculté. Un <b className="text-fds-ink">agent du secrétariat</b> instruit les dossiers
          (consultation, validation ou rejet motivé des pièces, export CSV/PDF) ; un <b className="text-fds-ink">administrateur</b> dispose en plus du
          réglage du calendrier d’admission et de la gestion des accès.
        </p>
      </section>

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

      {/* Formulaire de création d'un compte personnel */}
      <form onSubmit={creerCompte} noValidate className="rounded-xl border border-fds-line bg-fds-surface p-4 sm:p-6 flex flex-col gap-5">
        <h2 className="font-fds-serif text-xl font-bold text-fds-title">Ajouter un membre du personnel</h2>
        <div className="grid gap-4 sm:grid-cols-3">
          <div className="flex flex-col gap-1.5">
            <label htmlFor="nouvel-email" className="text-[15px] font-semibold">
              Adresse email <span className="text-fds-bad">*</span>
            </label>
            <input
              id="nouvel-email"
              type="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                if (erreursCreation.email) setErreursCreation((prec) => ({ ...prec, email: undefined }));
              }}
              placeholder="agent@fds.ueh.edu.ht"
              disabled={creationEnCours}
              aria-invalid={Boolean(erreursCreation.email)}
              aria-describedby="nouvel-email-aide"
              className={`${CLASSE_CHAMP} ${erreursCreation.email ? 'border-fds-bad' : 'border-fds-field'}`}
            />
            <p
              id="nouvel-email-aide"
              role={erreursCreation.email ? 'alert' : undefined}
              className={`text-[13px] ${erreursCreation.email ? 'font-semibold text-fds-bad' : 'text-fds-mute'}`}
            >
              {erreursCreation.email ?? 'Identifiant de connexion et trace d’audit.'}
            </p>
          </div>

          <div className="flex flex-col gap-1.5">
            <label htmlFor="nouveau-role" className="text-[15px] font-semibold">
              Rôle <span className="text-fds-bad">*</span>
            </label>
            <select
              id="nouveau-role"
              value={role}
              onChange={(e) => setRole(e.target.value as RolePersonnel)}
              disabled={creationEnCours}
              className={`${CLASSE_CHAMP} border-fds-field`}
            >
              <option value="agent">Agent du secrétariat</option>
              <option value="admin">Administrateur</option>
            </select>
            <p className="text-[13px] text-fds-mute">
              {role === 'agent' ? 'Accès aux dossiers et au calendrier (lecture).' : 'Accès complet (dossiers, calendrier, accès).'}
            </p>
          </div>

          <div className="flex flex-col gap-1.5">
            <label htmlFor="nouveau-mot-de-passe" className="text-[15px] font-semibold">
              Mot de passe temporaire <span className="text-fds-bad">*</span>
            </label>
            <input
              id="nouveau-mot-de-passe"
              type="password"
              value={motDePasse}
              onChange={(e) => {
                setMotDePasse(e.target.value);
                if (erreursCreation.mot_de_passe) setErreursCreation((prec) => ({ ...prec, mot_de_passe: undefined }));
              }}
              placeholder="12 caractères minimum"
              disabled={creationEnCours}
              aria-invalid={Boolean(erreursCreation.mot_de_passe)}
              aria-describedby="nouveau-mdp-aide"
              className={`${CLASSE_CHAMP} ${erreursCreation.mot_de_passe ? 'border-fds-bad' : 'border-fds-field'}`}
            />
            <p
              id="nouveau-mdp-aide"
              role={erreursCreation.mot_de_passe ? 'alert' : undefined}
              className={`text-[13px] ${erreursCreation.mot_de_passe ? 'font-semibold text-fds-bad' : 'text-fds-mute'}`}
            >
              {erreursCreation.mot_de_passe ?? 'Au moins 12 caractères, à remettre en main propre.'}
            </p>
          </div>
        </div>

        <button
          type="submit"
          disabled={creationEnCours}
          className="min-h-12 px-6 self-start rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white font-semibold flex items-center justify-center gap-2 transition-colors disabled:opacity-70"
        >
          <UserPlus className="w-5 h-5" aria-hidden="true" />
          {creationEnCours ? 'Création…' : 'Créer le compte'}
        </button>
      </form>

      {/* Liste des comptes existants */}
      <section className="rounded-xl border border-fds-line bg-fds-surface overflow-hidden">
        <div className="px-4 py-3.5 sm:px-6 border-b border-fds-line flex items-center justify-between">
          <h2 className="font-fds-serif text-xl font-bold text-fds-title">Comptes du personnel ({comptes.length})</h2>
        </div>
        <ul className="divide-y divide-fds-line">
          {comptes.map((compte) => {
            const estSoi = session?.email.toLowerCase() === compte.email.toLowerCase();
            const enCours = actionId === compte.id;
            const editionMdp = cibleMdpId === compte.id;

            return (
              <li key={compte.id} className="p-4 sm:px-6 flex flex-col gap-3">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div className="flex flex-col gap-1 min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="font-semibold text-fds-ink break-all">{compte.email}</span>
                      {estSoi && (
                        <span className="rounded-full bg-fds-chip px-2 py-0.5 text-xs font-semibold text-fds-mute">Vous</span>
                      )}
                      <span
                        className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                          compte.role === 'admin' ? 'bg-fds-navy-t text-fds-accent' : 'bg-fds-chip text-fds-ink'
                        }`}
                      >
                        {compte.role === 'admin' ? 'Administrateur' : 'Agent du secrétariat'}
                      </span>
                      <span
                        className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                          compte.est_actif ? 'bg-fds-ok-bg text-fds-ok' : 'bg-fds-bad-bg text-fds-bad'
                        }`}
                      >
                        {compte.est_actif ? 'Actif' : 'Désactivé'}
                      </span>
                    </div>
                    <div className="text-xs text-fds-mute">Créé le {formaterJourCourt(compte.created_at)}</div>
                  </div>

                  <div className="flex flex-wrap items-center gap-2">
                    <button
                      type="button"
                      disabled={estSoi || enCours}
                      onClick={() => void basculerRole(compte)}
                      title={estSoi ? 'Vous ne pouvez pas modifier votre propre rôle.' : undefined}
                      className="min-h-10 px-3 rounded-lg border border-fds-line bg-fds-surface hover:bg-fds-chip text-sm font-semibold flex items-center gap-1.5 disabled:opacity-50"
                    >
                      <ShieldCheck className="w-4 h-4 text-fds-accent" aria-hidden="true" />
                      {compte.role === 'admin' ? 'Passer agent' : 'Passer admin'}
                    </button>

                    <button
                      type="button"
                      disabled={estSoi || enCours}
                      onClick={() => void basculerStatut(compte)}
                      title={estSoi ? 'Vous ne pouvez pas désactiver votre propre compte.' : undefined}
                      className={`min-h-10 px-3 rounded-lg border text-sm font-semibold flex items-center gap-1.5 disabled:opacity-50 ${
                        compte.est_actif
                          ? 'border-fds-bad-line text-fds-bad hover:bg-fds-bad-bg'
                          : 'border-fds-ok-line text-fds-ok hover:bg-fds-ok-bg'
                      }`}
                    >
                      {compte.est_actif ? (
                        <>
                          <UserX className="w-4 h-4" aria-hidden="true" />
                          Désactiver
                        </>
                      ) : (
                        <>
                          <UserCheck className="w-4 h-4" aria-hidden="true" />
                          Réactiver
                        </>
                      )}
                    </button>

                    <button
                      type="button"
                      disabled={enCours}
                      onClick={() => {
                        setCibleMdpId(editionMdp ? null : compte.id);
                        setNouveauMdp('');
                        setErreurMdp(null);
                      }}
                      className="min-h-10 px-3 rounded-lg border border-fds-line bg-fds-surface hover:bg-fds-chip text-sm font-semibold flex items-center gap-1.5 disabled:opacity-50"
                    >
                      <KeyRound className="w-4 h-4 text-fds-mute" aria-hidden="true" />
                      Mot de passe
                    </button>
                  </div>
                </div>

                {editionMdp && (
                  <form
                    onSubmit={(e) => void enregistrerNouveauMdp(e, compte)}
                    noValidate
                    className="rounded-lg border border-fds-line bg-fds-page p-3 flex flex-col sm:flex-row sm:items-start gap-3"
                  >
                    <div className="flex-1 flex flex-col gap-1">
                      <label htmlFor={`mdp-${compte.id}`} className="text-xs font-semibold text-fds-ink">
                        Nouveau mot de passe temporaire pour {compte.email}
                      </label>
                      <input
                        id={`mdp-${compte.id}`}
                        type="password"
                        value={nouveauMdp}
                        onChange={(e) => {
                          setNouveauMdp(e.target.value);
                          if (erreurMdp) setErreurMdp(null);
                        }}
                        placeholder="12 caractères minimum"
                        disabled={enCours}
                        aria-invalid={Boolean(erreurMdp)}
                        className={`${CLASSE_CHAMP} ${erreurMdp ? 'border-fds-bad' : 'border-fds-field'}`}
                      />
                      {erreurMdp && (
                        <p role="alert" className="text-xs font-semibold text-fds-bad">
                          {erreurMdp}
                        </p>
                      )}
                    </div>
                    <div className="flex items-center gap-2 sm:pt-5">
                      <button
                        type="submit"
                        disabled={enCours}
                        className="min-h-11 px-4 rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white text-sm font-semibold disabled:opacity-70"
                      >
                        Enregistrer
                      </button>
                      <button
                        type="button"
                        disabled={enCours}
                        onClick={() => {
                          setCibleMdpId(null);
                          setNouveauMdp('');
                          setErreurMdp(null);
                        }}
                        className="min-h-11 px-3 rounded-lg border border-fds-line bg-fds-surface text-sm font-semibold"
                      >
                        Annuler
                      </button>
                    </div>
                  </form>
                )}
              </li>
            );
          })}
        </ul>
      </section>
    </div>
  );
};

