# -*- coding: utf-8 -*-
"""틀린 그림 찾기 — 넓은 화면에서는 두 판을 좌우로 놓는다.

두 판을 항상 세로로 쌓다 보니, 화면이 넓을 때는 좌우가 통째로 비면서 판은 판대로
작아지고(세로 공간을 반씩 나눠 쓰니까) 시선도 위아래로 크게 움직여야 했다.
비교 게임은 두 판이 눈에 한 번에 들어와야 한다.

- 넓을 때(판 영역 620px 이상): 좌우 배치. 세로 공간을 통째로 쓰므로 칸이 커진다.
- 좁을 때(휴대폰): 지금처럼 위아래. 세로로 쌓는 것 말고 방법이 없다 —
  대신 창 높이에 맞춰 칸을 줄여 두 판이 한 화면에 들어오게 이미 맞춰 두었다.
안내 문구도 배치에 따라 '위아래를 비교' / '좌우를 비교'로 바뀐다.
"""
import io

SRC = 'index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'
assert 'df-grids.wide' not in s, '이미 적용됨'


def one(old, new, what):
    global s
    assert s.count(old) == 1, what + ' — 대상을 못 찾음(또는 여러 개)'
    s = s.replace(old, new, 1)


# ── 0) 컨테이너에 안정적인 선택자를 준다 ────────────────────────────────────
one('<div class="df-grids">', '<div class="df-grids" id="df-grids">', 'df-grids id 부여')

# ── 1) 좌우 배치용 스타일 ───────────────────────────────────────────────────
one(".df-grids{display:flex;flex-direction:column;gap:.45rem;align-items:center}",
    NL.join([
        ".df-grids{display:flex;flex-direction:column;gap:.45rem;align-items:center}",
        "/* 넓은 화면에서는 좌우로 — 클래스는 dfRender가 실제 폭을 재서 붙인다(기준을 한 곳에 둔다) */",
        ".df-grids.wide{flex-direction:row;justify-content:center;gap:1rem}",
        ".df-grids.wide .df-vs-wrap{flex:0 0 auto;max-width:120px;text-align:center}",
        ".df-grids.wide .df-vs{justify-content:center}"]),
    'df-grids 좌우 스타일')

# ── 2) 렌더 — 배치에 따라 칸 크기 계산을 바꾼다 ─────────────────────────────
old = NL.join([
    "  /* 위아래 고정 영역의 실측 합계. 338이면 세로 640px 기기에서 아래 판이 63px 잘렸다.",
    "     (헤더 128 + 점수칸 · 타이머 · 안내문 · 남은개수 알약 + 하단 탭 90) */",
    "  const availW=328, availH=Math.max(180,(window.innerHeight||760)-404);",
    "  const cs=Math.max(26, Math.min(Math.floor(availW/DF.n), Math.floor((availH/2)/DF.n), 54));"])
assert s.count(old) == 1, '틀린그림 칸 크기 계산을 못 찾음'
new = NL.join([
    "  /* 배치를 먼저 정한다 — 판 영역이 620px 이상이면 좌우, 아니면 위아래.",
    "     좌우면 세로 공간을 통째로 쓰고, 위아래면 반씩 나눠 쓴다. */",
    "  const host=document.getElementById('df-grids');",
    "  const hostW=(host&&host.clientWidth)||328;",
    "  const wide=hostW>=620;",
    "  if(host) host.classList.toggle('wide', wide);",
    "  const vs=document.querySelector('#df-grids .df-vs');",
    "  if(vs) vs.textContent=t(wide?'diff.compareLR':'diff.compare');",
    "  /* 위아래 고정 영역의 실측 합계. 338이면 세로 640px 기기에서 아래 판이 63px 잘렸다.",
    "     (헤더 128 + 점수칸 · 타이머 · 안내문 · 남은개수 알약 + 하단 탭 90) */",
    "  const availW = wide ? Math.max(120,(hostW-140)/2) : Math.min(328,hostW);",
    "  const availH = wide ? Math.max(200,(window.innerHeight||760)-330)",
    "                      : Math.max(180,(window.innerHeight||760)-404)/2;",
    "  const cs=Math.max(26, Math.min(Math.floor(availW/DF.n), Math.floor(availH/DF.n), wide?70:54));"])
s = s.replace(old, new, 1)

# ── 3) 좌우 배치용 안내 문구 (3언어) ────────────────────────────────────────
anchor = None
for cand in ['"diff.compare":', "'diff.compare':"]:
    if s.count(cand) == 1:
        anchor = cand
        break
assert anchor, 'diff.compare 번역 항목을 못 찾음'
i = s.index(anchor)
j = s.index(NL, i)
line = s[i:j]
s = s[:j] + NL + ('  "diff.compareLR": {ko:"↔ 좌우를 비교하세요", '
                  'en:"↔ Compare left and right", '
                  'th:"↔ เทียบซ้ายกับขวา"},') + s[j:]

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — 좌우 배치 + 안내 문구 3언어')
print('   기존 항목:', line.strip()[:80])
