import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldAlert } from 'lucide-react';
import { useT, type Cle } from '../../../shared/i18n';

const SECTIONS: { titre: Cle; paragraphes: Cle[] }[] = [
  { titre: 'confid.editeurTitre', paragraphes: ['confid.editeurP1', 'confid.editeurP2'] },
  { titre: 'confid.donneesTitre', paragraphes: ['confid.donneesP1', 'confid.donneesP2'] },
  { titre: 'confid.securiteTitre', paragraphes: ['confid.securiteP1', 'confid.securiteP2'] },
  { titre: 'confid.paiementTitre', paragraphes: ['confid.paiementP1'] },
  { titre: 'confid.droitsTitre', paragraphes: ['confid.droitsP1'] },
];

/** Page officielle « Mentions légales et protection des données » (`/confidentialite`). */
export const ConfidentialitePage: React.FC = () => {
  const t = useT();

  return (
    <>
      <section className="lg:bg-fds-navy lg:text-white">
        <div className="max-w-3xl lg:max-w-5xl mx-auto px-4 pt-6 lg:py-11 flex flex-col gap-2 lg:gap-2.5">
          <h1 className="font-fds-serif text-2xl lg:text-[40px] font-bold text-fds-title lg:text-white">{t('confid.titre')}</h1>
          <p className="text-fds-mute lg:text-fds-on-navy lg:text-lg">{t('confid.sousTitre')}</p>
        </div>
      </section>

      <div className="max-w-3xl lg:max-w-5xl w-full mx-auto px-4 py-6 lg:pt-10 lg:pb-14 flex flex-col gap-6">
        <section
          role="note"
          aria-labelledby="alerte-anti-fraude"
          className="rounded-xl border-2 border-fds-warn-line bg-fds-warn-bg p-4 sm:p-5 flex gap-3 items-start text-fds-warn"
        >
          <ShieldAlert className="w-6 h-6 shrink-0 mt-0.5" aria-hidden="true" />
          <div className="flex flex-col gap-1">
            <h2 id="alerte-anti-fraude" className="font-semibold text-base">
              {t('confid.arnaqueTitre')}
            </h2>
            <p className="text-sm">{t('confid.arnaqueTexte')}</p>
          </div>
        </section>

        <div className="rounded-xl border border-fds-line bg-fds-surface p-4 sm:p-8 flex flex-col gap-6">
          {SECTIONS.map((s) => (
            <section key={s.titre} className="flex flex-col gap-2">
              <h2 className="font-fds-serif text-xl font-bold text-fds-title">{t(s.titre)}</h2>
              {s.paragraphes.map((p) => (
                <p key={p} className="text-sm sm:text-base text-fds-mute leading-relaxed">
                  {t(p)}
                </p>
              ))}
            </section>
          ))}

          <div className="pt-2 border-t border-fds-line flex flex-wrap gap-3">
            <Link
              to="/contact"
              className="min-h-12 px-5 rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white font-semibold flex items-center justify-center transition-colors"
            >
              {t('confid.contactBouton')}
            </Link>
            <Link
              to="/"
              className="min-h-12 px-5 rounded-lg border-2 border-fds-accent bg-fds-surface text-fds-accent font-semibold flex items-center justify-center"
            >
              {t('nav.accueil')}
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

