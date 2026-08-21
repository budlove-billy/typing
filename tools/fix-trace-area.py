# -*- coding: utf-8 -*-
"""길 따라가기 — 그리기 영역을 제대로 쓰고, 길 폭이 난이도를 따라가게 한다.

■ 좌표 환산이 밀려 있던 버그 (사용자 관찰: "가장자리를 눌러도 이탈로 안 잡힌다")
   SVG viewBox가 340×300으로 고정인데 `.tc-area`의 실제 비율은 그때그때 달랐다.
   `preserveAspectRatio="xMidYMid meet"`라 SVG는 여백을 두고 축소돼 그려지는데,
   tcPoint()는 영역 사각형이 viewBox와 1:1이라고 보고 환산했다. 그만큼(세로로 5~10px)
   판정 좌표가 그림과 어긋나 있었다.
   고침: viewBox를 영역의 '실제 픽셀 크기'로 맞춘다. 그러면 letterbox가 사라져
        환산이 정확해지고, 덤으로 그림이 영역을 꽉 채운다.

■ 영역이 작다
   `max-width:360px` · 높이 300px 고정이라 PC에서 카드 안이 텅 비었다.
   화면 폭에 따라 최대 560px까지 늘리고, 높이도 남는 세로 공간에 맞춘다.

■ 길이 영역을 안 채운다
   랜덤 워크를 한 번 만들어 그대로 썼다. 워크의 가로세로 비가 영역과 다르면
   한쪽이 통째로 남는다(첨부 화면이 그 경우). 후보를 여러 개 만들어
   영역 비율에 가장 가까운 것을 고른다.

■ 길 폭이 난이도를 안 따라간다
   폭을 레벨에서 직접 빼서 12px 바닥에 금방 닿았다. 대신 **칸 크기에서 폭을 유도**한다.
   초반은 칸이 크니 길이 넓고, 레벨이 오르면 칸이 촘촘해져 길이 저절로 좁아진다.
   판이 뭉개지지 않는 것도 같은 규칙으로 보장된다(폭 < 칸 크기).
"""
import io

SRC = 'index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'
assert 'tcFitArea' not in s, '이미 적용됨'


def one(old, new, what):
    global s
    assert s.count(old) == 1, what + ' — 대상을 못 찾음(또는 여러 개)'
    s = s.replace(old, new, 1)


# ── 1) 영역을 넓힌다 ────────────────────────────────────────────────────────
one(".tc-area{position:relative;width:100%;max-width:360px;",
    ".tc-area{position:relative;width:100%;max-width:560px;",
    'tc-area 최대 폭')

# ── 2) 난이도별 '길 폭 상한'을 넉넉히 — 실제 폭은 칸 크기에서 유도한다 ──────
one("const TC_CFG={ easy:{steps:7,w:32}, normal:{steps:12,w:24}, hard:{steps:17,w:19} };",
    NL.join([
        "/* w = 길 폭의 '상한'. 실제 폭은 칸 크기의 62%로 잡되 이 값을 넘지 않는다.",
        "   → 초반엔 칸이 커서 길이 넓고, 레벨이 오르면 칸이 촘촘해져 저절로 좁아진다. */",
        "const TC_CFG={ easy:{steps:5,w:54}, normal:{steps:9,w:46}, hard:{steps:13,w:38} };"]),
    'TC_CFG 폭 상한')

# ── 3) 영역 실측 → viewBox를 실제 픽셀에 맞춘다 ─────────────────────────────
one("function tcWalk(steps){",
    NL.join([
        "/* 그리기 영역의 실제 크기를 재서 viewBox 좌표계로 삼는다.",
        "   예전엔 viewBox가 340×300 고정이라 영역 비율과 어긋나 letterbox가 생겼고,",
        "   tcPoint()의 환산이 그만큼 밀려 길 가장자리 판정이 그림과 달랐다. */",
        "function tcFitArea(){",
        "  const area=document.getElementById('tc-area'); if(!area) return;",
        "  const w=Math.max(240, Math.round(area.clientWidth||328));",
        "  const h=Math.max(260, Math.min(Math.round(w*0.92), (window.innerHeight||760)-420));",
        "  TC.W=w; TC.H=h; area.style.height=h+'px';",
        "}",
        "function tcBBox(pts){ let minr=pts[0][0],maxr=pts[0][0],minc=pts[0][1],maxc=pts[0][1];",
        "  pts.forEach(p=>{ if(p[0]<minr)minr=p[0]; if(p[0]>maxr)maxr=p[0];",
        "                   if(p[1]<minc)minc=p[1]; if(p[1]>maxc)maxc=p[1]; });",
        "  return {minr,minc,rows:maxr-minr,cols:maxc-minc}; }",
        "function tcWalk(steps){"]),
    'tcFitArea 신설')

# ── 4) 영역 비율에 맞는 워크를 골라 꽉 채운다 ───────────────────────────────
old_gen_start = "function tcGenPath(steps){ let pts,tr=0; do{ pts=tcWalk(steps); tr++; }while(pts.length-1<Math.max(4,Math.floor(steps*0.65))&&tr<25);"
i = s.index(old_gen_start)
j = s.index('function segDist(', i)
new_gen = NL.join([
    "/* 후보를 여러 개 만들어 '그리기 영역의 가로세로 비'에 가장 가까운 워크를 고른다.",
    "   예전엔 첫 워크를 그대로 써서, 워크가 세로로 길면 가로가 통째로 비었다. */",
    "function tcGenPath(steps){",
    "  const m=TC.MARGIN, availW=Math.max(40,TC.W-2*m), availH=Math.max(40,TC.H-2*m);",
    "  const minLen=Math.max(4,Math.floor(steps*0.6));",
    "  let best=null, any=null;",
    "  for(let k=0;k<24;k++){",
    "    const pts=tcWalk(steps); const b=tcBBox(pts);",
    "    if(!any) any={pts,b};",
    "    if(pts.length-1<minLen || b.rows<1 || b.cols<1) continue;",
    "    const a=(b.cols/availW)/(b.rows/availH);       // 1이면 영역 비율과 정확히 일치",
    "    const sc=Math.min(a,1/a)*1000 + (pts.length-1);  // 비율 우선, 같으면 더 긴 경로",
    "    if(!best||sc>best.sc) best={sc,pts,b};",
    "  }",
    "  if(!best) best=any;",
    "  const b=best.b;",
    "  const cell=Math.min(availW/Math.max(1,b.cols), availH/Math.max(1,b.rows));",
    "  TC.cell=cell;",
    "  const offx=(availW-b.cols*cell)/2, offy=(availH-b.rows*cell)/2;",
    "  return best.pts.map(p=>({ x:m+offx+(p[1]-b.minc)*cell, y:m+offy+(p[0]-b.minr)*cell }));",
    "}",
    ""])
s = s[:i] + new_gen + s[j:]

# ── 5) 렌더 — 폭을 칸 크기에서 유도, 시작/끝 점과 커서도 같이 키운다 ────────
old_render_start = "function tcRender(){ const cfg=TC_CFG[TC.diff]; const steps=cfg.steps+(TC.level-1)*2; const w=Math.max(12, cfg.w-(TC.level-1)*1.2);"
i = s.index(old_render_start)
j = s.index("function tcResetTrail(", i)
new_render = NL.join([
    "function tcRender(){",
    "  const cfg=TC_CFG[TC.diff];",
    "  /* 길이는 계속 늘되 상한을 둔다 — 무한히 늘리면 칸이 작아져 굽이가 뭉개진다. */",
    "  const steps=Math.min(cfg.steps+(TC.level-1)*2, 44);",
    "  TC.MARGIN=Math.round(cfg.w*0.5+10);",
    "  tcFitArea();",
    "  TC.path=tcGenPath(steps); TC.trail=[];",
    "  /* 길 폭은 칸 크기에서 나온다 — 초반엔 칸이 커서 넓고, 레벨이 오르면 촘촘해져 좁아진다.",
    "     폭이 칸보다 커질 수 없으므로 굽이가 서로 뭉개지지도 않는다. */",
    "  /* 폭은 레벨이 정한다(단조 감소). 칸 크기는 상한으로만 써서 굽이가 뭉개지는 것만 막는다. */",
    "  const w=Math.max(11, Math.min(cfg.w-(TC.level-1)*1.6, Math.round(TC.cell*0.68)));",
    "  TC.tol=w/2+Math.max(4, 12-(TC.level-1)*0.5);",
    "  const d='M'+TC.path.map(p=>p.x.toFixed(1)+' '+p.y.toFixed(1)).join(' L');",
    "  const st=TC.path[0], en=TC.path[TC.path.length-1];",
    "  const tw=Math.max(5,Math.min(16,w*0.45)), cr=Math.max(7,Math.min(18,w*0.42));",
    "  const dot=Math.max(9,Math.min(20,w*0.42));",
    "  TC.startR=Math.max(24,dot*1.9); TC.endR=Math.max(20,dot*1.6);",
    "  const area=document.getElementById('tc-area');",
    "  area.innerHTML='<svg viewBox=\"0 0 '+TC.W+' '+TC.H+'\" preserveAspectRatio=\"none\">'",
    "    +'<path d=\"'+d+'\" fill=\"none\" stroke=\"#7680a7\" stroke-width=\"'+w+'\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>'",
    "    +'<path d=\"'+d+'\" fill=\"none\" stroke=\"#ffffff\" stroke-width=\"'+Math.max(2,w-7)+'\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>'",
    "    +'<polyline id=\"tc-trail\" fill=\"none\" stroke=\"#4f7cff\" stroke-width=\"'+tw+'\" stroke-linecap=\"round\" stroke-linejoin=\"round\" points=\"\"/>'",
    "    +'<circle cx=\"'+st.x.toFixed(1)+'\" cy=\"'+st.y.toFixed(1)+'\" r=\"'+dot+'\" fill=\"#21a67a\"/>'",
    "    +'<circle cx=\"'+en.x.toFixed(1)+'\" cy=\"'+en.y.toFixed(1)+'\" r=\"'+dot+'\" fill=\"#e0475a\"/>'",
    "    +'<circle id=\"tc-cursor\" r=\"'+cr+'\" fill=\"#4f7cff\" opacity=\"0\"/></svg>';",
    "  TC.active=false; tcStatus('trace.guide'); }",
    ""])
s = s[:i] + new_render + s[j:]

# ── 6) 시작/끝 판정 반경도 칸 크기를 따라간다 ───────────────────────────────
one("if(Math.hypot(p.x-s.x,p.y-s.y)<=28){",
    "if(Math.hypot(p.x-s.x,p.y-s.y)<=(TC.startR||28)){",
    '시작점 판정 반경')
one("if(Math.hypot(p.x-en.x,p.y-en.y)<=22){",
    "if(Math.hypot(p.x-en.x,p.y-en.y)<=(TC.endR||22)){",
    '끝점 판정 반경')

# ── 7) 상태에 새 필드 + 화면 회전/크기 변경 대응 ────────────────────────────
one("const TC={ diff:'normal', score:0, lives:3, level:1, running:false, active:false, path:[], tol:20, W:340, H:300,",
    "const TC={ diff:'normal', score:0, lives:3, level:1, running:false, active:false, path:[], tol:20, W:340, H:300, MARGIN:33, cell:40, startR:28, endR:22,",
    'TC 상태 필드')

one("function startTrace(){ TC.score=0;TC.lives=3;TC.level=1;TC.running=true;TC.active=false;",
    NL.join([
        "/* 화면 크기가 바뀌면(회전 등) 좌표계도 바뀌어야 한다. 그리는 중에는 건드리지 않는다. */",
        "let _tcResizeT=null;",
        "window.addEventListener('resize',()=>{ if(!TC.running||TC.active) return;",
        "  clearTimeout(_tcResizeT); _tcResizeT=setTimeout(()=>{ if(TC.running&&!TC.active) tcRender(); },160); });",
        "function startTrace(){ TC.score=0;TC.lives=3;TC.level=1;TC.running=true;TC.active=false;"]),
    'trace 리사이즈 대응')

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — 좌표 환산 · 영역 확대 · 채움 · 폭 램프')
