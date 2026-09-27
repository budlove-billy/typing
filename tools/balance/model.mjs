/* 밸런스 시뮬레이터 — 플레이어 5단계 × 게임 34종 × 난이도 3단계.
   점수 규칙은 index.html 코드를 그대로 옮겼고(주석에 원본 위치), 사람 쪽은 과제별 반응시간·오답률·기억폭 모델.
   핵심: 난이도가 올라가면 '사람이 느려지고 더 틀린다' — 예전 봇은 난이도와 무관하게 같은 간격으로 눌러서
   어려움 = 배수만큼 공짜 점수로 보였다.
   사용: import { TIERS, GAMES, CUR } from './model.mjs' */

export const TIERS = {
  // 백분위 대략: novice P25 · casual P50 · good P75 · skilled P90 · expert P99 (모바일 터치 기준, 성인)
  novice:  { rt0:360, mot:330, bit:190, inh:190, sw:330, err:.070, span:5.6, tsd:62, jndC:45, jndL:9.0, jndA:18, srch:58, rotMs:3.2, calc:1.55, mem:.55, cnt:.10, lex:1.5, steer:9.0, plan:.55, chop:360 },
  casual:  { rt0:320, mot:285, bit:160, inh:150, sw:260, err:.050, span:6.4, tsd:48, jndC:28, jndL:7.0, jndA:13, srch:46, rotMs:2.6, calc:1.20, mem:.66, cnt:.07, lex:1.2, steer:7.2, plan:.68, chop:300 },
  good:    { rt0:292, mot:255, bit:140, inh:120, sw:210, err:.035, span:7.1, tsd:38, jndC:18, jndL:5.6, jndA:10, srch:38, rotMs:2.1, calc:1.00, mem:.76, cnt:.05, lex:1.0, steer:5.8, plan:.80, chop:255 },
  skilled: { rt0:268, mot:228, bit:125, inh: 95, sw:170, err:.025, span:7.8, tsd:30, jndC:12, jndL:4.6, jndA: 8, srch:32, rotMs:1.7, calc:0.80, mem:.85, cnt:.035,lex:0.82,steer:4.7, plan:.90, chop:215 },
  expert:  { rt0:242, mot:202, bit:110, inh: 75, sw:130, err:.015, span:8.7, tsd:22, jndC: 7, jndL:3.6, jndA: 6, srch:26, rotMs:1.3, calc:0.62, mem:.93, cnt:.02, lex:0.66, steer:3.6, plan:.97, chop:180 },
};
export const TIER_KEYS = Object.keys(TIERS);
export const DIFFS = ['easy','normal','hard'];

// ---------- 난수·분포 ----------
let _s = 12345;
export function seed(n){ _s = n>>>0 || 1; }
export function rnd(){ _s = (_s + 0x6D2B79F5)>>>0; let q=_s; q=Math.imul(q^q>>>15,q|1); q^=q+Math.imul(q^q>>>7,q|61); return ((q^q>>>14)>>>0)/4294967296; }
function gauss(){ let u=0,v=0; while(!u) u=rnd(); while(!v) v=rnd(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }
function lognorm(mean, cv=0.25){ const s=Math.sqrt(Math.log(1+cv*cv)), m=Math.log(mean)-s*s/2; return Math.exp(m+s*gauss()); }
const Phi = z => 0.5*(1+Math.tanh(0.7978845608*(z+0.044715*z*z*z)));   // 표준정규 누적(근사)
const logistic = x => 1/(1+Math.exp(-x));
const ri = (a,b)=>a+Math.floor(rnd()*(b-a+1));
const pick = a => a[Math.floor(rnd()*a.length)];

// ---------- 공통 점수 (index.html L6370~6385) ----------
const COMBO_CAP = 10;
const comboBonus = c => Math.min(Math.max(0,(c|0)-1), COMBO_CAP)*2;
const comboPts = c => 10 + comboBonus(c);

/* ======================= 현재 설정값 (index.html에서 옮김) ======================= */
export const CUR = {
  DMULT:{easy:1, normal:1.4, hard:2},
  DMULT_GAME:{ merge:{easy:1,normal:7,hard:70} },
  ST:{ easy:{colors:4,incong:0.5}, normal:{colors:5,incong:0.7}, hard:{colors:6,incong:0.85} },
  FK:{ easy:{incong:0.4}, normal:{incong:0.62}, hard:{incong:0.82} },
  SW:{ easy:{switchP:0.3}, normal:{switchP:0.45}, hard:{switchP:0.6} },
  RT_ANG:{ easy:[90,180,270], normal:[45,90,135,180,225,270,315], hard:[30,60,90,120,150,180,210,240,270,300,330] },
  GU:{ easy:{mx:30}, normal:{mx:90}, hard:{mx:400} },
  SP:{ easy:{startN:2,maxN:6,d0:28,dStep:1.5,dMin:13}, normal:{startN:3,maxN:7,d0:23,dStep:1.3,dMin:10}, hard:{startN:4,maxN:8,d0:19,dStep:1.1,dMin:8} },
  OD:{ easy:{startN:2,maxN:6,a0:66,aStep:4,aMin:20}, normal:{startN:3,maxN:7,a0:54,aStep:3.5,aMin:15}, hard:{startN:4,maxN:8,a0:44,aStep:3,aMin:11} },
  BB:{ easy:{n:8,kMin:2,kMax:2,valMax:9}, normal:{n:10,kMin:2,kMax:3,valMax:12}, hard:{n:12,kMin:3,kMax:4,valMax:15} },
  NB:{ n:{easy:1,normal:2,hard:3}, int:{easy:2600,normal:2300,hard:2000} },
  TR_START:{easy:5,normal:7,hard:10},
  WK:{ easy:{max:1,win:950,gap:600,badP:0.15}, normal:{max:2,win:820,gap:420,badP:0.22}, hard:{max:3,win:780,gap:260,badP:0.28} },
  CA:{ easy:{spd:95,spawn:900,badP:0.18}, normal:{spd:135,spawn:720,badP:0.26}, hard:{spd:180,spawn:560,badP:0.34} },
  RC:{ easy:{trials:10,noGoP:0.15,win:1200}, normal:{trials:12,noGoP:0.25,win:1100}, hard:{trials:14,noGoP:0.35,win:1000} },
  CM:{ pairs:{easy:4,normal:6,hard:8}, time:{easy:60,normal:75,hard:90} },
  HC:{ easy:{events:[3,4],gap:900,kMax:1,pts:10}, normal:{events:[5,6],gap:700,kMax:2,pts:15}, hard:{events:[7,9],gap:500,kMax:3,pts:22} },
  FM:{ start:{easy:3,normal:4,hard:5}, speed:{easy:1.3,normal:1.0,hard:0.75} },
  ML:{ easy:{start:2,speed:620}, normal:{start:3,speed:500}, hard:{start:4,speed:400} },
  RV:{ easy:{start:3,speed:900}, normal:{start:4,speed:750}, hard:{start:5,speed:600} },
  RH:{ easy:{start:2,base:460}, normal:{start:3,base:400}, hard:{start:4,base:340} },
  PT:{ cfg:{ easy:{nStart:3,nMax:5,c0:100,cStep:6,cMin:35}, normal:{nStart:4,nMax:6,c0:80,cStep:5,cMin:26}, hard:{nStart:5,nMax:7,c0:62,cStep:5,cMin:18} }, time:{easy:60,normal:75,hard:90} },
  DF:{ cfg:{ easy:{nStart:3,nMax:5}, normal:{nStart:4,nMax:6}, hard:{nStart:5,nMax:7} }, time:{easy:30,normal:40,hard:50}, bonus:{easy:8,normal:10,hard:12} },
  AG:{ len:{easy:[2,3],normal:[4],hard:[5,6]}, mult:{easy:1,normal:1.4,hard:2}, pen:{easy:0,normal:1,hard:2}, hints:{easy:3,normal:2,hard:1} },
  WS:{ cfg:{ easy:{n:6,k:3,maxLen:4,diag:false}, normal:{n:8,k:4,maxLen:5,diag:false}, hard:{n:9,k:5,maxLen:6,diag:true} }, time:{easy:60,normal:80,hard:100} },
  TC:{ easy:{steps:5,w:54}, normal:{steps:9,w:46}, hard:{steps:13,w:38} },
  CP:{ easy:{decay:2.8,gain:8,forkP:0.5,accel:0.015}, normal:{decay:3.5,gain:6.5,forkP:0.55,accel:0.02}, hard:{decay:4.4,gain:5.5,forkP:0.65,accel:0.025} },
  RN:{ easy:{spd0:4.2,acc:0.0010,cap:9.0,gapRand:180,clusterP:0,clusterMax:0}, normal:{spd0:5.2,acc:0.0015,cap:11.0,gapRand:150,clusterP:0.24,clusterMax:1}, hard:{spd0:6.4,acc:0.0022,cap:12.5,gapRand:110,clusterP:0.36,clusterMax:2} },
  SO:{ easy:{k:4,base:500}, normal:{k:6,base:1000}, hard:{k:8,base:1600} },
  SL:{ easy:{n:3,base:600}, normal:{n:4,base:1200}, hard:{n:5,base:2000} },
  NO:{ easy:{n:5,base:500,rate:5}, normal:{n:8,base:1100,rate:3.5}, hard:{n:10,base:1800,rate:2.6} },
  SK:{ base:{easy:60,normal:85,hard:110} },
  MR:{ n:{easy:5,normal:4,hard:3} },
  // 메달: GAME_REF × {0.6,1.8,4,8}, run만 고정
  REF:{flash:70,count:770,nback:110,cards:530,stroop:1470,switch:1510,trail:130,react:5000,rotate:660,math:45,iq:135,sudoku:110,whack:2280,melody:460,bubble:460,spot:870,odd:900,slide:700,merge:20000,chop:1300,run:600,sort:650,flank:2510,guess:780,rev:160,rhythm:600,catch:2620,fit:800,nono:1300,anagram:980,wordsearch:890,diff:1820,pitch:480,trace:600},
  MEDAL_RATIO:[.6,1.8,4,8],
  MEDAL_FIXED:{ run:[600,1800,4000,8000] },
};
const dmOf = (C,id,d) => (C.DMULT_GAME[id]&&C.DMULT_GAME[id][d]) || C.DMULT[d] || 1;

/* 60초 문항형 공통 엔진: 문항 생성→반응시간→정오답, 오답 -2초(대부분 게임 공통) */
function timed(T, item, { pen=2, after=0, dm=1, maxItems=1e4 }={}){
  let t=0, score=0, combo=0, n=0, ok=0; let lim=T*1000;
  while(n<maxItems){ const it=item(n, ok); t += it.rt; if(t>lim) break; n++;
    if(rnd() >= it.pErr){ ok++; combo++; score += Math.round((it.pts?it.pts(combo):comboPts(combo))*dm); t += after; }
    else { combo=0; lim -= pen*1000; if(it.retry) { /* 같은 문항 재시도 — 다음 루프에서 다시 푼다 */ } }
  }
  return { score, ok, n };
}

/* ======================= 게임별 모델 ======================= */
export const GAMES = {
// 색깔 맞추기 L6744: 정답당 comboPts×dm, 오답 -2초. 색 수↑ = Hick 선택시간↑, 부조화↑ = 간섭시간↑
stroop:(d,P,C)=>{ const c=C.ST[d]; return timed(60, ()=>{ const inc=rnd()<c.incong; return {
  rt: lognorm(P.rt0 + 140 + P.bit*Math.log2(c.colors) + (inc?P.inh:0) + P.mot*0.4), pErr: P.err + (inc?0.035:0) + 0.006*(c.colors-4) }; }, {dm:dmOf(C,'stroop',d)}).score; },
// 화살표 집중 L9548
flank:(d,P,C)=>{ const c=C.FK[d]; return timed(60, ()=>{ const inc=rnd()<c.incong; return {
  rt: lognorm(P.rt0 + P.bit + (inc?P.inh*0.6:0) + P.mot*0.3), pErr: P.err*0.8 + (inc?0.03:0) }; }, {dm:dmOf(C,'flank',d)}).score; },
// 규칙 바꾸기 L8820: 전환 비율↑ = 전환비용
switch:(d,P,C)=>{ const c=C.SW[d]; return timed(60, ()=>{ const s=rnd()<c.switchP; return {
  rt: lognorm(P.rt0 + 260 + P.bit + (s?P.sw:0) + P.mot*0.3), pErr: P.err + (s?0.045:0) }; }, {dm:dmOf(C,'switch',d)}).score; },
// 도형 회전 L9025: 회전각이 클수록 느리고(셰퍼드) 틀린다
rotate:(d,P,C)=>{ const A=C.RT_ANG[d]; return timed(60, ()=>{ const a=pick(A), ang=Math.min(a,360-a); return {
  rt: lognorm(650 + P.rotMs*ang + P.mot*0.3), pErr: P.err + 0.11*ang/180 }; }, {dm:dmOf(C,'rotate',d)}).score; },
// 어림 계산 L9574: mx가 클수록 자릿수·곱셈 부담
guess:(d,P,C)=>{ const mx=C.GU[d].mx, f=Math.log10(mx)/Math.log10(30); return timed(60, ()=>{ const op=pick(['+','-','×']); const w={'+':650,'-':800,'×':1350}[op]; return {
  rt: lognorm(700 + P.calc*w*f + P.bit*Math.log2(3)), pErr: P.err + 0.02 + 0.03*(f-1) }; }, {dm:dmOf(C,'guess',d), after:140}).score; },
// 암산 L6125: 점수 = 정답 수(콤보·배수 없음), 직접 입력
math:(d,P,C)=>{ const k={easy:'b',normal:'a',hard:'e'}[d]; return timed(60, ()=>{ let w, dig;
  if(k==='b'){ w=1100; dig=1.5; } else if(k==='a'){ const op=pick(['+','-','×']); w={'+':2300,'-':2700,'×':3300}[op]; dig=2.6; } else { const op=pick(['+','-','×','÷']); w={'+':4200,'-':4800,'×':9500,'÷':5200}[op]; dig=3.3; }
  return { rt: lognorm(P.calc*w + 260*dig + 400, 0.3), pErr: P.err + (k==='e'?0.07:k==='a'?0.03:0.01), pts:()=>1 }; }, {dm:1, pen:0}).score; },
// 다른 색 찾기 L7749: 레벨마다 판↑(3레벨마다) 명도차↓. 명도차가 JND에 가까우면 탐색이 급격히 느려지고 오답↑
spot:(d,P,C)=>{ const c=C.SP[d]; return timed(60, (i,ok)=>{ const lv=ok+1, n=Math.min(c.maxN,c.startN+Math.floor((lv-1)/3)), del=Math.max(c.dMin,c.d0-(lv-1)*c.dStep); const r=del/P.jndL;
  return { rt: lognorm(380 + (n*n/2)*P.srch*(1+2.2*Math.exp(-(r-1)*1.3)) + P.mot*0.5), pErr: P.err*0.5 + 0.55*(1-Phi((r-1)*2.2)) }; }, {dm:dmOf(C,'spot',d)}).score; },
// 다른 모양 찾기 L7853: 회전각 차이
odd:(d,P,C)=>{ const c=C.OD[d]; return timed(60, (i,ok)=>{ const lv=ok+1, n=Math.min(c.maxN,c.startN+Math.floor((lv-1)/3)), del=Math.max(c.aMin,c.a0-(lv-1)*c.aStep); const r=del/P.jndA;
  return { rt: lognorm(420 + (n*n/2)*P.srch*1.15*(1+2.2*Math.exp(-(r-1)*1.3)) + P.mot*0.5), pErr: P.err*0.5 + 0.55*(1-Phi((r-1)*2.2)) }; }, {dm:dmOf(C,'odd',d)}).score; },
// 버블 톡톡 L7956: k개 합으로 목표 만들기, 3판마다 k+1, 숫자 크기↑
bubble:(d,P,C)=>{ const c=C.BB[d]; return timed(60, (i,ok)=>{ const lv=ok+1, k=Math.min(c.kMax,c.kMin+Math.floor((lv-1)/3)), vmax=Math.min(99,c.valMax+(lv-1)*2);
  return { rt: lognorm(900 + P.calc*(k*650 + c.n*110 + vmax*14) + k*P.mot, 0.3), pErr: P.err + 0.025*k }; }, {dm:dmOf(C,'bubble',d)}).score; },
// 엔백 L8920: 간격 고정 제시 → 반응시간이 아니라 적중률이 점수. n↑ = 적중률↓ 오경보↑
nback:(d,P,C)=>{ const n=C.NB.n[d], I=C.NB.int[d], dm=dmOf(C,'nback',d); const cap=P.span-1.2;  // 갱신형 작업기억 용량
  const hit=Math.min(.98, logistic((cap-n*1.9)*1.1+1.2)), fa=Math.min(.35, 0.015+ 0.05*Math.max(0,n-1)*(7.5-cap)/2.5);
  let t=0, lim=60000, score=0, combo=0, L=0; while(t<lim){ t+=I; if(L>=n){ const m=rnd()<0.3;
    if(m){ if(rnd()<hit){ combo++; score+=Math.round(comboPts(combo)*dm); } else combo=0; } else if(rnd()<fa){ combo=0; lim-=2000; } } L++; } return score; },
// 순서 잇기 L6869: 판 완료마다 n×dm, 다음 판 n+1. 한 번 누를 때 남은 노드 탐색
trail:(d,P,C)=>{ let n=C.TR_START[d], t=0, lim=60000, score=0; const dm=dmOf(C,'trail',d);
  while(true){ let k=0; for(k=0;k<n;k++){ t+=lognorm(P.mot + 90 + P.srch*0.55*(n-k)); if(rnd()<P.err*0.4){ lim-=2000; t+=lognorm(P.mot); } if(t>lim) return score; } score+=Math.round(n*dm); n++; } },
// 말로우 팡팡 L9330: 연속 스폰(gap마다, 동시 max), 창 win 안에 못 치면 놓침, 폭탄은 -3초
whack:(d,P,C)=>{ const c=C.WK[d], dm=dmOf(C,'whack',d); let t=0, lim=60000, score=0, combo=0, busy=0; const act=[]; let nextSpawn=600;
  const colors={easy:2,normal:4,hard:6}[d];
  while(t<lim){ t+=10;
    if(t>=nextSpawn){ if(act.length<c.max) act.push({at:t, end:t+c.win, bad:rnd()<c.badP}); nextSpawn=t+c.gap; }
    for(let i=act.length-1;i>=0;i--){ if(t>=act[i].end){ if(!act[i].bad) combo=0; act.splice(i,1); } }
    if(t>=busy){ const est=P.rt0 + P.mot*0.9 + 25*act.length; const cand=act.filter(a=>!a.bad && !a.tgt && a.end-t > est*0.85).sort((a,b)=>a.end-b.end)[0];
      const trap=act.find(a=>a.bad && !a.seen); if(trap){ trap.seen=true; if(rnd()< P.err*1.4 + 0.012*colors){ busy=t+lognorm(P.rt0+P.mot*0.8); lim-=3000; combo=0; const k=act.indexOf(trap); if(k>=0) act.splice(k,1); continue; } }
      if(cand){ const seen=Math.max(0, t-cand.at); const rt=lognorm(Math.max(P.mot*0.9, est - seen*0.6)); cand.tgt=true; cand.hitAt=t+rt; busy=t+rt; } }
    for(let i=act.length-1;i>=0;i--){ const a=act[i]; if(a.tgt && t>=a.hitAt){ if(a.hitAt<=a.end){ combo++; score+=Math.round(comboPts(combo)*dm); act.splice(i,1); } } }
  } return score; },
// 마시멜로 받기 L9673: 4레인, 낙하 시간 = 288px/spd, 한 번 탭에 한 칸. 계획 능력(plan)만큼 최적 목표 선택
catch:(d,P,C)=>{ const c=C.CA[d], dm=dmOf(C,'catch',d); const fall=288/c.spd*1000; let t=0, lim=60000, score=0, combo=0, lane=1, busy=0; const items=[]; let ns=0;
  while(t<lim){ t+=40; if(t>=ns){ items.push({lane:ri(0,3), land:t+fall, bad:rnd()<c.badP}); ns=t+c.spawn; }
    // 착지 판정을 먼저(같은 틱에 바구니가 먼저 움직이면 안 된다). 못 받은 착한 말로우는 콤보 리셋(L9692)
    for(let i=items.length-1;i>=0;i--){ const it=items[i]; if(t>=it.land){ if(it.lane===lane){ if(it.bad){ combo=0; lim-=3000; } else { combo++; score+=Math.round(comboPts(combo)*dm); } } else if(!it.bad) combo=0; items.splice(i,1); } }
    // 목표: 가장 먼저 떨어질 착한 아이템 중 제시간 도달 가능한 것. 나쁜 아이템이 곧 내 레인에 떨어지면 피한다
    if(t>=busy){ const soon=items.filter(i=>i.land>t).sort((a,b)=>a.land-b.land);
      const step=P.mot*0.7; const reach = i => i.lane===lane || Math.abs(i.lane-lane)*step + P.rt0*0.5 <= (i.land-t);
      let goal=soon.find(i=>!i.bad && reach(i));
      if(goal && rnd()>P.plan+0.25) goal=null;   // 판단 지연(가끔 늦게 본다)
      const danger=soon.find(i=>i.bad && i.lane===lane && i.land-t<700);
      let want = goal ? goal.lane : lane;
      if(danger && want===lane) want = lane===0?1:lane-1;
      if(danger && rnd()<P.err*2) want=lane;           // 판단 실수
      if(want!==lane){ lane+= want>lane?1:-1; busy=t+lognorm(step,0.2); } }
  } return score; },
// 반응 속도 L9226: go = max(20, 500-rt/2)×dm, no-go 참기 = 120×dm, 시행 수 고정
react:(d,P,C)=>{ const c=C.RC[d], dm=dmOf(C,'react',d); let s=0; for(let i=0;i<c.trials;i++){ if(rnd()<c.noGoP){ if(rnd()>P.err*2.2+0.03) s+=Math.round(120*dm); }
  else { const rt=lognorm(P.rt0+20, 0.18); if(rt<c.win) s+=Math.round(Math.max(20,500-rt*0.5)*dm); } } return s; },
// 카드 짝 L9116: 판 클리어 시 +20×dm, 다음 판 짝+1. 본 카드 기억 확률 mem
cards:(d,P,C)=>{ let pairs=C.CM.pairs[d]; const T=C.CM.time[d]*1000, dm=dmOf(C,'cards',d); let t=0, score=0, combo=0;
  while(true){ const deck=[]; for(let i=0;i<pairs;i++) deck.push(i,i); for(let i=deck.length-1;i>0;i--){ const j=Math.floor(rnd()*(i+1)); [deck[i],deck[j]]=[deck[j],deck[i]]; }
    const mem=new Map(), done=new Set(); const flip=()=>{ t+=lognorm(P.mot+260); };
    while(done.size<deck.length){ const open=[...deck.keys()].filter(i=>!done.has(i));
      let a=null,b=null; for(const [i,v] of mem){ if(done.has(i)) continue; for(const [j,w] of mem){ if(j!==i&&!done.has(j)&&w===v){ a=i;b=j; break; } } if(a!==null) break; }
      if(a===null){ const unseen=open.filter(i=>!mem.has(i)); a=pick(unseen.length?unseen:open); flip(); if(t>T) return score;
        const v=deck[a]; let m=null; for(const [j,w] of mem) if(j!==a&&!done.has(j)&&w===v){ m=j; break; }
        if(m!==null){ b=m; } else { const u2=open.filter(i=>i!==a&&!mem.has(i)); b=pick(u2.length?u2:open.filter(i=>i!==a)); } }
      else { flip(); if(t>T) return score; }
      flip(); if(t>T) return score;
      if(deck[a]===deck[b]){ done.add(a); done.add(b); combo++; score+=Math.round(comboPts(combo)*dm); }
      else { combo=0; t+=800; if(rnd()<P.mem) mem.set(a,deck[a]); if(rnd()<P.mem) mem.set(b,deck[b]); }
      for(const [i] of mem) if(rnd()<(1-P.mem)*0.08) mem.delete(i);   // 시간이 지나며 잊는다
    }
    score+=Math.round(20*dm); t+=550; pairs=Math.min(pairs+1,12); } },
// 인원수 세기 L6600: 목숨 3, 정답당 pts+(연속-1)×2 (배수 없음). 이벤트 수·간격·동시 인원↑ = 셈 실수↑
count:(d,P,C)=>{ const c=C.HC[d]; let lives=3, score=0, st=0; for(let r=0;r<200&&lives>0;r++){ const ev=ri(c.events[0],c.events[1]);
  const load = ev*0.55 + (c.kMax-1)*1.3 + (900-c.gap)/160; const p = 1 - Math.min(.9, P.cnt*0.55*load);
  if(rnd()<p){ st++; score += c.pts + (st-1)*2; } else { st=0; lives--; } } return score; },
// 순간기억 L6495: n개 순서 기억, 성공 +n×dm·n+1 / 실패 목숨-1·n-1(최소3). 위치+순서 기억폭 = 숫자폭-1.2, 노출이 짧을수록 -
flash:(d,P,C)=>{ let n=C.FM.start[d], lives=3, score=0; const dm=dmOf(C,'flash',d), sp=C.FM.speed[d];
  while(lives>0){ const reveal=Math.max(700,2200-n*120)*sp; const enc=Math.min(0, (reveal-(n*230))/400); const cap=P.span-1.2+enc;
    if(rnd()<logistic((cap-n)*1.6)*(1-P.err*0.3)){ score+=Math.round(dm*n); n=Math.min(n+1,25); } else { lives--; n=Math.max(n-1,3); } } return score; },
// 멜로디 L9460: 성공 len×10×dm, len+1 / 실패 목숨-1(같은 길이 재도전). 4패드 음·위치 순서 = 숫자폭-0.6
melody:(d,P,C)=>{ let L=C.ML[d].start, lives=3, score=0; const dm=dmOf(C,'melody',d), sp=C.ML[d].speed; const cap=P.span-0.6-(sp<450?0.3:0);
  while(lives>0){ if(rnd()<logistic((cap-L)*1.5)){ score+=Math.round(L*10*dm); L++; } else lives--; } return score; },
// 거꾸로 기억 L9610: 역순 숫자폭 ≈ 순방향-1.6
rev:(d,P,C)=>{ let L=C.RV[d].start, lives=3, score=0; const dm=dmOf(C,'rev',d), sp=C.RV[d].speed; const cap=P.span-1.6-(sp<700?0.3:0);
  while(lives>0){ if(rnd()<logistic((cap-L)*1.5)){ score+=Math.round(L*10*dm); L++; } else lives--; } return score; },
// 리듬 L9641: 패턴 길이 + 박자 간격이 짧을수록 타이밍 오차가 판정을 넘는다
rhythm:(d,P,C)=>{ let L=C.RH[d].start, lives=3, score=0; const dm=dmOf(C,'rhythm',d), base=C.RH[d].base; const cap=P.span-0.4 - (P.tsd/base)*6;
  while(lives>0){ if(rnd()<logistic((cap-L)*1.4)){ score+=Math.round(L*10*dm); L++; } else lives--; } return score; },
// 높은음 찾기 L10400: 청음 n개(1음 0.55초) → 선택. 음정차(센트)가 JND 근처면 찍기에 가깝다. 다음 문제 전 1.1초는 타이머 정지
pitch:(d,P,C)=>{ const c=C.PT.cfg[d], dm=dmOf(C,'pitch',d); let t=0, lim=C.PT.time[d]*1000, score=0, combo=0, lv=1;
  while(true){ const n=Math.min(c.nMax,c.nStart+Math.floor((lv-1)/3)), cents=Math.max(c.cMin,c.c0-(lv-1)*c.cStep); t+=n*550+lognorm(700+P.mot);
    if(t>lim) return score; const pd=Math.min(.99, Phi((cents-P.jndC)/(0.6*P.jndC)+0.5)); let left=n, first=true;
    while(true){ const ok = rnd() < (first ? pd + (1-pd)/left : 1/left); if(ok){ combo++; score+=Math.round(comboPts(combo)*dm); lv++; break; }
      combo=0; lim-=2000; left--; first=false; t+=lognorm(P.mot+300); if(t>lim) return score; } } },
// 틀린 그림 L10335: 시작시간 30/40/50초, 판 클리어 시 최대 +8/10/12초(시작시간 한도), 3레벨마다 판↑
diff:(d,P,C)=>{ const c=C.DF.cfg[d], T0=C.DF.time[d]*1000, B=C.DF.bonus[d]*1000, dm=dmOf(C,'diff',d); let left=T0, score=0, combo=0, lv=1, el=0;
  while(left>0 && lv<400){ const n=Math.min(c.nMax,c.nStart+Math.floor((lv-1)/3)), k=Math.max(1,Math.min(Math.floor(n*n/4),1+Math.floor((lv-1)/2)));
    for(let j=0;j<k;j++){ const rt=lognorm(300 + (n*n/(k-j+1))*P.srch*5.5 + P.mot*0.6, 0.35); left-=rt; if(left<=0) return score;
      if(rnd()<P.err*0.7){ combo=0; left-=2000; } combo++; score+=Math.round(comboPts(combo)*dm); }
    lv++; left=Math.min(T0, left+B); left-=350; } return score; },
// 글자 맞추기 L10185: (길이×5 + 속도보너스(10-초) + 콤보보너스)×배율, 오답 시 -0/1/2초
anagram:(d,P,C)=>{ const Ls=C.AG.len[d], mult=C.AG.mult[d], pen=C.AG.pen[d]; let t=0, lim=60000, score=0, combo=0;
  while(true){ const L=pick(Ls); const solve=lognorm(P.lex*(500*Math.pow(L,1.75)) + L*P.mot, 0.45); t+=solve; if(t>lim) return score;
    if(rnd()< P.err + 0.025*L){ combo=0; lim-=pen*1000; t+=lognorm(P.lex*400*L); if(t>lim) return score; }
    combo++; const sp=Math.max(0,10-Math.floor(solve/1000)); score+=Math.round((L*5+sp+comboBonus(combo))*mult); } },
// 숨은 단어 L10244: 단어당 (길이×4+콤보보너스)×dm, 판 완료 +20×dm. 판이 클수록·대각선이면 탐색 시간↑
wordsearch:(d,P,C)=>{ const c=C.WS.cfg[d], dm=dmOf(C,'wordsearch',d); let t=0, lim=C.WS.time[d]*1000, score=0, combo=0;
  while(true){ for(let j=0;j<c.k;j++){ const L=ri(3,c.maxLen); t+=lognorm(900 + (c.n*c.n/(c.k-j+0.6))*P.srch*3.2*(c.diag?1.45:1) + 700, 0.4); if(t>lim) return score;
      combo++; score+=Math.round((L*4+comboBonus(combo))*dm); } score+=Math.round(20*dm); t+=400; } },
// 길 따라가기 L10442: 목숨 3, 클리어 (30+레벨×10)×dm. 길 폭·판정 여유가 레벨마다 좁아지고 길이는 늘어난다 → 이탈 확률
trace:(d,P,C)=>{ const c=C.TC[d], dm=dmOf(C,'trace',d); let lives=3, lv=1, score=0;
  while(lives>0 && lv<200){ const stage=Math.max(1, lv-((lv%4===0)?2:0)); const steps=Math.min(c.steps+(stage-1)*2,44); const w=Math.max(11,c.w-(stage-1)*1.6);
    const tol=w/2+Math.max(4,12-(stage-1)*0.5)*0.8; const pSeg=2*(1-Phi(tol/P.steer)); const pStray=1-Math.pow(1-pSeg*0.35, steps*2.2);
    if(rnd()>pStray){ lv++; score+=Math.round(dm*(30+lv*10)); } else lives--; } return score; },
// 말로우 타워 L7391: 0.1초마다 게이지 -(decay + 점수×accel)×0.1, 깨물 때 +gain. 점수는 dm이 곱해진 값 → 어려움은 가속까지 2배
chop:(d,P,C)=>{ const c=C.CP[d], dm=dmOf(C,'chop',d); let g=100, t=0, score=0, chops=0; let next=lognorm(P.chop);
  while(t<600000){ t+=100; g-=(c.decay+score*c.accel)*0.1; if(g<=0) return score;
    while(next<=100 && g>0){ const pErr = P.err*0.45 + 0.004*(c.forkP-0.5)*10; if(rnd()<pErr) return score; score+=Math.round(10*dm); chops++; g=Math.min(100,g+c.gain); next+=lognorm(P.chop*(1+c.forkP*0.25), 0.2); }
    next-=100; } return score; },
// 블록 채우기 L10000: 난이도 선택 없음(레벨로 상승). 초당 4.5+0.9(레벨-1) 감소, 줄 삭제 +13/줄. 배치 판단 시간과 줄 만들기 효율(plan)
fit:(d,P,C)=>{ let time=100, lv=1, lines=0, next=8, score=0, combo=0, t=0;
  while(t<900000){ const think=lognorm(1500/(0.6+P.plan*0.6)*(1+lv*0.03), 0.35); t+=think; time-=(4.5+(lv-1)*0.9)*think/1000; if(time<=0) return score;
    score+=4; const pL = 0.28+P.plan*0.22 - lv*0.004; if(rnd()<pL){ const L= rnd()<0.18*P.plan?2:1; combo++; score+=Math.round(L*8*4*(1+(combo-1)*0.5)*(1+(lv-1)*0.12)); time=Math.min(100,time+13*L+combo*2); lines+=L;
      while(lines>=next){ lv++; next+=8; time=Math.min(100,time+12); } } else combo=0;
    if(rnd()< 0.004 + (1-P.plan)*0.012 + lv*0.0008) return score; } return score; },
// 컬러 소트 L7231: max(10, base - 초×2 - 이동×3)
sort:(d,P,C)=>{ const k=C.SO[d].k; const ideal=k*3.2; const moves=Math.round(ideal*(1+ (1-P.plan)*1.1)*lognorm(1,0.15)); const sec=moves*lognorm(1.8*P.calc*(1+k*0.06),0.25)+k*4*P.calc;
  return Math.max(10, Math.round(C.SO[d].base - sec*2 - moves*3)); },
// 슬라이딩 퍼즐 L7645: max(10, base - 초×3 - 이동)
slide:(d,P,C)=>{ const n=C.SL[d].n; const moves={3:48,4:190,5:520}[n]*(1+(1-P.plan)*1.3)*lognorm(1,0.2); const sec=moves*lognorm(0.75*P.calc,0.2)+n*n*2;
  return Math.max(10, Math.round(C.SL[d].base - sec*3 - moves)); },
// 노노그램 L10136: max(50, base - 초×rate)
nono:(d,P,C)=>{ const n=C.NO[d].n; const sec=lognorm(Math.pow(n,2.2)*1.35*P.calc*(1.4-P.plan*0.5), 0.3); return Math.max(50, Math.round(C.NO[d].base - sec*C.NO[d].rate)); },
// 스도쿠 L6121: max(30, base - 실수×4 - 힌트×6 - 초/20)
sudoku:(d,P,C)=>{ const sec=lognorm({easy:420,normal:900,hard:1800}[d]*P.calc*(1.5-P.plan*0.6),0.35); const mis=Math.round((1-P.plan)*4*rnd()*{easy:1,normal:1.5,hard:2}[d]); const hint=d==='hard'?Math.round((1-P.plan)*3*rnd()):0;
  return Math.max(30, Math.round(C.SK.base[d] - mis*4 - hint*6 - sec/20)); },
// IQ 테스트 L5629: 55~145
iq:(d,P,C)=>{ const w=Math.min(1,Math.max(0, 0.45 + P.plan*0.45 - (P.calc-1)*0.12 + (rnd()-0.5)*0.12)); const sp=Math.max(0,Math.min(1, 0.15+P.plan*0.3 + (rnd()-0.5)*0.1));
  return Math.round(Math.max(55,Math.min(145, 55+Math.pow(w,1.3)*75+sp*15))); },
// 말랑 2048 L7502: 400판 시뮬(merge_sim) 중앙값 easy 20916/normal 2880/hard 272 → 배수 1/7/70로 보정됨. 사람 실력은 판의 몇 %까지 가는지로
merge:(d,P,C)=>{ const med={easy:20916,normal:2880,hard:272}[d]; const f=Math.pow(0.35+P.plan*0.75, 2.2)*lognorm(1,0.45); return Math.round(med*f*dmOf(C,'merge',d)); },
// 말로우 런: 물리는 코드와 동일(프레임 단위). 사람은 '점프 시점 오차 ~ N(0, tsd)' — 창 밖이면 충돌
run:(d,P,C)=>runSim(d,P,C.RN[d],dmOf(C,'run',d),{W:338}),        // 390px 폰의 캔버스 폭
run_pc:(d,P,C)=>runSim(d,P,C.RN[d],dmOf(C,'run',d),{W:786}),     // PC·태블릿 캔버스 폭(같은 코드)
};

/* ---- 말로우 런 (L9714~9950 물리 그대로) ---- */
const RN_G=0.9, RN_JV=15, RN_PW=40, RN_OBW=26, RN_OBH=46, RN_AIR=2*RN_JV/RN_G;
function runSim(d,P,cfg,dm,{W=338,capFrames=60*600}={}){
  const px=Math.round(W*0.16); let spd=cfg.spd0, dist=0, py=0, vy=0, gr=true, burst=0; const obs=[{x:W+40}];
  const safe=s=>s*RN_AIR+RN_OBW+24;
  const nextGap=()=>{ const base=safe(spd); if(burst>0){ burst--; return base*(1.03+rnd()*0.12); } if(cfg.clusterMax>0&&rnd()<cfg.clusterP){ burst=cfg.clusterMax; return base*(1.03+rnd()*0.12); } return base*1.15+rnd()*cfg.gapRand; };
  let gap=nextGap(), plan=null;
  for(let f=0; f<capFrames; f++){
    spd=Math.min(cfg.cap, spd+cfg.acc);
    // 사람: 다음 장애물의 '이상적 점프 시점'(창 한가운데)을 보고, 오차를 더해 누른다
    if(gr && !plan){ const o=obs.find(o=>o.x+RN_OBW>px); if(o){ const s=(o.x-px-RN_PW)/spd, e=(o.x+RN_OBW-px)/spd, ideal=(s+e-35)/2;   // 겹침 [s,e]가 체공 4~31프레임 안에 들어가는 창의 한가운데
        plan={ o, at: f + ideal + gauss()*P.tsd/16.67 }; } }
    if(plan && gr && f>=plan.at){ vy=RN_JV; gr=false; plan=null; }
    if(!gr){ py+=vy; vy-=RN_G; if(py<=0){ py=0; vy=0; gr=true; } }
    for(const o of obs) o.x-=spd; while(obs.length && obs[0].x<-RN_OBW-6) obs.shift();
    if(plan && !obs.includes(plan.o)) plan=null;
    const last=obs[obs.length-1]; if(!last || (W-last.x)>=gap){ obs.push({x:W}); gap=nextGap(); }
    dist+=spd;
    for(const o of obs){ if(o.x+RN_OBW<px) continue; if(o.x>px+RN_PW) break; if(py<RN_OBH) return Math.floor(dist*dm/12); }
  }
  return Math.floor(dist*dm/12);
}

export function medalTargets(C,id){ const f=C.MEDAL_FIXED[id]; if(f) return f; const r=C.REF[id]||100; return C.MEDAL_RATIO.map(x=>Math.max(1,Math.round(r*x))); }
export function pct(a,p){ const s=[...a].sort((x,y)=>x-y); return s[Math.min(s.length-1,Math.floor(p*s.length))]; }
