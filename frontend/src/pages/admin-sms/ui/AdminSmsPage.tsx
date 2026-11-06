import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Info, RefreshCw } from 'lucide-react';
import { dossierAdminApi, type SmsSimule } from '../../../entities/dossier-admin';
import { useSessionStore } from '../../../entities/session';
import { formaterHorodatage } from '../../../features/candidature-form';

/**
 * SMS simulés (US-016) : ce que le candidat aurait reçu sur son téléphone, à la soumission et à chaque décision.
 * Comme le paiement MonCash / NatCash, l'envoi est simulé : aucun fournisseur SMS n'est branché en V1.
 */
export const AdminSmsPage: React.FC = () => {
  const session = useSessionStore((s) => s.session);
  const [sms, setSms] = useState<SmsSimule[] | null>(null);
  const [erreur, setErreur] = useState(false);
  const [version, setVersion] = useState(0);

  useEffect(() => {
    if (!session) return;
    let annule = false;
    dossierAdminApi
      .listerSms(session)
      .then((liste) => {
        if (!annule) {
          setSms(liste);
          setErreur(false);
        }
      })
      .catch(() => {
        if (!annule) setErreur(true);
      });
    return () => {
      annule = true;
    };
  }, [session, version]);

  return (
    <div className="max-w-4xl w-full flex flex-col gap-5">
      <section className="flex flex-col gap-2">
        <div className="flex flex-wrap items-center gap-3">
          <h1 className="font-fds-serif text-[28px] font-bold text-fds-title mr-auto">SMS envoyés aux candidats</h1>
          <button
            type="button"
            onClick={() => setVersion((v) => v + 1)}
            className="min-h-11 px-4 rounded-lg border-2 border-fds-accent text-fds-accent font-semibold flex items-center gap-2"
          >
            <RefreshCw className="w-4 h-4" aria-hidden="true" />
            Actualiser
          </button>
        </div>
        <p className="flex gap-2.5 items-start rounded-[10px] border border-fds-accent-line bg-fds-navy-t px-3.5 py-3 text-sm">
          <Info className="w-5 h-5 shrink-0 text-fds-accent" aria-hidden="true" />
          <span>
            <b>Simulation.</b> Aucun SMS réel n'est envoyé : comme le paiement MonCash / NatCash, l'envoi est simulé. Cette page montre
            ce que le candidat aurait reçu sur son téléphone, en plus de l'email, à la soumission de son dossier et à chaque décision.
          </span>
        </p>
      </section>

      {erreur && (
        <p role="alert" className="text-fds-bad">
          Les SMS n'ont pas pu être chargés. Réessayez avec « Actualiser ».
        </p>
      )}
      {!erreur && sms === null && (
        <p role="status" className="text-fds-mute">
          Chargement…
        </p>
      )}
      {sms !== null && sms.length === 0 && <p className="text-fds-mute">Aucun SMS pour le moment. Ils apparaissent dès qu'un dossier est soumis.</p>}

      {sms !== null && sms.length > 0 && (
        <ul className="flex flex-col gap-3" aria-label="SMS simulés">
          {sms.map((s, i) => (
            <li key={`${s.envoye_le}-${i}`} className="rounded-xl border border-fds-line bg-fds-surface p-4 flex flex-col gap-2">
              <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1 text-sm">
                <b className="text-fds-ink">{s.destinataire}</b>
                {s.reference_dossier && (
                  <Link to={`/admin/candidatures/${s.reference_dossier}`} className="font-semibold text-fds-accent underline">
                    {s.reference_dossier}
                  </Link>
                )}
                <span className="text-fds-mute ml-auto">{formaterHorodatage(s.envoye_le)}</span>
              </div>
              <p className="rounded-lg bg-fds-navy-t px-3 py-2 text-[15px] break-words">{s.texte}</p>
              <span className="text-xs text-fds-mute">{s.texte.length} caractères sur 160</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
