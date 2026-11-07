import React from 'react';
import { Link } from 'react-router-dom';
import { useT } from '../../../shared/i18n';

/** Page 404 explicite aux couleurs de la FDS pour toute route inconnue. */
export const NotFoundPage: React.FC = () => {
  const t = useT();

  return (
    <div className="max-w-xl w-full mx-auto px-4 py-12 lg:py-20 flex-1 flex flex-col items-start justify-center gap-4">
      <span className="rounded-full bg-fds-navy-t text-fds-accent px-3 py-1 text-xs font-semibold">404</span>
      <h1 className="font-fds-serif text-2xl lg:text-4xl font-bold text-fds-title">{t('page404.titre')}</h1>
      <p className="text-fds-mute lg:text-lg">{t('page404.texte')}</p>
      <div className="flex flex-wrap gap-3 pt-2">
        <Link
          to="/"
          className="min-h-12 px-5 rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white font-semibold flex items-center justify-center transition-colors"
        >
          {t('nav.accueil')}
        </Link>
        <Link
          to="/suivi"
          className="min-h-12 px-5 rounded-lg border-2 border-fds-accent bg-fds-surface text-fds-accent font-semibold flex items-center justify-center"
        >
          {t('accueil.suivre')}
        </Link>
      </div>
    </div>
  );
};

