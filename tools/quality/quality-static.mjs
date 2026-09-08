import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { gameRegistry, ROOT } from './lib.mjs';

const root = fileURLToPath(ROOT);
const html = readFileSync(new URL('index.html', ROOT), 'utf8');
const games = gameRegistry(html);
const issues = [];
const check = (condition, message) => { if (!condition) issues.push(message); };

const trackedHtml = execFileSync('git', ['ls-files', '*.html'], { cwd: root, encoding: 'utf8' })
  .trim().split(/\r?\n/).filter(Boolean);
for (const relative of trackedHtml) {
  const source = readFileSync(new URL(relative.replaceAll('\\', '/'), ROOT), 'utf8');
  const scripts = [...source.matchAll(/<script(?![^>]*\bsrc=)([^>]*)>([\s\S]*?)<\/script>/gi)]
    .filter((match) => !/type=["'](?:application\/ld\+json|application\/json)["']/i.test(match[1]));
  scripts.forEach((match, index) => {
    try { new Function(match[2]); }
    catch (error) { issues.push(`${relative}: 인라인 스크립트 ${index + 1} 문법 오류 (${error.message})`); }
  });
}

const visibleSkillGames = games.filter((game) => !game.external && !['cat.daily', 'cat.fun'].includes(game.group));
const ids = visibleSkillGames.map((game) => game.id);
check(new Set(ids).size === ids.length, 'HOME_GAMES에 중복 게임 ID가 있습니다.');
check(ids.length === 34, `현재 노출 스킬 게임 수가 예상값 34와 다릅니다 (${ids.length}).`);
check(html.includes(`10개 능력 영역의 ${ids.length}가지 미니게임`), `홈 한국어 게임 수 안내가 실제 노출 수 ${ids.length}와 다릅니다.`);
check(html.includes(`Try ${ids.length} mini games across 10 skill areas`), `홈 영어 게임 수 안내가 실제 노출 수 ${ids.length}와 다릅니다.`);
check(html.includes(`มินิเกม ${ids.length} เกมใน 10 ด้านความสามารถ`), `홈 태국어 게임 수 안내가 실제 노출 수 ${ids.length}와 다릅니다.`);
const guide = readFileSync(new URL('guide/brain-games/index.html', ROOT), 'utf8');
check(guide.includes(`<h1>두뇌게임 ${ids.length}종 총정리</h1>`), `두뇌게임 가이드의 게임 수가 실제 노출 수 ${ids.length}와 다릅니다.`);

const pgBlock = html.match(/const PG_START=\{([^}]+)\}/)?.[1] || '';
const retryIds = [...pgBlock.matchAll(/([a-z]+):'start[^']+'/g)].map((match) => match[1]);
check(ids.every((id) => retryIds.includes(id)), `바로 다시 연결 누락: ${ids.filter((id) => !retryIds.includes(id)).join(', ')}`);
check(retryIds.every((id) => ids.includes(id)), `비노출 게임이 바로 다시 목록에 남음: ${retryIds.filter((id) => !ids.includes(id)).join(', ')}`);

const abilityBlock = html.match(/const ABILITY_MAP=\{([\s\S]*?)\n\};/)?.[1] || '';
const refBlock = html.match(/const GAME_REF=\{([^}]+)\}/)?.[1] || '';
for (const id of ids) {
  check(html.includes(`id="screen-${id}"`), `${id}: 화면 누락`);
  check(html.includes(`id="${id}-intro-card"`), `${id}: 시작 안내 카드 누락`);
  check(html.includes(`id="${id}-result-card"`), `${id}: 결과 카드 누락`);
  check(new RegExp(`(?:^|[,\\s])${id}:\\{`).test(abilityBlock), `${id}: 능력치 연결 누락`);
  check(new RegExp(`(?:^|,)${id}:\\d`).test(refBlock), `${id}: 기록 기준값 누락`);
  check(html.includes(`"nav.${id}":`), `${id}: 이름 번역 키 누락`);
}

const usedI18n = new Set([...html.matchAll(/data-i18n(?:-ph)?="([^"]+)"/g)].map((match) => match[1]));
const definedI18n = new Set([...html.matchAll(/"([a-zA-Z0-9_.-]+)":\s*\{\s*ko:/g)].map((match) => match[1]));
const missingI18n = [...usedI18n].filter((key) => !definedI18n.has(key));
check(missingI18n.length === 0, `사용 중인 번역 키 누락: ${missingI18n.join(', ')}`);

for (const asset of ['manifest.webmanifest', 'sw.js', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png', 'favicon-32.png']) {
  check(existsSync(new URL(asset, ROOT)), `PWA 필수 파일 누락: ${asset}`);
}
const manifest = JSON.parse(readFileSync(new URL('manifest.webmanifest', ROOT), 'utf8'));
check(manifest.display === 'standalone', 'manifest display가 standalone이 아닙니다.');
check(Array.isArray(manifest.icons) && manifest.icons.some((icon) => icon.sizes === '192x192'), '192px PWA 아이콘 선언 누락');
check(Array.isArray(manifest.icons) && manifest.icons.some((icon) => icon.sizes === '512x512'), '512px PWA 아이콘 선언 누락');
const sw = readFileSync(new URL('sw.js', ROOT), 'utf8');
check(/const CACHE\s*=\s*'mallow-v\d+'/.test(sw), '서비스워커 캐시 버전 형식 오류');
check(sw.includes("caches.match('index.html')"), '오프라인 HTML 폴백 누락');

console.log(`정적 검사: HTML ${trackedHtml.length}개 · 노출 스킬 게임 ${ids.length}개 · 번역 키 ${usedI18n.size}개`);
if (issues.length) {
  issues.forEach((issue) => console.error(`FAIL ${issue}`));
  process.exit(1);
}
console.log('PASS 게임 계약·스크립트 문법·번역·PWA 필수 항목');
