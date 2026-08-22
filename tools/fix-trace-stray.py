# -*- coding: utf-8 -*-
"""길 따라가기 — 길을 벗어나도 이탈로 안 잡히던 문제.

증상(사용자 화면): 파란 궤적이 길 밖 빈 공간을 대각선으로 가로질렀는데 생명이 그대로.

원인 1 — **이동 구간의 중간을 검사하지 않았다.**
  pointermove가 올 때마다 '그 지점'만 검사했다. 손가락이 빠르면 이벤트 사이 간격이
  수십 px씩 벌어지는데, 그 사이를 잇는 직선은 한 번도 검사되지 않는다.
  출발점과 도착점이 각각 길 위에 있기만 하면, 그 사이가 통째로 길 밖이어도 통과했다.
  → 이전 위치에서 새 위치까지 6px 간격으로 잘라 전부 검사한다.

원인 2 — **판정이 '아무 구간과의 최단거리'였다.**
  tcDist는 경로의 어느 구간이든 가장 가까운 것과의 거리다. 그래서 나란히 지나가는
  두 갈래 사이를 건너뛰어도, 건너간 쪽 갈래가 가까우면 계속 '길 위'로 인정됐다.
  실제로 허용 오차가 갈래 간격의 절반보다 커지는 구간이 있었다(칸 34px일 때 허용 20px,
  갈래 중심 간 거리 34px의 절반은 17px) — 지그재그를 가로질러 질러갈 수 있었다는 뜻이다.
  → ㉠ 경로를 따라 얼마나 왔는지(진행도)를 추적해서, **실제 움직인 거리보다 진행도가
       훨씬 크게 튀면** 다른 구간으로 건너뛴 것으로 보고 이탈 처리한다.
    ㉡ 허용 오차에 '칸 크기의 45%' 상한을 둔다. 두 갈래의 중간 지점은 각 갈래에서
       칸 크기의 50%만큼 떨어져 있으므로, 이 상한이면 양쪽 어디에도 걸리지 않아
       가로지르기 자체가 성립하지 않는다.

되돌아오는 것(진행도가 줄어드는 것)은 그대로 허용한다 — 왔던 길을 되짚는 건 정상 플레이다.
"""
import io

SRC = 'index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'
assert 'tcNearest' not in s, '이미 적용됨'


def one(old, new, what):
    global s
    assert s.count(old) == 1, what + ' — 대상을 못 찾음(또는 여러 개)'
    s = s.replace(old, new, 1)


# ── 1) 경로 진행도(호 길이) 계산 ────────────────────────────────────────────
one("function tcDist(p){",
    NL.join([
        "/* 경로의 누적 길이 — '얼마나 왔는지(진행도)'를 재기 위해 미리 계산해 둔다. */",
        "function tcArcInit(){",
        "  TC.arc=[0];",
        "  for(let i=1;i<TC.path.length;i++)",
        "    TC.arc.push(TC.arc[i-1]+Math.hypot(TC.path[i].x-TC.path[i-1].x, TC.path[i].y-TC.path[i-1].y));",
        "}",
        "/* 점 p에서 가장 가까운 경로 지점을 '거리'와 '진행도'로 함께 돌려준다.",
        "   거리만 보면 나란한 다른 갈래로 건너뛴 것을 구별할 수 없어서 진행도가 필요하다. */",
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
        "}",
        "function tcDist(p){"]),
    'tcNearest 신설')

# ── 2) 이동 구간 전체 검사 + 진행도 검사 ────────────────────────────────────
old_move = NL.join([
    "  area.onpointermove=e=>{ if(!TC.running||!TC.active||!TC.grip)return;",
    "    const p=tcPoint(e);",
    "    const nx=Math.max(0,Math.min(TC.W, TC.cur.x+(p.x-TC.grip.x)));",
    "    const ny=Math.max(0,Math.min(TC.H, TC.cur.y+(p.y-TC.grip.y)));",
    "    TC.grip=p; TC.cur={x:nx,y:ny};",
    "    if(tcDist(TC.cur)>TC.tol){ tcStray(); return; }",
    "    tcAddTrail(TC.cur);",
    "    const en=TC.path[TC.path.length-1];",
    "    if(Math.hypot(nx-en.x,ny-en.y)<=(TC.endR||22)) tcClearLevel(); };"])
new_move = NL.join([
    "  area.onpointermove=e=>{ if(!TC.running||!TC.active||!TC.grip)return;",
    "    const p=tcPoint(e);",
    "    const nx=Math.max(0,Math.min(TC.W, TC.cur.x+(p.x-TC.grip.x)));",
    "    const ny=Math.max(0,Math.min(TC.H, TC.cur.y+(p.y-TC.grip.y)));",
    "    TC.grip=p;",
    "    const from=TC.cur, step=Math.hypot(nx-from.x, ny-from.y);",
    "    /* 이벤트가 오는 지점만 검사하면, 손가락이 빠를 때 그 사이 구간이 통째로",
    "       검사되지 않아 길 밖을 가로질러도 통과한다. 6px 간격으로 잘라 전부 본다. */",
    "    const n=Math.max(1, Math.ceil(step/6)), per=step/n;",
    "    for(let k=1;k<=n;k++){",
    "      const q={ x:from.x+(nx-from.x)*k/n, y:from.y+(ny-from.y)*k/n };",
    "      const near=tcNearest(q);",
    "      if(near.d>TC.tol){ TC.cur=q; tcStray(); return; }",
    "      /* 움직인 거리에 비해 '경로상 진행도'가 훨씬 크게 튀면 = 길을 가로질러",
    "         다른 구간으로 건너뛴 것. 되짚어 오는 것(진행도 감소)은 정상이므로 절댓값으로 본다. */",
    "      if(TC.prog!=null && Math.abs(near.t-TC.prog) > per*1.6+20){ TC.cur=q; tcStray(); return; }",
    "      TC.prog=near.t;",
    "      TC.cur=q; tcAddTrail(q);",
    "    }",
    "    TC.cur={x:nx,y:ny};",
    "    const en=TC.path[TC.path.length-1];",
    "    if(Math.hypot(nx-en.x,ny-en.y)<=(TC.endR||22)) tcClearLevel(); };"])
one(old_move, new_move, 'pointermove 검사')

# ── 3) 시작할 때 진행도 0에서 출발 ──────────────────────────────────────────
one("      TC.cur={x:st.x,y:st.y}; TC.trail=[{x:st.x,y:st.y}];",
    "      TC.cur={x:st.x,y:st.y}; TC.trail=[{x:st.x,y:st.y}]; TC.prog=0;",
    '시작 진행도')

# ── 4) 이탈·클리어·새 판에서 진행도 초기화 ──────────────────────────────────
one("function tcStray(){ if(!TC.active) return; TC.active=false; TC.cur=null; TC.grip=null;",
    "function tcStray(){ if(!TC.active) return; TC.active=false; TC.cur=null; TC.grip=null; TC.prog=null;",
    'tcStray 진행도 초기화')
one("function tcClearLevel(){ TC.active=false; TC.cur=null; TC.grip=null;",
    "function tcClearLevel(){ TC.active=false; TC.cur=null; TC.grip=null; TC.prog=null;",
    'tcClearLevel 진행도 초기화')
one("  TC.active=false; TC.cur=null; TC.grip=null; tcStatus('trace.guide'); }",
    "  TC.active=false; TC.cur=null; TC.grip=null; TC.prog=null; tcStatus('trace.guide'); }",
    'tcRender 진행도 초기화')

# ── 5) 허용 오차에 상한 — 나란한 두 갈래를 동시에 만족할 수 없게 ────────────
one("  TC.tol=w/2+Math.max(4, 12-(TC.level-1)*0.5);",
    NL.join([
        "  /* 허용 오차가 갈래 간격(=칸 크기)의 절반을 넘으면, 나란한 두 갈래의 중간에서도",
        "     양쪽 다 '길 위'로 인정돼 지그재그를 가로질러 질러갈 수 있다. 45%로 막는다. */",
        "  TC.tol=Math.min(w/2+Math.max(4, 12-(TC.level-1)*0.5), TC.cell*0.45);"]),
    '허용 오차 상한')

# ── 6) 경로를 만든 뒤 진행도 표 준비 ────────────────────────────────────────
one("  TC.path=tcGenPath(steps); TC.trail=[];",
    "  TC.path=tcGenPath(steps); TC.trail=[]; tcArcInit();",
    '진행도 표 준비')

# ── 7) 상태 필드 ────────────────────────────────────────────────────────────
one("cur:null, grip:null,",
    "cur:null, grip:null, prog:null, arc:[],",
    'TC 상태 필드')

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — 이동 구간 전수 검사 · 진행도 기반 가로지르기 차단 · 허용 오차 상한')
