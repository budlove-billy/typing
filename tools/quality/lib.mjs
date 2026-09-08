import { existsSync, readdirSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

export const ROOT = new URL('../../', import.meta.url);

export function stripComments(source) {
  return source
    .replace(/\/\*[\s\S]*?\*\//g, '')
    .replace(/^\s*\/\/.*$/gm, '');
}

export function gameRegistry(html) {
  const start = html.indexOf('const HOME_GAMES=[');
  const end = html.indexOf('];', start);
  if (start < 0 || end < 0) throw new Error('HOME_GAMES 블록을 찾을 수 없습니다.');
  const block = stripComments(html.slice(start, end + 2));
  return [...block.matchAll(/\{id:'([^']+)'([^\n}]*)\}/g)].map((match) => {
    const tail = match[2];
    const group = tail.match(/grp:'([^']+)'/)?.[1] || '';
    const langs = tail.match(/langs:\[([^\]]+)\]/)?.[1]
      ?.split(',').map((value) => value.replace(/[\s']/g, '')).filter(Boolean);
    return {
      id: match[1],
      group,
      external: /external:/.test(tail),
      koOnly: /koOnly:true/.test(tail),
      langs: langs || null,
    };
  });
}

export async function loadPlaywright() {
  try {
    return await import('playwright');
  } catch {}

  const explicit = process.env.PLAYWRIGHT_PATH;
  if (explicit && existsSync(explicit)) return import(pathToFileURL(explicit).href);

  const cache = 'C:/Users/budlo/AppData/Local/npm-cache/_npx';
  if (existsSync(cache)) {
    for (const dir of readdirSync(cache)) {
      const candidate = `${cache}/${dir}/node_modules/playwright/index.js`;
      if (existsSync(candidate)) return import(pathToFileURL(candidate).href);
    }
  }
  throw new Error('Playwright를 찾지 못했습니다. PLAYWRIGHT_PATH에 playwright/index.js 경로를 지정하세요.');
}
