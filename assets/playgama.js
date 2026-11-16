/* Playgama 허브(/arcade/) 동작 — 설정은 assets/playgama-config.js 하나에서 읽는다.
   원칙(파트너 약관): 게임은 사용자가 '플레이'를 눌러야만 불러온다 · 게임/위젯/브랜딩은 손대지 않는다 ·
   말로우의 미션·연속 기록·메달·공유와 엮지 않는다(이 파일은 그런 함수를 부르지 않고 저장소도 쓰지 않는다). */
(function(){
  'use strict';
  var C = window.PLAYGAMA || {};
  var LIVE = !!(C.enabled && C.clid);
  var lang = (document.documentElement.lang || 'ko').slice(0, 2);
  var T = {
    ko: { loading:'게임을 불러오는 중…', fail:'게임을 불러오지 못했어요. 잠시 후 다시 시도하거나 다른 게임을 골라 보세요.', retry:'다시 시도', close:'닫기 ✕', full:'⛶ 전체 화면', exitFull:'✕ 전체 화면 끝내기' },
    en: { loading:'Loading the game…', fail:"The game didn't load. Try again in a moment or pick another game.", retry:'Try again', close:'Close ✕', full:'⛶ Full screen', exitFull:'✕ Exit full screen' },
    th: { loading:'กำลังโหลดเกม…', fail:'โหลดเกมไม่สำเร็จ ลองใหม่อีกครั้งหรือเลือกเกมอื่น', retry:'ลองใหม่', close:'ปิด ✕', full:'⛶ เต็มจอ', exitFull:'✕ ออกจากเต็มจอ' }
  }[lang] || null;
  if (!T) T = { loading:'Loading…', fail:'Failed to load.', retry:'Retry', close:'Close', full:'Full screen', exitFull:'Exit full screen' };
  // 전체 화면(2026-11-16): 브라우저 전체 화면을 먼저 쓰고, 안 되는 곳(아이폰 사파리 등)은 화면을 꽉 채우는 덮개로 대신한다.
  function fsEl(){ return document.fullscreenElement || document.webkitFullscreenElement || null; }
  function enterFull(wrap){
    var req = wrap.requestFullscreen || wrap.webkitRequestFullscreen;
    if (req) { try { var r = req.call(wrap); if (r && r.catch) r.catch(function(){ wrap.classList.add('pg-max'); }); return; } catch (e) {} }
    wrap.classList.add('pg-max'); document.documentElement.classList.add('pg-noscroll');
  }
  function exitFull(wrap){
    if (fsEl()) { var ex = document.exitFullscreen || document.webkitExitFullscreen; try { ex && ex.call(document); } catch (e) {} }
    if (wrap) wrap.classList.remove('pg-max'); document.documentElement.classList.remove('pg-noscroll');
  }
  var TIMEOUT_MS = 15000;
  function track(name, params){ try{ if (typeof gtag === 'function') gtag('event', name, params || {}); }catch(e){} }

  var list = document.getElementById('pg-games'), off = document.getElementById('pg-off');
  var games = {}; (C.games || []).forEach(function(g){ if (g && g.id) games[g.id] = g; });
  function qsa(sel){ return Array.prototype.slice.call(document.querySelectorAll(sel)); }
  function ok(id){ var g = games[id]; return !!(g && g.enabled !== false && g.url); }
  var cards = qsa('.pg-card'), tiles = qsa('.ag-card[data-id]');
  var isGame = cards.length > 0;   // 게임별 하위 페이지인지(허브는 그림 카드 목록만 있다)
  var view = isGame ? 'pg_game_view' : 'pg_hub_view';
  var fromUs = false; try { fromUs = !!document.referrer && new URL(document.referrer).origin === location.origin; } catch (e) {}
  var want = decodeURIComponent((location.hash || '').slice(1));

  // 꺼져 있으면(킬 스위치) 게임·목록을 통째로 지우고 '준비 중'만 보인다 — 빌드를 다시 하지 않아도 즉시 적용된다.
  if (!LIVE) {
    if (list) list.remove(); cards.concat(tiles).forEach(function(n){ n.remove(); });
    if (off) off.hidden = false; track(view, { enabled: 0, game_count: 0, lang: lang }); return;
  }
  if (off) off.hidden = true;

  // 설정에서 빠졌거나 꺼진 게임은 그 카드를 지운다(Playgama가 게임을 내리면 여기서 바로 반영).
  tiles.forEach(function(t){ if (!ok(t.dataset.id)) t.remove(); else t.addEventListener('click', function(){ track('pg_tile_click', { game: t.dataset.id, from: isGame ? 'game' : 'hub', lang: lang }); }); });
  cards.forEach(function(c){ if (!ok(c.dataset.id)) c.remove(); });
  cards = qsa('.pg-card');
  if (isGame && !cards.length && off) off.hidden = false;
  if (list && !list.querySelector('.ag-card')) { list.remove(); if (off) off.hidden = false; }

  // 허브 분류 칩 — 보이는 카드만 거른다(저장 없음).
  qsa('.chips .chip').forEach(function(chip){
    chip.addEventListener('click', function(){
      var c = chip.dataset.cat;
      qsa('.chips .chip').forEach(function(x){ x.classList.toggle('on', x === chip); });
      qsa('#pg-games .ag-card').forEach(function(t){ t.hidden = !(c === 'all' || t.dataset.cat === c); });
      track('pg_chip', { cat: c, lang: lang });
    });
  });

  // 예전 주소(/arcade/#게임id)는 그 게임 페이지로 옮긴다. 같은 사이트에서 온 경우만 바로 열기(#play)를 붙인다.
  if (!isGame && want && want !== 'play' && list) {
    var t0 = list.querySelector('.ag-card[data-id="' + want.replace(/[^a-z0-9-]/g, '') + '"]');
    if (t0) { location.replace(t0.getAttribute('href').split('#')[0] + (fromUs ? '#play' : '')); return; }
  }
  track(view, { enabled: 1, game_count: isGame ? cards.length : qsa('#pg-games .ag-card').length, lang: lang, game: isGame && cards[0] ? cards[0].dataset.id : '' });

  var open = null;   // { card, stage, timer, t0, id }
  function closeOpen(reason){
    if (!open) return;
    var o = open; open = null; clearTimeout(o.timer);
    track('pg_close', { game: o.id, sec: Math.round((Date.now() - o.t0) / 1000), reason: reason || 'close' });
    exitFull(o.stage.querySelector('.pg-frame-wrap'));
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
    var fs = document.createElement('button'); fs.type = 'button'; fs.className = 'pg-btn pg-fs'; fs.textContent = T.full;
    bar.appendChild(fs); bar.appendChild(x); stage.appendChild(bar);
    var wrap = document.createElement('div'); wrap.className = 'pg-frame-wrap';
    var wait = document.createElement('div'); wait.className = 'pg-wait'; wait.textContent = T.loading; wrap.appendChild(wait);
    var f = document.createElement('iframe');
    f.src = g.url; f.title = card.querySelector('h3') ? card.querySelector('h3').textContent : id;
    f.setAttribute('allow', 'fullscreen'); f.setAttribute('allowfullscreen', ''); f.setAttribute('frameborder', '0');
    var o = { card: card, stage: stage, id: id, t0: Date.now(), timer: 0 };
    f.addEventListener('load', function(){ if (open !== o) return; clearTimeout(o.timer); wait.remove(); track('pg_iframe_load', { game: id, ms: Date.now() - o.t0 }); });
    f.addEventListener('error', function(){ if (open === o) fallback(o, 'error'); });
    var out = document.createElement('button'); out.type = 'button'; out.className = 'pg-fs-out'; out.textContent = '✕'; out.setAttribute('aria-label', T.exitFull); out.title = T.exitFull;  // 게임 메뉴(위쪽 양 끝)를 가리지 않게 위 가운데 작은 ✕만
    out.onclick = function(){ exitFull(wrap); };
    fs.onclick = function(){ enterFull(wrap); track('pg_fullscreen', { game: id }); };
    wrap.appendChild(f); wrap.appendChild(out); stage.appendChild(wrap);
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
  // 목록·홈에서 게임 카드를 눌러 들어오면(#play, 같은 사이트에서 온 이동) 그 게임을 바로 연다 — 사용자가 그 게임을 직접 고른 클릭이다.
  // 검색·외부 링크로 #play를 달고 와도 열지 않는다(클릭 없는 로딩 금지).
  if (isGame && want === 'play' && fromUs && cards[0]) play(cards[0], 'list');
  window.addEventListener('pagehide', function(){ closeOpen('leave'); });
})();
