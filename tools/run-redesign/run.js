// ========== 말로우 런 (순발력·집중력 · 엔들리스 러너) — 물리·간격은 .logs/run_sim.mjs 검증본 ==========
// 그래픽: 황혼 숲 횡스크롤(하늘·산 2겹·숲 2겹 패럴랙스 + 지면 타일 + 장애물 4종). 컨셉아트는 canvas/ 무한 캔버스.
// 히트박스(RN_PW×RN_PH, RN_OBW×RN_OBH)와 물리 상수는 그대로 두고 외형만 바꾼다 — 공정성 검증을 다시 할 필요가 없게.
const RN_G=0.9, RN_JV=15, RN_PW=40, RN_PH=42, RN_OBW=26, RN_OBH=46, RN_AIR=2*RN_JV/RN_G;
const RN_CFG={ easy:{spd0:4.2,acc:0.0010,cap:9.0,gapRand:180,clusterP:0,clusterMax:0}, normal:{spd0:5.2,acc:0.0015,cap:11.0,gapRand:150,clusterP:0.24,clusterMax:1}, hard:{spd0:6.4,acc:0.0022,cap:12.5,gapRand:110,clusterP:0.36,clusterMax:2} };
const RN_KINDS=['fence','rock','crate','crystal'];
const RN_PX_PER_M=20;   // HUD 거리 환산(표시 전용 — 점수 공식과 무관)
const RN={ diff:'normal', running:false, over:false, raf:0, overT:0, best:bt_loadBest('brain.run.best'),
  score:0, dist:0, spd:0, py:0, vy:0, grounded:true, obs:[], burst:0, nextGap:0, W:0, H:0, groundY:0, px:0, run:0,
  parts:[], flies:[], lines:[], landT:0, crashT:0, shake:0, prevBest:0, beat:false, hudM:-1, hudS:-1 };
// 인트로 화면의 자동 달리기 미리보기(점수·기록 없음)
const RNP={ running:false, raf:0, dist:0, spd:4.6, py:0, vy:0, grounded:true, obs:[], W:0, H:0, groundY:0, px:0, run:0,
  parts:[], flies:[], lines:[], landT:0, crashT:0, shake:0, gap:0 };
function RN_DIFF_LABEL(d){ return d==='easy'?t('run.easy'):d==='hard'?t('run.hard'):t('run.normal'); }
function rnUpdateBestLine(){ const el=document.getElementById('rn-intro-best'); if(el) el.textContent=bt_bestLineText(RN.best,RN.diff); }
function setRunDiff(d){ RN.diff=d; ['easy','normal','hard'].forEach(k=>document.getElementById('rn-diff-'+k).classList.toggle('active',k===d)); rnUpdateBestLine(); }
function safeGapRun(spd){ return spd*RN_AIR + RN_OBW + 24; }
// 다음 장애물까지 간격 — 군집(연속 타이트) + 가변 간격으로 리듬 깨기. 항상 safeGap 이상(공정)
function rnNextGap(){ const cfg=RN_CFG[RN.diff], base=safeGapRun(RN.spd);
  if(RN.burst>0){ RN.burst--; return base*(1.03+Math.random()*0.12); }
  if(cfg.clusterMax>0 && Math.random()<cfg.clusterP){ RN.burst=cfg.clusterMax; return base*(1.03+Math.random()*0.12); }
  return base*1.15 + Math.random()*cfg.gapRand; }
function rnKind(obs){ const prev=obs.length?obs[obs.length-1].k:-1; let k=Math.floor(Math.random()*RN_KINDS.length); if(k===prev) k=(k+1)%RN_KINDS.length; return k; }

// ---- 배경 아트: 크기별로 한 번만 오프스크린에 그려 두고 매 프레임 이어 붙인다 ----
const RN_ART={};
function rnRng(seed){ let s=seed>>>0; return ()=>{ s=(s+0x6D2B79F5)>>>0; let q=s; q=Math.imul(q^q>>>15,q|1); q^=q+Math.imul(q^q>>>7,q|61); return ((q^q>>>14)>>>0)/4294967296; }; }
function rnLayerCanvas(w,h,dpr){ const cv=document.createElement('canvas'); cv.width=Math.ceil(w*dpr); cv.height=Math.ceil(h*dpr); const c=cv.getContext('2d'); c.setTransform(dpr,0,0,dpr,0,0); return {cv,c}; }
// 주기 P 안에서 정수 배 주파수만 쓰므로 타일 양 끝이 이음새 없이 맞는다
function rnRidge(P,baseY,amp,ks,rnd,sharp){ const ph=ks.map(()=>rnd()*Math.PI), w=ks.map(()=>0.45+rnd()*0.55), sw=w.reduce((a,b)=>a+b,0);
  return x=>{ let v=0; ks.forEach((k,i)=>{ const s=Math.abs(Math.sin(Math.PI*k*x/P+ph[i])); v+=w[i]*(sharp?Math.pow(1-s,1.7):s); }); return baseY-amp*v/sw; }; }
function rnFillRidge(c,P,H,hAt,fill,edge){ c.beginPath(); c.moveTo(0,H); for(let x=0;x<P+3;x+=3) c.lineTo(Math.min(x,P),hAt(Math.min(x,P))); c.lineTo(P,H); c.closePath(); c.fillStyle=fill; c.fill();
  if(edge){ c.beginPath(); for(let x=0;x<P+3;x+=3){ const xx=Math.min(x,P), y=hAt(xx); x?c.lineTo(xx,y):c.moveTo(xx,y); } c.strokeStyle=edge; c.lineWidth=1.6; c.stroke(); } }
function rnPine(c,x,y,s,col,rim){ c.fillStyle=col; c.fillRect(x-s*0.035,y-s*0.16,s*0.07,s*0.18);
  for(let i=0;i<3;i++){ const by=y-s*(0.12+i*0.25), hw=s*(0.3-i*0.07), ty=by-s*(0.42-i*0.04);
    c.beginPath(); c.moveTo(x,ty); c.lineTo(x+hw,by); c.lineTo(x-hw,by); c.closePath(); c.fill();
    if(rim){ c.beginPath(); c.moveTo(x,ty); c.lineTo(x+hw,by); c.strokeStyle=rim; c.lineWidth=1.3; c.stroke(); } } }
function rnFog(c,P,y0,y1,rgb,a){ const g=c.createLinearGradient(0,y0,0,y1); g.addColorStop(0,'rgba('+rgb+',0)'); g.addColorStop(1,'rgba('+rgb+','+a+')'); c.fillStyle=g; c.fillRect(0,y0,P,y1-y0); }
function rnBuildArt(W,H,gy,dpr){
  const key=W+'x'+H+'x'+dpr; if(RN_ART[key]) return RN_ART[key];
  const rnd=rnRng(20260927), art={layers:[],stars:[]};
  // 하늘 + 해
  const sky=rnLayerCanvas(W,H,dpr), c=sky.c;
  const g=c.createLinearGradient(0,0,0,H*0.78);
  [[0,'#131238'],[.34,'#302d6b'],[.56,'#7c4585'],[.72,'#d9614f'],[.86,'#f4a35e'],[1,'#ffd898']].forEach(s=>g.addColorStop(s[0],s[1]));
  c.fillStyle=g; c.fillRect(0,0,W,H);
  const sx=W*0.63, sy=H*0.52, sr=Math.max(22,H*0.15);
  const glow=c.createRadialGradient(sx,sy,sr*0.6,sx,sy,sr*3.4); glow.addColorStop(0,'rgba(255,214,150,.55)'); glow.addColorStop(1,'rgba(255,190,120,0)');
  c.fillStyle=glow; c.fillRect(0,0,W,H);
  const disk=c.createLinearGradient(0,sy-sr,0,sy+sr); disk.addColorStop(0,'#fff3cf'); disk.addColorStop(1,'#ffc77e');
  c.fillStyle=disk; c.beginPath(); c.arc(sx,sy,sr,0,Math.PI*2); c.fill();
  art.sky=sky.cv;
  for(let i=0;i<22;i++) art.stars.push({x:rnd()*W, y:rnd()*H*0.42, r:0.6+rnd()*1.3, ph:rnd()*6.3, big:rnd()<0.18});
  // 먼 산 → 가까운 산 → 먼 숲 → 가까운 숲 (속도 비율 = 패럴랙스 깊이)
  const mk=(P,spd,draw)=>{ const L=rnLayerCanvas(P,H,dpr); draw(L.c,P); art.layers.push({cv:L.cv,P,spd}); };
  mk(620,0.06,(c,P)=>{ const h=rnRidge(P,H*0.62,H*0.34,[2,3,5],rnd,true); rnFillRidge(c,P,H,h,'#5d4a8e','rgba(170,140,210,.55)'); });
  mk(540,0.13,(c,P)=>{ const h=rnRidge(P,H*0.68,H*0.25,[3,4,6],rnd,true); rnFillRidge(c,P,H,h,'#433873','rgba(140,115,190,.5)'); rnFog(c,P,H*0.5,H*0.78,'214,160,190',.32); });
  mk(600,0.26,(c,P)=>{ const h=rnRidge(P,H*0.74,H*0.05,[1,2,3],rnd,false); rnFillRidge(c,P,H,h,'#2d5a67');
    for(let i=0;i<30;i++){ const x=rnd()*P, s=H*(0.1+rnd()*0.09); [x-P,x,x+P].forEach(xx=>rnPine(c,xx,h(((x%P)+P)%P)+3,s,'#274f5c')); }
    rnFog(c,P,H*0.62,H*0.86,'170,196,214',.42); });
  mk(760,0.52,(c,P)=>{ const h=rnRidge(P,gy-2,H*0.04,[2,3],rnd,false); rnFillRidge(c,P,H,h,'#193d47');
    for(let i=0;i<13;i++){ const x=rnd()*P, s=H*(0.24+rnd()*0.16); [x-P,x,x+P].forEach(xx=>rnPine(c,xx,h(((x%P)+P)%P)+4,s,'#163842','rgba(110,220,160,.55)')); }
    rnFog(c,P,gy-H*0.16,gy+4,'150,185,200',.28); });
  // 지면 타일(주기 96): 풀 윗면 + 흙 블록 두 줄 + 자갈·풀잎
  const GP=96, gt=rnLayerCanvas(GP,H,dpr), q=gt.c;
  q.fillStyle='#5a331b'; q.fillRect(0,gy,GP,H-gy);
  for(let row=0; gy+9+row*14<H; row++){ const y=gy+9+row*14, off=(row%2)*24;
    for(let x=-48+off; x<GP+48; x+=48){ q.fillStyle='#855030'; q.strokeStyle='#3b2010'; q.lineWidth=1.5;
      q.beginPath(); q.roundRect(x+1.5,y,45,12.5,3); q.fill(); q.stroke();
      q.fillStyle='rgba(255,210,160,.14)'; q.fillRect(x+4,y+2,39,2); } }
  q.fillStyle='#4f9b33'; q.fillRect(0,gy-3,GP,11);
  q.fillStyle='#3d7f27'; for(let x=0;x<GP;x+=8){ q.beginPath(); q.moveTo(x,gy+7); q.lineTo(x+4,gy+11+((x/8)%3)*2); q.lineTo(x+8,gy+7); q.closePath(); q.fill(); }
  q.fillStyle='#8ad65a'; q.fillRect(0,gy-3,GP,2.5);
  const tufts=[[6,5],[19,3],[33,6],[47,4],[58,7],[71,3],[84,5],[91,4]];
  tufts.forEach(([x,hh])=>{ q.fillStyle='#6cc447'; q.beginPath(); q.moveTo(x-2.5,gy-2); q.lineTo(x,gy-2-hh); q.lineTo(x+2.5,gy-2); q.closePath(); q.fill(); });
  [[28,gy+22,3.2],[70,gy+17,2.4]].forEach(([x,y,r])=>{ if(y+r<H){ q.fillStyle='#9e9aa6'; q.beginPath(); q.ellipse(x,y,r*1.3,r,0,0,Math.PI*2); q.fill(); } });
  art.ground={cv:gt.cv,P:GP};
  RN_ART[key]=art; return art;
}
function rnSize(cv,S,minH,maxH,ratio){ const cssW=Math.round(cv.clientWidth||340), cssH=Math.round(Math.min(maxH,Math.max(minH,cssW*ratio)));
  const dpr=Math.min(2,window.devicePixelRatio||1); cv.width=Math.round(cssW*dpr); cv.height=Math.round(cssH*dpr); cv.style.height=cssH+'px';
  cv.getContext('2d').setTransform(dpr,0,0,dpr,0,0); S.W=cssW; S.H=cssH; S.dpr=dpr; S.groundY=cssH-32; S.px=Math.round(cssW*0.16);
  S.art=rnBuildArt(cssW,cssH,S.groundY,dpr);
  S.flies=Array.from({length:7},(_,i)=>({x:(i+0.5)*cssW/7, y:cssH*(0.55+Math.random()*0.25), ph:Math.random()*6.3}));
  S.lines=Array.from({length:5},()=>({x:Math.random()*cssW, y:12+Math.random()*(S.groundY-24), len:30+Math.random()*50})); }
function rnResize(){ const cv=document.getElementById('rn-canvas'); if(cv) rnSize(cv,RN,228,300,0.56); }

// ---- 파티클(먼지·불꽃) ----
function rnPuff(S,x,y,n,spread,rgb,kind){ for(let i=0;i<n;i++) S.parts.push({x,y,vx:(Math.random()-0.5)*spread,vy:-Math.random()*(kind==='spark'?4.5:1.4),life:0,max:kind==='spark'?30:22+Math.random()*12,r:kind==='spark'?2+Math.random()*2:2+Math.random()*3,rgb:rgb||'232,208,172',kind:kind||'dust'}); }
function rnStepParts(S){ for(const p of S.parts){ p.life++; p.x+=p.vx-S.spd*0.85; p.vx*=0.95; p.vy+=(p.kind==='spark'?0.22:0.03); p.y+=p.vy; if(p.kind==='dust') p.r+=0.12; }
  S.parts=S.parts.filter(p=>p.life<p.max); }
function rnDrawParts(c,S){ for(const p of S.parts){ const a=1-p.life/p.max; c.fillStyle='rgba('+p.rgb+','+(p.kind==='spark'?a:a*0.65).toFixed(3)+')';
  if(p.kind==='spark'){ c.save(); c.translate(p.x,p.y); c.rotate(p.life*0.3); c.fillRect(-p.r,-p.r*0.35,p.r*2,p.r*0.7); c.fillRect(-p.r*0.35,-p.r,p.r*0.7,p.r*2); c.restore(); }
  else { c.beginPath(); c.arc(p.x,p.y,p.r,0,Math.PI*2); c.fill(); } } }

// ---- 장애물 4종 (모두 RN_OBW×RN_OBH 상자를 거의 꽉 채운다 → 보이는 대로 부딪힌다) ----
function rnObShadow(c,x,gy){ c.fillStyle='rgba(10,6,20,.32)'; c.beginPath(); c.ellipse(x+RN_OBW/2,gy+1,RN_OBW*0.68,3.2,0,0,Math.PI*2); c.fill(); }
function rnObFence(c,x,gy){ const top=gy-RN_OBH;
  [[x+1,9],[x+9.5,0],[x+18,6]].forEach(([sx,off])=>{ const w=7.5, y0=top+off;
    c.beginPath(); c.moveTo(sx,gy); c.lineTo(sx,y0+8); c.lineTo(sx+w/2,y0); c.lineTo(sx+w,y0+8); c.lineTo(sx+w,gy); c.closePath();
    c.fillStyle='#a86b3c'; c.fill(); c.fillStyle='#7c4a26'; c.fillRect(sx+w/2,y0+6,w/2,gy-y0-6);
    c.strokeStyle='#341d0e'; c.lineWidth=1.6; c.stroke(); c.fillStyle='#e8d2b0'; c.beginPath(); c.moveTo(sx+w/2,y0); c.lineTo(sx+w*0.72,y0+4); c.lineTo(sx+w*0.28,y0+4); c.closePath(); c.fill(); });
  [[gy-13,-0.14],[gy-29,0.11]].forEach(([y,a])=>{ c.save(); c.translate(x+13,y); c.rotate(a); c.beginPath(); c.roundRect(-17,-3.5,34,7,2);
    c.fillStyle='#93592f'; c.fill(); c.strokeStyle='#341d0e'; c.lineWidth=1.5; c.stroke(); c.fillStyle='#d0cabf'; c.fillRect(-12,-1,2,2); c.fillRect(9,-1,2,2); c.restore(); }); }
function rnObRock(c,x,gy,tk){ const top=gy-RN_OBH;
  c.beginPath(); c.moveTo(x-3,gy); c.quadraticCurveTo(x-4,top+20,x+6,top+13); c.quadraticCurveTo(x+13,top+7,x+21,top+13); c.quadraticCurveTo(x+31,top+20,x+29,gy); c.closePath();
  const g=c.createLinearGradient(x,top,x+26,gy); g.addColorStop(0,'#7d8894'); g.addColorStop(1,'#434c58'); c.fillStyle=g; c.fill(); c.strokeStyle='#232833'; c.lineWidth=1.8; c.stroke();
  c.beginPath(); c.moveTo(x-2.5,top+22); c.quadraticCurveTo(x+2,top+11,x+13,top+10); c.quadraticCurveTo(x+25,top+11,x+28.5,top+22); c.quadraticCurveTo(x+20,top+19,x+13,top+22); c.quadraticCurveTo(x+5,top+19,x-2.5,top+22); c.closePath();
  c.fillStyle='#57a83a'; c.fill(); c.fillStyle='rgba(160,230,110,.7)'; c.fillRect(x+5,top+12,10,1.6);
  c.save(); c.shadowColor='rgba(170,255,110,'+(0.55+0.3*Math.sin(tk*0.12))+')'; c.shadowBlur=8; c.fillStyle='#c4f59a'; c.strokeStyle='#3e6b22'; c.lineWidth=1.1;
  [[x+13,top,0],[x+4,top+6,-0.5],[x+22,top+5,0.45],[x-4,top+25,-1.3],[x+30,top+26,1.3]].forEach(([sx,sy,a])=>{ c.save(); c.translate(sx,sy); c.rotate(a); c.beginPath(); c.moveTo(0,0); c.lineTo(3.4,10); c.lineTo(-3.4,10); c.closePath(); c.fill(); c.stroke(); c.restore(); });
  c.restore(); }
function rnObCrate(c,x,gy){ [[gy-23,x-1],[gy-46,x+0.5]].forEach(([y,cx])=>{ const w=27,h=23;
  c.fillStyle='#9c6437'; c.fillRect(cx,y,w,h); c.strokeStyle='#6a3f1f'; c.lineWidth=1.2;
  for(let i=1;i<3;i++){ c.beginPath(); c.moveTo(cx+3,y+i*h/3); c.lineTo(cx+w-3,y+i*h/3); c.stroke(); }
  c.beginPath(); c.moveTo(cx+4,y+h-4); c.lineTo(cx+w-4,y+4); c.strokeStyle='#744522'; c.lineWidth=3; c.stroke();
  c.strokeStyle='#464c57'; c.lineWidth=2.6; c.strokeRect(cx+1.3,y+1.3,w-2.6,h-2.6);
  c.strokeStyle='#1f1a1a'; c.lineWidth=1; c.strokeRect(cx,y,w,h);
  c.fillStyle='#c9ced6'; [[cx+3,y+3],[cx+w-3,y+3],[cx+3,y+h-3],[cx+w-3,y+h-3]].forEach(([bx,by])=>{ c.beginPath(); c.arc(bx,by,1.3,0,Math.PI*2); c.fill(); }); }); }
function rnObCrystal(c,x,gy,tk){ const top=gy-RN_OBH;
  c.fillStyle='#4a4458'; c.beginPath(); c.ellipse(x+13,gy-2,16,5,0,Math.PI,0); c.fill();
  c.save(); c.shadowColor='rgba(200,140,255,'+(0.5+0.35*Math.sin(tk*0.1))+')'; c.shadowBlur=10;
  [[x+4,top+15,5.5],[x+22,top+11,5.5],[x+13,top,7]].forEach(([cx,ty,w])=>{
    const g=c.createLinearGradient(cx-w,0,cx+w,0); g.addColorStop(0,'#e7c5ff'); g.addColorStop(.5,'#b27af0'); g.addColorStop(1,'#6a34bf');
    c.beginPath(); c.moveTo(cx,ty); c.lineTo(cx+w,ty+w*1.5); c.lineTo(cx+w*0.85,gy-1); c.lineTo(cx-w*0.85,gy-1); c.lineTo(cx-w,ty+w*1.5); c.closePath();
    c.fillStyle=g; c.fill(); c.strokeStyle='#35196a'; c.lineWidth=1.4; c.stroke();
    c.fillStyle='rgba(255,255,255,.55)'; c.beginPath(); c.moveTo(cx-1,ty+4); c.lineTo(cx-w*0.55,ty+w*1.6); c.lineTo(cx-w*0.45,gy-6); c.lineTo(cx-1.5,gy-6); c.closePath(); c.fill(); });
  c.restore(); }
function rnObstacle(c,o,gy,tk){ rnObShadow(c,o.x,gy); const k=RN_KINDS[o.k|0];
  if(k==='rock') rnObRock(c,o.x,gy,tk); else if(k==='crate') rnObCrate(c,o.x,gy); else if(k==='crystal') rnObCrystal(c,o.x,gy,tk); else rnObFence(c,o.x,gy); }

// ---- 말로우(외곽선·셀 셰이딩·달리기/점프/착지 스쿼시/충돌 포즈) ----
function rnMallow(c,x,by,S){
  const w=RN_PW,h=RN_PH, air=!S.grounded, dead=S.crashT>0, ph=S.run*Math.PI*2, s=Math.sin(ph);
  let sx=1, sy=1; if(dead){ sx=1.08; sy=0.9; } else if(S.landT>0){ const k=S.landT/8; sx=1+0.16*k; sy=1-0.14*k; } else if(air){ sx=0.93; sy=1.07; }
  const rot = dead ? -Math.min(0.55,S.crashT*0.05) : air ? Math.max(-0.3,Math.min(0.22,-S.vy*0.018)) : 0;
  const bob = (!air&&!dead) ? Math.abs(s)*2 : 0, OL='#3a1a2c';
  c.save(); c.translate(x+w/2, by-bob); c.rotate(rot); c.scale(sx,sy);
  // 다리 + 운동화
  const feet = dead ? [[-9,-2],[7,-3]] : air ? [[-9,1],[8,-1]] : [[-7+s*6,-1-Math.max(0,s)*3],[6-s*6,-1-Math.max(0,-s)*3]];
  feet.forEach(([fx,fy],i)=>{ const hx=i?5:-6; c.strokeStyle=OL; c.lineWidth=4.4; c.beginPath(); c.moveTo(hx,-6); c.lineTo(fx,fy); c.stroke();
    c.strokeStyle='#f6a8c2'; c.lineWidth=2.4; c.stroke();
    c.fillStyle='#e8413f'; c.strokeStyle=OL; c.lineWidth=1.6; c.beginPath(); c.roundRect(fx-4,fy-3.5,11,6,3); c.fill(); c.stroke(); c.fillStyle='#fff'; c.fillRect(fx-3,fy+1.2,9,1.2); });
  // 뒤쪽 팔
  const armA = dead ? -2.2 : air ? -2.4 : -0.9 - s*0.7;
  const arm=(ax,ay,a)=>{ c.save(); c.translate(ax,ay); c.rotate(a); c.fillStyle='#ffc6d9'; c.strokeStyle=OL; c.lineWidth=1.6; c.beginPath(); c.roundRect(-2.8,0,5.6,10,2.8); c.fill(); c.stroke(); c.restore(); };
  arm(-w/2+4,-h*0.55,-armA);
  // 몸통(마시멜로)
  const top=-h, bh=h-5;
  const g=c.createLinearGradient(0,top,0,top+bh); g.addColorStop(0,'#fff5f8'); g.addColorStop(.55,'#ffc9dc'); g.addColorStop(1,'#f394b6');
  c.beginPath(); c.roundRect(-w/2,top,w,bh,12); c.fillStyle=g; c.fill();
  c.save(); c.clip(); c.fillStyle='rgba(205,80,135,.22)'; c.beginPath(); c.ellipse(w*0.42,top+bh*0.8,w*0.42,bh*0.62,0,0,Math.PI*2); c.fill();
  c.fillStyle='rgba(255,255,255,.85)'; c.beginPath(); c.ellipse(-w*0.18,top+5.5,8,3,-0.15,0,Math.PI*2); c.fill(); c.restore();
  c.strokeStyle=OL; c.lineWidth=2.2; c.beginPath(); c.roundRect(-w/2,top,w,bh,12); c.stroke();
  // 새싹(사이트 공통 마스코트 mallowSVG의 두 잎과 같은 색) — 달릴 때 살랑
  const sway=dead?0.5:air?-0.25:Math.sin(ph*2)*0.12;
  c.save(); c.translate(1,top+1); c.rotate(sway); c.strokeStyle='#38995D'; c.lineWidth=2.2; c.lineCap='round'; c.beginPath(); c.moveTo(0,0); c.lineTo(0,-6); c.stroke();
  [[-1,'#62C681'],[1,'#89DB8B']].forEach(([d,col])=>{ c.beginPath(); c.moveTo(0,-5); c.bezierCurveTo(d*3,-11,d*9,-11,d*11,-8); c.bezierCurveTo(d*8,-5,d*4,-4,0,-5); c.closePath();
    c.fillStyle=col; c.fill(); c.strokeStyle='#38995D'; c.lineWidth=1.3; c.stroke(); });
  c.restore();
  // 얼굴(오른쪽을 본다)
  const ey=top+bh*0.4;
  if(dead){ c.strokeStyle=OL; c.lineWidth=2; [[3,ey],[13,ey]].forEach(([ex,yy])=>{ c.beginPath(); c.moveTo(ex-2.5,yy-2.5); c.lineTo(ex+2.5,yy+2.5); c.moveTo(ex+2.5,yy-2.5); c.lineTo(ex-2.5,yy+2.5); c.stroke(); });
    c.fillStyle=OL; c.beginPath(); c.ellipse(9,top+bh*0.68,2.6,3.2,0,0,Math.PI*2); c.fill(); }
  else { c.fillStyle=OL; [[3,ey],[13,ey]].forEach(([ex,yy])=>{ c.beginPath(); c.ellipse(ex,yy,2.3,3.6,0,0,Math.PI*2); c.fill(); });
    c.fillStyle='#fff'; c.fillRect(3.2,ey-2.6,1.3,1.5); c.fillRect(13.2,ey-2.6,1.3,1.5);
    c.strokeStyle=OL; c.lineWidth=1.8; c.beginPath(); c.moveTo(0,ey-6.5); c.lineTo(5.5,ey-5); c.moveTo(10.5,ey-5); c.lineTo(16,ey-6.5); c.stroke();
    c.fillStyle='rgba(255,120,150,.55)'; c.beginPath(); c.ellipse(-3,ey+5,3,1.8,0,0,Math.PI*2); c.fill(); c.beginPath(); c.ellipse(17,ey+5,2.4,1.8,0,0,Math.PI*2); c.fill();
    c.strokeStyle=OL; c.lineWidth=1.8; c.beginPath(); if(air){ c.ellipse(8.5,ey+7.5,2.4,2.8,0,0,Math.PI*2); c.fillStyle='#c2344f'; c.fill(); c.stroke(); } else { c.moveTo(5.5,ey+6); c.quadraticCurveTo(8.5,ey+9.5,11.5,ey+6); c.stroke(); } }
  // 앞쪽 팔
  arm(w/2-5,-h*0.55,armA);
  c.restore();
}

// ---- 한 장면 그리기(게임·미리보기 공용) ----
function rnScene(c,S,tk){
  const W=S.W,H=S.H,gy=S.groundY,art=S.art; if(!art) return;
  c.save();
  if(S.shake>0 && !fxReduced()){ c.translate((Math.random()-0.5)*S.shake,(Math.random()-0.5)*S.shake*0.6); }
  c.drawImage(art.sky,0,0,W,H);
  for(const st of art.stars){ const a=0.35+0.45*Math.sin(tk*0.05+st.ph); c.fillStyle='rgba(255,247,220,'+a.toFixed(2)+')';
    if(st.big){ c.fillRect(st.x-st.r*1.8,st.y-0.5,st.r*3.6,1); c.fillRect(st.x-0.5,st.y-st.r*1.8,1,st.r*3.6); } c.beginPath(); c.arc(st.x,st.y,st.r,0,Math.PI*2); c.fill(); }
  const snap=v=>Math.round(v*(S.dpr||1))/(S.dpr||1);   // 기기 픽셀에 맞춰 타일 이음새 틈 제거
  art.layers.forEach((L,i)=>{ const off=snap((S.dist*L.spd)%L.P); for(let x=-off; x<W; x+=L.P) c.drawImage(L.cv,x,0,L.P,H);
    if(i===2){ for(const f of S.flies){ const a=0.45+0.4*Math.sin(tk*0.08+f.ph), fy=f.y+Math.sin(tk*0.03+f.ph)*6;
      c.fillStyle='rgba(200,255,140,'+(a*0.25).toFixed(2)+')'; c.beginPath(); c.arc(f.x,fy,5,0,Math.PI*2); c.fill();
      c.fillStyle='rgba(230,255,190,'+a.toFixed(2)+')'; c.beginPath(); c.arc(f.x,fy,1.6,0,Math.PI*2); c.fill(); } } });
  const G=art.ground, goff=snap(S.dist%G.P); for(let x=-goff; x<W; x+=G.P) c.drawImage(G.cv,x,0,G.P,H);
  // 속도감 줄
  const la=Math.min(0.32,(S.spd-7)/12); if(la>0){ c.strokeStyle='rgba(255,255,255,'+la.toFixed(2)+')'; c.lineWidth=1.4; for(const l of S.lines){ c.beginPath(); c.moveTo(l.x,l.y); c.lineTo(l.x+l.len,l.y); c.stroke(); } }
  for(const o of S.obs) rnObstacle(c,o,gy,tk);
  // 말로우 그림자(높이 뜰수록 작고 옅게)
  const k=Math.max(0.35,1-S.py/150); c.fillStyle='rgba(10,6,20,'+(0.34*k).toFixed(2)+')'; c.beginPath(); c.ellipse(S.px+RN_PW/2,gy+1,17*k,3.4*k,0,0,Math.PI*2); c.fill();
  rnMallow(c,S.px,gy-S.py,S,tk);
  rnDrawParts(c,S);
  c.restore();
}
function rnFx(S){ // 게임 규칙과 무관한 연출 갱신
  if(S.landT>0) S.landT--; if(S.shake>0) S.shake*=0.86; if(S.shake<0.3) S.shake=0;
  for(const f of S.flies){ f.x-=S.spd*0.3; if(f.x<-10) f.x=S.W+10; }
  for(const l of S.lines){ l.x-=S.spd*2.4; if(l.x+l.len<0){ l.x=S.W+Math.random()*60; l.y=12+Math.random()*(S.groundY-24); } }
  if(S.grounded && S.crashT===0 && Math.random()<0.28) rnPuff(S,S.px+10,S.groundY-2,1,0.6);
  rnStepParts(S);
}
function rnSnd(kind){ try{ if(!sndOn()) return;
  if(kind==='jump') _tone({freq:360,dur:0.13,type:'square',vol:0.05,glide:420});
  else if(kind==='beat') [659,880,1175].forEach((f,i)=>_tone({freq:f,dur:0.1,type:'triangle',vol:0.11,when:i*0.07}));
}catch(e){} }

function startRun(){
  clearTimeout(RN.overT); RNP.running=false; cancelAnimationFrame(RNP.raf);
  document.getElementById('run-intro-card').style.display='none'; document.getElementById('run-result-card').style.display='none'; document.getElementById('run-game-card').style.display='block';
  rnResize(); const cfg=RN_CFG[RN.diff];
  RN.running=true; RN.over=false; RN.score=0; RN.dist=0; RN.spd=cfg.spd0; RN.py=0; RN.vy=0; RN.grounded=true; RN.run=0; RN.burst=0;
  RN.parts=[]; RN.landT=0; RN.crashT=0; RN.shake=0; RN.tk=0; RN.beat=false; RN.hudM=-1; RN.hudS=-1; RN.prevBest=RN.best[RN.diff].all||0;
  RN.obs=[{x:RN.W+40,k:rnKind([])}]; RN.nextGap=rnNextGap();
  document.getElementById('rn-score').textContent='0'; document.getElementById('rn-dist').textContent='0';
  document.getElementById('rn-hud-best').textContent=RN.prevBest; document.getElementById('rn-score-plate').classList.remove('beat');
  const cue=document.getElementById('rn-cue'); if(cue) cue.classList.remove('hide');
  const toast=document.getElementById('rn-toast'); if(toast) toast.classList.remove('show');
  cancelAnimationFrame(RN.raf); RN.raf=requestAnimationFrame(rnLoop);
}
function rnJump(){ if(!RN.running) return; if(RN.grounded){ RN.vy=RN_JV; RN.grounded=false; rnPuff(RN,RN.px+RN_PW/2,RN.groundY-2,6,2.4); rnSnd('jump');
  try{if(navigator.vibrate)navigator.vibrate(10);}catch(e){} const cue=document.getElementById('rn-cue'); if(cue) cue.classList.add('hide'); } }
function rnHud(){
  if(RN.score!==RN.hudS){ RN.hudS=RN.score; document.getElementById('rn-score').textContent=RN.score; }
  const m=Math.floor(RN.dist/RN_PX_PER_M); if(m!==RN.hudM){ RN.hudM=m; document.getElementById('rn-dist').textContent=m.toLocaleString(); }
  const cfg=RN_CFG[RN.diff], sp=document.getElementById('rn-speed-fill'); if(sp) sp.style.width=Math.round(100*(RN.spd-cfg.spd0)/(cfg.cap-cfg.spd0))+'%';
  if(!RN.beat && RN.prevBest>0 && RN.score>RN.prevBest){ RN.beat=true; rnSnd('beat');
    document.getElementById('rn-score-plate').classList.add('beat'); const toast=document.getElementById('rn-toast'); if(toast){ toast.classList.remove('show'); void toast.offsetWidth; toast.classList.add('show'); } }
}
function rnLoop(){
  if(!RN.running) return; const cfg=RN_CFG[RN.diff]; RN.tk++;
  RN.spd=Math.min(cfg.cap, RN.spd+cfg.acc); RN.run=(RN.run+RN.spd*0.05)%1;
  if(!RN.grounded){ RN.py+=RN.vy; RN.vy-=RN_G; if(RN.py<=0){ RN.py=0; RN.vy=0; RN.grounded=true; RN.landT=8; rnPuff(RN,RN.px+RN_PW/2,RN.groundY-2,7,3); } }
  for(const o of RN.obs) o.x-=RN.spd;
  while(RN.obs.length && RN.obs[0].x < -RN_OBW-6) RN.obs.shift();
  const last=RN.obs[RN.obs.length-1];
  if(!last || (RN.W - last.x) >= RN.nextGap){ RN.obs.push({x:RN.W,k:rnKind(RN.obs)}); RN.nextGap=rnNextGap(); }
  RN.dist+=RN.spd; RN.score=Math.floor(RN.dist*dm(RN.diff)/12); rnHud();
  // 충돌(AABB): 플레이어[px,px+PW]×[py,py+PH] vs 장애물[x,x+OBW]×[0,OBH]
  const pxL=RN.px, pxR=RN.px+RN_PW;
  for(const o of RN.obs){ if(o.x+RN_OBW < pxL) continue; if(o.x > pxR) break; if(RN.py < RN_OBH){ rnGameOver(); return; } }
  rnFx(RN); rnDraw(); RN.raf=requestAnimationFrame(rnLoop);
}
function rnDraw(){ const cv=document.getElementById('rn-canvas'); if(!cv) return; rnScene(cv.getContext('2d'),RN,RN.tk); }
// 충돌 연출(약 0.75초: 흔들림·불꽃·쓰러짐) 뒤 결과 카드. 기록은 충돌 즉시 저장한다(연출 중 이탈해도 유지).
function rnCrashLoop(){
  if(!RN.over || RN.crashT===0) return; RN.crashT++; RN.tk++;
  if(RN.py>0){ RN.py=Math.max(0,RN.py+RN.vy); RN.vy-=RN_G; }
  const cv=document.getElementById('rn-canvas'); if(!cv) return; const c=cv.getContext('2d');
  const spd=RN.spd; RN.spd=0; rnFx(RN); rnScene(c,RN,RN.tk); RN.spd=spd;
  const a=Math.min(1,RN.crashT/10); c.fillStyle='rgba(12,8,30,'+(0.42*a).toFixed(2)+')'; c.fillRect(0,0,RN.W,RN.H);
  c.save(); c.globalAlpha=a; c.textAlign='center'; c.textBaseline='middle'; const fs=Math.round(Math.min(40,RN.W*0.09));
  c.font='900 '+fs+'px Pretendard, system-ui, sans-serif'; c.lineJoin='round'; c.lineWidth=6; c.strokeStyle='#2a1030';
  const y=RN.H*0.42-(1-a)*14; c.strokeText(t('run.gameOver'),RN.W/2,y); c.fillStyle='#ffd66b'; c.fillText(t('run.gameOver'),RN.W/2,y); c.restore();
  if(RN.crashT<46) RN.raf=requestAnimationFrame(rnCrashLoop);
}
function rnShowResult(){ if(!RN.over) return; RN.crashT=0;
  document.getElementById('run-game-card').style.display='none'; document.getElementById('run-result-card').style.display='block'; }
function rnGameOver(){ if(RN.over) return; RN.over=true; RN.running=false; cancelAnimationFrame(RN.raf);
  try{sfx('bad');}catch(e){} try{if(navigator.vibrate)navigator.vibrate(60);}catch(e){}
  const nr=bt_recordScore(RN.best,RN.diff,RN.score); bt_saveBest('brain.run.best',RN.best); missionMark('run');
  document.getElementById('rn-result-emoji').textContent=nr?'🏆':'💥'; document.getElementById('rn-result-title').textContent=nr?t('run.newRecord'):t('run.gameOver');
  document.getElementById('rn-result-score').textContent=RN.score; document.getElementById('rn-r-diff').textContent=RN_DIFF_LABEL(RN.diff); document.getElementById('rn-r-best').textContent=RN.best[RN.diff].all;
  document.getElementById('rn-r-dist').textContent=Math.floor(RN.dist/RN_PX_PER_M).toLocaleString()+' m'; rnUpdateBestLine();
  RN.crashT=1; RN.shake=11; rnPuff(RN,RN.px+RN_PW,RN.groundY-RN.py-RN_PH/2,14,7,'255,214,107','spark');
  RN.raf=requestAnimationFrame(rnCrashLoop); clearTimeout(RN.overT); RN.overT=setTimeout(rnShowResult,780); }
function leaveRun(){ resetRun(); showScreen('games'); }
function resetRun(){ RN.running=false; RN.over=false; RN.crashT=0; clearTimeout(RN.overT); cancelAnimationFrame(RN.raf);
  const g=document.getElementById('run-game-card'); if(g)g.style.display='none'; const r=document.getElementById('run-result-card'); if(r)r.style.display='none'; const i=document.getElementById('run-intro-card'); if(i)i.style.display='block'; rnUpdateBestLine(); }

// ---- 인트로 미리보기: 자동으로 점프하며 달리는 모습(화면이 보일 때만 돈다) ----
function rnPreviewStart(){ const cv=document.getElementById('rn-preview'); if(!cv || RNP.running || RN.running) return;
  requestAnimationFrame(()=>{ if(!cv.offsetParent || RNP.running || RN.running) return;
    rnSize(cv,RNP,232,270,0.56); RNP.dist=0; RNP.py=0; RNP.vy=0; RNP.grounded=true; RNP.parts=[]; RNP.obs=[{x:RNP.W*0.7,k:0}]; RNP.gap=RNP.W*0.55; RNP.tk=0;
    RNP.running=true; cancelAnimationFrame(RNP.raf); RNP.raf=requestAnimationFrame(rnPreviewLoop); }); }
function rnPreviewLoop(){ const cv=document.getElementById('rn-preview');
  if(!cv || !cv.offsetParent || RN.running){ RNP.running=false; return; }
  const S=RNP; S.tk++; S.run=(S.run+S.spd*0.05)%1;
  const nx=S.obs.find(o=>o.x+RN_OBW>S.px);
  if(S.grounded && nx && nx.x-(S.px+RN_PW)<40 && nx.x-(S.px+RN_PW)>0){ S.vy=RN_JV; S.grounded=false; rnPuff(S,S.px+RN_PW/2,S.groundY-2,6,2.4); }
  if(!S.grounded){ S.py+=S.vy; S.vy-=RN_G; if(S.py<=0){ S.py=0; S.vy=0; S.grounded=true; S.landT=8; rnPuff(S,S.px+RN_PW/2,S.groundY-2,7,3); } }
  for(const o of S.obs) o.x-=S.spd; while(S.obs.length && S.obs[0].x<-RN_OBW-6) S.obs.shift();
  const last=S.obs[S.obs.length-1]; if(!last || S.W-last.x>=S.gap){ S.obs.push({x:S.W,k:rnKind(S.obs)}); S.gap=S.W*(0.5+Math.random()*0.35); }
  S.dist+=S.spd; rnFx(S); rnScene(cv.getContext('2d'),S,S.tk);
  if(fxReduced()){ S.running=false; return; }   // 움직임 줄이기: 첫 장면만 정지 화면으로
  S.raf=requestAnimationFrame(rnPreviewLoop); }
document.addEventListener('keydown',e=>{ if((e.code==='Space'||e.code==='ArrowUp') && RN.running){ e.preventDefault(); rnJump(); } });
