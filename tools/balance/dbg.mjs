import { TIERS, GAMES, CUR, seed } from './model.mjs';
const [id, d, tk, n] = process.argv.slice(2);
seed(7); const a=[]; for(let i=0;i<(+n||20);i++) a.push(GAMES[id](d, TIERS[tk||'casual'], CUR)); a.sort((x,y)=>x-y); console.log(id,d,tk, 'p10',a[Math.floor(a.length*.1)],'p50',a[Math.floor(a.length/2)],'p90',a[Math.floor(a.length*.9)]);
