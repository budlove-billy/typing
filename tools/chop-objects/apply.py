# -*- coding: utf-8 -*-
"""말로우 타워 오브젝트 개편 (2026-09-30, 1회용·기록용) — 표지(assets/cover/chop.jpg) 톤에 맞춤.
- 블록(80×52): 납작한 사각형 → 파스텔 마시멜로 큐브(5색, 광택·설탕가루·그림자). 색은 블록을 따라 내려온다.
- 포크: 🍴 이모지 → 은빛 포크 SVG(손잡이는 블록에 박히고 날은 바깥으로)
- 캐릭터: 크게(52→64) + 깨무는 얼굴(chomp)·돌진, 실패 시 우는 얼굴
- 깨문 블록이 이빨 자국을 남기고 반대쪽으로 날아가고 탑이 한 칸 내려앉는다. 판정·밸런스는 그대로."""
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'daily-redesign')); from _patch import Patch
p = Patch(os.path.join(os.path.dirname(__file__), '..', '..', 'index.html')); R = p.R

p.between('.cp-stage{position:relative;max-width:300px', '.cp-controls{', r'''.cp-stage{position:relative;max-width:300px;height:350px;margin:0 auto;overflow:hidden}
/* 2026-09-30 오브젝트 개편: 파스텔 마시멜로 큐브 탑 + 은빛 포크 + 깨무는 말로우 (표지 assets/cover/chop.jpg 톤) */
.cp-stage::before{content:"";position:absolute;left:50%;bottom:0;width:150px;height:22px;transform:translateX(-50%);border-radius:50%;
  background:radial-gradient(ellipse at 50% 35%,#fff 0,#f3e6f0 45%,#cdb3c9 100%);box-shadow:0 4px 0 #9d7f9a,0 8px 14px rgba(20,5,30,.45)}
.cp-tower{position:absolute;left:50%;transform:translateX(-50%);bottom:8px;width:80px}
.cp-stage.dead .cp-tower{z-index:3}
.cp-tower.drop{animation:cpDrop .09s ease-out}
@keyframes cpDrop{from{transform:translate(-50%,-56px)}to{transform:translate(-50%,0)}}
.cp-fx{pointer-events:none;height:0;z-index:3}
.cp-seg{position:absolute;left:0;width:80px;height:52px;border-radius:17px 17px 14px 14px;--a:#ffe6f0;--b:#ffc4da;--e:#e79ab8;
  background:radial-gradient(circle,rgba(255,255,255,.4) 0 1px,transparent 1.7px) 3px 4px/19px 15px,radial-gradient(circle,rgba(255,255,255,.3) 0 .9px,transparent 1.6px) 12px 11px/23px 19px,linear-gradient(180deg,var(--a) 0%,var(--b) 68%,var(--e) 100%);
  box-shadow:inset 0 7px 0 rgba(255,255,255,.5),inset 0 -6px 0 rgba(90,20,60,.08),inset 10px 0 12px rgba(255,255,255,.28),inset -10px 0 12px rgba(110,40,90,.13),0 3px 0 rgba(90,30,70,.28),0 6px 10px rgba(20,5,30,.3)}
.cp-seg::before{content:"";position:absolute;left:10px;top:8px;width:26px;height:8px;border-radius:50%;background:rgba(255,255,255,.75);transform:rotate(-7deg)}
.cp-seg.c1{--a:#e6fcf1;--b:#b9edd2;--e:#86cfaa}
.cp-seg.c2{--a:#fffae4;--b:#fbe7ad;--e:#e0c274}
.cp-seg.c3{--a:#f2ebff;--b:#d8c8fc;--e:#ab95e5}
.cp-seg.c4{--a:#fff0e6;--b:#ffd2b8;--e:#e9a584}
.cp-seg .cp-fork{position:absolute;top:50%;z-index:-1;width:82px;height:34px;line-height:0;transform:translateY(-50%);filter:drop-shadow(0 2px 1px rgba(20,5,30,.5))}
.cp-seg .cp-fork svg{display:block;width:100%;height:100%}
.cp-seg .cp-fork.R{right:-66px}
.cp-seg .cp-fork.L{left:-66px;transform:translateY(-50%) scaleX(-1)}
.cp-fly{animation:cpFlyR .38s ease-in forwards}
.cp-fly.toL{animation-name:cpFlyL}
@keyframes cpFlyR{to{transform:translate(150px,-36px) rotate(38deg);opacity:0}}
@keyframes cpFlyL{to{transform:translate(-150px,-36px) rotate(-38deg);opacity:0}}
.cp-fly.bitL{-webkit-mask:radial-gradient(circle 11px at 0 34%,#0000 95%,#000),radial-gradient(circle 12px at 3px 64%,#0000 95%,#000);-webkit-mask-composite:source-in;mask-composite:intersect}
.cp-fly.bitR{-webkit-mask:radial-gradient(circle 11px at 100% 34%,#0000 95%,#000),radial-gradient(circle 12px at calc(100% - 3px) 64%,#0000 95%,#000);-webkit-mask-composite:source-in;mask-composite:intersect}
.cp-player{position:absolute;bottom:4px;display:inline-flex;transition:left .08s;z-index:2;filter:drop-shadow(0 4px 4px rgba(20,5,30,.4))}
.cp-player svg{transform-origin:50% 90%}
.cp-player.bite svg{animation:cpLunge .16s ease-out}
@keyframes cpLunge{40%{transform:translateX(12px) scale(1.08,.94)}}
.cp-player.hit{animation:bbShake .3s ease 1}
.cp-fork.hit{animation:cpForkHit .35s ease 2;filter:drop-shadow(0 0 4px #ff3355) drop-shadow(0 0 2px #ff3355)}
@keyframes cpForkHit{0%,100%{transform:translateY(-50%) scale(1)}50%{transform:translateY(-50%) scale(1.25)}}
.cp-fork.L.hit{animation:cpForkHitL .35s ease 2}
@keyframes cpForkHitL{0%,100%{transform:translateY(-50%) scaleX(-1) scale(1)}50%{transform:translateY(-50%) scaleX(-1) scale(1.25)}}
''')

# 무대: 포크 금속 그라디언트(한 번만 정의) + 날아가는 조각 층 + 캐릭터 64px
R('''      <div class="cp-tower" id="cp-tower"></div>
      <span class="cp-player" id="cp-player" data-mallow="focus" data-mallow-size="52"></span>''',
'''      <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><linearGradient id="cpSteel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdfeff"/><stop offset=".45" stop-color="#cfd5e0"/><stop offset=".6" stop-color="#9aa3b4"/><stop offset="1" stop-color="#e6eaf1"/></linearGradient></defs></svg>
      <div class="cp-tower" id="cp-tower"></div>
      <div class="cp-tower cp-fx" id="cp-fx"></div>
      <span class="cp-player" id="cp-player" data-mallow="focus" data-mallow-size="64"></span>''')

# 마스코트 얼굴: 깨물기(눈 질끈 + 크게 벌린 입과 앞니)
R('''<path d="M45 63.5 Q50 66 55 63.5" fill="none" stroke="${_EYE}" stroke-width="2.4" stroke-linecap="round"/>`,
};''', '''<path d="M45 63.5 Q50 66 55 63.5" fill="none" stroke="${_EYE}" stroke-width="2.4" stroke-linecap="round"/>`,
  chomp:_mCheeks+
    `<path d="M32 47 Q37 41.5 42 47" fill="none" stroke="${_EYE}" stroke-width="2.6" stroke-linecap="round"/>`+
    `<path d="M58 47 Q63 41.5 68 47" fill="none" stroke="${_EYE}" stroke-width="2.6" stroke-linecap="round"/>`+
    `<path d="M40 56 Q50 53 60 56 Q59 71 50 71 Q41 71 40 56 Z" fill="#B8435C" stroke="${_EYE}" stroke-width="1.6" stroke-linejoin="round"/>`+
    `<path d="M44 55 h4.5 v3.4 q0 1.3 -1.3 1.3 h-1.9 q-1.3 0 -1.3 -1.3 Z M51.5 55 h4.5 v3.4 q0 1.3 -1.3 1.3 h-1.9 q-1.3 0 -1.3 -1.3 Z" fill="#fff"/>`+
    `<ellipse cx="50" cy="67" rx="5" ry="2.6" fill="#F49BB1"/>`,
};''')

R('''function cpRender(){
  const tower=document.getElementById('cp-tower');''', '''// 은빛 포크(오른쪽을 향함 — 왼쪽은 CSS로 뒤집는다). 손잡이 끝 14px는 블록 뒤에 박힌다.
function cpForkSVG(){
  const tine=y=>`<rect x="51" y="${y}" width="22" height="3.6" rx="1.8" fill="url(#cpSteel)" stroke="#5d6679" stroke-width=".9"/>`;
  return '<svg viewBox="0 0 74 30" aria-hidden="true">'+
    '<rect x="0" y="12" width="41" height="6" rx="3" fill="url(#cpSteel)" stroke="#5d6679" stroke-width=".9"/>'+
    '<rect x="3" y="12.9" width="34" height="1.3" rx=".6" fill="#fff" opacity=".85"/>'+
    tine(5)+tine(10.5)+tine(16)+tine(21.5)+
    '<path d="M38 12 Q46 12 49 4.5 H53 V25.5 H49 Q46 18 38 18 Z" fill="url(#cpSteel)" stroke="#5d6679" stroke-width=".9" stroke-linejoin="round"/></svg>';
}
// 깨물기 연출: 바닥 블록이 이빨 자국을 남기고 반대쪽으로 날아가고, 탑이 한 칸 내려앉고, 말로우가 앙 문다
function cpBiteFx(side){
  const bot=document.querySelector('#cp-tower .cp-seg'), fx=document.getElementById('cp-fx');
  if(bot&&fx){
    const c=bot.cloneNode(true); c.querySelectorAll('.cp-fork').forEach(f=>f.remove());
    c.classList.add('cp-fly', side==='L'?'bitL':'bitR'); if(side==='R') c.classList.add('toL');
    fx.appendChild(c); setTimeout(()=>c.remove(),420);
  }
  const tw=document.getElementById('cp-tower'); tw.classList.remove('drop'); void tw.offsetWidth; tw.classList.add('drop');
  const p=document.getElementById('cp-player');
  p.innerHTML=mallowSVG('chomp',{size:64}); p.classList.remove('bite'); void p.offsetWidth; p.classList.add('bite');
  clearTimeout(CP._face); CP._face=setTimeout(()=>{ if(CP.running) p.innerHTML=mallowSVG('focus',{size:64}); },170);
}
function cpRender(){
  const tower=document.getElementById('cp-tower');''')
R("""    seg.className='cp-seg';""", """    seg.className='cp-seg c'+(((CP.chops||0)+i)%5);   // 색은 블록을 따라 내려온다""")
R("""      fk.className='cp-fork '+CP.segs[i]; fk.textContent='🍴';""", """      fk.className='cp-fork '+CP.segs[i]; fk.innerHTML=cpForkSVG();""")
R("""  p.style.left = CP.side==='L' ? '14%' : 'auto';
  p.style.right = CP.side==='R' ? '14%' : 'auto';""", """  p.style.left = CP.side==='L' ? '12%' : 'auto';
  p.style.right = CP.side==='R' ? '12%' : 'auto';""")
R("""  CP.score += dmScore(CP.diff, 10, 'chop'); CP.chops=(CP.chops||0)+1;""",
  """  cpBiteFx(side);
  CP.score += dmScore(CP.diff, 10, 'chop'); CP.chops=(CP.chops||0)+1;""")
R("""  const p=document.getElementById('cp-player'); if(p){ p.classList.add('hit'); }""",
  """  const p=document.getElementById('cp-player'); if(p){ clearTimeout(CP._face); p.innerHTML=mallowSVG('sad',{size:64}); p.classList.add('hit'); }
  document.querySelector('#chop-game-card .cp-stage').classList.add('dead');   // 찌른 포크가 캐릭터 위로 보이게""")
R("""  CP.segs=['N','N','N','N','N']; // 워밍업: 첫 5칸은 포크 없음""",
  """  CP.segs=['N','N','N','N','N']; // 워밍업: 첫 5칸은 포크 없음
  document.getElementById('cp-player').innerHTML=mallowSVG('focus',{size:64});
  document.querySelector('#chop-game-card .cp-stage').classList.remove('dead');""")
p.save()
