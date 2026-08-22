# -*- coding: utf-8 -*-
"""길 따라가기 이탈 판정 — 규칙을 '그려진 길과의 거리' 하나로 되돌리고, 대신 여유를 틈보다 작게.

앞선 두 번의 시도가 각각 다른 방향으로 어긋나 있었다.

  ① 진행도 급변 검사 — 벗어난 쪽에 다른 갈래가 있을 때만 발동해서, 같은 정도로 벗어나도
     지형에 따라 잡히기도 하고 안 잡히기도 했다. (사용자가 말한 '애매함'의 정체)
  ② 판정을 '지금 지나는 구간'으로 한정 — 반대로 눈에 보이는 흰 길 위에 있는데도
     이탈로 잡히는 경우가 생긴다. 플레이어는 어느 부분이 '지금 구간'인지 알 수 없다.
     계측(.logs/trace_consistency.mjs)에서도 개선이 46.8%→35.2%에 그쳤는데,
     남은 35%는 사실 '모퉁이 근처라 실제로는 길 안'이었다 — 즉 잘못 잡은 게 아니라
     내 판정 모델이 화면과 달랐던 것이다.

플레이어가 볼 수 있는 것은 **그려진 길 전체**뿐이다. 그러니 규칙도 그것 하나여야 한다:
  「그려진 길의 가장자리에서 N px 넘게 나가면 이탈」
그려진 길은 경로 폴리라인을 굵기 w로 둥근 이음으로 그린 것이므로,
'그려진 길과의 거리'는 정확히 tcDist(p) - w/2 다. 모퉁이의 둥근 부분까지 그대로 맞는다.

그럼 나란한 갈래로 건너뛰는 문제는? **여유(N)를 갈래 사이 틈의 절반보다 작게** 두면
애초에 다리가 놓이지 않는다. 두 갈래의 그려진 가장자리 사이 간격은 (칸 크기 - 폭)이므로
N < (칸 크기 - 폭)/2 이면 건너가는 도중 반드시 어느 쪽에서도 벗어난 지점을 지난다.

그래서:
  - tcNearest / 진행도(prog) / 진행도 창(win) 전부 제거 — 규칙이 하나면 필요 없다.
  - 이탈 판정은 tcDist 하나로. 이동 구간을 6px로 잘라 검사하는 것은 유지(빠른 손 대응).
  - 여유 N = min(레벨에 따라 줄어드는 기본값, (칸 - 폭)/2 × 0.8).
"""
import io

SRC = 'index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'
assert 'tcNearest' in s, 'fix-trace-window.py 이후 상태여야 함'


def one(old, new, what):
    global s
    assert s.count(old) == 1, what + ' — 대상을 못 찾음(또는 여러 개)'
    s = s.replace(old, new, 1)


def cut(start_marker, end_marker, what):
    global s
    i = s.index(start_marker)
    j = s.index(end_marker, i)
    s = s[:i] + s[j:]


# ── 1) tcNearest와 진행도 계산을 통째로 걷어낸다 ────────────────────────────
i = s.index("/* 경로의 누적 길이")
j = s.index("function tcDist(p){")
s = s[:i] + s[j:]

# ── 2) 이동 판정 — tcDist 하나로 ────────────────────────────────────────────
old_chk = NL.join([
    "      /* '지금 지나는 구간'과의 거리만 본다 — 옆 갈래가 가깝다는 이유로 봐주지 않는다.",
    "         다른 갈래로 건너뛰면 밟고 있던 길에서 멀어지므로 여기서 자연히 이탈이 된다. */",
    "      const near=tcNearest(q, TC.prog, TC.win);",
    "      if(near.d>TC.tol){ TC.cur=q; tcStray(); return; }",
    "      TC.prog=near.t;"])
new_chk = NL.join([
    "      /* 규칙은 하나 — 그려진 길에서 얼마나 나갔나. 그려진 길은 경로를 굵기 w로",
    "         둥글게 그린 것이라 tcDist가 곧 화면상의 거리이고, 모퉁이의 둥근 부분도 그대로 맞는다. */",
    "      if(tcDist(q)>TC.tol){ TC.cur=q; tcStray(); return; }"])
one(old_chk, new_chk, '이동 판정 단순화')

# ── 3) 여유를 틈보다 작게 ───────────────────────────────────────────────────
one(NL.join([
    "  /* 규칙은 한 문장 — '보이는 길의 가장자리에서 이만큼까지는 봐준다'.",
    "     (나란한 갈래로 건너뛰는 것은 위의 '진행도 창'이 막으므로 여기서 조일 필요가 없다) */",
    "  TC.tol=w/2+Math.max(4, 12-(TC.level-1)*0.5);",
    "  /* 판정에 쓸 구간의 범위. 한 칸보다 넉넉해 정상 이동은 늘 창 안에 들어오고,",
    "     나란한 갈래(왕복이면 두 칸 이상 떨어져 있다)는 확실히 창 밖이다. */",
    "  TC.win=Math.max(70, TC.cell*1.6);"]),
    NL.join([
        "  /* 규칙은 한 문장 — '그려진 길의 가장자리에서 이만큼까지는 봐준다'.",
        "     여유를 나란한 두 갈래 사이 틈((칸-폭))의 절반보다 작게 두면, 건너가는 도중",
        "     반드시 양쪽 어디에서도 벗어난 지점을 지나므로 질러가기가 성립하지 않는다. */",
        "  const slack=Math.max(4, 12-(TC.level-1)*0.5);",
        "  TC.tol=w/2+Math.min(slack, Math.max(2,(TC.cell-w)/2*0.8));"]),
    '여유 상한')

# ── 4) 상태 필드 정리 ───────────────────────────────────────────────────────
one("cur:null, grip:null, prog:null, arc:[], win:80,", "cur:null, grip:null,", 'TC 상태 필드')
one("  TC.path=tcGenPath(steps); TC.trail=[]; tcArcInit();",
    "  TC.path=tcGenPath(steps); TC.trail=[];", '진행도 표 제거')
for a, b in [("TC.cur=null; TC.grip=null; TC.prog=null;", "TC.cur=null; TC.grip=null;")]:
    s = s.replace(a, b)
one("      TC.cur={x:st.x,y:st.y}; TC.trail=[{x:st.x,y:st.y}]; TC.prog=0;",
    "      TC.cur={x:st.x,y:st.y}; TC.trail=[{x:st.x,y:st.y}];", '시작 진행도 제거')

assert 'TC.prog' not in s, 'prog 잔여: ' + s[s.index('TC.prog') - 80:s.index('TC.prog') + 80]
assert 'TC.win' not in s and 'tcArcInit' not in s and 'tcNearest' not in s, '잔여 코드 있음'

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — 규칙을 tcDist 하나로 · 여유를 갈래 틈의 절반 미만으로')
