// Mallow PWA service worker — HTML은 network-first(항상 최신), 정적 자산은 cache-first
const CACHE = 'mallow-v5';
const ASSETS = ['./', 'index.html', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png', 'favicon-32.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith('mallow-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  const url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== self.location.origin) return;
  const isHTML = req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html');
  if (isHTML) {
    // network-first: 최신 앱 우선, 오프라인이면 캐시
    e.respondWith(
      fetch(req).then(async res => { if(res.status>=500) throw new Error('server unavailable'); if(res.ok){ const c=await caches.open(CACHE); await c.put(req,res.clone()); } return res; })
        .catch(async () => {
          const cached=await caches.match(req); if(cached) return cached;
          if(['/', '/index.html', '/en', '/th'].includes(url.pathname)){ const app=await caches.match('index.html'); if(app) return app; }
          return new Response('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Offline · Mallow</title><h1>인터넷 연결이 필요해요 · You are offline</h1><p>연결 후 다시 시도해주세요.</p><a href="/">홈 · Home</a></html>',{status:503,headers:{'Content-Type':'text/html; charset=utf-8'}});
        })
    );
  } else {
    // cache-first: 아이콘/매니페스트
    const fresh=fetch(req).then(async res=>{ if(res.ok){ const c=await caches.open(CACHE); await c.put(req,res.clone()); } return res; });
    e.waitUntil(fresh.catch(()=>{}));
    e.respondWith(caches.match(req).then(r=>r||fresh));
  }
});
