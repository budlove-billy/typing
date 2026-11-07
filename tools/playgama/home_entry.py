# -*- coding: utf-8 -*-
"""홈 로비 '쉬어가는 게임' 선반 (index.html). 여러 번 실행해도 된다.
v2 (2026-11-08, 사용자: '광고 자리 같은 카드라 눈에 안 띈다 → 게임 목록처럼 그림 + 전체 보기'):
- 오늘의 퍼즐 바로 아래에 [🎮 쉬어가는 게임 · 외부 게임 · 전체 보기 ›] 제목 + 게임 그림 카드 가로 선반.
- 카드를 누르면 해당 언어 허브(/arcade/…#게임id)로 가서 그 게임이 바로 열린다(사용자가 그 게임을 직접 고른 클릭).
- 그림·주소·이름은 assets/playgama-config.js(PLAYGAMA, PLAYGAMA_NAMES)에서만 읽는다. 꺼져 있으면 섹션 전체가 hidden.
- 그 자리에서 동기로 그려 첫 화면 뒤 밀림이 없다. 미션·연속 기록·추천 목록과 엮지 않는다(GA4 pg_entry_click만).
v1(능력별 아래 가로 카드 #lb-pg)이 있으면 지운다."""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'daily-redesign'))
from _patch import Patch

p = Patch(os.path.join(ROOT, 'index.html'))
nl = p.nl

# ---- v1 걷어내기 ----
if 'id="lb-pg"' in p.s:
    p.s = re.sub(r'/\* 쉬어가는 게임\(Playgama\) 진입 카드[^\n]*\n(?:\.lb-pg[^\n]*\n)+', '', p.s)
    p.s = re.sub(r'  <script src="/assets/playgama-config\.js\?v=1"></script>\r?\n  <a class="lb-pg" id="lb-pg"[^\n]*\n  <script>\(function\(\)\{var c=window\.PLAYGAMA[^\n]*\n', '', p.s)
    p.s = re.sub(r'  "pg\.entry\.(?:title|ext|sub)":[^\n]*\n', '', p.s)
    p.s = re.sub(r'// 쉬어가는 게임\(Playgama\) 진입[^\n]*\nfunction pgEntryClick\(a\)\{\r?\n(?:[^\n]*\n){2}\}\r?\n', '', p.s)
    assert 'lb-pg"' not in p.s and 'pgEntryClick' not in p.s, 'v1 leftovers'

if 'id="lb-pgsec"' in p.s: p.save(); print('v2 already applied'); sys.exit()

# ---- v2 ----
p.R('.lb-me{display:grid;grid-template-columns:1fr 1fr;gap:.6rem}',
    '.lb-me{display:grid;grid-template-columns:1fr 1fr;gap:.6rem}\n'
    '/* 쉬어가는 게임(Playgama) 선반 — assets/playgama-config.js가 켜져 있을 때만 보인다 */\n'
    '.lb-pgsec{margin-top:1.4rem;border-radius:24px;padding:.2rem 1rem 1rem;background:linear-gradient(160deg,#0f4a5e,#13284f);border:2px solid rgba(120,230,255,.5);box-shadow:0 14px 30px rgba(0,0,0,.4)}\n'
    '.lb-pgsec[hidden]{display:none}\n'
    '.lb-pgsec .lb-h2{margin-top:1rem}\n'
    '.lb-pgx{font-style:normal;font-size:.7rem;font-weight:800;color:#a5e6ff;border:1px solid rgba(165,230,255,.55);border-radius:6px;padding:.08rem .38rem;line-height:1.3}\n'
    '.lb-pgsec .lb-more{color:#a5e6ff;text-decoration:none}\n'
    '.lb-pgsec .lb-shelf{margin:0 -.2rem;padding-bottom:.2rem}\n'
    '.lb-shelf>.lb-card.lb-pgc{flex:0 0 168px;width:168px;text-decoration:none}\n'
    '.lb-pgc .lb-play-i{position:absolute;top:.45rem;right:.45rem;z-index:2;width:1.9rem;height:1.9rem;border-radius:50%;display:grid;place-items:center;font-size:.8rem;background:rgba(40,70,200,.9);box-shadow:0 2px 6px rgba(0,0,0,.4)}\n'
    '.lb-pgsub{margin:.55rem .15rem 0;color:#bfe6f5;font-size:.84rem}')

p.R('  <p class="lb-count" id="lb-count">&nbsp;</p>\n',
    '  <p class="lb-count" id="lb-count">&nbsp;</p>\n'
    '  <script src="/assets/playgama-config.js?v=2"></script>\n'
    '  <section class="lb-pgsec" id="lb-pgsec" hidden aria-labelledby="lb-pg-title">\n'
    '    <h2 class="lb-h2">🎮 <span id="lb-pg-title" data-i18n="pg.title">쉬어가는 게임</span><em class="lb-pgx" data-i18n="pg.ext">외부 게임</em><a class="lb-more" id="lb-pg-all" href="/arcade/" onclick="pgEntry(\'all\')" data-i18n="lb.all">전체 보기 ›</a></h2>\n'
    '    <div class="lb-shelf" id="lb-pgshelf"></div>\n'
    '    <p class="lb-pgsub" data-i18n="pg.sub">두뇌게임 사이 머리 식히기 · 설치 없이 바로 · Playgama 제공</p>\n'
    '  </section>\n'
    '  <script>pgShelf();</script>\n')

p.R('  "nav.exit": {ko:"홈", en:"Home", th:"หน้าแรก"},',
    '  "nav.exit": {ko:"홈", en:"Home", th:"หน้าแรก"},\n'
    '  "pg.title": {ko:"쉬어가는 게임", en:"Take a Break", th:"เกมพักสมอง"},\n'
    '  "pg.ext": {ko:"외부 게임", en:"External", th:"เกมภายนอก"},\n'
    '  "pg.sub": {ko:"두뇌게임 사이 머리 식히기 · 설치 없이 바로 · Playgama 제공", en:"Unwind between brain games · no install · by Playgama", th:"พักสมองระหว่างเกมฝึกสมอง · ไม่ต้องติดตั้ง · โดย Playgama"},')

# 선반 그리기 — 본문 첫 <script>보다 앞(마크업 바로 뒤)에서 불리므로 head에 둔다
p.R('<script async src="https://www.googletagmanager.com/gtag/js?id=G-9EQEH5BF0C"></script>',
    '<script async src="https://www.googletagmanager.com/gtag/js?id=G-9EQEH5BF0C"></script>\n'
    '<script>\n'
    '// 쉬어가는 게임(Playgama) 홈 선반 — 설정이 켜져 있을 때만. 언어가 바뀌면 다시 그린다(setLanguage).\n'
    'function pgLang(){ var l=(document.documentElement.lang||"ko").slice(0,2); return l==="en"||l==="th"?l:"ko"; }\n'
    'function pgHub(){ var l=pgLang(); return l==="en"?"/arcade/en":l==="th"?"/arcade/th":"/arcade/"; }\n'
    'function pgEntry(game){ try{ if(typeof gtag==="function") gtag("event","pg_entry_click",{game:game,lang:pgLang()}); }catch(e){} }\n'
    'function pgShelf(){\n'
    '  var c=window.PLAYGAMA||{}, N=window.PLAYGAMA_NAMES||{}, sec=document.getElementById("lb-pgsec"), box=document.getElementById("lb-pgshelf");\n'
    '  if(!sec||!box) return;\n'
    '  var games=(c.games||[]).filter(function(g){ return g&&g.enabled!==false&&g.url&&g.thumb&&N[g.id]; });\n'
    '  if(!(c.enabled&&c.clid&&c.homeEntry!==false)||!games.length){ sec.hidden=true; return; }\n'
    '  var l=pgLang(), hub=pgHub(); box.innerHTML="";\n'
    '  games.forEach(function(g,i){ var a=document.createElement("a"); a.className="lb-card lb-pgc"; a.href=hub+"#"+g.id;\n'
    '    a.onclick=function(){ pgEntry(g.id); };\n'
    '    var img=document.createElement("img"); img.className="lb-img"; img.src=g.thumb; img.alt=""; img.width=240; img.height=135; img.decoding="async"; if(i>2) img.loading="lazy";\n'
    '    var nm=document.createElement("span"); nm.className="lb-name"; nm.textContent=N[g.id][l]||N[g.id].ko;\n'
    '    var pl=document.createElement("i"); pl.className="lb-play-i"; pl.setAttribute("aria-hidden","true"); pl.textContent="▶";\n'
    '    a.appendChild(img); a.appendChild(pl); a.appendChild(nm); box.appendChild(a); });\n'
    '  var all=document.getElementById("lb-pg-all"); if(all) all.href=hub;\n'
    '  sec.hidden=false;\n'
    '}\n'
    '</script>')

p.R('  applyLanguage();\n  syncLanguageSEO(lang,!!syncUrl);\n',
    '  applyLanguage();\n  syncLanguageSEO(lang,!!syncUrl);\n  try{ pgShelf(); }catch(e){}\n')
p.save()
