import { TIERS, seed, pct } from './model.mjs';
import { PROP, runV2 } from './proposal.mjs';
const N=+(process.argv[2]||120);
for(const d of ['easy','normal','hard']){ const row=[]; for(const tk of Object.keys(TIERS)){ seed(77+tk.length); const a=[]; for(let i=0;i<N;i++) a.push(runV2(TIERS[tk],PROP.RN2[d],1,{trace:true}).sec); row.push(tk+' '+Math.round(pct(a,.5))+'s(p90 '+Math.round(pct(a,.9))+')'); } console.log(d.padEnd(7),row.join(' | ')); }
