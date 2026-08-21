# -*- coding: utf-8 -*-
"""GAME_REF 재보정 + 옛 기록 환산.

■ 왜
능력 레이더와 '약점 보완 추천'은 gameLevel = 최고점 / GAME_REF × 100 을 근거로 쓴다.
그런데 실측해 보니 현실적인 반응속도와 오답률로 한 판만 해도 대부분의 게임이 100%
상한을 찍었고(측정 9게임 중 7게임), 반대로 순서 잇기는 아무리 잘해도 28%였다.
즉 기준점수가 게임마다 최대 17배까지 어긋나 있어서 레이더가 전부 평평해지고
추천이 실제 약점을 못 짚었다.

■ 어떻게
게임마다 '실력 좋은 사람'의 한 판을 봇으로 3번 재서 중앙값을 구하고(.logs/refcal.mjs,
refcal2.mjs), 그 1.3배를 100% 기준으로 삼는다. → 실력자가 약 77%에 서고,
100%는 아주 잘 나온 판에만 닿는다.

측정하지 못한 게임(chop·run·fit·nono·merge·slide·sort·math·sudoku·iq 등)은
근거 없이 건드리지 않고 기존 값을 그대로 둔다. merge는 이미 400판 시뮬로 보정돼 있다.

■ 옛 기록 환산
콤보 상한(comboPts)을 도입하면서 같은 실력의 점수 규모가 내려갔다. 옛 최고기록을
그대로 두면 한동안 신기록이 뜨지 않는다. 기록은 '여러 판 중 최댓값'이라 상한의 영향을
평균보다 크게 받으므로, 게임별로 최댓값끼리의 비율을 시뮬레이션해 환산 계수를 구했다
(.logs/migr_factor.mjs · 0.53~0.94). 단일 계수를 썼다면 최대 2배 어긋났을 값이다.
"""
import io, json, os, re

SRC = 'index.html'

# ── 측정 결과 읽기 ───────────────────────────────────────────────────────────
meas = {}
for f in ['.logs/refcal.json', '.logs/refcal2.json']:
    if not os.path.exists(f):
        continue
    for o in json.load(io.open(f, encoding='utf-8')):
        meas[o['id']] = o          # 뒤 파일이 앞 파일을 덮어쓴다(재측정본 우선)
assert meas, '측정 결과가 없다 — .logs/refcal.mjs 를 먼저 돌려야 함'

# ── 기록 환산 계수 (.logs/migr_factor.mjs 산출) ──────────────────────────────
COMBO_MIGR = {
    "stroop": 0.53, "flank": 0.53, "switch": 0.61, "guess": 0.79, "spot": 0.68,
    "odd": 0.68, "whack": 0.76, "rotate": 0.69, "nback": 0.80, "diff": 0.72,
    "pitch": 0.89, "bubble": 0.84, "cards": 0.79, "catch": 0.60,
    "anagram": 0.94, "wordsearch": 0.88,
}

s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'
assert 'COMBO_MIGR' not in s, '이미 적용됨'

# ── 1) GAME_REF 갱신 ────────────────────────────────────────────────────────
m = re.search(r'const GAME_REF=\{(.*?)\};', s, re.S)
assert m, 'GAME_REF를 못 찾음'
cur = {}
for k, v in re.findall(r'(\w+):(\d+)', m.group(1)):
    cur[k] = int(v)

new, changed = dict(cur), []
for gid, o in sorted(meas.items()):
    val = int(round(o['med'] * 1.3 / 10.0) * 10)
    val = max(10, val)
    if gid in new and new[gid] != val:
        changed.append((gid, new[gid], val, o['med']))
    new[gid] = val

body = ','.join('%s:%d' % (k, new[k]) for k in cur)   # 원래 순서 유지
head = NL.join([
    "/* 능력 레이더의 100% 기준 — 게임마다 '실력 좋은 사람의 한 판'을 봇으로 재서 중앙값의 1.3배로 잡았다.",
    "   (측정: .logs/refcal.mjs · refcal2.mjs — 현실적인 반응 간격과 오답률을 넣고 3판씩)",
    "   예전 값은 근거 없이 잡혀 있어 한 판만 해도 대부분 100%에 닿았고(9개 중 7개) 순서 잇기는 28%가 한계였다.",
    "   측정하지 못한 게임(chop·run·fit·nono·slide·sort·math·sudoku·iq)은 근거가 없어 그대로 뒀다.",
    "   merge는 이미 400판 시뮬로 보정된 값이다. */",
    "const GAME_REF={%s};" % body])
s = s[:m.start()] + head + s[m.end():]

# ── 2) 옛 기록 환산 (기존 migrateScales 옆에 같은 방식으로) ──────────────────
anchor = "/* 마지막 한 판의 결과 — 결과 화면 공통 블록(최고 기록까지 N점·봇 대결)에서 쓴다 */"
if anchor not in s:
    anchor = "let _LR=null;"
assert s.count(anchor) == 1, '마이그레이션을 붙일 위치를 못 찾음'

migr = NL.join([
    "/* ══════════ 콤보 상한 도입에 따른 기록 환산 ══════════",
    "   comboPts()로 콤보 보너스에 상한이 생기면서 같은 실력의 점수 규모가 내려갔다.",
    "   옛 최고기록을 그대로 두면 한동안 신기록이 뜨지 않아 기록의 의미가 사라진다.",
    "   기록은 '여러 판 중 최댓값'이라 상한의 영향을 평균보다 크게 받으므로,",
    "   게임별로 최댓값끼리의 비율을 시뮬레이션해 계수를 구했다(.logs/migr_factor.mjs). */",
    "const COMBO_MIGR=" + json.dumps(COMBO_MIGR, ensure_ascii=False).replace(' ', '') + ";",
    "(function migrateComboCap(){",
    "  try{",
    "    if(localStorage.getItem('brain.comboMigr')==='1') return;",
    "    Object.keys(COMBO_MIGR).forEach(id=>{",
    "      const key='brain.'+id+'.best', raw=localStorage.getItem(key); if(!raw) return;",
    "      const o=JSON.parse(raw), f=COMBO_MIGR[id];",
    "      ['easy','normal','hard'].forEach(d=>{ if(o[d]){",
    "        o[d].all=Math.round((Number(o[d].all)||0)*f); o[d].day=Math.round((Number(o[d].day)||0)*f); } });",
    "      localStorage.setItem(key,JSON.stringify(o));",
    "    });",
    "    localStorage.setItem('brain.comboMigr','1');",
    "  }catch(e){}",
    "})();",
    anchor])
s = s.replace(anchor, migr, 1)

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)

print('GAME_REF 변경 %d개 (측정 %d게임)' % (len(changed), len(meas)))
print('%-12s %8s %8s   %s' % ('게임', '이전', '새값', '측정 중앙값'))
for gid, old, val, med in sorted(changed, key=lambda x: -(x[2] / max(1, x[1]))):
    print('%-12s %8d %8d   %d  (%.1f배)' % (gid, old, val, med, val / float(old)))
kept = [k for k in cur if k not in meas]
print('\n그대로 둔 게임(미측정):', ' '.join(kept))
