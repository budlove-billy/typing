/* PUZZLES 데이터 무결성 검사: 그룹 4개×4낱말, 퍼즐 내 중복 금지 */
const fs = require('fs');
const html = fs.readFileSync('D:/claude/result/puzzle-connections/index.html', 'utf8');
const m = html.match(/const PUZZLES = (\[[\s\S]*?\n\]);/);
if (!m) { console.error('PUZZLES 블록 추출 실패'); process.exit(1); }
const PUZZLES = eval(m[1]);

let ok = true;
PUZZLES.forEach((p, i) => {
  const errs = [];
  if (p.groups.length !== 4) errs.push(`그룹 수 ${p.groups.length}`);
  const words = p.groups.flatMap(g => g.words);
  if (words.length !== 16) errs.push(`낱말 수 ${words.length}`);
  const dup = words.filter((w, j) => words.indexOf(w) !== j);
  if (dup.length) errs.push(`중복: ${[...new Set(dup)].join(',')}`);
  const diffs = p.groups.map(g => g.diff).sort().join('');
  if (diffs !== '0123') errs.push(`난이도 ${diffs}`);
  p.groups.forEach(g => { if (g.words.length !== 4) errs.push(`"${g.name}" ${g.words.length}개`); });
  if (errs.length) { ok = false; console.log(`❌ #${i + 1}: ${errs.join(' | ')}`); }
});
console.log(ok ? `✅ ${PUZZLES.length}개 퍼즐 전부 무결` : '무결성 실패');
process.exit(ok ? 0 : 1);
