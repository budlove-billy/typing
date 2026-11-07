/* Playgama 허브(/arcade/) 동작 — 설정은 assets/playgama-config.js 하나에서 읽는다.
   원칙(파트너 약관): 게임은 사용자가 '플레이'를 눌러야만 불러온다 · 게임/위젯/브랜딩은 손대지 않는다 ·
   말로우의 미션·연속 기록·메달·공유와 엮지 않는다(이 파일은 그런 함수를 부르지 않고 저장소도 쓰지 않는다). */
(function(){
  'use strict';
  var C = window.PLAYGAMA || {};
  var LIVE = !!(C.enabled && C.clid);
  var lang = (document.documentElement.lang || 'ko').slice(0, 2);
  var T = {
    ko: { loading:'게임을 불러오는 중…', fail:'게임을 불러오지 못했어요. 잠시 후 다시 시도하거나 다른 게임을 골라 보세요.', retry:'다시 시도', close:'닫기 ✕' },
    en: { loading:'Loading the game…', fail:"The game didn't load. Try again in a moment or pick another game.", retry:'Try again', close:'Close ✕' },
    th: { loading:'กำลังโหลดเกม…', fail:'โหลดเกมไม่สำเร็จ ลองใหม่อีกครั้งหรือเลือกเกมอื่น', retry:'ลองใหม่', close:'ปิด ✕' }
  }[lang] || null;
  if (!T) T = { loading:'Loading…', fail:'Failed to load.', retry:'Retry', close:'Close' };
  var TIMEOUT_MS = 15000;
  function track(name, params){ try{ if (typeof gtag === 'function') gtag('event', name, params || {}); }catch(e){} }

  var list = document.getElementById('pg-games'), off = document.getElementById('pg-off');
  var games = {}; (C.games || []).forEach(function(g){ if (g && g.id) games[g.id] = g; });

  // 꺼져 있으면(킬 스위치) 목록을 통째로 지우고 '준비 중'만 보인다 — 빌드를 다시 하지 않아도 즉시 적용된다.
  if (!LIVE) { if (list) list.remove(); if (off) off.hidden = false; track('pg_hub_view', { enabled: 0, game_count: 0, lang: lang }); return; }
  if (off) off.hidden = true;
  if (!list) return;

  // 설정에서 빠졌거나 꺼진 게임은 카드째 지운다(Playgama가 게임을 내리면 여기서 바로 반영).
  var cards = Array.prototype.slice.call(list.querySelectorAll('.pg-card'));
  cards.forEach(function(card){ var g = games[card.dataset.id]; if (!g || g.enabled === false || !g.url) card.remove(); });
  cards = Array.prototype.slice.call(list.querySelectorAll('.pg-card'));
  if (!cards.length) { list.remove(); if (off) off.hidden = false; }
  track('pg_hub_view', { enabled: 1, game_count: cards.length, lang: lang });

  var open = null;   // { card, stage, timer, t0, id }
  function closeOpen(reason){
    if (!open) return;
    var o = open; open = null; clearTimeout(o.timer);
    track('pg_close', { game: o.id, sec: Math.round((Date.now() - o.t0) / 1000), reason: reason || 'close' });
    o.stage.innerHTML = ''; o.stage.hidden = true; o.card.classList.remove('is-open');
    var poster = o.card.querySelector('.pg-poster'); if (poster) poster.hidden = false;
  }
  function fallback(o, reason){
    track('pg_fallback', { game: o.id, reason: reason });
    var box = document.createElement('div'); box.className = 'pg-fail'; box.setAttribute('role', 'alert');
    var p = document.createElement('p'); p.textContent = T.fail; box.appendChild(p);
    var again = document.createElement('button'); again.type = 'button'; again.className = 'pg-btn'; again.textContent = T.retry;
    again.onclick = function(){ var card = o.card; closeOpen('retry'); play(card); };
    box.appendChild(again);
    o.stage.querySelector('.pg-frame-wrap').appendChild(box);
  }
  function play(card, from){
    var id = card.dataset.id, g = games[id]; if (!g) return;
    if (open && open.card === card) return;
    closeOpen('switch');
    var stage = card.querySelector('.pg-stage'), poster = card.querySelector('.pg-poster');
    stage.innerHTML = '';
    var bar = document.createElement('div'); bar.className = 'pg-bar';
    var x = document.createElement('button'); x.type = 'button'; x.className = 'pg-close'; x.textContent = T.close;
    x.onclick = function(){ closeOpen('close'); poster && poster.focus && poster.focus(); };
    bar.appendChild(x); stage.appendChild(bar);
    var wrap = document.createElement('div'); wrap.className = 'pg-frame-wrap';
    var wait = document.createElement('div'); wait.className = 'pg-wait'; wait.textContent = T.loading; wrap.appendChild(wait);
    var f = document.createElement('iframe');
    f.src = g.url; f.title = card.querySelector('h3') ? card.querySelector('h3').textContent : id;
    f.setAttribute('allow', 'fullscreen'); f.setAttribute('allowfullscreen', ''); f.setAttribute('frameborder', '0');
    var o = { card: card, stage: stage, id: id, t0: Date.now(), timer: 0 };
    f.addEventListener('load', function(){ if (open !== o) return; clearTimeout(o.timer); wait.remove(); track('pg_iframe_load', { game: id, ms: Date.now() - o.t0 }); });
    f.addEventListener('error', function(){ if (open === o) fallback(o, 'error'); });
    wrap.appendChild(f); stage.appendChild(wrap);
    if (poster) poster.hidden = true;
    stage.hidden = false; card.classList.add('is-open'); open = o;
    o.timer = setTimeout(function(){ if (open === o && wait.isConnected) { wait.remove(); fallback(o, 'timeout'); } }, TIMEOUT_MS);
    track('pg_play_click', { game: id, lang: lang, from: from || 'hub' });
    stage.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  cards.forEach(function(card){
    var poster = card.querySelector('.pg-poster');
    if (poster) poster.addEventListener('click', function(){ play(card); });
  });
  // 홈 선반에서 게임 카드를 눌러 들어오면(#게임id, 같은 사이트에서 온 이동) 그 게임을 바로 연다 — 사용자가 그 게임을 직접 고른 클릭이다.
  // 검색·외부 링크로 #게임id에 들어오면 열지 않고 그 카드로만 데려간다(클릭 없는 로딩 금지).
  var want = decodeURIComponent((location.hash || '').slice(1));
  var target = want ? cards.filter(function(c){ return c.dataset.id === want; })[0] : null;
  if (target) {
    var fromUs = false; try { fromUs = !!document.referrer && new URL(document.referrer).origin === location.origin; } catch (e) {}
    if (fromUs) play(target, 'home'); else target.scrollIntoView({ block: 'start' });
  }
  window.addEventListener('pagehide', function(){ closeOpen('leave'); });
})();
