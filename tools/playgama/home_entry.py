# -*- coding: utf-8 -*-
"""홈 로비에 '쉬어가는 게임' 진입 카드 1개 추가 (index.html, 한 번만 실행).
- assets/playgama-config.js를 카드 바로 앞에서 동기로 불러, 켜져 있을 때만 그 자리에서 보이게 한다(첫 화면 뒤 밀림 없음).
- 꺼져 있으면(enabled=false·clid 비어 있음·homeEntry=false) 카드는 hidden 그대로 — 아무것도 그려지지 않는다.
- 미션·연속 기록·추천 목록(HOME_GAMES)과 엮지 않는다. 클릭 시 GA4 이벤트 pg_entry_click만 남긴다."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'daily-redesign'))
from _patch import Patch

p = Patch(os.path.join(ROOT, 'index.html'))
if 'id="lb-pg"' in p.s: print('already applied'); sys.exit()

# 1) 스타일 — 로비 톤(어두운 보라)에 맞춘 가로 카드
p.R('.lb-me{display:grid;grid-template-columns:1fr 1fr;gap:.6rem}',
    '.lb-me{display:grid;grid-template-columns:1fr 1fr;gap:.6rem}\n'
    '/* 쉬어가는 게임(Playgama) 진입 카드 — assets/playgama-config.js가 켜져 있을 때만 보인다 */\n'
    '.lb-pg{display:flex;align-items:center;gap:.8rem;margin-top:1.1rem;padding:.85rem 1rem;border-radius:18px;text-decoration:none;color:#fff;background:linear-gradient(135deg,#123a5c,#1d5a6e);border:1px solid rgba(140,220,255,.3);box-shadow:0 8px 20px rgba(0,0,0,.28)}\n'
    '.lb-pg[hidden]{display:none}\n'
    '.lb-pg-i{flex:0 0 2.6rem;height:2.6rem;border-radius:12px;display:grid;place-items:center;font-size:1.45rem;background:rgba(255,255,255,.12)}\n'
    '.lb-pg-t{flex:1;min-width:0;line-height:1.4}\n'
    '.lb-pg-t b{display:block;font-size:1.02rem;font-weight:900}\n'
    '.lb-pg-t span{display:block;font-size:.84rem;color:#cdeaf5}\n'
    '.lb-pg-t b span{display:inline}\n'
    '.lb-pg-t b .lb-pg-x{display:inline-block;font-size:.72rem;font-weight:800;color:#9fd2e6;border:1px solid rgba(159,210,230,.5);border-radius:6px;padding:.05rem .35rem;margin-left:.4rem;vertical-align:.12rem;line-height:1.3}\n'
    '.lb-pg-go{font-weight:900;color:#9fe3ff}')

# 2) 마크업 — '능력별로 골라 하기' 선반 바로 뒤
p.R('  <div class="lb-shelf" id="lb-abil"></div>\n',
    '  <div class="lb-shelf" id="lb-abil"></div>\n'
    '  <script src="/assets/playgama-config.js?v=1"></script>\n'
    '  <a class="lb-pg" id="lb-pg" href="/arcade/" hidden onclick="pgEntryClick(this)"><span class="lb-pg-i" aria-hidden="true">🎮</span>'
    '<span class="lb-pg-t"><b><span data-i18n="pg.entry.title">쉬어가는 게임</span><span class="lb-pg-x" data-i18n="pg.entry.ext">외부 게임</span></b>'
    '<span data-i18n="pg.entry.sub">두뇌게임 사이 머리 식히기 · 말로우가 고른 8가지</span></span><span class="lb-pg-go" aria-hidden="true">›</span></a>\n'
    '  <script>(function(){var c=window.PLAYGAMA||{};if(c.enabled&&c.clid&&c.homeEntry!==false){var a=document.getElementById(\'lb-pg\');if(a)a.hidden=false;}})();</script>\n')

# 3) 문구
p.R('  "nav.exit": {ko:"홈", en:"Home", th:"หน้าแรก"},',
    '  "nav.exit": {ko:"홈", en:"Home", th:"หน้าแรก"},\n'
    '  "pg.entry.title": {ko:"쉬어가는 게임", en:"Take a Break", th:"เกมพักสมอง"},\n'
    '  "pg.entry.ext": {ko:"외부 게임", en:"External", th:"เกมภายนอก"},\n'
    '  "pg.entry.sub": {ko:"두뇌게임 사이 머리 식히기 · 말로우가 고른 8가지", en:"Unwind between brain games · 8 picks by Mallow", th:"พักสมองระหว่างเกมฝึกสมอง · 8 เกมที่ Mallow คัดมา"},')

# 4) 클릭 — 언어별 허브로 보내고 이벤트만 남긴다
p.R('function setLanguage(lang,syncUrl){',
    '// 쉬어가는 게임(Playgama) 진입 — 언어별 허브 주소로 바꾸고 이벤트만 기록(미션·기록과 무관)\n'
    'function pgEntryClick(a){\n'
    "  a.href = CURRENT_LANG==='en' ? '/arcade/en' : CURRENT_LANG==='th' ? '/arcade/th' : '/arcade/';\n"
    "  try{ track('pg_entry_click',{lang:CURRENT_LANG}); }catch(e){}\n"
    '}\n'
    'function setLanguage(lang,syncUrl){')
p.save()
