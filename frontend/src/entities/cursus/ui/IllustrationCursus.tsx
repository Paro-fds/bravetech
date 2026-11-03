import React from 'react';

/**
 * Illustrations des cursus (maquettes « Accueil » et « Cursus » bureau), en SVG en ligne.
 * Les couleurs passent par les jetons fds-* (classes fill-/stroke-) : elles suivent le mode sombre (règle R4, spec WS-01).
 * Décoratives à côté du nom du cursus : masquées aux lecteurs d'écran.
 */
const Cadre: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = '' }) => (
  <svg viewBox="0 0 320 120" aria-hidden="true" focusable="false" className={`block w-full h-auto ${className}`}>
    <rect width="320" height="120" className="fill-fds-navy-t" />
    {children}
  </svg>
);

const Atome: React.FC<{ className?: string }> = ({ className }) => (
  <Cadre className={className}>
    <g fill="none" strokeWidth="3" className="stroke-fds-accent">
      <ellipse cx="160" cy="60" rx="64" ry="22" />
      <ellipse cx="160" cy="60" rx="64" ry="22" transform="rotate(60 160 60)" />
      <ellipse cx="160" cy="60" rx="64" ry="22" transform="rotate(120 160 60)" />
    </g>
    <circle cx="160" cy="60" r="9" className="fill-fds-gold" />
  </Cadre>
);

const Pont: React.FC<{ className?: string }> = ({ className }) => (
  <Cadre className={className}>
    <rect y="96" width="320" height="24" className="fill-fds-accent-line" />
    <path d="M30 80h260" strokeWidth="6" className="stroke-fds-accent" />
    <path d="M60 80Q160 0 260 80" fill="none" strokeWidth="5" className="stroke-fds-accent" />
    <path d="M90 80V45M120 80V27M160 80V20M200 80V27M230 80V45" strokeWidth="2" className="stroke-fds-accent" />
    <g className="fill-fds-title">
      <rect x="52" y="80" width="12" height="30" />
      <rect x="256" y="80" width="12" height="30" />
    </g>
    <circle cx="272" cy="26" r="12" className="fill-fds-gold" />
  </Cadre>
);

const Engrenages: React.FC<{ className?: string }> = ({ className }) => (
  <Cadre className={className}>
    <g fill="none" className="stroke-fds-accent">
      <circle cx="130" cy="62" r="32" strokeWidth="12" strokeDasharray="7 7.2" />
      <circle cx="130" cy="62" r="26" strokeWidth="4" />
      <circle cx="130" cy="62" r="8" strokeWidth="4" />
    </g>
    <g fill="none" className="stroke-fds-title">
      <circle cx="205" cy="48" r="22" strokeWidth="10" strokeDasharray="6 6.1" />
      <circle cx="205" cy="48" r="17" strokeWidth="3" />
      <circle cx="205" cy="48" r="5" strokeWidth="3" />
    </g>
    <path d="M20 108h280" strokeWidth="4" className="stroke-fds-accent-line" />
    <circle cx="268" cy="26" r="12" className="fill-fds-gold" />
  </Cadre>
);

const Puce: React.FC<{ className?: string }> = ({ className }) => (
  <Cadre className={className}>
    <rect x="118" y="30" width="84" height="60" rx="8" className="fill-fds-accent" />
    <rect x="136" y="46" width="48" height="28" rx="4" className="fill-fds-gold" />
    <path
      d="M132 30v-14M160 30v-14M188 30v-14M132 90v14M160 90v14M188 90v14M118 48h-14M118 72h-14M202 48h14M202 72h14"
      strokeWidth="4"
      strokeLinecap="round"
      className="stroke-fds-accent"
    />
    <path d="M104 48H50M104 72H70L56 86M216 48h54M216 72h34l14 14" fill="none" strokeWidth="2" className="stroke-fds-title" />
    <g className="fill-fds-title">
      <circle cx="50" cy="48" r="4" />
      <circle cx="56" cy="86" r="4" />
      <circle cx="270" cy="48" r="4" />
      <circle cx="264" cy="86" r="4" />
    </g>
  </Cadre>
);

const Batiment: React.FC<{ className?: string }> = ({ className }) => (
  <Cadre className={className}>
    <g fill="none" strokeWidth="3" strokeLinejoin="round" className="stroke-fds-accent">
      <path d="M90 104V50l40-24 40 24v54z" />
      <path d="M170 104V64h60v40" />
    </g>
    <g className="fill-fds-accent">
      <rect x="112" y="62" width="14" height="14" />
      <rect x="134" y="62" width="14" height="14" />
      <rect x="112" y="84" width="14" height="20" />
      <rect x="186" y="76" width="12" height="12" />
    </g>
    <path d="M80 112h160M80 108v8M240 108v8" strokeWidth="2" className="stroke-fds-title" />
    <path d="M250 20l40 60h-40z" fill="none" strokeWidth="4" strokeLinejoin="round" className="stroke-fds-gold" />
  </Cadre>
);

const PAR_CURSUS: Record<string, React.FC<{ className?: string }>> = {
  mpc: Atome,
  'genie-civil': Pont,
  'genie-electromecanique': Engrenages,
  'genie-electronique': Puce,
  architecture: Batiment,
};

/** Illustration d'un cursus par son identifiant ; rien pour un cursus inconnu (nouveau fichier JSON sans dessin). */
export const IllustrationCursus: React.FC<{ id: string; className?: string }> = ({ id, className }) => {
  const Dessin = PAR_CURSUS[id];
  return Dessin ? <Dessin className={className} /> : null;
};
