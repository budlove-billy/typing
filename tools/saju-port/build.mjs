// 사주 엔진을 브라우저용 한 파일(assets/saju-engine.js, 전역 SajuEngine)로 묶는다. 원본은 D:\claude\saju(읽기만).
import { execFileSync } from 'child_process';
const SAJU = 'D:/claude/saju';
execFileSync(`${SAJU}/node_modules/.bin/esbuild.cmd`, ['tools/saju-port/entry.ts', '--bundle', '--minify', '--format=iife', '--global-name=SajuEngine',
  '--platform=browser', '--target=es2019', `--tsconfig=${SAJU}/tsconfig.json`, `--alias:@=${SAJU}/src`, `--resolve-extensions=.ts,.js,.mjs,.json`,
  '--outfile=assets/saju-engine.js', '--legal-comments=none', '--alias:node:crypto=./tools/saju-port/crypto-shim.ts'], { stdio: 'inherit', shell: true, env: { ...process.env, NODE_PATH: `${SAJU}/node_modules` } });
