# -*- coding: utf-8 -*-
"""말로우 탱고: 게임 월드 스킨(낮·밤 하늘) + 그린 해·달 + 공용 사운드·연출 연결 (1회용, 기록용)"""
import os, sys; sys.path.insert(0, os.path.dirname(__file__)); from _patch import Patch
p = Patch(os.path.join(os.path.dirname(__file__), '..', '..', 'tango', 'index.html')); R = p.R
R('.seo .tlist li{font-size:12.5px;}\n</style>', '''.seo .tlist li{font-size:12.5px;}
/* ===== 게임 월드 스킨 (2026-09-28) — 낮과 밤이 갈리는 하늘. 아트 /assets/stage/tango.jpg(원본: 무한 캔버스)
   판 = 금테 두른 밤하늘 유리 위의 도톰한 타일. 처음부터 놓인 칸은 판에 새겨진 것처럼 눌려 보인다. ===== */
body{background:#241a52;}
body::before{content:"";position:fixed;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(20,12,50,.05),rgba(20,12,50,.1) 45%,rgba(20,12,50,.4)),url(/assets/stage/tango.jpg) center top/cover no-repeat;}
header{padding-bottom:12px;}
#backHome{color:#fff;background:rgba(20,14,50,.55);border:1.5px solid rgba(255,255,255,.3);box-shadow:0 3px 0 rgba(0,0,0,.35);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);}
#langSel,#muteBtn{background:rgba(20,14,50,.55);color:#fff;border:1.5px solid rgba(255,255,255,.3);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);}
#langSel option{color:#2a2140;}
h1{font-size:27px;color:#fff;text-shadow:0 3px 0 #2c1f63,0 0 18px rgba(255,190,90,.5);}
h1 .sp{background:linear-gradient(90deg,#ffc14d 0%,#ffc14d 45%,#b9c4ff 55%,#b9c4ff 100%);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none;filter:drop-shadow(0 3px 0 #2c1f63);}
.tagline{display:inline-block;margin-top:8px;padding:5px 14px;border-radius:999px;background:rgba(20,14,50,.6);color:#ffe2b0;font-weight:700;border:1px solid rgba(255,193,77,.35);}
main>.card:first-child{position:relative;background:linear-gradient(160deg,rgba(64,40,110,.84),rgba(22,20,64,.9));border:3px solid #d9a441;border-radius:22px;
  box-shadow:0 0 0 2px rgba(44,31,99,.9),0 16px 36px rgba(10,5,40,.5),inset 0 1px 0 rgba(255,255,255,.18);backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);}
.datebar{color:#ffd27a;text-shadow:0 1px 0 rgba(0,0,0,.4);}
.timer{color:#fff;font-size:15px;background:linear-gradient(180deg,#34305a,#18163a);border:2px solid #d9a441;border-radius:999px;padding:3px 13px;box-shadow:inset 0 1px 0 rgba(255,255,255,.2),0 2px 0 rgba(0,0,0,.4),0 0 12px rgba(255,190,90,.25);}
.sizes button{background:linear-gradient(180deg,#463f7c,#2a2556);color:#d6d0ff;border:1.5px solid #6a62a8;box-shadow:0 2px 0 rgba(0,0,0,.45);}
.sizes button.on{background:linear-gradient(180deg,#ffe08a,#f0b429);color:#4a2a05;border-color:#fff1c2;box-shadow:0 2px 0 #8c5a12,0 0 10px rgba(255,210,100,.45);}
#board{padding:7px;gap:5px;border-radius:15px;background:linear-gradient(135deg,#3b2a6e,#141238);border:3px solid #b98a3a;box-shadow:inset 0 2px 8px rgba(0,0,0,.6),0 6px 18px rgba(0,0,0,.35);}
.cell{background:linear-gradient(180deg,#ffffff,#eeeafc);border-radius:9px;box-shadow:inset 0 -3px 0 rgba(60,40,120,.18),inset 0 1px 0 #fff,0 1px 0 rgba(0,0,0,.25);}
.cell.given{background:linear-gradient(180deg,#bfb3ea,#d6ccf5);box-shadow:inset 0 3px 5px rgba(40,20,90,.35),inset 0 -1px 0 rgba(255,255,255,.4);}
.cell .sm{width:74%;height:auto;display:block;filter:drop-shadow(0 2px 1px rgba(40,20,80,.25));}
.cell.given .sm{width:66%;opacity:.9;}
.cell .sm.pop{animation:smPop .3s cubic-bezier(.3,1.6,.5,1);}
@keyframes smPop{0%{transform:scale(.2) rotate(-40deg);opacity:0}100%{transform:scale(1) rotate(0);opacity:1}}
.cell.bad{background:linear-gradient(180deg,#ffe3ea,#ffc9d5);box-shadow:inset 0 0 0 3px #ff3b5c,0 0 12px rgba(255,59,92,.7);animation:badPulse .9s ease-in-out infinite;}
@keyframes badPulse{50%{box-shadow:inset 0 0 0 3px #ff3b5c,0 0 3px rgba(255,59,92,.3)}}
.cell.glow{animation:cellGlow .7s ease-out both;}
@keyframes cellGlow{0%{filter:brightness(1)}40%{filter:brightness(1.3) saturate(1.3);transform:scale(1.07)}100%{filter:brightness(1.05)}}
.btn{background:linear-gradient(180deg,#ffc14d,#ff7a59);box-shadow:0 4px 0 #b24a2e,0 8px 16px rgba(0,0,0,.3);text-shadow:0 1px 0 rgba(0,0,0,.25);}
.btn:active{transform:translateY(3px);box-shadow:0 1px 0 #b24a2e;}
.btn.sub{background:rgba(255,255,255,.1);color:#fff;border:1.5px solid rgba(255,255,255,.45);box-shadow:0 3px 0 rgba(0,0,0,.35);text-shadow:none;}
.won .big{font-size:26px;color:#ffd27a;text-shadow:0 2px 0 #2c1f63,0 0 16px rgba(255,200,100,.6);animation:smPop .5s cubic-bezier(.3,1.6,.5,1);}
.won .t{color:#e6e2ff;font-weight:700;}
.hint{color:#e2ddff;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:10px 12px;}
.hint b{color:#ffd27a;}
.disc{color:#b7b0dd;} .disc b{color:#e2ddff;}
.seo .card{background:rgba(255,255,255,.95);}
footer,footer a{color:#e2ddff;}
</style>''')
R('<canvas id="shareCanvas"', '<script src="/assets/daily-sound.js"></script>\n<script src="/assets/daily-fx.js"></script>\n<canvas id="shareCanvas"')
R('<button id="muteBtn" onclick="toggleMute()"', '<button id="muteBtn" onclick="toggleMute(event)"')
R("const SUN='☀️', MOON='🌙';", """const SUN='☀️', MOON='🌙';   // 공유 카드 글자용 — 판에는 아래 그림을 쓴다(이모지는 기기마다 모양이 달라 그림체와 겉돈다)
const SUN_SVG='<svg class="sm" viewBox="0 0 100 100" aria-label="sun"><g stroke="#b5561b" stroke-width="4" stroke-linejoin="round" fill="#ffb13b">'+[0,45,90,135,180,225,270,315].map(a=>'<path transform="rotate('+a+' 50 50)" d="M50 3 L58 20 L42 20 Z"/>').join('')+'</g><circle cx="50" cy="50" r="27" fill="#ffd23f" stroke="#b5561b" stroke-width="5"/><circle cx="41" cy="41" r="8" fill="#fff3b0" opacity=".8"/></svg>';
const MOON_SVG='<svg class="sm" viewBox="0 0 100 100" aria-label="moon"><path d="M62 10 A40 40 0 1 0 90 66 A31 31 0 1 1 62 10 Z" fill="#c9d2ff" stroke="#3b3a8c" stroke-width="5" stroke-linejoin="round"/><circle cx="40" cy="62" r="5" fill="#a7b2f0"/><circle cx="30" cy="44" r="3.5" fill="#a7b2f0"/><path d="M80 18 l2.5 6 6 2.5 -6 2.5 -2.5 6 -2.5 -6 -6 -2.5 6 -2.5 Z" fill="#ffe27a"/></svg>';""")
p.between('/* ===== 사운드 + 햅틱 ===== */', '/* ===== i18n ===== */', '''/* ===== 사운드 + 햅틱 — /assets/daily-sound.js(공용 엔진). 🔊 = 켜기/끄기·음악·효과음 음량 패널 ===== */
function filledRatio(){ let n=0,e=0; for(let r=0;r<N;r++)for(let c=0;c<N;c++) if(GIVEN[r][c]===-1){ e++; if(ST[r][c]!==-1) n++; } return e?n/e:1; }
function sndLevel(){ const f=filledRatio(); DS.level(f>=0.85?2:f>=0.5?1:0); }   // 판이 찰수록 음악이 쌓인다
function lineDone(r,c,bad){ let row=true,col=true;   // 방금 놓은 칸의 가로·세로줄이 규칙대로 가득 찼나(빨간 칸 없이)
  for(let i=0;i<N;i++){ if(ST[r][i]===-1||bad.has(r*N+i)) row=false; if(ST[i][c]===-1||bad.has(i*N+c)) col=false; } return row||col; }
function muteIcon(){ const b=document.getElementById('muteBtn'); if(b) b.textContent=DS.on()?'🔊':'🔇'; }
function toggleMute(ev){ if(ev) ev.stopPropagation(); DS.panel(document.getElementById('muteBtn'),LANG,muteIcon); }

''')
R("""    d.textContent=sym(ST[r][c]); d.classList.toggle('bad',bad.has(r*N+c));});""",
  """    const v=ST[r][c]; if(d._v!==v){ const first=d._v===undefined; d._v=v; d.innerHTML=v===1?SUN_SVG:(v===0?MOON_SVG:''); if(!first&&d.firstChild) d.firstChild.classList.add('pop'); }   // 바뀐 칸만 다시 그린다
    d.classList.toggle('bad',bad.has(r*N+c));});""")
R("""  if(nv===-1){ sndCancel(); } else if(conflicts().has(r*N+c)){ sndBad(); } else { nv===1?sndSun():sndMoon(); }
  checkWin(); }""", """  if(!DS.playing()) DS.bgm('sky');
  const bad=conflicts(), step=Math.floor(filledRatio()*10);
  if(nv===-1){ DS.play('erase'); } else if(bad.has(r*N+c)){ DS.play('bad'); }
  else { DS.play(nv===1?'sun':'moon',step); if(lineDone(r,c,bad)) DS.play('line');
    const el=document.querySelector('#board .cell[data-r="'+r+'"][data-c="'+c+'"]'); if(el){ const q=DFX.center(el); DFX.burst(q[0],q[1],nv===1?['#ffd23f','#ffb13b','#fff3b0']:['#c9d2ff','#8f9cff','#ffe27a'],8); } }
  sndLevel(); checkWin(); }""")
R("""  WON=true; if(tick)clearInterval(tick); const t=fmt(Date.now()-startT); sndWin();""",
  """  WON=true; if(tick)clearInterval(tick); const t=fmt(Date.now()-startT);
  DS.stop(); DS.play('win'); DFX.cascade(document.querySelectorAll('#board .cell'),'glow',Math.round(560/(N*N))); setTimeout(()=>DFX.confetti(['#ffd23f','#ffb13b','#c9d2ff','#8f9cff','#ff8fb1']),560);   // 판이 물결처럼 빛난 뒤(0.56초) 팡파르·색종이""")
R("""  document.getElementById('againBtn').onclick=()=>newPuzzle(false);""", """  document.getElementById('againBtn').onclick=()=>{ DS.play('new'); newPuzzle(false); };""")
R("""document.getElementById('newBtn').onclick=()=>newPuzzle(false);}""", """document.getElementById('newBtn').onclick=()=>{ DS.play('new'); newPuzzle(false); };}""")
p.save()
# 2차: 크기·지우기·음소거 아이콘
p = Patch(p.path); R = p.R
R("b.onclick=()=>{N=n;renderSizes();newPuzzle(DAILY);};", "b.onclick=()=>{N=n;DS.play('ui');renderSizes();newPuzzle(DAILY);};")
R("document.getElementById('clearBtn').onclick=()=>{ if(WON)return; ST=GIVEN.map(row=>row.slice()); paint(); };",
  "document.getElementById('clearBtn').onclick=()=>{ if(WON)return; ST=GIVEN.map(row=>row.slice()); paint(); DS.play('clear'); sndLevel(); };")
R("document.getElementById('muteBtn').textContent=MUTED?'🔇':'🔊';", "muteIcon();")
p.save()
