import React from 'react';

/**
 * Illustration du bandeau d'accueil sur ordinateur (maquette « Accueil » bureau) : un téléphone montrant un dossier
 * validé pièce par pièce. Couleurs par jetons fds-* : en mode sombre l'écran du téléphone passe lui aussi en sombre.
 * Décorative (le titre du bandeau dit déjà la même chose) : masquée aux lecteurs d'écran.
 */
export const IllustrationDossier: React.FC<{ className?: string }> = ({ className = '' }) => (
  <svg viewBox="0 0 400 440" aria-hidden="true" focusable="false" className={`block w-full h-auto ${className}`}>
    <circle cx="200" cy="230" r="190" className="fill-white/[0.06]" />
    <circle cx="330" cy="90" r="34" className="fill-fds-gold" />
    <g transform="translate(110 30)">
      <rect x="0" y="0" width="180" height="370" rx="26" className="fill-fds-navy-d" />
      <rect x="8" y="10" width="164" height="350" rx="20" className="fill-fds-page" />
      <rect x="8" y="10" width="164" height="44" rx="20" className="fill-fds-navy" />
      <rect x="8" y="34" width="164" height="20" className="fill-fds-navy" />
      <rect x="20" y="26" width="60" height="8" rx="4" className="fill-white" />
      <rect x="20" y="70" width="140" height="44" rx="8" className="fill-fds-surface stroke-fds-line" />
      <text x="30" y="88" fontSize="9" className="fill-fds-mute font-fds-sans">
        Dossier
      </text>
      <text x="30" y="106" fontSize="14" fontWeight="700" className="fill-fds-title font-fds-serif">
        CAN-2026-0089
      </text>
      <rect x="20" y="126" width="140" height="8" rx="4" className="fill-fds-line" />
      <rect x="20" y="126" width="84" height="8" rx="4" className="fill-fds-accent" />
      <g className="fill-fds-surface stroke-fds-line">
        <rect x="20" y="148" width="140" height="34" rx="8" />
        <rect x="20" y="190" width="140" height="34" rx="8" />
        <rect x="20" y="232" width="140" height="34" rx="8" />
        <rect x="20" y="274" width="140" height="34" rx="8" />
      </g>
      <g className="fill-fds-ok-solid">
        <circle cx="38" cy="165" r="9" />
        <circle cx="38" cy="207" r="9" />
      </g>
      <g fill="none" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="stroke-white">
        <path d="M33 165l3.5 3.5L43 161" />
        <path d="M33 207l3.5 3.5L43 203" />
      </g>
      <g fill="none" strokeWidth="2" className="stroke-fds-accent">
        <circle cx="38" cy="249" r="9" />
        <circle cx="38" cy="291" r="9" />
      </g>
      <g className="fill-fds-line">
        <rect x="56" y="160" width="70" height="8" rx="4" />
        <rect x="56" y="202" width="86" height="8" rx="4" />
        <rect x="56" y="244" width="60" height="8" rx="4" />
        <rect x="56" y="286" width="76" height="8" rx="4" />
      </g>
      <rect x="20" y="322" width="140" height="26" rx="8" className="fill-fds-gold" />
    </g>
    <g transform="translate(262 250)">
      <circle cx="40" cy="40" r="40" className="fill-fds-ok-solid" />
      <path d="M22 41l13 13 24-26" fill="none" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round" className="stroke-white" />
    </g>
  </svg>
);
