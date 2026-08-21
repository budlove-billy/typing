# -*- coding: utf-8 -*-
"""말로우 크라운 — 왕관을 앱 그림체로 새로 그리고 크게, 말로우에게도 왕관을 씌운다.

■ 왕관이 작다 (측정)
   칸이 모바일 44px · PC 55px인데 이모지 글자 크기는 min(7vw,26px)로 고정이라
   칸의 48~59%만 채웠다. 칸 한가운데 작게 떠 있는 것처럼 보인다.
   → 전용 SVG로 바꾸고 칸의 82%를 채우게 한다. 칸이 커지면 왕관도 같이 커진다.

■ 이모지라서 생기는 문제
   👑는 기기마다 모양·색이 다르게 그려진다(안드로이드·iOS·윈도우가 전부 다르다).
   앱의 파스텔 그림체와도 겉돈다.
   → 직접 그린다. 구역 색이 연노랑(#f7e2a8)·연살구(#f7c9a8)인 칸에서도 읽히도록
     외곽선을 진한 호박색(#8C5A12)으로 두른다. 칸 색 8종 어디에 놓여도 형태가 산다.

■ 말로우에게 왕관 씌우기
   헤더 마스코트는 별 두 개만 달고 있었다. 크라운 게임이니 왕관을 씌우고,
   30px로 줄어들어도 형태가 뭉개지지 않게 별은 뺀다(둘 다 두면 지저분하다).

공유 카드의 왕관도 같은 모양으로 그린다 — 화면과 공유 이미지의 왕관이 달라 보이면 안 된다.
"""
import io

SRC = 'queens/index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'
assert 'CROWN_SVG' not in s, '이미 적용됨'


def one(old, new, what):
    global s
    assert s.count(old) == 1, what + ' — 대상을 못 찾음(또는 여러 개)'
    s = s.replace(old, new, 1)


# 왕관 — 그라디언트를 쓰지 않는다. 칸마다 SVG가 하나씩 들어가는데 defs의 id가 중복되면
# 브라우저마다 처리가 달라진다. 단색 두 톤 + 진한 외곽선으로 충분히 읽힌다.
CROWN = ('<svg class="cr" viewBox="0 0 100 92" aria-hidden="true">'
         '<path d="M13 60 L13 30 L33 44 L50 18 L67 44 L87 30 L87 60 Z" fill="#F9C74F" '
         'stroke="#8C5A12" stroke-width="6" stroke-linejoin="round"/>'
         '<rect x="10" y="57" width="80" height="21" rx="10.5" fill="#FFE08A" '
         'stroke="#8C5A12" stroke-width="6"/>'
         '<circle cx="13" cy="27" r="7.5" fill="#E8557F" stroke="#8C5A12" stroke-width="3"/>'
         '<circle cx="50" cy="15" r="8.5" fill="#E8557F" stroke="#8C5A12" stroke-width="3"/>'
         '<circle cx="87" cy="27" r="7.5" fill="#E8557F" stroke="#8C5A12" stroke-width="3"/>'
         '<circle cx="50" cy="68" r="6" fill="#FFF6DC"/></svg>')

# ── 1) 왕관 SVG 상수 + 칸 렌더 교체 ────────────────────────────────────────
one("const MHEAD_SVG=",
    NL.join([
        "/* 칸에 놓이는 왕관 — 이모지는 기기마다 모양이 달라 앱 그림체와 겉돌아서 직접 그린다.",
        "   구역 색이 연노랑·연살구인 칸에서도 읽히도록 외곽선을 진하게 둘렀다. */",
        "const CROWN_SVG='" + CROWN + "';",
        "const MHEAD_SVG="]),
    '왕관 SVG 상수')

one("    d.innerHTML = s===2?'👑':(s===1?'<span class=\"x\">✕</span>':'');",
    "    d.innerHTML = s===2?CROWN_SVG:(s===1?'<span class=\"x\">✕</span>':'');",
    '칸 렌더')

# ── 2) 칸의 82%를 채우게 ───────────────────────────────────────────────────
one(".cell:active{transform:scale(.93);}",
    NL.join([
        ".cell:active{transform:scale(.93);}",
        "/* 이모지는 글자 크기가 고정이라 칸의 절반밖에 못 채웠다. SVG라 칸을 따라 커진다. */",
        ".cell .cr{width:82%;height:auto;display:block;filter:drop-shadow(0 1px 1px rgba(60,40,10,.18));}"]),
    '왕관 크기 스타일')

# ── 3) 말로우에게 왕관 — 별 두 개를 왕관으로 바꾼다 ────────────────────────
stars = ('<path d="M24 17 L26 22 L31 24 L26 26 L24 31 L22 26 L17 24 L22 22 Z" fill="#FFC94D"/>'
         '<path d="M77 19 L79 24 L84 26 L79 28 L77 33 L75 28 L70 26 L75 24 Z" fill="#FFC94D"/>')
crown_head = ('<path d="M30 23 L30 7 L40 15 L50 2 L60 15 L70 7 L70 23 Z" fill="#F9C74F" '
              'stroke="#8C5A12" stroke-width="3.4" stroke-linejoin="round"/>'
              '<circle cx="50" cy="2" r="3.6" fill="#E8557F"/>')
one(stars, crown_head, '말로우 왕관')

# 왕관이 머리 위로 올라가므로 머리 자체를 조금 내린다(30px에서도 잘리지 않게)
one('<rect x="15" y="19" width="70" height="63" rx="29" fill="url(#mh)"',
    '<rect x="15" y="22" width="70" height="60" rx="28" fill="url(#mh)"',
    '말로우 머리 위치')

# ── 4) 공유 카드도 같은 왕관으로 ───────────────────────────────────────────
one("function drawCard(t){",
    NL.join([
        "/* 공유 카드의 왕관 — 화면과 같은 모양이어야 한다(이모지로 두면 기기마다 다르게 나온다). */",
        "function drawCrown(c,cx,cy,size){",
        "  const k=size/100, X=v=>cx+(v-50)*k, Y=v=>cy+(v-44)*k;",
        "  c.save(); c.lineJoin='round'; c.lineCap='round'; c.strokeStyle='#8C5A12';",
        "  c.lineWidth=6*k;",
        "  c.beginPath(); c.moveTo(X(13),Y(60)); c.lineTo(X(13),Y(30)); c.lineTo(X(33),Y(44));",
        "  c.lineTo(X(50),Y(18)); c.lineTo(X(67),Y(44)); c.lineTo(X(87),Y(30)); c.lineTo(X(87),Y(60));",
        "  c.closePath(); c.fillStyle='#F9C74F'; c.fill(); c.stroke();",
        "  roundRect(c,X(10),Y(57),80*k,21*k,10.5*k); c.fillStyle='#FFE08A'; c.fill(); c.stroke();",
        "  c.lineWidth=3*k;",
        "  [[13,27,7.5],[50,15,8.5],[87,27,7.5]].forEach(j=>{ c.beginPath();",
        "    c.arc(X(j[0]),Y(j[1]),j[2]*k,0,Math.PI*2); c.fillStyle='#E8557F'; c.fill(); c.stroke(); });",
        "  c.beginPath(); c.arc(X(50),Y(68),6*k,0,Math.PI*2); c.fillStyle='#FFF6DC'; c.fill();",
        "  c.restore();",
        "}",
        "function drawCard(t){"]),
    '공유카드 왕관 함수')

one("    if(ST[r][cc]===2){ c.font=Math.floor(cell*0.62)+'px sans-serif'; c.fillStyle='#2a2140'; "
    "c.textBaseline='middle'; c.fillText('👑',x+cell/2,y+cell/2+2); c.textBaseline='alphabetic'; }",
    "    if(ST[r][cc]===2) drawCrown(c, x+cell/2, y+cell/2, cell*0.82);",
    '공유카드 칸 왕관')

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — 칸 왕관 SVG(82%) · 말로우 왕관 · 공유카드')
