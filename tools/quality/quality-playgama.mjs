// Playgama(쉬어가는 게임) 품질 검사 — 파트너 약관·킬 스위치·클릭 전 미로딩·화면 넘침·밀림을 확인한다. (docs/playgama-plan.md)
// 실행: node tools/quality/quality-playgama.mjs   (먼저 python tools/playgama/build.py --preview 로 미리보기를 만든다)
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
import { loadPlaywright, ROOT } from './lib.mjs';

const port = Number(process.env.PG_QUALITY_PORT || 8227);
if (port < 8226 || port > 8230) throw new Error('PG_QUALITY_PORT는 8226~8230만 사용할 수 있습니다.');
const root = fileURLToPath(ROOT);
const read = (p) => readFileSync(path.join(root, p), 'utf8');
const fails = [];
const check = (ok, msg) => { if (!ok) fails.push(msg); };

// ---------- 정적 검사 ----------
const cfgSrc = read('assets/playgama-config.js');
try { vm.runInNewContext(cfgSrc, { window: {} }); } catch (e) { fails.push('config: 브라우저에서 JS 오류 ' + e.message); }
const a = cfgSrc.indexOf('= /*CONFIG*/') + 12;
let cfg = null;
try { cfg = JSON.parse(cfgSrc.slice(a, cfgSrc.indexOf('/*END*/', a))); } catch (e) { fails.push('config: /*CONFIG*/ 블록이 JSON이 아님 ' + e.message); }
if (cfg) {
  check(Array.isArray(cfg.games) && cfg.games.every((g) => g.id && 'url' in g && 'enabled' in g), 'config: games 항목에 id·url·enabled 필요');
  check(new Set(cfg.games.map((g) => g.id)).size === cfg.games.length, 'config: game id 중복');
}
const pgJs = read('assets/playgama.js');
for (const bad of ['missionMark', 'homeVisit', 'bt_saveBest', 'gameShare', 'sendChallenge', 'localStorage', 'sessionStorage', 'autoplay', '.click()'])
  check(!pgJs.includes(bad), `playgama.js: 기록·미션·자동 실행과 엮이면 안 됨 (${bad})`);
const indexHtml = read('index.html');
const homeGames = (indexHtml.match(/const HOME_GAMES\s*=\s*\[[^\]]*\]/) || [''])[0];
check(!/playgama|arcade/i.test(homeGames), 'index.html: HOME_GAMES에 외부 게임이 들어가면 안 됨');
check(!/playgama\.com\/export|clid=/i.test(indexHtml + pgJs), 'clid·게임 주소는 assets/playgama-config.js에만 있어야 함');
const pages = { ko: 'arcade/index.html', en: 'arcade/en.html', th: 'arcade/th.html' };
const live = !!(cfg && cfg.enabled && cfg.clid);
for (const [l, p] of Object.entries(pages)) {
  check(existsSync(path.join(root, p)), `${p} 없음 — python tools/playgama/build.py`);
  if (!existsSync(path.join(root, p))) continue;
  const s = read(p);
  check(!/adsbygoogle|pagead2/.test(s), `${p}: AdSense가 들어가면 안 됨`);
  check(!/playgama\.com\/export|clid=/.test(s), `${p}: 게임 주소·clid가 HTML에 박혀 있으면 안 됨(설정 파일에서만 읽음)`);
  check(s.includes(`<html lang="${l}">`), `${p}: lang`);
  if (!live) {
    check(!s.includes('id="pg-games"'), `${p}: 꺼진 상태인데 게임 목록이 그려짐`);
    check(s.includes('noindex'), `${p}: 꺼진 상태는 noindex여야 함`);
  }
}
if (!live) {
  check(!read('sitemap.xml').includes('/arcade/'), 'sitemap: 꺼진 상태인데 /arcade/가 있음');
  check(!read('llms.txt').includes('/arcade/'), 'llms.txt: 꺼진 상태인데 /arcade/가 있음');
}
const preview = path.join(root, '.logs/arcade-preview/index.html');
check(existsSync(preview), '미리보기 없음 — python tools/playgama/build.py --preview');

// ---------- 브라우저 검사 ----------
const mime = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webmanifest': 'application/manifest+json' };
const server = http.createServer(async (req, res) => {
  try {
    let p = decodeURIComponent(new URL(req.url, `http://127.0.0.1:${port}`).pathname);
    if (p === '/arcade/en' || p === '/arcade/th') p += '.html';
    if (p.endsWith('/')) p += 'index.html';
    const f = path.resolve(root, '.' + p);
    if (!f.startsWith(path.resolve(root))) throw new Error('bad path');
    const data = await readFile(f);
    res.setHeader('content-type', mime[path.extname(f)] || 'application/octet-stream'); res.end(data);
  } catch { res.statusCode = 404; res.end('not found'); }
});
await new Promise((ok, no) => server.once('error', no).listen(port, '127.0.0.1', ok));
const base = `http://127.0.0.1:${port}`;
const pw = await loadPlaywright(); const chromium = pw.chromium || pw.default.chromium;
const browser = await chromium.launch();

// opts.forceLive: 설정 파일을 켜진 값으로 바꿔 내려준다. opts.hang: 게임 주소 응답을 주지 않는다(불러오기 실패 상황).
async function open(url, { width = 390, forceLive = false, hang = false } = {}) {
  const ctx = await browser.newContext({ viewport: { width, height: 800 }, isMobile: width < 600, hasTouch: width < 600 });
  const page = await ctx.newPage();
  const ext = { export: 0, any: 0 };
  await ctx.route('**/*', async (route) => {
    const u = route.request().url();
    if (u.startsWith(base)) {
      if (forceLive && u.includes('/assets/playgama-config.js')) {
        const body = cfgSrc.replace('"enabled": false', '"enabled": true').replace('"clid": ""', '"clid": "TEST"');
        return route.fulfill({ contentType: 'text/javascript', body });
      }
      return route.continue();
    }
    ext.any++;
    if (/playgama\.com\/export/.test(u)) {
      ext.export++;
      if (hang) return; // 응답하지 않음
      return route.fulfill({ contentType: 'text/html', body: '<!doctype html><title>stub</title><p>game</p>' });
    }
    return route.abort();
  });
  await page.addInitScript(() => {
    window.__cls = 0;
    try { new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true }); } catch (e) {}
  });
  await page.goto(base + url, { waitUntil: 'load' });
  await page.waitForTimeout(400);
  return { ctx, page, ext };
}

try {
  // 1) 홈: 꺼진 설정이면 진입 카드 숨김·외부 요청 없음 / 켜면 카드 보임
  { const { ctx, page, ext } = await open('/');
    check(await page.$eval('#lb-pg', (e) => e.hidden), '홈: 꺼진 상태인데 진입 카드가 보임');
    check(ext.export === 0, '홈: Playgama 게임 요청이 생김'); await ctx.close(); }
  { const { ctx, page } = await open('/', { forceLive: true });
    check(!(await page.$eval('#lb-pg', (e) => e.hidden)), '홈: 켜진 상태인데 진입 카드가 안 보임');
    await page.evaluate(() => setLanguage('en'));
    await page.$eval('#lb-pg', (e) => { e.addEventListener('click', (ev) => ev.preventDefault()); e.click(); });
    check((await page.$eval('#lb-pg', (e) => e.getAttribute('href'))) === '/arcade/en', '홈: 영어일 때 진입 카드가 /arcade/en으로 가야 함');
    await ctx.close(); }

  // 2) 실제 허브(현재 설정): 꺼져 있으면 iframe 없음·준비 중 보임
  for (const u of ['/arcade/', '/arcade/en', '/arcade/th']) {
    const { ctx, page, ext } = await open(u);
    if (!live) {
      check(await page.locator('iframe').count() === 0, `${u}: 꺼진 상태인데 iframe이 있음`);
      check(await page.locator('#pg-off').isVisible(), `${u}: 준비 중 안내가 안 보임`);
    }
    check(ext.export === 0, `${u}: 클릭 전 게임 요청이 생김`);
    await ctx.close();
  }

  // 3) 미리보기(켜진 상태): 클릭 전 0 → 클릭 후 iframe 1개 → 다른 게임 눌러도 1개 → 닫기 0개
  { const { ctx, page, ext } = await open('/.logs/arcade-preview/index.html');
    const n = await page.locator('.pg-card').count();
    check(n === (cfg ? cfg.games.filter((g) => g.enabled !== false && g.url).length : 0), `미리보기: 카드 수(${n})가 설정과 다름`);
    check(await page.locator('iframe').count() === 0 && ext.export === 0, '미리보기: 클릭 전에 게임을 불러옴(자동 실행 금지)');
    await page.locator('.pg-poster').nth(0).click(); await page.waitForTimeout(300);
    check(await page.locator('iframe').count() === 1 && ext.export === 1, '미리보기: 플레이 클릭 후 iframe 1개가 아님');
    const allow = await page.locator('iframe').getAttribute('allow');
    check(allow === 'fullscreen', `미리보기: iframe allow 값(${allow})`);
    await page.locator('.pg-poster').nth(1).click(); await page.waitForTimeout(300);
    check(await page.locator('iframe').count() === 1, '미리보기: 다른 게임을 눌렀는데 iframe이 여러 개');
    await page.locator('.pg-close').click();
    check(await page.locator('iframe').count() === 0, '미리보기: 닫기 후 iframe이 남음');
    await ctx.close(); }

  // 4) 불러오기 실패: 15초 뒤 안내+다시 시도
  { const { ctx, page } = await open('/.logs/arcade-preview/index.html', { hang: true });
    await page.clock.install();
    await page.locator('.pg-poster').nth(0).click();
    await page.clock.fastForward(16000); await page.waitForTimeout(200);
    check(await page.locator('.pg-fail').isVisible(), '미리보기: 불러오기 실패 안내가 안 나옴');
    await ctx.close(); }

  // 5) 화면 넘침·밀림 (320/390/1000)
  for (const w of [320, 390, 1000]) for (const u of ['/.logs/arcade-preview/index.html', '/.logs/arcade-preview/th.html', '/arcade/']) {
    const { ctx, page } = await open(u, { width: w });
    const over = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    check(over <= 0, `${u} @${w}: 가로 넘침 ${over}px`);
    const cls = await page.evaluate(() => window.__cls);
    check(cls < 0.1, `${u} @${w}: CLS ${cls.toFixed(3)}`);
    await ctx.close();
  }
} finally {
  await browser.close(); server.close();
}

if (fails.length) { console.error('FAIL playgama\n- ' + fails.join('\n- ')); process.exit(1); }
console.log(`PASS playgama (${live ? 'live' : 'off'})`);
