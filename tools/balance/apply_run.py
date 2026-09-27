# -*- coding: utf-8 -*-
"""밸런스 v2 — 말로우 런 루프 교체(1회용, 기록용). apply.py 다음에 실행.
① 스폰을 '지나온 거리 누적'으로(배열이 비어도 간격 유지 — 예전엔 간격>캔버스폭이면 즉시 스폰되어 폰에서는 넘을 수 없는 벽, PC에서는 끝없는 판)
② 세계를 논리 400×240으로 고정하고 캔버스에 맞춰 확대(폰·PC 같은 판정)
③ 속도 대신 '시간 배속'이 오른다: 지형·점프 궤적은 그대로, 모든 것이 ts배 빨라져 점프 창(ms)이 계속 좁아지고 템포가 빨라진다
④ 불규칙 간격 + 연속 장애물 + 키 큰 장애물. 실제 경과 시간 기준이라 120Hz 화면에서도 같은 속도.
물리 상수(RN_G·RN_JV·히트박스)는 그대로 — tools/balance/proposal.mjs runV2가 같은 규칙으로 검증했다."""
import io, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, 'index.html')
s = io.open(P, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s else '\n'
def R(a, b, n=1, label=''):
    global s
    a2, b2 = a.replace('\n', NL), b.replace('\n', NL)
    c = s.count(a2); assert c == n, (label or a[:70], c); s = s.replace(a2, b2)
def RX(pat, repl, n=1, label=''):
    global s
    new, c = re.subn(pat, repl, s, flags=re.S); assert c == n, (label or pat[:60], c); s = new

R("// 히트박스(RN_PW×RN_PH, RN_OBW×RN_OBH)와 물리 상수는 그대로 두고 외형만 바꾼다 — 공정성 검증을 다시 할 필요가 없게.",
  "// 밸런스 v2: 논리 세계 400×240·시간 배속 상승·거리 누적 스폰·키 큰 장애물. 규칙 검증 = tools/balance/proposal.mjs runV2.", label='header')
RX(r"const RN_CFG=\{ easy:\{spd0:[^\n]*\};",
   "const RN_CFG={ easy:{ts0:0.80,a:0.0042,gLo:1.25,gHi:2.20,clusterP:0,clusterMax:0,tallP:0},\n"
   "  normal:{ts0:1.00,a:0.0052,gLo:1.12,gHi:2.00,clusterP:0.18,clusterMax:1,tallP:0.15},\n"
   "  hard:{ts0:1.18,a:0.0078,gLo:1.05,gHi:1.85,clusterP:0.30,clusterMax:2,tallP:0.30} };   // ts=시간 배속(초당 a씩 상승), 간격=안전간격×[gLo,gHi]\n"
   "const RN_WW=400, RN_WH=240, RN_BASE=6, RN_OBH_TALL=64;   // 논리 세계 크기 · 1스텝 이동량 · 키 큰 장애물 높이", label='cfg')
R("  score:0, dist:0, spd:0, py:0, vy:0, grounded:true, obs:[], burst:0, nextGap:0, W:0, H:0, groundY:0, px:0, run:0,",
  "  score:0, dist:0, spd:0, ts:1, t:0, acc:0, last:0, since:0, gap:0, py:0, vy:0, grounded:true, obs:[], burst:0, W:0, H:0, groundY:0, px:0, run:0,", label='state')
R("""function safeGapRun(spd){ return spd*RN_AIR + RN_OBW + 24; }
// 다음 장애물까지 간격 — 군집(연속 타이트) + 가변 간격으로 리듬 깨기. 항상 safeGap 이상(공정)
function rnNextGap(){ const cfg=RN_CFG[RN.diff], base=safeGapRun(RN.spd);
  if(RN.burst>0){ RN.burst--; return base*(1.03+Math.random()*0.12); }
  if(cfg.clusterMax>0 && Math.random()<cfg.clusterP){ RN.burst=cfg.clusterMax; return base*(1.03+Math.random()*0.12); }
  return base*1.15 + Math.random()*cfg.gapRand; }""",
  """const RN_SAFE=RN_BASE*RN_AIR + RN_OBW + 24;   // 착지 후 바로 다시 뛰어 넘을 수 있는 최소 간격(논리 px)
// 다음 장애물까지 간격 — 연속(안전간격 바로 위) + 불규칙 간격으로 리듬을 깬다. 항상 안전간격 이상(공정)
function rnNextGap(){ const cfg=RN_CFG[RN.diff];
  if(RN.burst>0){ RN.burst--; return RN_SAFE*(1.03+Math.random()*0.09); }
  if(cfg.clusterMax>0 && Math.random()<cfg.clusterP){ RN.burst=cfg.clusterMax; return RN_SAFE*(1.03+Math.random()*0.09); }
  return RN_SAFE*(cfg.gLo + Math.random()*(cfg.gHi-cfg.gLo)); }""", label='gap')
# 크기: 논리 세계를 캔버스 폭에 맞춰 확대
R("""function rnSize(cv,S,minH,maxH,ratio){ const cssW=Math.round(cv.clientWidth||340), cssH=Math.round(Math.min(maxH,Math.max(minH,cssW*ratio)));
  const dpr=Math.min(2,window.devicePixelRatio||1); cv.width=Math.round(cssW*dpr); cv.height=Math.round(cssH*dpr); cv.style.height=cssH+'px';
  cv.getContext('2d').setTransform(dpr,0,0,dpr,0,0); S.W=cssW; S.H=cssH; S.dpr=dpr; S.groundY=cssH-32; S.px=Math.round(cssW*0.16);
  S.art=rnBuildArt(cssW,cssH,S.groundY,dpr);
  S.flies=Array.from({length:7},(_,i)=>({x:(i+0.5)*cssW/7, y:cssH*(0.55+Math.random()*0.25), ph:Math.random()*6.3}));
  S.lines=Array.from({length:5},()=>({x:Math.random()*cssW, y:12+Math.random()*(S.groundY-24), len:30+Math.random()*50})); }
function rnResize(){ const cv=document.getElementById('rn-canvas'); if(cv) rnSize(cv,RN,228,300,0.56); }""",
  """/* 논리 세계(400×240)를 캔버스 폭에 맞춰 확대한다 — 화면이 넓어도 보이는 거리·판정이 같다(예전엔 PC가 훨씬 쉬웠다) */
function rnSize(cv,S){ const cssW=Math.round(cv.clientWidth||340), k=cssW/RN_WW, cssH=Math.round(RN_WH*k);
  const dpr=Math.min(2,window.devicePixelRatio||1); cv.width=Math.round(cssW*dpr); cv.height=Math.round(cssH*dpr); cv.style.height=cssH+'px';
  cv.getContext('2d').setTransform(dpr*k,0,0,dpr*k,0,0); S.W=RN_WW; S.H=RN_WH; S.dpr=dpr*k; S.groundY=RN_WH-32; S.px=Math.round(RN_WW*0.16);
  S.art=rnBuildArt(RN_WW,RN_WH,S.groundY,dpr*k);
  S.flies=Array.from({length:7},(_,i)=>({x:(i+0.5)*RN_WW/7, y:RN_WH*(0.55+Math.random()*0.25), ph:Math.random()*6.3}));
  S.lines=Array.from({length:5},()=>({x:Math.random()*RN_WW, y:12+Math.random()*(S.groundY-24), len:30+Math.random()*50})); }
function rnResize(){ const cv=document.getElementById('rn-canvas'); if(cv) rnSize(cv,RN); }""", label='size')
# 키 큰 장애물: 같은 그림을 세로로 늘려 그린다(그림자는 그대로)
R("""function rnObstacle(c,o,gy,tk){ rnObShadow(c,o.x,gy); const k=RN_KINDS[o.k|0];
  if(k==='rock') rnObRock(c,o.x,gy,tk); else if(k==='crate') rnObCrate(c,o.x,gy); else if(k==='crystal') rnObCrystal(c,o.x,gy,tk); else rnObFence(c,o.x,gy); }""",
  """function rnObstacle(c,o,gy,tk){ rnObShadow(c,o.x,gy); const k=RN_KINDS[o.k|0], tall=(o.h||RN_OBH)>RN_OBH;
  if(tall){ c.save(); c.translate(0,gy); c.scale(1,o.h/RN_OBH); c.translate(0,-gy); }
  if(k==='rock') rnObRock(c,o.x,gy,tk); else if(k==='crate') rnObCrate(c,o.x,gy); else if(k==='crystal') rnObCrystal(c,o.x,gy,tk); else rnObFence(c,o.x,gy);
  if(tall) c.restore(); }""", label='obstacle')
# 연출: 표시 프레임 길이(f=60Hz 기준 프레임 수)만큼 움직인다
R("function rnFx(S){ // 게임 규칙과 무관한 연출 갱신\n  if(S.landT>0) S.landT--;",
  "function rnFx(S,f){ // 게임 규칙과 무관한 연출 갱신(f = 이번 화면 프레임이 60Hz 몇 프레임인지)\n  const sp=S.spd; if(f) S.spd=sp*f;\n  if(S.landT>0) S.landT--;", label='fx1')
R("  if(S.grounded && S.crashT===0 && Math.random()<0.28) rnPuff(S,S.px+10,S.groundY-2,1,0.6);\n  rnStepParts(S);\n}",
  "  if(S.grounded && S.crashT===0 && Math.random()<0.28) rnPuff(S,S.px+10,S.groundY-2,1,0.6);\n  rnStepParts(S); S.spd=sp;\n}", label='fx2')
# 시작
R("""  rnResize(); const cfg=RN_CFG[RN.diff];
  RN.running=true; RN.over=false; RN.score=0; RN.dist=0; RN.spd=cfg.spd0; RN.py=0; RN.vy=0; RN.grounded=true; RN.run=0; RN.burst=0;""",
  """  rnResize(); const cfg=RN_CFG[RN.diff];
  RN.running=true; RN.over=false; RN.score=0; RN.dist=0; RN.ts=cfg.ts0; RN.spd=RN_BASE*cfg.ts0; RN.t=0; RN.acc=0; RN.last=0; RN.py=0; RN.vy=0; RN.grounded=true; RN.run=0; RN.burst=0;""", label='start1')
R("  RN.obs=[{x:RN.W+40,k:rnKind([])}]; RN.nextGap=rnNextGap();", "  RN.obs=[]; RN.since=0; RN.gap=RN_WW*0.9;   // 첫 장애물은 약 1.5초 뒤", label='start2')
R("  const cfg=RN_CFG[RN.diff], sp=document.getElementById('rn-speed-fill'); if(sp) sp.style.width=Math.round(100*(RN.spd-cfg.spd0)/(cfg.cap-cfg.spd0))+'%';",
  "  const cfg=RN_CFG[RN.diff], sp=document.getElementById('rn-speed-fill'); if(sp) sp.style.width=Math.min(100,Math.round(100*(RN.ts-cfg.ts0)/1.5))+'%';", label='hud')
# 루프
RX(r"function rnLoop\(\)\{\r?\n  if\(!RN\.running\) return; const cfg=RN_CFG\[RN\.diff\]; RN\.tk\+\+;.*?\r?\n  rnFx\(RN\); rnDraw\(\); RN\.raf=requestAnimationFrame\(rnLoop\);\r?\n\}",
   lambda m: """function rnLoop(now){
  if(!RN.running) return; const cfg=RN_CFG[RN.diff]; RN.tk++;
  if(!RN.last) RN.last=now; const dt=Math.min(0.05, Math.max(0,(now-RN.last)/1000)); RN.last=now; RN.t+=dt;
  RN.ts=cfg.ts0+cfg.a*RN.t; RN.spd=RN_BASE*RN.ts; RN.acc+=dt*60*RN.ts;   // 실제 시간 기준 — 120Hz 화면에서도 같은 속도
  let n=Math.floor(RN.acc); RN.acc-=n;
  for(let i=0;i<n;i++){ if(rnStep(cfg)) return; }
  RN.run=(RN.run+RN.spd*0.05*dt*60)%1;
  RN.score=Math.floor(RN.dist*dm(RN.diff,'run')/12); rnHud();
  rnFx(RN,dt*60); rnDraw(); RN.raf=requestAnimationFrame(rnLoop);
}
/* 물리 1스텝(예전 1프레임과 같다). 충돌하면 true */
function rnStep(cfg){
  if(!RN.grounded){ RN.py+=RN.vy; RN.vy-=RN_G; if(RN.py<=0){ RN.py=0; RN.vy=0; RN.grounded=true; RN.landT=8; rnPuff(RN,RN.px+RN_PW/2,RN.groundY-2,7,3); } }
  for(const o of RN.obs) o.x-=RN_BASE;
  while(RN.obs.length && RN.obs[0].x < -RN_OBW-6) RN.obs.shift();
  RN.since+=RN_BASE;   // 거리 누적 스폰 — 화면에 장애물이 없어도 간격이 유지된다
  if(RN.since>=RN.gap){ RN.obs.push({x:RN_WW, k:rnKind(RN.obs), h:Math.random()<cfg.tallP?RN_OBH_TALL:RN_OBH}); RN.since=0; RN.gap=rnNextGap(); }
  RN.dist+=RN_BASE;
  // 충돌(AABB): 플레이어[px,px+PW]×[py,py+PH] vs 장애물[x,x+OBW]×[0,h]
  const pxL=RN.px, pxR=RN.px+RN_PW;
  for(const o of RN.obs){ if(o.x+RN_OBW < pxL) continue; if(o.x > pxR) break; if(RN.py < (o.h||RN_OBH)){ rnGameOver(); return true; } }
  return false;
}""", label='loop')
R("    rnSize(cv,RNP,232,270,0.56); RNP.dist=0;", "    rnSize(cv,RNP); RNP.dist=0;", label='preview size')
io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('run v2 applied')
