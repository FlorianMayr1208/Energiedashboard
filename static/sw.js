// Service Worker für PWA
const CACHE_NAME = 'energiedashboard-v1';

self.addEventListener('install', (event) => {
    console.log('Service Worker installiert');
});

self.addEventListener('fetch', (event) => {
    // Einfache Fetch-Strategie ohne aggressives Caching
    event.respondWith(fetch(event.request));
});
