/* 플레이말로우 15초 홍보 영상 만들기 — render.html의 프레임(450장)·소리(WAV)를 받아 ffmpeg로 mp4를 만든다.
   사용: node tools/promo-video/prep.mjs  →  node tools/promo-video/render.mjs [--preview]
   필요: 포트 8226 정적 서버(저장소 루트), ffmpeg(.logs/pylib의 imageio-ffmpeg — pip install --target .logs/pylib imageio-ffmpeg)
   --preview: 몇 장면만 PNG로 뽑아 확인(영상은 만들지 않음) */
import pw from 'file:///c:/Users/budlo/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
import fs from 'fs'; import { execFileSync } from 'child_process';
const PREVIEW = process.argv.includes('--preview');
const WORK = '.logs/video', FR = `${WORK}/frames`; fs.mkdirSync(FR, { recursive: true });
const FFMPEG = fs.readdirSync('.logs/pylib/imageio_ffmpeg/binaries').find(f => f.startsWith('ffmpeg'));
const b = await pw.chromium.launch();
const p = await (await b.newContext({ viewport: { width: 400, height: 700 } })).newPage();
const errs = []; p.on('pageerror', e => errs.push(String(e)));
await p.goto('http://127.0.0.1:8226/tools/promo-video/render.html', { waitUntil: 'load' });
const n = await p.evaluate(() => window.ready); console.log('images', n);
const save = (file, dataUrl) => fs.writeFileSync(file, Buffer.from(dataUrl.split(',')[1], 'base64'));
if (PREVIEW) {
  for (const t of [0, 0.6, 1.2, 1.7, 3.0, 6.1, 8.8, 9.9, 11.2, 12.0, 13.2, 14.97]) save(`${WORK}/preview_${t.toFixed(2)}.jpg`, await p.evaluate(t => renderFrame(t), t));
  console.log('preview ok', errs); await b.close(); process.exit(0);
}
const FPS = 30, TOTAL = 15 * FPS;
for (let f = 0; f < TOTAL; f++) save(`${FR}/f${String(f).padStart(4, '0')}.jpg`, await p.evaluate(t => renderFrame(t), f / FPS));
const au = await p.evaluate(() => renderAudio()); fs.writeFileSync(`${WORK}/audio.wav`, Buffer.from(au.b64, 'base64'));
console.log('frames', TOTAL, 'audio peak before normalize', au.peakDb, 'dB', errs);
await b.close();
fs.mkdirSync('generated_images', { recursive: true });
execFileSync(`.logs/pylib/imageio_ffmpeg/binaries/${FFMPEG}`, ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', `${FR}/f%04d.jpg`, '-i', `${WORK}/audio.wav`,
  '-vf', 'scale=in_range=full:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-crf', '23', '-profile:v', 'high', '-level', '4.1', '-preset', 'medium', '-r', String(FPS), '-c:a', 'aac', '-b:a', '192k', '-t', '15', '-movflags', '+faststart',
  'generated_images/mallow-promo-15s.mp4'], { stdio: 'inherit' });
console.log('mp4 ok', (fs.statSync('generated_images/mallow-promo-15s.mp4').size / 1e6).toFixed(1), 'MB');
