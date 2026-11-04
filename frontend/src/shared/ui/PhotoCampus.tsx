import React from 'react';
import { useT } from '../i18n/useT';

/**
 * Photo de la cour du campus de Delmas 33 (maquettes bureau « Accueil », « Histoire », « Contact »).
 * Chargement différé : cachée sur mobile (`hidden lg:block`), elle n'est pas téléchargée, ce qui ménage les forfaits.
 */
export const PhotoCampus: React.FC<{ className?: string; tailles?: string }> = ({ className = '', tailles = '50vw' }) => {
  const t = useT();
  return (
    <img
      src="/campus-delmas33-1440.jpg"
      srcSet="/campus-delmas33-800.jpg 800w, /campus-delmas33-1440.jpg 1440w"
      sizes={tailles}
      width={1440}
      height={764}
      loading="lazy"
      decoding="async"
      alt={t('marque.photoCampusAlt')}
      className={`object-cover ${className}`}
    />
  );
};
