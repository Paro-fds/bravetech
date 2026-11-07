// Service Worker FDS Portail — Installation PWA (Android / iOS / Bureau)
// Stratégie « réseau d'abord » : garantit des données et un code toujours à jour,
// avec repli hors ligne sur la coquille de l'application en cas de coupure mobile.
// Règle absolue (AGENTS.md) : aucun appel `/api/` n'est jamais mis en cache.

const CACHE_COQUILLE = 'fds-portail-v1';
const FICHIERS_COQUILLE = ['/', '/manifest.webmanifest', '/logo-fds.png', '/icon-192.png', '/icon-512.png'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(CACHE_COQUILLE)
      .then((cache) => cache.addAll(FICHIERS_COQUILLE))
      .catch(() => undefined),
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((cles) => Promise.all(cles.filter((c) => c !== CACHE_COQUILLE).map((c) => caches.delete(c))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin || url.pathname.startsWith('/api/')) return;

  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((reponse) => {
          const copie = reponse.clone();
          caches.open(CACHE_COQUILLE).then((cache) => cache.put('/', copie)).catch(() => undefined);
          return reponse;
        })
        .catch(() => caches.match('/')),
    );
    return;
  }

  event.respondWith(
    fetch(request)
      .then((reponse) => {
        if (reponse.ok) {
          const copie = reponse.clone();
          caches.open(CACHE_COQUILLE).then((cache) => cache.put(request, copie)).catch(() => undefined);
        }
        return reponse;
      })
      .catch(() => caches.match(request)),
  );
});

