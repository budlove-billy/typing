# -*- coding: utf-8 -*-
"""길 따라가기 — "살짝 벗어났을 때 잡힐 때도 있고 아닐 때도 있다"의 원인.

tcNearest()가 **경로 전체**에서 가장 가까운 지점을 찾는 것이 문제였다.
같은 정도로 길을 벗어나도 주변 지형에 따라 결과가 갈린다:

  ① 벗어난 쪽에 다른 갈래가 지나가면 → 그쪽까지의 거리가 짧아서 '아직 길 위'로 인정 → 안 잡힘
  ② 최근접 구간이 그 다른 갈래로 넘어가면 → 진행도(t)가 확 튀어서 '건너뛰기'로 판정 → 잡힘

즉 **판정 기준이 '내가 지나던 길'이 아니라 '가장 가까운 아무 길'**이었다.
플레이어는 자기가 밟고 있던 길에서 얼마나 벗어났는지로 생각하는데, 코드는 다른 걸 보고 있었다.

고침: 거리를 **지금 지나고 있는 구간 근처에서만** 잰다(진행도 기준 창).
  - 벗어남은 항상 '밟고 있던 길'과의 거리로 판정된다 → 어디서든 같은 규칙.
  - 다른 갈래는 창 밖이라 애초에 후보가 아니다 → 가로질러 건너뛰는 것도 그대로 막힌다
    (건너가는 순간 밟고 있던 길에서 멀어지므로 자연스럽게 이탈이 된다).
  - 진행도가 튀는 일이 없어지므로, 그걸 잡으려고 넣었던 '진행도 급변' 검사는 지운다.
    그 검사가 ②의 오탐을 만들던 장본인이다.
  - 허용 오차의 '칸 크기 45%' 상한도 지운다. 나란한 갈래를 잇는 다리를 막으려던 것인데
    창으로 이미 막히므로, 규칙을 **"보이는 길 바깥으로 N px까지 봐준다"** 하나로 단순하게 되돌린다.

결과적으로 규칙이 한 문장이 된다 — "밟고 있던 길의 보이는 가장자리에서 N px 넘게 나가면 이탈".
"""
import io

SRC = 'index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'
assert 'TC.win' not in s, '이미 적용됨'


def one(old, new, what):
    global s
    assert s.count(old) == 1, what + ' — 대상을 못 찾음(또는 여러 개)'
    s = s.replace(old, new, 1)


# ── 1) 진행도 창 안에서만 최근접을 찾는다 ───────────────────────────────────
old_near = NL.join([
    "function tcNearest(p){",
    "  let md=1e9, mt=0;",
    "  for(let i=0;i<TC.path.length-1;i++){",
    "    const a=TC.path[i], b=TC.path[i+1];",
    "    const dx=b.x-a.x, dy=b.y-a.y, l2=dx*dx+dy*dy;",
    "    let u=l2?((p.x-a.x)*dx+(p.y-a.y)*dy)/l2:0; u=Math.max(0,Math.min(1,u));",
    "    const d=Math.hypot(p.x-(a.x+u*dx), p.y-(a.y+u*dy));",
    "    if(d<md){ md=d; mt=(TC.arc[i]||0)+u*Math.sqrt(l2); }",
    "  }",
    "  return {d:md, t:mt};",
    "}"])
new_near = NL.join([
    "/* p에서 가장 가까운 경로 지점을 '거리'와 '진행도'로 돌려준다.",
    "   around/win을 주면 **진행도가 그 창 안에 있는 구간만** 본다 = '지금 지나고 있는 길'만 본다.",
    "   경로 전체에서 찾으면, 같은 정도로 벗어나도 옆을 지나가는 다른 갈래가 있느냐 없느냐에 따라",
    "   판정이 갈려서 플레이어에게는 기준이 없어 보인다. */",
    "function tcNearest(p, around, win){",
    "  let md=1e9, mt=(around||0), found=false;",
    "  for(let i=0;i<TC.path.length-1;i++){",
    "    if(win!=null){",
    "      const a0=TC.arc[i], a1=TC.arc[i+1];",
    "      if(a1 < around-win || a0 > around+win) continue;   // 창 밖의 갈래는 후보가 아니다",
    "    }",
    "    const a=TC.path[i], b=TC.path[i+1];",
    "    const dx=b.x-a.x, dy=b.y-a.y, l2=dx*dx+dy*dy;",
    "    let u=l2?((p.x-a.x)*dx+(p.y-a.y)*dy)/l2:0; u=Math.max(0,Math.min(1,u));",
    "    const d=Math.hypot(p.x-(a.x+u*dx), p.y-(a.y+u*dy));",
    "    found=true;",
    "    if(d<md){ md=d; mt=(TC.arc[i]||0)+u*Math.sqrt(l2); }",
    "  }",
    "  if(!found) return tcNearest(p);   // 창 안에 구간이 없으면(있을 수 없지만) 전체에서",
    "  return {d:md, t:mt};",
    "}"])
one(old_near, new_near, 'tcNearest 창 한정')

# ── 2) 이동 판정 — 창을 넘기고, 진행도 급변 검사는 제거 ─────────────────────
old_chk = NL.join([
    "      const near=tcNearest(q);",
    "      if(near.d>TC.tol){ TC.cur=q; tcStray(); return; }",
    "      /* 움직인 거리에 비해 '경로상 진행도'가 훨씬 크게 튀면 = 길을 가로질러",
    "         다른 구간으로 건너뛴 것. 되짚어 오는 것(진행도 감소)은 정상이므로 절댓값으로 본다. */",
    "      if(TC.prog!=null && Math.abs(near.t-TC.prog) > per*1.6+20){ TC.cur=q; tcStray(); return; }",
    "      TC.prog=near.t;"])
new_chk = NL.join([
    "      /* '지금 지나는 구간'과의 거리만 본다 — 옆 갈래가 가깝다는 이유로 봐주지 않는다.",
    "         다른 갈래로 건너뛰면 밟고 있던 길에서 멀어지므로 여기서 자연히 이탈이 된다. */",
    "      const near=tcNearest(q, TC.prog, TC.win);",
    "      if(near.d>TC.tol){ TC.cur=q; tcStray(); return; }",
    "      TC.prog=near.t;"])
one(old_chk, new_chk, '이동 판정')

# per(샘플당 이동량)는 더 이상 쓰이지 않는다
one("    const n=Math.max(1, Math.ceil(step/6)), per=step/n;",
    "    const n=Math.max(1, Math.ceil(step/6));",
    'per 제거')

# ── 3) 허용 오차를 다시 단순하게 — 창이 다리 놓기를 막으므로 상한이 필요 없다 ──
one(NL.join([
    "  /* 허용 오차가 갈래 간격(=칸 크기)의 절반을 넘으면, 나란한 두 갈래의 중간에서도",
    "     양쪽 다 '길 위'로 인정돼 지그재그를 가로질러 질러갈 수 있다. 45%로 막는다. */",
    "  TC.tol=Math.min(w/2+Math.max(4, 12-(TC.level-1)*0.5), TC.cell*0.45);"]),
    NL.join([
        "  /* 규칙은 한 문장 — '보이는 길의 가장자리에서 이만큼까지는 봐준다'.",
        "     (나란한 갈래로 건너뛰는 것은 위의 '진행도 창'이 막으므로 여기서 조일 필요가 없다) */",
        "  TC.tol=w/2+Math.max(4, 12-(TC.level-1)*0.5);",
        "  /* 판정에 쓸 구간의 범위. 한 칸보다 넉넉해 정상 이동은 늘 창 안에 들어오고,",
        "     나란한 갈래(왕복이면 두 칸 이상 떨어져 있다)는 확실히 창 밖이다. */",
        "  TC.win=Math.max(70, TC.cell*1.6);"]),
    '허용 오차 단순화 + 창 크기')

# ── 4) 상태 필드 ────────────────────────────────────────────────────────────
one("cur:null, grip:null, prog:null, arc:[],",
    "cur:null, grip:null, prog:null, arc:[], win:80,",
    'TC 상태 필드')

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — 판정을 지나는 구간으로 한정 · 진행도 급변 검사 제거 · 허용 오차 단순화')
