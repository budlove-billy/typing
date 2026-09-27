# -*- coding: utf-8 -*-
"""말로우 크라운: 공용 사운드(/assets/daily-sound.js)·연출(/assets/daily-fx.js) 연결 (1회용, 기록용)"""
import os, sys; sys.path.insert(0, os.path.dirname(__file__)); from _patch import Patch
p = Patch(os.path.join(os.path.dirname(__file__), '..', '..', 'queens', 'index.html')); R = p.R
R('<canvas id="shareCanvas"', '<script src="/assets/daily-sound.js"></script>\n<script src="/assets/daily-fx.js"></script>\n<canvas id="shareCanvas"')
R('<button id="muteBtn" onclick="toggleMute()"', '<button id="muteBtn" onclick="toggleMute(event)"')
p.between('/* ===== 사운드 + 햅틱 ===== */', '/* ===== i18n ===== */', '''/* ===== 사운드 + 햅틱 — /assets/daily-sound.js(공용 엔진). 🔊 = 켜기/끄기·음악·효과음 음량 패널 ===== */
function crownCount(){ let n=0; for(let r=0;r<N;r++)for(let c=0;c<N;c++) if(ST[r][c]===2) n++; return n; }
function sndLevel(){ const n=crownCount(); DS.level(n>=N-1?2:n>=Math.ceil(N/2)?1:0); }   // 끝이 가까울수록 음악이 쌓인다
function muteIcon(){ const b=document.getElementById('muteBtn'); if(b) b.textContent=DS.on()?'🔊':'🔇'; }
function toggleMute(ev){ if(ev) ev.stopPropagation(); DS.panel(document.getElementById('muteBtn'),LANG,muteIcon); }

''')
R("""    d.innerHTML = s===2?CROWN_SVG:(s===1?'<span class="x">✕</span>':'');""",
  """    if(d._s!==s){ d._s=s; d.innerHTML = s===2?CROWN_SVG:(s===1?'<span class="x">✕</span>':''); }   // 바뀐 칸만 다시 그려 등장 연출이 새 왕관에만 나온다""")
R("""  if(ns===2){ conflicts().has(r*N+c)?sndBad():sndPlace(); } else if(ns===1){ sndMark(); } else { sndCancel(); }
  checkWin(); }""", """  if(!DS.playing()) DS.bgm('royal');
  if(ns===2){ if(conflicts().has(r*N+c)) DS.play('bad'); else { DS.play('crown',crownCount()); const el=document.querySelector('#board .cell[data-r="'+r+'"][data-c="'+c+'"]'); if(el){ const q=DFX.center(el); DFX.burst(q[0],q[1],['#ffd66b','#fff3c4','#ff8fb1'],10); } } }
  else if(ns===1){ DS.play('mark'); } else { DS.play('erase'); }
  sndLevel(); checkWin(); }""")
R("""  WON=true; if(tick)clearInterval(tick); const t=fmt(Date.now()-startT); sndWin();""",
  """  WON=true; if(tick)clearInterval(tick); const t=fmt(Date.now()-startT);
  DS.stop(); DS.play('win'); DFX.cascade(document.querySelectorAll('#board .cell'),'glow',Math.round(560/(N*N))); setTimeout(()=>DFX.confetti(),560);   // 판이 물결처럼 빛난 뒤(0.56초) 팡파르·색종이""")
R("""  document.getElementById('newBtn').onclick=()=>newPuzzle(false);""", """  document.getElementById('newBtn').onclick=()=>{ DS.play('new'); newPuzzle(false); };""")
R("""  document.getElementById('againBtn').onclick=()=>newPuzzle(false);""", """  document.getElementById('againBtn').onclick=()=>{ DS.play('new'); newPuzzle(false); };""")
R("""b.onclick=()=>{N=n;renderSizes();newPuzzle(DAILY);};""", """b.onclick=()=>{N=n;DS.play('ui');renderSizes();newPuzzle(DAILY);};""")
R("""document.getElementById('clearBtn').onclick=()=>{ if(WON)return; ST=Array.from({length:N},()=>new Array(N).fill(0)); paint(); };""",
  """document.getElementById('clearBtn').onclick=()=>{ if(WON)return; ST=Array.from({length:N},()=>new Array(N).fill(0)); paint(); DS.play('clear'); sndLevel(); };""")
R("""document.getElementById('muteBtn').textContent=MUTED?'🔇':'🔊';""", """muteIcon();""")
R("""const d=document.createElement('div'); d.className='cell'; d.style.background=REGCOL[REGION[r][c]%REGCOL.length];""",
  """const d=document.createElement('div'); d.className='cell'; d.style.backgroundColor=REGCOL[REGION[r][c]%REGCOL.length];   // backgroundColor — 입체감 그라데이션(CSS)을 덮지 않게""")
p.save()
