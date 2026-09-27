# -*- coding: utf-8 -*-
"""모아모아: 게임 월드 스킨(한옥 서재의 밤) + 공용 사운드·연출 연결 (1회용, 기록용)"""
import os, sys; sys.path.insert(0, os.path.dirname(__file__)); from _patch import Patch
p = Patch(os.path.join(os.path.dirname(__file__), '..', '..', 'moamoa', 'index.html')); R = p.R
R('@media(max-width:380px){.tile{font-size:13.5px;min-height:58px}.tile.long{font-size:11px}}\n</style>', '''@media(max-width:380px){.tile{font-size:13.5px;min-height:58px}.tile.long{font-size:11px}}
/* ===== 게임 월드 스킨 (2026-09-28) — 등불 켠 한옥 서재의 밤. 아트 /assets/stage/moamoa.jpg(원본: 무한 캔버스)
   낱말 = 한지를 붙인 나무 낱말패, 고르면 먹물 든 패가 떠오른다. 맞힌 그룹은 색 비단 띠. 로직은 그대로. ===== */
body{background:#2b1a14;}
body::before{content:"";position:fixed;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(30,16,10,.1),rgba(30,16,10,.2) 45%,rgba(30,16,10,.45)),url(/assets/stage/moamoa.jpg) center top/cover no-repeat;}
header{border-bottom:none;padding-bottom:12px;}
#backHome{color:#fff;background:rgba(40,22,14,.6);border:1.5px solid rgba(255,255,255,.3);box-shadow:0 3px 0 rgba(0,0,0,.35);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);}
#muteBtn{position:absolute;right:12px;top:13px;z-index:20;font-size:15px;line-height:1;border-radius:11px;padding:7px 10px;cursor:pointer;color:#fff;background:rgba(40,22,14,.6);border:1.5px solid rgba(255,255,255,.3);box-shadow:0 3px 0 rgba(0,0,0,.35);}
#muteBtn:active{transform:scale(.92);}
h1{margin-top:30px;font-size:32px;color:#fff6e0;text-shadow:0 3px 0 #4a2414,0 0 20px rgba(255,190,100,.55);}
h1 .dot{color:#ffb35c;}
.tagline{display:inline-block;margin-top:8px;padding:5px 14px;border-radius:999px;background:rgba(40,22,14,.62);color:#ffe2b8;font-weight:700;border:1px solid rgba(255,179,92,.35);}
#puzzleNo{color:#f4d9b8;margin-top:6px;text-shadow:0 1px 2px rgba(0,0,0,.6);}
.mm-board{background:linear-gradient(180deg,rgba(70,38,24,.86),rgba(38,20,14,.92));border:3px solid #d49a52;border-radius:22px;padding:14px 12px 16px;
  box-shadow:0 0 0 2px rgba(60,28,14,.9),0 16px 36px rgba(20,8,4,.5),inset 0 1px 0 rgba(255,255,255,.16),inset 0 0 30px rgba(255,170,80,.08);backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);}
.tile{background:linear-gradient(180deg,#fff8ea,#f1e2c6);color:#3a2616;border-radius:11px;border-bottom:4px solid #b88a54;
  box-shadow:0 2px 0 #6e4a26,0 5px 10px rgba(0,0,0,.28),inset 0 1px 0 #fff;transition:transform .1s,background .12s,color .12s,box-shadow .12s;}
.tile:active{transform:translateY(2px) scale(.97);}
.tile.sel{background:linear-gradient(180deg,#5b2e5e,#3c1d44);color:#ffe7a8;border-bottom-color:#241028;transform:translateY(-3px);
  box-shadow:0 2px 0 #1c0b20,0 9px 16px rgba(0,0,0,.4),0 0 0 2px #ffcf6b,0 0 14px rgba(255,200,100,.55);}
.tile.shake{animation:shake .4s;}
.solved{border-radius:12px;padding:10px 6px;color:#2a1a10;border:2px solid rgba(255,255,255,.55);box-shadow:0 3px 0 rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.6),inset 0 -8px 16px rgba(0,0,0,.1);
  background-image:linear-gradient(180deg,rgba(255,255,255,.35),rgba(255,255,255,0) 50%)!important;animation:ribbon .45s cubic-bezier(.3,1.4,.5,1);}
.solved b{font-size:15.5px;} .solved span{font-weight:600;}
@keyframes ribbon{0%{transform:scaleX(.3);opacity:0}100%{transform:scaleX(1);opacity:1}}
#lives{color:#f4d9b8;font-weight:700;}
#lives .heart{font-size:18px;letter-spacing:4px;}
#lives.last .heart{animation:lastLife 1s ease-in-out infinite;display:inline-block;}
@keyframes lastLife{50%{transform:scale(1.25)}}
.btn{background:linear-gradient(180deg,rgba(255,255,255,.14),rgba(255,255,255,.06));color:#fff3e0;border:1.5px solid rgba(255,220,170,.5);box-shadow:0 3px 0 rgba(0,0,0,.4);}
.btn:active{transform:translateY(2px);box-shadow:0 1px 0 rgba(0,0,0,.4);}
.btn.primary{background:linear-gradient(180deg,#ffc56b,#ff8a4c);color:#3a1a08;border-color:#ffe1a8;box-shadow:0 4px 0 #9c4a1c,0 8px 16px rgba(0,0,0,.3);}
.btn.primary:disabled{opacity:.45;}
#modal{background:linear-gradient(180deg,#fff8ea,#f3e3c6);border:3px solid #d49a52;box-shadow:0 0 0 2px #6e3a18,0 20px 40px rgba(0,0,0,.45);}
#modal h2{color:#5a2e12;animation:ribbon .5s cubic-bezier(.3,1.4,.5,1);}
#modal .btn{color:#5a2e12;background:#fff;border-color:#d49a52;box-shadow:0 3px 0 #b88a54;}
#modal .btn.primary{background:linear-gradient(180deg,#ffc56b,#ff8a4c);color:#3a1a08;border-color:#ffe1a8;box-shadow:0 4px 0 #9c4a1c;}
.seo-info{background:rgba(255,250,240,.96);border-top:none;border-radius:18px;padding:22px 18px;margin-top:22px;box-shadow:0 8px 24px rgba(0,0,0,.25);}
footer{color:#f4d9b8;}
</style>''')
R('<a id="backHome" href="/" aria-label="Mallow 홈으로">← Mallow</a>',
  '<a id="backHome" href="/" aria-label="Mallow 홈으로">← Mallow</a>\n  <button id="muteBtn" onclick="mmMute(event)" title="sound" aria-label="sound">🔊</button>')
R('  <div id="solvedRows"></div>', '  <div class="mm-board">\n  <div id="solvedRows"></div>')
R('''    <button class="btn primary" id="submitBtn" disabled>확인</button>
  </div>''', '''    <button class="btn primary" id="submitBtn" disabled>확인</button>
  </div>
  </div>''')
R('<footer>\n  매일 자정', '<script src="/assets/daily-sound.js"></script>\n<script src="/assets/daily-fx.js"></script>\n<footer>\n  매일 자정')
# 목숨: 먹점 → 하트(마지막 한 번 남으면 두근거림)
R("""  $('heartRow').textContent = '●'.repeat(MAX_MISS-state.miss) + '○'.repeat(state.miss);""",
  """  $('heartRow').textContent = '❤️'.repeat(MAX_MISS-state.miss) + '🤍'.repeat(state.miss);
  $('lives').classList.toggle('last', !state.done && state.miss===MAX_MISS-1);""")
# 사운드: 고르기·해제·섞기
R("""  const i = selected.indexOf(w);
  if(i>=0) selected.splice(i,1);
  else if(selected.length<4) selected.push(w);
  render();""", """  const i = selected.indexOf(w);
  if(!DS.playing()) mmMusic();
  if(i>=0){ selected.splice(i,1); DS.play('unpick'); }
  else if(selected.length<4){ selected.push(w); DS.play('pick', selected.length); }   // 고른 수만큼 음이 한 칸씩 오른다
  render();""")
R("""$('clearBtn').onclick=()=>{ selected=[]; render(); };
$('shuffleBtn').onclick=()=>{ order=seededShuffle(order, Date.now()%233280); render(); };""",
  """$('clearBtn').onclick=()=>{ if(selected.length) DS.play('unpick'); selected=[]; render(); };
$('shuffleBtn').onclick=()=>{ DS.play('shuffle'); order=seededShuffle(order, Date.now()%233280); render(); };""")
R("""    if(state.solved.length===4){ finish(true); }
    else toast(PUZZLE.groups[gi].name+' 정답!');""", """    DS.play('group', PUZZLE.groups[gi].diff); mmLevel();
    setTimeout(()=>{ const rows=document.querySelectorAll('#solvedRows .solved'), el=rows[rows.length-1]; if(el){ const q=DFX.center(el); DFX.burst(q[0],q[1],['#f5d547','#9fc25f','#78a9d1','#b07fc7','#fff'],14); } },40);
    if(state.solved.length===4){ finish(true); }
    else toast(PUZZLE.groups[gi].name+' 정답!');""")
R("""    if(best===3 && state.oneAway<MAX_ONEAWAY){ state.oneAway++; toast('하나만 달라요!'); }
    else toast('틀렸어요');""", """    if(best===3 && state.oneAway<MAX_ONEAWAY){ state.oneAway++; toast('하나만 달라요!'); DS.play('oneaway'); }
    else { toast('틀렸어요'); DS.play('miss'); }
    mmLevel();""")
R("""function finish(win){
  stopClock();""", """function finish(win){
  stopClock();
  if(!state.done){ DS.stop(); if(win){ DS.play('win'); setTimeout(()=>DFX.confetti(['#f5d547','#9fc25f','#78a9d1','#b07fc7','#ffb35c']),550); } else setTimeout(()=>DS.play('lose'),380); }""")
R("""$('closeBtn').onclick=()=>$('overlay').classList.remove('show');""", """$('closeBtn').onclick=()=>{ DS.play('ui'); $('overlay').classList.remove('show'); };""")
R("""/* ══════════════ 시작 ══════════════ */""", """/* ══════════════ 사운드 — /assets/daily-sound.js(공용 엔진). 🔊 = 켜기/끄기·음악·효과음 음량 패널 ══════════════ */
function mmMusic(){ if(!state.done){ DS.bgm('study'); mmLevel(); } }
function mmLevel(){ DS.level(state.miss>=MAX_MISS-1 ? 2 : state.solved.length>=2 ? 1 : 0); }   // 마지막 기회엔 맥박이 붙어 긴장이 오른다
function mmIcon(){ $('muteBtn').textContent = DS.on()?'🔊':'🔇'; }
function mmMute(ev){ if(ev) ev.stopPropagation(); DS.panel($('muteBtn'),'ko',mmIcon); }
mmIcon();

/* ══════════════ 시작 ══════════════ */""")
p.save()
