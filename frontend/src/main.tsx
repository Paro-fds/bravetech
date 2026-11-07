import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { App } from './app';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);

// Enregistrement du Service Worker en production pour permettre l'installation PWA sur mobile
if (import.meta.env.PROD && 'serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => undefined);
  });
}
