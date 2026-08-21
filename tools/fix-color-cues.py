# -*- coding: utf-8 -*-
"""색으로만 구분하던 두 게임을 고친다 — 컬러소트와 길 따라가기.

■ 컬러소트
문제(측정): 8색이 색상만으로 구분됐고, 적록색약 2형으로 시뮬레이션하면 최소 색차가
      CIEDE2000 1.6까지 떨어졌다(파랑-보라). 쉬움 난이도(앞 4색)에도 핑크-초록 5.2가
      들어 있어 색약인 사람은 쉬움조차 풀 수 없었다. 정상 시야에서도 핑크-살구가 11.5로 위험.
해결: (1) 팔레트를 앱의 파스텔 범위(S 42~72 · L 56~84) 안에서 다시 탐색해
          정상/2형/1형 세 조건의 최소 색차를 최대화했다 → 쉬움 24.2 · 보통 16.2 · 어려움 16.0.
      (2) 그래도 파스텔 범위에서 8색을 색만으로 완전히 가르는 건 원리상 불가능하므로
          (색약에서는 적-녹 축이 통째로 무너진다) 블록마다 모양 기호를 얹어
          색과 무관하게 100% 구분되게 했다. 색은 보조 단서로 남는다.
      탐색: .logs/palette_search.mjs · 순서: .logs/palette_order.mjs

■ 길 따라가기
문제(측정): 길 테두리가 배경 대비 1.40:1, 길 안쪽이 1.01:1 — WCAG의 UI 요소 최소 3:1에
      한참 못 미쳐 길이 사실상 안 보였다.
해결: 테두리를 3:1을 넘기는 가장 부드러운 값(#7680a7, 3.42:1)으로 올리고
      안쪽은 흰색으로 빼서 '길'이 형태로 읽히게 한다.
"""
import io, re

SRC = 'index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'
assert 'SO_GLYPH' not in s, '이미 적용됨'

# ── 1) 팔레트 교체 + 모양 기호 ───────────────────────────────────────────────
old_pal = "const SO_COLORS=['#ff9eb5','#ffb877','#ffe07a','#8fd9a8','#6fd6d0','#7fb3ff','#b79bf5','#f08080'];"
assert s.count(old_pal) == 1, '컬러소트 팔레트를 못 찾음'
new_pal = NL.join([
    "/* 색약(2형·1형) 시뮬레이션까지 넣고 탐색한 팔레트 — 난이도가 앞에서부터 4·6·8색을 쓰므로",
    "   적은 색으로 하는 판일수록 더 벌어지도록 순서까지 골랐다(쉬움 24.2·보통 16.2·어려움 16.0). */",
    "const SO_COLORS=['#4d4ad5','#d6f0bc','#98bfe7','#db5861','#ddc743','#d5589a','#b5f3ec','#e397a6'];",
    "/* 색과 1:1로 붙는 모양 — 색을 전혀 구분하지 못해도 이것만으로 풀 수 있어야 한다. */",
    "const SO_GLYPH=['\\u25cf','\\u25b2','\\u25a0','\\u25c6','\\u2605','\\u271a','\\u25bc','\\u2715'];",
])
s = s.replace(old_pal, new_pal, 1)

# 블록을 그릴 때 기호도 같이 넣는다
old_unit = "      u.style.background=SO_COLORS[c];"
assert s.count(old_unit) == 1, '컬러소트 블록 렌더를 못 찾음'
s = s.replace(old_unit,
              "      u.style.background=SO_COLORS[c];" + NL +
              "      u.textContent=SO_GLYPH[c];   // 색약 대비 — 색과 별개인 확실한 단서", 1)

# 기호가 보이도록 블록 스타일 보강 (색을 가리지 않게 반투명 검정)
old_css = ".so-unit{width:100%;height:36px;border-radius:8px}"
assert s.count(old_css) == 1
s = s.replace(old_css,
              ".so-unit{width:100%;height:36px;border-radius:8px;display:flex;align-items:center;"
              "justify-content:center;font-size:.82rem;line-height:1;color:rgba(20,16,45,.42);"
              "font-family:'Segoe UI Symbol','Apple Color Emoji',sans-serif}", 1)

# ── 2) 길 따라가기 대비 ─────────────────────────────────────────────────────
old_stroke = 'stroke="#c7cde0" stroke-width="\'+w+\'"'
assert s.count(old_stroke) == 1, '길 테두리 stroke를 못 찾음'
s = s.replace(old_stroke, 'stroke="#7680a7" stroke-width="\'+w+\'"', 1)   # 배경 대비 3.42:1

old_inner = 'stroke="#f0f2f9" stroke-width="\'+Math.max(2,w-7)+\'"'
assert s.count(old_inner) == 1, '길 안쪽 stroke를 못 찾음'
s = s.replace(old_inner, 'stroke="#ffffff" stroke-width="\'+Math.max(2,w-7)+\'"', 1)

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — 컬러소트 팔레트+기호, 길 따라가기 대비 1.40:1 → 3.42:1')
