/* 현재(또는 제안) 설정으로 전 게임 시뮬 → 표 + JSON
   node .logs/bal/run.mjs [cur|prop] [N]   */
import fs from 'fs';
import { TIERS, TIER_KEYS, DIFFS, GAMES, CUR, seed, medalTargets, pct } from './model.mjs';
const mode = process.argv[2] || 'cur';
const N = +(process.argv[3] || 300);
let C = CUR, G = GAMES;
if (mode === 'prop') { const m = await import('./proposal.mjs'); C = m.PROP; G = Object.assign({}, GAMES, m.GAMES_OVERRIDE || {}); }
const only = process.argv[4] ? process.argv[4].split(',') : Object.keys(G);
const NODIFF = new Set(['fit']);   // 난이도 선택 없는 게임
const out = {};
for (const id of only) {
  out[id] = {};
  for (const tk of TIER_KEYS) {
    out[id][tk] = {};
    for (const d of (NODIFF.has(id) ? ['normal'] : DIFFS)) {
      seed(1000 + id.length * 97 + tk.length * 13 + d.length);
      const a = []; for (let i = 0; i < (id === 'run' ? Math.min(N, 200) : N); i++) a.push(G[id](d, TIERS[tk], C));
      out[id][tk][d] = { p10: pct(a, .1), p50: pct(a, .5), p90: pct(a, .9), max: pct(a, .999) };
    }
  }
  const med = medalTargets(C, id === 'run_pc' ? 'run' : id);
  const best = tk => Math.max(...Object.values(out[id][tk]).map(v => v.p50));
  const medalOf = s => med.reduce((m, x, i) => s >= x ? i + 1 : m, 0);
  const icons = ['·', '🥉', '🥈', '🥇', '💎'];
  const row = TIER_KEYS.map(tk => icons[medalOf(best(tk))]).join(' ');
  const r = (tk, d) => out[id][tk][d] ? out[id][tk][d].p50 : NaN;
  const he = (r('casual', 'hard') / r('casual', 'easy'));
  const cap = Math.max(...TIER_KEYS.flatMap(tk => Object.values(out[id][tk]).map(v => v.max)));
  out[id]._meta = { medals: med, medalsByTier: row, hardOverEasy: +he.toFixed(2), attainMax: cap };
  const f = n => String(Math.round(n)).padStart(7);
  console.log(id.padEnd(11), 'casual E/N/H', f(r('casual', 'easy')), f(r('casual', 'normal')), f(r('casual', 'hard')), ' H/E', String(isNaN(he) ? '-' : he.toFixed(2)).padStart(5),
    ' expert best', f(best('expert')), ' 💎', f(med[3]), ' 최대치', f(cap), '  메달(초보→상위1%)', row);
}
fs.writeFileSync(new URL(`./result_${mode}.json`, import.meta.url), JSON.stringify(out, null, 1));
