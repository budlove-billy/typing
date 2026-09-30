/* 홍보 영상 재료 준비: 마스코트 SVG(표정별), 홈 로비 화면 캡처(고해상도). 사용: node tools/promo-video/prep.mjs (포트 8226 서버 필요) */
import pw from 'file:///c:/Users/budlo/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
import fs from 'fs';
const OUT = '.logs/video/art'; fs.mkdirSync(OUT, { recursive: true });
const b = await pw.chromium.launch();
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, serviceWorkers: 'block' });
await ctx.addInitScript(() => { if (!sessionStorage.getItem('s')) { sessionStorage.setItem('s', '1'); localStorage.clear(); } });
const p = await ctx.newPage();
await p.goto('http://127.0.0.1:8226/index.html?lang=ko', { waitUntil: 'load' }); await p.waitForTimeout(1500);
for (const [mood, variant] of [['success', 'mint'], ['happy', 'mint'], ['focus', 'mint'], ['success', 'sky']]) {
  const svg = await p.evaluate(({ mood, variant }) => mallowSVG(mood, { size: 600, variant, standalone: true }), { mood, variant });
  fs.writeFileSync(`${OUT}/mallow-${mood}-${variant}.svg`, svg);
}
// 홈 화면: 오늘의 3판 1판 완료 상태로(링이 조금 차 있는 모습)
await p.evaluate(() => { const s = missionToday(); localStorage.setItem('brain.mission', JSON.stringify({ date: bt_today(), done: [s[0]] })); showScreen('home'); });
await p.waitForTimeout(1200);
await p.screenshot({ path: `${OUT}/home.png` });
await b.close(); console.log('prep ok');
