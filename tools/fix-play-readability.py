# -*- coding: utf-8 -*-
"""플레이 화면의 읽힘 문제 5가지 — 캡처와 계측에서 나온 것들.

1) 컬러소트 기호가 진한 블록 위에서 묻힘
   새 팔레트는 명도 폭이 넓다(색약 구분을 명도로도 벌렸기 때문). 기호 색을 하나로 두면
   진한 블록에서는 어두운 기호가 안 보인다 → 블록 밝기에 따라 기호 색을 뒤집는다.

2) 틀린 그림 찾기 — 작은 폰에서 아래 판이 잘림
   두 판을 세로로 쌓고 창 높이에 맞춰 칸을 줄이는 처리는 이미 있었지만,
   위아래 고정 영역(헤더·점수·타이머·안내·남은개수 알약·하단 탭)을 338px로 잡은 게
   과소평가였다. 360×640에서 아래 판이 63px 잘렸다(계측). 실측값으로 올린다.

3) 픽셀 로직 힌트 숫자가 10px 미만
   0.6rem = 9.6px. 힌트를 못 읽으면 게임 자체가 성립하지 않는다.

4) 블록 채우기 — 트레이 조각이 판 칸보다 훨씬 작다
   조각 칸이 15px 고정인데 판 칸은 약 42px이라 크기 감각이 안 맞았다.
   (끌기 시작하면 판 배율의 미리보기가 나오므로 심각하진 않다)
   트레이에 실제로 있는 조각들의 총 폭을 보고 남는 공간만큼 키운다.

5) 신기록 색종이가 점수를 덮음
   점수 글자 한가운데서 80개를 터뜨려 1.7~2.8초 동안 '신기록 달성'과 점수가 안 읽혔다.
   축포는 살리되 분사 위치를 점수 좌우로 옮긴다.
"""
import io, re

SRC = 'index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'
assert 'soGlyphInk' not in s, '이미 적용됨'


def one(old, new, what):
    global s
    assert s.count(old) == 1, what + ' — 대상을 못 찾음(또는 여러 개)'
    s = s.replace(old, new, 1)


# ── 1) 컬러소트 기호 대비 ────────────────────────────────────────────────────
one("const SO_GLYPH=",
    NL.join([
        "/* 팔레트의 명도 폭이 넓어서 기호 색을 하나로 두면 진한 블록에서 묻힌다.",
        "   블록의 상대휘도를 재서 밝으면 어두운 기호, 어두우면 흰 기호를 쓴다. */",
        "function soGlyphInk(hex){",
        "  const v=i=>{ let c=parseInt(hex.slice(i,i+2),16)/255; return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4); };",
        "  const L=0.2126*v(1)+0.7152*v(3)+0.0722*v(5);",
        "  return L>0.42 ? 'rgba(20,16,45,.5)' : 'rgba(255,255,255,.82)';",
        "}",
        "const SO_GLYPH="]),
    '컬러소트 기호 잉크')

one("      u.textContent=SO_GLYPH[c];   // 색약 대비 — 색과 별개인 확실한 단서",
    "      u.textContent=SO_GLYPH[c];   // 색약 대비 — 색과 별개인 확실한 단서" + NL +
    "      u.style.color=soGlyphInk(SO_COLORS[c]);",
    '컬러소트 기호 색 적용')

# ── 2) 틀린 그림 찾기 여유값 ────────────────────────────────────────────────
one("const availW=328, availH=Math.max(200,(window.innerHeight||760)-338);",
    NL.join([
        "  /* 위아래 고정 영역의 실측 합계. 338이면 세로 640px 기기에서 아래 판이 63px 잘렸다.",
        "     (헤더 128 + 점수칸 · 타이머 · 안내문 · 남은개수 알약 + 하단 탭 90) */",
        "  const availW=328, availH=Math.max(180,(window.innerHeight||760)-404);"]),
    '틀린그림 여유값')

# ── 3) 픽셀 로직 힌트 크기 ──────────────────────────────────────────────────
one(".no-clue{background:var(--bg3);font-size:.6rem;",
    ".no-clue{background:var(--bg3);font-size:.72rem;",   # 9.6px → 11.5px
    '픽셀로직 힌트 글자')

# ── 4) 블록 채우기 트레이 조각 크기 ─────────────────────────────────────────
one("  FT.tray.forEach((item,idx)=>{ const b=ftBounds(item.p); const pc=document.createElement('div');",
    NL.join([
        "  /* 조각 칸을 15px로 고정하면 판 칸(약 42px)과 크기 감각이 어긋난다.",
        "     트레이에 실제로 놓일 조각들의 총 가로 칸 수를 세서 남는 폭만큼 키운다. */",
        "  const trayCols=FT.tray.reduce((a,it)=>a+ftBounds(it.p).mc+1,0)||1;",
        "  const tcs=Math.max(15, Math.min(26, Math.floor(268/trayCols)));",
        "  FT.tray.forEach((item,idx)=>{ const b=ftBounds(item.p); const pc=document.createElement('div');"]),
    '블록 트레이 크기 계산')

one("    pc.style.gridTemplateColumns='repeat('+(b.mc+1)+',15px)';",
    "    pc.style.gridTemplateColumns='repeat('+(b.mc+1)+','+tcs+'px)';",
    '블록 트레이 열 폭')

one("    for(let r=0;r<=b.mr;r++)for(let c=0;c<=b.mc;c++){ const d=document.createElement('div'); d.className='ft-pcell'+(set.has(r+'_'+c)?' on':''); pc.appendChild(d); }",
    "    for(let r=0;r<=b.mr;r++)for(let c=0;c<=b.mc;c++){ const d=document.createElement('div'); d.className='ft-pcell'+(set.has(r+'_'+c)?' on':'');"
    " d.style.width=tcs+'px'; d.style.height=tcs+'px'; pc.appendChild(d); }",
    '블록 트레이 칸 크기')

# ── 5) 신기록 색종이 ────────────────────────────────────────────────────────
one("    fxConfetti(cx,cy,{count:80,power:180,arc:2.6});",
    NL.join([
        "    /* 점수 글자 위에서 터뜨리면 축하 문구와 점수가 1.7~2.8초 동안 가려진다.",
        "       분사 위치를 점수 좌우 바깥으로 옮겨 글자가 계속 읽히게 한다. */",
        "    fxConfetti(cx-w*0.75, cy, {count:40,power:190,arc:1.5,ang:-Math.PI/2-0.5});",
        "    fxConfetti(cx+w*0.75, cy, {count:40,power:190,arc:1.5,ang:-Math.PI/2+0.5});"]),
    '신기록 색종이 분사 위치')

one("  const blast=()=>{ if(!scoreEl.offsetParent) return; const {cx,cy}=center();",
    "  const blast=()=>{ if(!scoreEl.offsetParent) return; const {cx,cy,w}=center();",
    '신기록 색종이 폭 변수')

one("    fxBurst(cx,cy,{count:22,spread:80}); };",
    "    fxBurst(cx,cy,{count:12,spread:110}); };",
    '신기록 반짝임 밀도')

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — 5건 적용')
