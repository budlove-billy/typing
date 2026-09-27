/* 밸런스 제안 — 현재값(CUR)에서 바뀌는 것만. calibrate.mjs가 난이도 배수·메달 목표를 여기에 채운다.
   원칙: ① 같은 사람 점수비 쉬움 0.8 : 보통 1 : 어려움 1.25  ② 메달 = 🥉초보 중앙값 🥈상위25% 🥇상위10% 💎상위1%
        ③ 끝없는 게임은 위험이 계속 오른다(상한 없음)  ④ 어려움은 '배수'가 아니라 '다른 압박'으로 느껴진다 */
import fs from 'fs';
import { CUR, GAMES, rnd } from './model.mjs';

const clone = o => JSON.parse(JSON.stringify(o));
export const PROP = clone(CUR);

// ---- ④ 60초 문항형 어려움: 문항당 제한시간(넘기면 오답 처리 — 콤보 끊김, 시간 감점 없음) ----
PROP.DEADLINE = { stroop:{hard:1500}, flank:{hard:900}, switch:{hard:1500}, rotate:{hard:2200}, guess:{hard:3200} };

// ---- 말로우 런 v2 ----
// 스폰은 '거리 누적'으로(배열이 비어도 간격 유지 → 기기 폭과 무관), 세계 폭은 논리 400px로 고정(PC·폰 동일 판정).
// 속도 대신 '시간 배속'이 오른다: 지형·점프 궤적은 그대로, 모든 것이 ts배 빨라진다 → 점프 창(ms)이 계속 좁아지고 템포가 빨라진다.
PROP.RN2 = {
  easy:  { ts0:0.80, a:0.0042, gLo:1.25, gHi:2.20, clusterP:0.00, clusterMax:0, tallP:0.00 },
  normal:{ ts0:1.00, a:0.0052, gLo:1.12, gHi:2.00, clusterP:0.18, clusterMax:1, tallP:0.15 },
  hard:  { ts0:1.18, a:0.0078, gLo:1.05, gHi:1.85, clusterP:0.30, clusterMax:2, tallP:0.30 },
};
// ---- 말로우 타워: 가속을 '점수'(난이도 배수가 곱해진 값)가 아니라 '깨문 횟수'에 건다 ----
PROP.CP2 = { easy:{decay:2.6,gain:8.0,forkP:0.45,accel:0.13}, normal:{decay:3.4,gain:7.0,forkP:0.55,accel:0.20}, hard:{decay:4.2,gain:6.2,forkP:0.65,accel:0.28} };
// ---- 인원수 세기: 연속 보너스 상한(+20) + 4연속마다 이벤트 1개 추가(판이 스스로 어려워진다) ----
PROP.HC2 = { streakCap:10, rampEvery:4 };
// ---- 틀린 그림: 판 클리어 시간 보너스가 레벨마다 줄어든다(상위권도 언젠가 끝난다) ----
PROP.DF2 = { bonusDecay:0.6, bonusMin:2 };
// ---- 높은음 찾기: 음정차 하한을 낮춰 상위권도 끝까지 변별(지금은 상위10%와 1%가 둘 다 하한에서 만점) ----
PROP.PT.cfg.normal.cMin=16; PROP.PT.cfg.hard.cMin=10;
// ---- 풀이형: '기준 시간 대비' 점수 — 기준(par)에 풀면 K, 빠를수록 더(상한 없음 — 사람 손 속도가 상한), 느려도 0.15배는 남는다 ----
PROP.PAR = {   // par = 보통 실력(casual)의 대략적인 풀이 시간(초)
  sort:{ easy:45, normal:110, hard:220 }, slide:{ easy:70, normal:330, hard:900 }, nono:{ easy:60, normal:280, hard:560 }, sudoku:{ easy:560, normal:1150, hard:2200 },
};

// calibrate.mjs 결과(있으면)
try { const c = JSON.parse(fs.readFileSync(new URL('./calib.json', import.meta.url), 'utf8'));
  PROP.DMULT_GAME = c.dm; PROP.MEDAL_FIXED = c.medals; PROP.K = c.K || {}; } catch (e) { PROP.K = {}; }
PROP.MEDAL_FIXED = PROP.MEDAL_FIXED || {};
PROP.MEDAL_FIXED.iq = [100, 112, 122, 132];   // IQ 척도 그대로: 평균 · 상위25% · 상위7% · 상위2%

/* ======================= 바뀌는 게임 모델 ======================= */
const Phi = z => 0.5*(1+Math.tanh(0.7978845608*(z+0.044715*z*z*z)));
function gauss(){ let u=0,v=0; while(!u) u=rnd(); while(!v) v=rnd(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }
function lognorm(mean, cv=0.25){ const s=Math.sqrt(Math.log(1+cv*cv)), m=Math.log(mean)-s*s/2; return Math.exp(m+s*gauss()); }
const pick = a => a[Math.floor(rnd()*a.length)];
const ri = (a,b)=>a+Math.floor(rnd()*(b-a+1));
const comboBonus = c => Math.min(Math.max(0,(c|0)-1), 10)*2;
const comboPts = c => 10 + comboBonus(c);
const dmOf = (C,id,d) => (C.DMULT_GAME[id]&&C.DMULT_GAME[id][d]) || C.DMULT[d] || 1;

function timedDL(T, item, { pen=2, after=0, dm=1, deadline=0 }={}){
  let t=0, score=0, combo=0, lim=T*1000;
  while(true){ const it=item(); let rt=it.rt, timeout=false; if(deadline && rt>deadline){ rt=deadline; timeout=true; }
    t+=rt; if(t>lim) break;
    if(!timeout && rnd()>=it.pErr){ combo++; score+=Math.round((it.pts?it.pts(combo):comboPts(combo))*dm); t+=after; }
    else { combo=0; if(!timeout) lim-=pen*1000; t+=250; } }
  return score;
}
// 60초 문항형 5종: 모델 식은 model.mjs와 같고 어려움에 제한시간만 더한다
const TIMED = {
  stroop:(d,P,C)=>{ const c=C.ST[d]; return timedDL(60, ()=>{ const inc=rnd()<c.incong; return { rt: lognorm(P.rt0+140+P.bit*Math.log2(c.colors)+(inc?P.inh:0)+P.mot*0.4), pErr: P.err+(inc?0.035:0)+0.006*(c.colors-4) }; }, {dm:dmOf(C,'stroop',d), deadline:(C.DEADLINE.stroop||{})[d]}); },
  flank:(d,P,C)=>{ const c=C.FK[d]; return timedDL(60, ()=>{ const inc=rnd()<c.incong; return { rt: lognorm(P.rt0+P.bit+(inc?P.inh*0.6:0)+P.mot*0.3), pErr: P.err*0.8+(inc?0.03:0) }; }, {dm:dmOf(C,'flank',d), deadline:(C.DEADLINE.flank||{})[d]}); },
  switch:(d,P,C)=>{ const c=C.SW[d]; return timedDL(60, ()=>{ const s=rnd()<c.switchP; return { rt: lognorm(P.rt0+260+P.bit+(s?P.sw:0)+P.mot*0.3), pErr: P.err+(s?0.045:0) }; }, {dm:dmOf(C,'switch',d), deadline:(C.DEADLINE.switch||{})[d]}); },
  rotate:(d,P,C)=>{ const A=C.RT_ANG[d]; return timedDL(60, ()=>{ const a=pick(A), ang=Math.min(a,360-a); return { rt: lognorm(650+P.rotMs*ang+P.mot*0.3), pErr: P.err+0.11*ang/180 }; }, {dm:dmOf(C,'rotate',d), deadline:(C.DEADLINE.rotate||{})[d]}); },
  guess:(d,P,C)=>{ const mx=C.GU[d].mx, f=Math.log10(mx)/Math.log10(30); return timedDL(60, ()=>{ const op=pick(['+','-','×']); const w={'+':650,'-':800,'×':1350}[op]; return { rt: lognorm(700+P.calc*w*f+P.bit*Math.log2(3)), pErr: P.err+0.02+0.03*(f-1) }; }, {dm:dmOf(C,'guess',d), after:140, deadline:(C.DEADLINE.guess||{})[d]}); },
};

export const GAMES_OVERRIDE = Object.assign({}, TIMED, {
// 암산: 정답 수 → 다른 게임처럼 comboPts×배수(오답 -2초 없음은 유지)
math:(d,P,C)=>{ const k={easy:'b',normal:'a',hard:'e'}[d], dm=dmOf(C,'math',d); let t=0, score=0, combo=0;
  while(true){ let w, dig; if(k==='b'){ w=1100; dig=1.5; } else if(k==='a'){ const op=pick(['+','-','×']); w={'+':2300,'-':2700,'×':3300}[op]; dig=2.6; } else { const op=pick(['+','-','×','÷']); w={'+':4200,'-':4800,'×':9500,'÷':5200}[op]; dig=3.3; }
    t+=lognorm(P.calc*w+260*dig+400,0.3); if(t>60000) return score; if(rnd()>=P.err+(k==='e'?0.07:k==='a'?0.03:0.01)){ combo++; score+=Math.round(comboPts(combo)*dm); } else combo=0; } },
// 글자 맞추기: 전용 배율(AG_MULT) 대신 보정 배수
anagram:(d,P,C)=>{ const Ls=C.AG.len[d], mult=dmOf(C,'anagram',d), pen=C.AG.pen[d]; let t=0, lim=60000, score=0, combo=0;
  while(true){ const L=pick(Ls); const solve=lognorm(P.lex*(500*Math.pow(L,1.75))+L*P.mot,0.45); t+=solve; if(t>lim) return score;
    if(rnd()<P.err+0.025*L){ combo=0; lim-=pen*1000; t+=lognorm(P.lex*400*L); if(t>lim) return score; }
    combo++; const sp=Math.max(0,10-Math.floor(solve/1000)); score+=Math.round((L*5+sp+comboBonus(combo))*mult); } },
// 인원수 세기: 연속 보너스 상한 + 4연속마다 이벤트 +1, 점수에 배수 적용
count:(d,P,C)=>{ const c=C.HC[d], H=C.HC2, dm=dmOf(C,'count',d); let lives=3, score=0, st=0, ok=0;
  for(let r=0;r<400&&lives>0;r++){ const ev=ri(c.events[0],c.events[1])+Math.floor(ok/H.rampEvery);
    const load=ev*0.55+(c.kMax-1)*1.3+(900-c.gap)/160; const p=1-Math.min(.95,P.cnt*0.55*load);
    if(rnd()<p){ st++; ok++; score+=Math.round((c.pts+Math.min(st-1,H.streakCap)*2)*dm); } else { st=0; lives--; } } return score; },
// 틀린 그림: 보너스 감소
diff:(d,P,C)=>{ const c=C.DF.cfg[d], T0=C.DF.time[d]*1000, B=C.DF.bonus[d], dm=dmOf(C,'diff',d), D2=C.DF2; let left=T0, score=0, combo=0, lv=1;
  while(left>0 && lv<400){ const n=Math.min(c.nMax,c.nStart+Math.floor((lv-1)/3)), k=Math.max(1,Math.min(Math.floor(n*n/4),1+Math.floor((lv-1)/2)));
    for(let j=0;j<k;j++){ const rt=lognorm(300+(n*n/(k-j+1))*P.srch*5.5+P.mot*0.6,0.35); left-=rt; if(left<=0) return score;
      if(rnd()<P.err*0.7){ combo=0; left-=2000; } combo++; score+=Math.round(comboPts(combo)*dm); }
    lv++; left=Math.min(T0, left+Math.max(D2.bonusMin, B-D2.bonusDecay*(lv-2))*1000); left-=350; } return score; },
// 타워: 가속 = 깨문 횟수 기준
chop:(d,P,C)=>{ const c=C.CP2[d], dm=dmOf(C,'chop',d); let g=100, t=0, score=0, chops=0; let next=lognorm(P.chop);
  while(t<900000){ t+=100; g-=(c.decay+chops*c.accel)*0.1; if(g<=0) return score;
    while(next<=100 && g>0){ const pErr=P.err*0.45+0.004*(c.forkP-0.5)*10; if(rnd()<pErr) return score; score+=Math.round(10*dm); chops++; g=Math.min(100,g+c.gain); next+=lognorm(P.chop*(1+c.forkP*0.25),0.2); }
    next-=100; } return score; },
// 풀이형 4종: 기준시간 대비 점수 (시간·이동 모델은 model.mjs와 같다)
sort:(d,P,C)=>{ const k=C.SO[d].k; const moves=Math.round(k*3.2*(1+(1-P.plan)*1.1)*lognorm(1,0.15)); const sec=moves*lognorm(1.8*P.calc*(1+k*0.06),0.25)+k*4*P.calc; return parScore(C,'sort',d,sec,0); },
slide:(d,P,C)=>{ const n=C.SL[d].n; const moves={3:48,4:190,5:520}[n]*(1+(1-P.plan)*1.3)*lognorm(1,0.2); const sec=moves*lognorm(0.75*P.calc,0.2)+n*n*2; return parScore(C,'slide',d,sec,0); },
nono:(d,P,C)=>{ const n=C.NO[d].n; const sec=lognorm(Math.pow(n,2.2)*1.35*P.calc*(1.4-P.plan*0.5),0.3); return parScore(C,'nono',d,sec,0); },
sudoku:(d,P,C)=>{ const sec=lognorm({easy:420,normal:900,hard:1800}[d]*P.calc*(1.5-P.plan*0.6),0.35); const mis=Math.round((1-P.plan)*4*rnd()*{easy:1,normal:1.5,hard:2}[d]); const hint=d==='hard'?Math.round((1-P.plan)*3*rnd()):0;
  return parScore(C,'sudoku',d,sec,mis*0.04+hint*0.06); },
// 반응 속도: 500-rt/2는 상위1%와 초보의 차이가 19%뿐 → 1000-2.2×rt (최소 20). no-go 참기 150, 조기·오탭 0
react:(d,P,C)=>{ const c=C.RC[d], dm=dmOf(C,'react',d); let s=0; for(let i=0;i<c.trials;i++){ if(rnd()<c.noGoP){ if(rnd()>P.err*2.2+0.03) s+=Math.round(150*dm); }
  else { const rt=lognorm(P.rt0+20,0.18); if(rt<c.win) s+=Math.round(Math.max(20,1000-2.2*rt)*dm); } } return s; },
// 받기: 판 안에서 점점 빨라진다(낙하 속도 +1.2%/초, 생성 간격 -0.6%/초) — 지금은 끝까지 같은 속도라 실력 차가 안 난다
catch:(d,P,C)=>{ const c=C.CA[d], dm=dmOf(C,'catch',d); let t=0, lim=60000, score=0, combo=0, lane=1, busy=0; const items=[]; let ns=0; const step=P.mot*0.7;
  while(t<lim){ t+=40; const k=t/1000, spd=c.spd*(1+0.012*k), spawn=c.spawn*Math.max(0.45,1-0.006*k), fall=288/spd*1000;
    if(t>=ns){ items.push({lane:ri(0,3), land:t+fall, bad:rnd()<c.badP}); ns=t+spawn; }
    for(let i=items.length-1;i>=0;i--){ const it=items[i]; if(t>=it.land){ if(it.lane===lane){ if(it.bad){ combo=0; lim-=3000; } else { combo++; score+=Math.round(comboPts(combo)*dm); } } else if(!it.bad) combo=0; items.splice(i,1); } }
    if(t>=busy){ const soon=items.filter(i=>i.land>t).sort((a,b)=>a.land-b.land); const reach=i=>i.lane===lane||Math.abs(i.lane-lane)*step+P.rt0*0.5<=(i.land-t);
      let goal=soon.find(i=>!i.bad&&reach(i)); if(goal&&rnd()>P.plan+0.25) goal=null; const danger=soon.find(i=>i.bad&&i.lane===lane&&i.land-t<700);
      let want=goal?goal.lane:lane; if(danger&&want===lane) want=lane===0?1:lane-1; if(danger&&rnd()<P.err*2) want=lane;
      if(want!==lane){ lane+=want>lane?1:-1; busy=t+lognorm(step,0.2); } } } return score; },
run:(d,P,C)=>runV2(P,C.RN2[d],dmOf(C,'run',d)),
run_pc:(d,P,C)=>runV2(P,C.RN2[d],dmOf(C,'run',d)),   // 논리 폭 고정 → PC도 같은 판
});
function parScore(C,id,d,sec,pen){ const K=(C.K[id]&&C.K[id][d])||1000; const r=Math.max(0.15,Math.pow(C.PAR[id][d]/sec,0.8)); return Math.max(10,Math.round(K*r*(1-pen))); }

/* ---- 런 v2 ---- 물리 1스텝 = 현재 1프레임과 같다(G 0.9, JV 15). 한 화면 프레임에 ts스텝 진행. */
const G=0.9, JV=15, PW=40, OBH_LOW=46, OBH_TALL=64, OBW=26, BASE=6, WORLD=400, PX=Math.round(WORLD*0.16);
function aboveSteps(h){ let py=0,vy=JV,k=0,a=[]; while(true){ k++; py+=vy; vy-=G; if(py<=0) break; if(py>=h) a.push(k); } return [a[0],a[a.length-1]]; }
const ABOVE={ [OBH_LOW]:aboveSteps(OBH_LOW), [OBH_TALL]:aboveSteps(OBH_TALL) };
export function runV2(P, cfg, dm, { capSec=600, trace=false }={}){
  const AIR=2*JV/G, safe=BASE*AIR+OBW+24;
  let step=0, frame=0, acc=0, dist=0, py=0, vy=0, gr=true, since=0, burst=0, gap=0, jumpAt=null, planFor=null;
  const obs=[];
  const nextGap=()=>{ if(burst>0){ burst--; return safe*(1.03+rnd()*0.09); } if(cfg.clusterMax>0 && rnd()<cfg.clusterP){ burst=cfg.clusterMax; return safe*(1.03+rnd()*0.09); } return safe*(cfg.gLo+rnd()*(cfg.gHi-cfg.gLo)); };
  gap=WORLD*0.9;
  const lapse=P.err*0.03;
  while(frame < capSec*60){
    frame++; const sec=frame/60, ts=cfg.ts0+cfg.a*sec; acc+=ts; let n=Math.floor(acc); acc-=n;
    // 사람의 판단은 '화면 프레임' 단위: 가장 가까운 장애물의 창 한가운데를 노리고 오차를 더한다(실제 ms)
    if(gr && planFor===null){ const o=obs.find(o=>o.x+OBW>PX); if(o){ const [a0,a1]=ABOVE[o.h]; const s=(o.x-PX-PW)/BASE, e=(o.x+OBW-PX)/BASE; const idealStep=(s+e-(a0+a1))/2;
        const idealFrame=frame+idealStep/ts; let press=idealFrame+gauss()*P.tsd/16.67;
        const seeFrame=o.born+ (P.rt0*0.85)/16.67;           // 나타난 뒤 반응할 시간이 있어야 누를 수 있다
        if(press<seeFrame) press=seeFrame+Math.abs(gauss())*1.5;
        if(rnd()<lapse) press+= (rnd()<0.5?-1:1)*(8+rnd()*10);  // 가끔 한눈판다
        planFor=o; jumpAt=press; } }
    for(let k=0;k<n;k++){
      step++;
      if(gr && jumpAt!==null && frame+ k/n >= jumpAt){ vy=JV; gr=false; jumpAt=null; }
      if(!gr){ py+=vy; vy-=G; if(py<=0){ py=0; vy=0; gr=true; planFor=null; } }
      for(const o of obs) o.x-=BASE; while(obs.length && obs[0].x<-OBW-6){ if(obs[0]===planFor){ planFor=null; jumpAt=null; } obs.shift(); }
      since+=BASE; if(since>=gap){ obs.push({x:WORLD, h: rnd()<cfg.tallP?OBH_TALL:OBH_LOW, born:frame}); since=0; gap=nextGap(); }
      dist+=BASE;
      for(const o of obs){ if(o.x+OBW<PX) continue; if(o.x>PX+PW) break; if(py<o.h) return trace?{score:Math.floor(dist*dm/12),sec}:Math.floor(dist*dm/12); }
    }
  }
  return trace?{score:Math.floor(dist*dm/12),sec:capSec}:Math.floor(dist*dm/12);
}
