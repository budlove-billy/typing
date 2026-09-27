/* 제안값 보정: ① 난이도 배수 — 같은 사람(casual·good 평균) 점수비가 쉬움0.8:보통1:어려움1.25가 되게
   ② 풀이형 K — 보통 casual 중앙값이 현재 보통 점수 규모와 비슷하게  ③ 메달 — 🥉novice 🥈good 🥇skilled 💎expert 의 '최고 난이도' 중앙값
   보통 난이도의 점수 규모는 현재값에 맞춘다(기존 기록과 대략 비교 가능하게). 결과 → calib.json */
import fs from 'fs';
import { TIERS, GAMES, CUR, seed, pct } from './model.mjs';
const N=+(process.argv[2]||200);
const R={easy:0.8, normal:1, hard:1.25};
const calibPath=new URL('./calib.json', import.meta.url);
if(fs.existsSync(calibPath)) fs.unlinkSync(calibPath);
const { PROP, GAMES_OVERRIDE } = await import('./proposal.mjs?'+Date.now());
const G=Object.assign({}, GAMES, GAMES_OVERRIDE);
const ids=Object.keys(G).filter(id=>id!=='iq' && id!=='run_pc');
const NODIFF=new Set(['fit']);
const med=(id,d,tk,C,n=N)=>{ seed(500+id.length*31+tk.length*7+d.length); const a=[]; for(let i=0;i<(id==='run'?Math.min(n,120):n);i++) a.push(G[id](d,TIERS[tk],C)); return a; };
const C=JSON.parse(JSON.stringify(PROP)); C.K=C.K||{}; C.DMULT_GAME={};
const curNormal={}; for(const id of ids){ const cd=(CUR.DMULT_GAME[id]&&CUR.DMULT_GAME[id].normal)||CUR.DMULT.normal; curNormal[id]= (id==='math'||id==='count')?1:cd; }
// 풀이형 K: 보통 casual 중앙값을 현재 보통 casual 중앙값 규모에 맞춘다
const PARG=['sort','slide','nono','sudoku'];
for(const id of PARG){ C.K[id]={easy:1000,normal:1000,hard:1000}; }
const dm={}, out={};
for(const id of ids){
  const diffs=NODIFF.has(id)?['normal']:['easy','normal','hard'];
  C.DMULT_GAME[id]={easy:1,normal:1,hard:1};
  const raw={}; for(const d of diffs){ const a=med(id,d,'casual',C), b=med(id,d,'good',C); raw[d]=(pct(a,.5)+pct(b,.5))/2; }
  if(PARG.includes(id)){ // K로 흡수(배수는 1): 기준시간 점수 → 보통 1000 규모 대신 현재 보통 casual 규모
    const target={sort:700,slide:600,nono:600,sudoku:60}[id];
    for(const d of diffs) C.K[id][d]=Math.round(1000*target*R[d]/raw[d]); dm[id]={easy:1,normal:1,hard:1};
  } else {
    const base=raw.normal*curNormal[id]; dm[id]={}; for(const d of diffs) dm[id][d]=+(R[d]*base/raw[d]).toFixed(3);
    if(NODIFF.has(id)) dm[id]={easy:1,normal:1,hard:1};
  }
  C.DMULT_GAME[id]=dm[id];
  // 메달: 🥉 초보의 '보통' 중앙값 / 🥈 max(good 중앙값, casual P75) / 🥇 max(skilled 중앙값, good P75) / 💎 max(expert 중앙값, skilled P90)
  //  → 각 메달은 한 단계 아래 사람이 '아주 잘한 판'으로도 잘 안 닿는다. 모든 비교는 그 사람의 가장 유리한 난이도 기준
  const nice=v=>{ const p=Math.pow(10,Math.max(0,Math.floor(Math.log10(Math.max(1,v)))-1)); return Math.max(1,Math.round(v/p)*p); };
  const up=v=>{ const p=Math.pow(10,Math.max(0,Math.floor(Math.log10(Math.max(1,v)))-1)); return Math.max(1,Math.ceil((v+0.5)/p)*p); };
  const down=v=>{ const p=Math.pow(10,Math.max(0,Math.floor(Math.log10(Math.max(1,v)))-1)); return Math.max(1,Math.floor(v/p)*p); };
  const dist={}; for(const tk of ['novice','casual','good','skilled','expert']){ let bestMed=-1; for(const d of diffs){ const a=med(id,d,tk,C); const m=pct(a,.5); if(m>bestMed){ bestMed=m; dist[tk]={a,d}; } } dist[tk].nov_n = tk==='novice' ? pct(med(id,NODIFF.has(id)?'normal':'normal',tk,C),.5) : 0; }
  const P_=(tk,p)=>pct(dist[tk].a,p);
  let m=[ down(dist.novice.nov_n), nice(Math.max(P_('good',.5),P_('casual',.75))), up(Math.max(P_('skilled',.5),P_('good',.75))), up(Math.max(P_('expert',.5),P_('skilled',.9))) ];
  for(let i=1;i<4;i++) if(m[i]<=m[i-1]) m[i]=nice(m[i-1]*1.12);
  const t=['novice','good','skilled','expert'].map(tk=>({at:dist[tk].d}));
  const share=(tk,th)=>dist[tk].a.filter(v=>v>=th).length/dist[tk].a.length;
  const chk={ casualGold:+share('casual',m[2]).toFixed(2), skilledDia:+share('skilled',m[3]).toFixed(2), expertDia:+share('expert',m[3]).toFixed(2), noviceBronze:+(()=>{ const a=med(id,'normal','novice',C); return a.filter(v=>v>=m[0]).length/a.length; })().toFixed(2) };
  out[id]={medals:m, bestAt:t.map(x=>x.at), raw, chk};
  console.log(id.padEnd(11),'dm',JSON.stringify(dm[id]).padEnd(40),'medals',m.join('/').padEnd(26),'best',t.map(x=>x.at[0]).join(''),'  P(초보≥🥉)',chk.noviceBronze,'P(평균≥🥇)',chk.casualGold,'P(상위10%≥💎)',chk.skilledDia,'P(상위1%≥💎)',chk.expertDia);
}
const medals={}; for(const id of ids) medals[id]=out[id].medals;
fs.writeFileSync(calibPath, JSON.stringify({dm, medals, K:C.K, detail:out}, null, 1));
console.log('→ calib.json');
