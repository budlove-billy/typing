import http from 'node:http';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { gameRegistry, loadPlaywright, ROOT } from './lib.mjs';

const port = Number(process.env.QUALITY_PORT || 8065);
if (port < 8065 || port > 8069) throw new Error('QUALITY_PORT는 8065~8069만 사용할 수 있습니다.');
const root = fileURLToPath(ROOT);
const html = await readFile(new URL('index.html', ROOT), 'utf8');
const games = gameRegistry(html).filter((game) => !game.external && !['cat.daily', 'cat.fun'].includes(game.group));
const startMap = Object.fromEntries([...html.matchAll(/([a-z]+):'(start[^']+)'/g)].map((match) => [match[1], match[2]]));
const mime = { '.html':'text/html; charset=utf-8', '.js':'text/javascript; charset=utf-8', '.json':'application/json', '.webmanifest':'application/manifest+json', '.svg':'image/svg+xml', '.png':'image/png', '.jpg':'image/jpeg' };

const server = http.createServer(async (request, response) => {
  try {
    let pathname = decodeURIComponent(new URL(request.url, `http://127.0.0.1:${port}`).pathname);
    if (pathname.endsWith('/')) pathname += 'index.html';
    const resolved = path.resolve(root, `.${pathname}`);
    if (!resolved.startsWith(path.resolve(root))) throw new Error('invalid path');
    const data = await readFile(resolved);
    response.setHeader('content-type', mime[path.extname(resolved)] || 'application/octet-stream');
    response.end(data);
  } catch {
    response.statusCode = 404;
    response.end('not found');
  }
});
await new Promise((resolve, reject) => server.once('error', reject).listen(port, '127.0.0.1', resolve));

const playwright = await loadPlaywright();
const chromium = playwright.chromium || playwright.default?.chromium;
const browser = await chromium.launch();
const failures = [];
let runs = 0;

try {
  for (const lang of ['ko', 'en', 'th']) {
    const context = await browser.newContext({
      viewport: { width: 390, height: 844 },
      locale: lang === 'ko' ? 'ko-KR' : lang === 'th' ? 'th-TH' : 'en-US',
      serviceWorkers: 'block',
    });
    for (const game of games.filter((item) => !item.koOnly && (!item.langs || item.langs.includes(lang)))) {
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', (error) => errors.push(error.message));
      page.on('console', (message) => {
        if (message.type() === 'error' && !/^Failed to load resource: net::ERR_/.test(message.text())) errors.push(message.text());
      });
      try {
        await page.goto(`http://127.0.0.1:${port}/index.html?lang=${lang}&game=${game.id}`, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(120);
        const state = await page.evaluate((id) => ({
          opened: document.getElementById(`screen-${id}`)?.classList.contains('active'),
          active: [...document.querySelectorAll('.screen.active')].map((screen) => screen.id),
          href: location.href,
          canShow: typeof window.showScreen === 'function',
        }), game.id);
        if (!state.opened) failures.push(`${lang}/${game.id}: 게임 화면이 열리지 않음 (active=${state.active.join(',') || '없음'}, showScreen=${state.canShow}, url=${state.href})`);
        const fn = startMap[game.id];
        const started = await page.evaluate((name) => {
          if (typeof window[name] !== 'function') return `시작 함수 없음: ${name}`;
          try { window[name](); return true; } catch (error) { return error.message; }
        }, fn);
        if (started !== true) failures.push(`${lang}/${game.id}: ${started}`);
        await page.waitForTimeout(120);
        if(game.id==='flash'){
          const result=await page.evaluate(()=>{
            FM.score=200;
            const imported=JSON.parse(JSON.stringify(FM.best)); imported[FM.diff].all=1000;
            localStorage.setItem('brain.flash.best',JSON.stringify(imported));
            finishFlash();
            const saved=JSON.parse(localStorage.getItem('brain.flash.best'))[FM.diff].all;
            const visible=document.getElementById('flash-result-card').style.display==='block';
            const retry=!!document.querySelector('#flash-result-card .pg-box');
            pgRetry('flash');
            return saved===1000&&visible&&retry&&document.getElementById('flash-game-card').style.display==='block';
          });
          if(!result) failures.push(`${lang}/flash: record/result/retry failed`);
        }
        if (errors.length) failures.push(`${lang}/${game.id}: ${errors[0]}`);
        runs++;
      } catch (error) {
        failures.push(`${lang}/${game.id}: ${error.message}`);
      } finally {
        await page.close();
      }
    }
    await context.close();
  }

  for (const width of [320, 390]) {
    for (const lang of ['ko', 'en', 'th']) {
      const context = await browser.newContext({ viewport: { width, height: 844 }, serviceWorkers: 'block' });
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', (error) => errors.push(error.message));
      await page.goto(`http://127.0.0.1:${port}/index.html?lang=${lang}`, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(180);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      if (overflow > 1) failures.push(`${lang}/${width}px 홈: 가로 넘침 ${overflow}px`);
      if (errors.length) failures.push(`${lang}/${width}px 홈: ${errors[0]}`);
      await context.close();
    }
  }
  const offlineContext=await browser.newContext();
  const offlinePage=await offlineContext.newPage();
  await offlinePage.goto(`http://127.0.0.1:${port}/`,{waitUntil:'load'});
  await offlinePage.evaluate(()=>navigator.serviceWorker.ready);
  await offlinePage.reload({waitUntil:'load'});
  await offlineContext.setOffline(true);
  await offlinePage.goto(`http://127.0.0.1:${port}/`,{waitUntil:'domcontentloaded'});
  if(!await offlinePage.locator('#screen-home').count()) failures.push('offline home unavailable');
  await offlinePage.goto(`http://127.0.0.1:${port}/unvisited-content/`,{waitUntil:'domcontentloaded'});
  if(!await offlinePage.locator('h1').textContent().then(t=>t.includes('offline'))) failures.push('offline content fallback incorrect');
  await offlineContext.close();
} finally {
  await browser.close();
  await new Promise((resolve) => server.close(resolve));
}

console.log(`브라우저 검사: 게임 시작 ${runs}회 · 홈 모바일 6회`);
if (failures.length) {
  failures.forEach((failure) => console.error(`FAIL ${failure}`));
  process.exit(1);
}
console.log('PASS 언어별 게임 시작·모바일 화면·런타임 오류');
