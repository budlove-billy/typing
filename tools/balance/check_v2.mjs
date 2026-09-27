/* 밸런스 v2 통합 검증 — 실제 index.html 코드로 바뀐 규칙을 전부 확인한다.
   ① 기록 초기화 마이그레이션(1회만) ② 말로우 런 v2: 실제 rnLoop를 가상 시계로 돌려 사람 모델 봇으로 생존 시간 측정(시뮬 예측과 비교),
   폰·PC 판정 동일, 스폰 간격 ≥ 안전간격, 키 큰 장애물 ③ 어려움 문항 제한시간 5종 ④ 게임별 규칙(타워·인원수·반응·받기·암산·풀이형·틀린그림)
   ⑤ 메달·배수 표 */
import pw from 'file:///c:/Users/budlo/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const b = await pw.chromium.launch();
const BASE = 'http://127.0.0.1:8226/index.html';
const out = {}; const fail = [];
const ok = (c, m) => { if (!c) fail.push(m); };

// ① 마이그레이션
{ const ctx = await b.newContext({ serviceWorkers: 'block' });
  await ctx.addInitScript(() => { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1');
    localStorage.setItem('brain.run.best', JSON.stringify({ easy:{all:99999,day:0,date:''}, normal:{all:0,day:0,date:''}, hard:{all:0,day:0,date:''} }));
    localStorage.setItem('brain.math.flat', '44'); localStorage.setItem('brain.bot.run', '{"normal":{"lv":3,"target":9000}}');
    localStorage.setItem('brain.recent', '[1]'); localStorage.setItem('brain.week', '{"keep":1}'); localStorage.setItem('brain.lang', 'ko'); } });
  const p = await ctx.newPage(); await p.goto(BASE, { waitUntil: 'domcontentloaded' }); await p.waitForTimeout(800);
  const m1 = await p.evaluate(() => ({ run: localStorage.getItem('brain.run.best'), flat: localStorage.getItem('brain.math.flat'), bot: localStorage.getItem('brain.bot.run'),
    recent: localStorage.getItem('brain.recent'), week: localStorage.getItem('brain.week'), lang: localStorage.getItem('brain.lang'), flag: localStorage.getItem('brain.balanceV2'), RNbest: RN.best.easy.all }));
  await p.evaluate(() => localStorage.setItem('brain.math.flat', '500')); await p.reload({ waitUntil: 'domcontentloaded' }); await p.waitForTimeout(600);
  const m2 = await p.evaluate(() => localStorage.getItem('brain.math.flat'));
  out.migration = { m1, secondLoadKeeps: m2 };
  ok(!m1.flat && !m1.bot && !m1.recent && m1.RNbest === 0 && m1.week && m1.lang === 'ko' && m1.flag === '1', 'migration first load');
  ok(m2 === '500', 'migration runs only once');
  await ctx.close(); }

async function page(w) { const ctx = await b.newContext({ viewport: { width: w, height: 900 }, serviceWorkers: 'block' }); const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 160)));
  await p.goto(BASE + '?lang=ko', { waitUntil: 'domcontentloaded' }); await p.waitForTimeout(900);
  await p.evaluate(() => { window.sfx = () => {}; window._tone = () => {}; window._beep = () => {}; });
  return { ctx, p, errs }; }

// ② 말로우 런 v2
const RUN_BOT = ({ diff, tsd, rt0, N, seed }) => {
  let s = seed >>> 0; const rnd = () => { s = (s + 0x6D2B79F5) >>> 0; let q = s; q = Math.imul(q ^ q >>> 15, q | 1); q ^= q + Math.imul(q ^ q >>> 7, q | 61); return ((q ^ q >>> 14) >>> 0) / 4294967296; };
  const gauss = () => { let u = 0, v = 0; while (!u) u = rnd(); while (!v) v = rnd(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
  const above = h => { let py = 0, vy = RN_JV, k = 0, a = []; while (true) { k++; py += vy; vy -= RN_G; if (py <= 0) break; if (py >= h) a.push(k); } return [a[0], a[a.length - 1]]; };
  const AB = { 46: above(46), 64: above(64) };
  window.requestAnimationFrame = () => 0; window.rnDraw = () => {};
  const res = [], gaps = []; let tall = 0, total = 0;
  for (let r = 0; r < N; r++) {
    setRunDiff(diff); startRun(); let now = 1000, plan = null; const seen = new Map(); let lastLen = 0, lastX = null;
    for (let f = 0; f < 60 * 900; f++) {
      RN.obs.forEach((o, i) => { if (!seen.has(o)) { seen.set(o, now); total++; if (o.h > RN_OBH) tall++; if (i > 0) gaps.push(o.x - RN.obs[i - 1].x); } });   // 같은 프레임의 두 위치로 간격을 잰다
      if (RN.grounded && !plan) { const o = RN.obs.find(o => o.x + RN_OBW > RN.px); if (o) { const [a0, a1] = AB[o.h]; const st = (o.x - RN.px - RN_PW) / RN_BASE, en = (o.x + RN_OBW - RN.px) / RN_BASE;
        let at = now + ((st + en - (a0 + a1)) / 2) / RN.ts * 16.667 + gauss() * tsd; const see = seen.get(o) + rt0 * 0.85; if (at < see) at = see + Math.abs(gauss()) * 25; plan = { o, at }; } }
      if (plan && !RN.obs.includes(plan.o)) plan = null;
      if (plan && RN.grounded && now >= plan.at) { rnJump(); plan = null; }
      now += 16.667; rnLoop(now); if (!RN.running) break;
      // 다음 프레임 전에 새로 생긴 장애물의 x(=간격 측정용)는 위 루프에서 잡는다
    }
    res.push({ t: +RN.t.toFixed(1), score: RN.score, ts: +RN.ts.toFixed(2) });
    clearTimeout(RN.overT); RN.over = false;
  }
  return { res, minGap: Math.min(...gaps), safe: RN_SAFE, tallShare: +(tall / Math.max(1, total)).toFixed(2), W: RN.W, H: RN.H, cssH: document.getElementById('rn-canvas').style.height };
};
const med = a => { const x = [...a].sort((p, q) => p - q); return x[Math.floor(x.length / 2)]; };
out.run = {};
for (const w of [390, 900]) {
  const { ctx, p, errs } = await page(w);
  await p.evaluate(() => showScreen('run'));
  for (const [tier, tsd, rt0] of [['casual', 48, 320], ['expert', 22, 242]]) for (const diff of ['easy', 'normal', 'hard']) {
    const r = await p.evaluate(RUN_BOT, { diff, tsd, rt0, N: tier === 'expert' ? 12 : 24, seed: 7 + w + diff.length });
    const k = `${w}/${tier}/${diff}`; out.run[k] = { medT: med(r.res.map(x => x.t)), medScore: med(r.res.map(x => x.score)), minGap: Math.round(r.minGap), safe: Math.round(r.safe), tall: r.tallShare, world: r.W + 'x' + r.H, cssH: r.cssH };
    ok(r.minGap >= r.safe * 1.03 - 1, `${k}: gap ${r.minGap} < safe ${r.safe}`);
    ok(Math.max(...r.res.map(x => x.t)) < 900, `${k}: run never ended`);
  }
  ok(!errs.length, `run ${w} errors ${errs[0]}`); await ctx.close();
}

// ③ 어려움 문항 제한시간 + ④ 규칙
{ const { ctx, p, errs } = await page(390);
  out.deadline = await p.evaluate(async () => {
    const r = {};
    const wait = ms => new Promise(x => setTimeout(x, ms));
    const cases = [['stroop', () => { setStroopDiff('hard'); startStroop(); }, () => ST, 'qdl-stroop', 1500],
                   ['flank', () => { setFlankDiff('hard'); startFlank(); }, () => FK, 'qdl-flank', 900],
                   ['switch', () => { setSwitchDiff('hard'); startSwitch(); }, () => SW, 'qdl-switch', 1500],
                   ['rotate', () => { setRotateDiff('hard'); startRotate(); }, () => RT, 'qdl-rotate', 2200],
                   ['guess', () => { setGuessDiff('hard'); startGuess(); }, () => GU, 'qdl-guess', 3200]];
    for (const [id, start, S, bar, ms] of cases) { showScreen(id); start(); await wait(ms * 0.5); const barOn = document.getElementById(bar).style.display === 'block';
      S().combo = 5; const t0 = S().timeLeft; await wait(ms * 0.6 + 150); r[id] = { barOn, comboAfter: S().combo, timeKept: S().timeLeft >= t0 - 2 }; haltRunningGames(); }
    showScreen('stroop'); setStroopDiff('normal'); startStroop(); await wait(300); r.normalNoBar = document.getElementById('qdl-stroop').style.display === 'none'; haltRunningGames();
    return r; });
  for (const [id, v] of Object.entries(out.deadline)) if (typeof v === 'object') ok(v.barOn && v.comboAfter === 0 && v.timeKept, `deadline ${id} ${JSON.stringify(v)}`);
  ok(out.deadline.normalNoBar, 'deadline bar hidden on normal');

  out.rules = await p.evaluate(async () => {
    const r = {}; const wait = ms => new Promise(x => setTimeout(x, ms));
    // 타워: 깨문 횟수 기준 가속
    showScreen('chop'); setChopDiff('hard'); startChop(); CP.segs = Array(12).fill('N'); for (let i = 0; i < 5; i++) { CP.segs[0] = 'N'; CP.segs[1] = 'N'; cpChop(CP.side === 'L' ? 'R' : 'L'); }
    r.chop = { chops: CP.chops, score: CP.score, perChop: CP.score / Math.max(1, CP.chops) }; haltRunningGames();
    // 인원수: 4번 맞히면 이벤트 +1, 연속 보너스 상한
    showScreen('count'); setCountDiff('easy'); startCount(); await wait(50); hcClearTimers(); HC.ok = 8; const seq = hcBuildSequence(); r.count = { eventsAt8: seq.seq.length };
    HC.ok = 0; HC.streak = 30; HC.answer = 1; const btn = document.createElement('button'); document.body.appendChild(btn); const before = HC.score; hcAnswer(1, btn); r.count.gainAtStreak31 = HC.score - before; hcClearTimers(); haltRunningGames();
    // 반응
    showScreen('react'); setReactDiff('normal'); startReact(); clearTimeout(RC.waitT); RC.state = 'go'; RC.goAt = _rcNow() - 250; const s0 = RC.score; rcTap(); r.react = { at250ms: RC.score - s0 }; haltRunningGames();
    // 받기: 생성이 이어지는지, 속도 램프
    showScreen('catch'); setCatchDiff('normal'); startCatch(); await wait(2600); r.catch = { items: CA.items.length + '', ticks: CA.ticks }; haltRunningGames();
    // 암산: 콤보 점수
    showScreen('math'); setMathDiff('advanced'); startMathGame(); const inp = document.getElementById('mg-answer-input');
    for (let i = 0; i < 3; i++) { MG.lockInput = false; inp.value = String(MG.currentProblem.answer); mgSubmitAnswer(); MG.lockInput = false; mgNextProblem(); }
    r.math = { score: MG.score, combo: MG.combo }; haltRunningGames();
    // 풀이형
    r.par = { sortPar: parScore('sort', 'normal', 110), sortFast: parScore('sort', 'normal', 55), sortSlow: parScore('sort', 'normal', 2000), sudokuHardPar: parScore('sudoku', 'hard', 2200, 0.08) };
    // 메달·배수
    r.medal = { run6500: medalState('run', 6500).current.key, iq125: medalState('iq', 125).current.key, stroopDiamond: medalTargets('stroop')[3].score };
    r.dm = { runHard: dm('hard', 'run'), mergeHard: dm('hard', 'merge'), anagramHard: AG_MULT.hard, sudokuNone: dm('normal', 'sudoku') };
    return r; });
  const R_ = out.rules;
  ok(R_.chop.chops === 5 && Math.abs(R_.chop.perChop - 10 * 2.07) < 0.6, 'chop ' + JSON.stringify(R_.chop));
  ok(R_.count.eventsAt8 >= 5 && R_.count.gainAtStreak31 === Math.round((10 + 20) * 0.36), 'count ' + JSON.stringify(R_.count));
  ok(R_.react.at250ms >= Math.round((1000 - 2.2 * 260) * 1.4) - 5 && R_.react.at250ms <= Math.round((1000 - 2.2 * 240) * 1.4) + 5, 'react ' + JSON.stringify(R_.react));
  ok(+R_.catch.items >= 1, 'catch spawn ' + JSON.stringify(R_.catch));
  ok(R_.math.combo === 3 && R_.math.score === 10 + 12 + 14, 'math ' + JSON.stringify(R_.math));
  ok(R_.par.sortPar === 581 && R_.par.sortFast > R_.par.sortPar && R_.par.sortSlow === Math.round(581 * 0.15), 'par ' + JSON.stringify(R_.par));
  ok(R_.medal.run6500 === 'silver' && R_.medal.iq125 === 'gold' && R_.medal.stroopDiamond === 3700, 'medal ' + JSON.stringify(R_.medal));
  ok(!errs.length, 'rules errors ' + errs[0]);
  await ctx.close(); }

await b.close();
console.log(JSON.stringify({migration:out.migration, rules:out.rules}));
for (const [k, v] of Object.entries(out.run)) console.log(k.padEnd(18), JSON.stringify(v));
console.log(fail.length ? 'FAIL\n - ' + fail.join('\n - ') : 'ALL PASS');
