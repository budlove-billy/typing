/* ===== 오늘의 퍼즐 연출 (모아모아·말로우 크라운·말로우 탱고 공용, 2026-09-28) =====
   DFX.confetti()           — 풀이 완료: 화면 위에서 색종이가 쏟아진다(약 2.4초, 자동 정리)
   DFX.burst(x,y,colors)    — 한 점에서 튀는 작은 불꽃(왕관·해·달 놓기, 그룹 정답)
   DFX.cascade(els,cls,ms)  — 칸마다 차례로 클래스를 붙인다(완성 판이 물결처럼 빛남)
   움직임 줄이기 설정을 켠 사용자에게는 색종이·불꽃을 생략한다. */
(function(){
'use strict';
const reduce=()=>{ try{ return matchMedia('(prefers-reduced-motion: reduce)').matches; }catch(e){ return false; } };
const PAL=['#ffd166','#ff6f9c','#8b6ff0','#4cc9f0','#7bd88f','#ff9f43'];
function layer(){ let c=document.getElementById('dfx-layer'); if(c) return c;
  c=document.createElement('canvas'); c.id='dfx-layer';
  c.style.cssText='position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:9000';
  document.body.appendChild(c); return c; }
let parts=[], raf=0;
function run(){ const c=layer(), dpr=Math.min(2,window.devicePixelRatio||1);
  if(c.width!==innerWidth*dpr){ c.width=innerWidth*dpr; c.height=innerHeight*dpr; }
  const g=c.getContext('2d'); g.setTransform(dpr,0,0,dpr,0,0); g.clearRect(0,0,innerWidth,innerHeight);
  parts=parts.filter(p=>p.life>0);
  for(const p of parts){ p.life--; p.vy+=p.g; p.vx*=0.99; p.x+=p.vx; p.y+=p.vy; p.rot+=p.vr;
    g.save(); g.globalAlpha=Math.min(1,p.life/25); g.translate(p.x,p.y); g.rotate(p.rot); g.fillStyle=p.c;
    if(p.round){ g.beginPath(); g.arc(0,0,p.s/2,0,Math.PI*2); g.fill(); } else g.fillRect(-p.s/2,-p.s/4,p.s,p.s/2);
    g.restore(); }
  if(parts.length) raf=requestAnimationFrame(run); else { raf=0; g.clearRect(0,0,innerWidth,innerHeight); } }
function kick(){ if(!raf) raf=requestAnimationFrame(run); }
function confetti(colors){ if(reduce()) return; const P=colors||PAL;
  for(let i=0;i<130;i++) parts.push({x:Math.random()*innerWidth, y:-20-Math.random()*innerHeight*0.4, vx:(Math.random()-0.5)*2.2, vy:2+Math.random()*3,
    g:0.05, rot:Math.random()*6, vr:(Math.random()-0.5)*0.3, s:7+Math.random()*7, c:P[i%P.length], life:130+Math.random()*40, round:false});
  kick(); }
function burst(x,y,colors,n){ if(reduce()) return; const P=colors||PAL;
  for(let i=0;i<(n||12);i++){ const a=Math.PI*2*i/(n||12)+Math.random()*0.4, v=2.2+Math.random()*2.6;
    parts.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v-1,g:0.12,rot:0,vr:0,s:4+Math.random()*4,c:P[i%P.length],life:34+Math.random()*14,round:true}); }
  kick(); }
function center(el){ const r=el.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }
function cascade(els,cls,ms){ [...els].forEach((el,i)=>setTimeout(()=>el.classList.add(cls),i*(ms||28))); }
window.DFX={confetti,burst,cascade,center};
})();
