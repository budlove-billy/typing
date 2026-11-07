// Playgama 설정 점검 — 게임 주소가 살아 있는지, 수익 추적용 clid가 붙었는지 본다. 오픈 전·주 1회 실행.
// node tools/playgama/check.mjs
import { readFileSync } from 'node:fs';
const src = readFileSync(new URL('../../assets/playgama-config.js', import.meta.url), 'utf8');
const a = src.indexOf('= /*CONFIG*/') + 12;
const cfg = JSON.parse(src.slice(a, src.indexOf('/*END*/', a)));
let bad = 0;
console.log(`enabled=${cfg.enabled} clid=${cfg.clid ? '(설정됨)' : '(비어 있음 — 허브·홈 카드 안 보임)'}`);
for (const g of cfg.games) {
  if (g.enabled === false) { console.log(`- ${g.id}: 꺼짐`); continue; }
  let status = 'ERR';
  try { status = (await fetch(g.url, { redirect: 'follow' })).status; } catch (e) { status = e.cause?.code || 'ERR'; }
  let thumb = 'ERR';
  try { thumb = (await fetch(g.thumb, { method: 'HEAD' })).status; } catch {}
  const clid = /[?&]clid=/.test(g.url) ? 'clid ok' : '⚠ clid 없음(대시보드 iframe 주소로 교체 필요)';
  if (status !== 200 || thumb !== 200) bad++;
  console.log(`- ${g.id}: 게임 ${status} · 썸네일 ${thumb} · ${clid}`);
}
process.exit(bad ? 1 : 0);
