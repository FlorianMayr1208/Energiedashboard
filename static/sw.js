// Service Worker für PWA mit Offline-Caching
const CACHE_NAME = 'energiedashboard-v3';
const urlsToCache = [
    '/',
    '/eingabe',
    '/manifest.json',
    '/static/icon-192.png',
    '/static/icon-512.png',
    'https://cdn.jsdelivr.net/npm/chart.js',
    'https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns'
];

// Installation: Cache wichtige Dateien
self.addEventListener('install', (event) => {
    console.log('Service Worker: Installation...');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Service Worker: Dateien werden gecacht');
                return cache.addAll(urlsToCache.map(url => new Request(url, { cache: 'reload' })))
                    .catch(err => {
                        console.warn('Service Worker: Einige Dateien konnten nicht gecacht werden', err);
                    });
            })
    );
    self.skipWaiting();
});

// Aktivierung: Alte Caches löschen
self.addEventListener('activate', (event) => {
    console.log('Service Worker: Aktivierung...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Service Worker: Alter Cache wird gelöscht', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    return self.clients.claim();
});

// Fetch: Network-First-Strategie (für dynamische Daten)
self.addEventListener('fetch', (event) => {
    event.respondWith(
        fetch(event.request)
            .then((response) => {
                // Wenn erfolgreich, speichere im Cache
                if (response && response.status === 200) {
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseClone);
                    });
                }
                return response;
            })
            .catch(() => {
                // Bei Fehler (offline), versuche aus Cache zu laden
                return caches.match(event.request)
                    .then((cachedResponse) => {
                        if (cachedResponse) {
                            console.log('Service Worker: Aus Cache geladen', event.request.url);
                            return cachedResponse;
                        }
                        // Fallback für Offline-Seite
                        return caches.match('/');
                    });
            })
    );
});
