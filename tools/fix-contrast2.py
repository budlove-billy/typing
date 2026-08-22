# -*- coding: utf-8 -*-
"""대비 교정 2차 — 1차에서 덜 잡힌 것들을 실제 계산된 색(.logs/probe_colors.mjs)으로 정확히 고친다.

1차에서 놓친 이유
  - 글자색을 '밝기 임계값'으로 골랐더니 경계에 걸린 색(초록·노랑)이 잘못 선택됐다.
    → 임계값 대신 **흰 글자와 진한 글자의 대비를 실제로 계산해 큰 쪽**을 쓴다. 경계가 없어진다.
  - 반투명 잉크(rgba)는 배경과 섞여서 실제 대비가 계산과 다르다.
    → 불투명 색으로 바꾼다. 보이는 대로 계산되고 검사도 정확해진다.

나머지는 실측값 그대로 교정:
  나가기 버튼 #e0475a on #fff2f5 3.69 · 틀린그림 '원본' 태그 흰글자 on #4f7cff 3.71
  '다른 곳 찾기' 태그 4.24 · 남은 개수 #5a6683 on #eef1f7 4.10
  규칙 바꾸기의 '크기' 배너 #178a63 on #daf3ea 3.71
"""
import io

SRC = 'index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'
assert 'pickInk' not in s, '이미 적용됨'


def one(old, new, what):
    global s
    assert s.count(old) == 1, what + ' — 대상을 못 찾음(또는 여러 개)'
    s = s.replace(old, new, 1)


# ── 1) 배경색 위 글자색을 '대비가 큰 쪽'으로 고르는 공용 함수 ───────────────
one("/* 선택 버튼의 글자색 — 배경이 색이라 흰 글자로 고정하면 노랑·주황에서 안 읽힌다.",
    NL.join([
        "/* 배경색 위에 올릴 글자색을 고른다 — 흰 글자와 진한 글자 중 **대비가 실제로 큰 쪽**.",
        "   밝기 임계값으로 가르면 경계에 걸친 색(초록 0.269 · 노랑 0.292)에서 잘못 고른다. */",
        "function _relLum(hex){ const v=i=>{ let c=parseInt(hex.slice(i,i+2),16)/255;",
        "    return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4); };",
        "  return 0.2126*v(1)+0.7152*v(3)+0.0722*v(5); }",
        "function pickInk(hex){",
        "  const L=_relLum(hex);",
        "  const onWhite=(1.05)/(L+0.05), onDark=(L+0.05)/(_relLum('#14102d')+0.05);",
        "  return onWhite>=onDark ? '#ffffff' : '#14102d';",
        "}",
        "/* 선택 버튼의 글자색 — 배경이 색이라 흰 글자로 고정하면 노랑·주황에서 안 읽힌다."]),
    'pickInk 공용 함수')

one(NL.join([
    "function stOptInk(hex){",
    "  const v=i=>{ let c=parseInt(hex.slice(i,i+2),16)/255; return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4); };",
    "  const L=0.2126*v(1)+0.7152*v(3)+0.0722*v(5);",
    "  return L>0.30 ? {c:'#1a1a28', sh:'none'} : {c:'#ffffff', sh:'0 1px 2px rgba(0,0,0,.28)'};",
    "}"]),
    NL.join([
        "function stOptInk(hex){ const c=pickInk(hex);",
        "  return {c:c, sh:(c==='#ffffff')?'0 1px 2px rgba(0,0,0,.28)':'none'}; }"]),
    '스트룹 버튼 잉크')

one("  return L>0.42 ? 'rgba(20,16,45,.68)' : 'rgba(255,255,255,.92)';"
    "   /* 색약 대비용 기호인데 정작 기호가 3.7:1이었다 */",
    "  return pickInk(hex);   /* 반투명이면 배경과 섞여 실제 대비가 달라진다 — 불투명으로 */",
    '컬러소트 기호 잉크')
# soGlyphInk 안의 자체 휘도 계산은 이제 필요 없다
one(NL.join([
    "function soGlyphInk(hex){",
    "  const v=i=>{ let c=parseInt(hex.slice(i,i+2),16)/255; return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4); };",
    "  const L=0.2126*v(1)+0.7152*v(3)+0.0722*v(5);",
    "  return pickInk(hex);   /* 반투명이면 배경과 섞여 실제 대비가 달라진다 — 불투명으로 */",
    "}"]),
    NL.join([
    "function soGlyphInk(hex){",
    "  return pickInk(hex);   /* 반투명이면 배경과 섞여 실제 대비가 달라진다 — 불투명으로 */",
    "}"]),
    '컬러소트 잉크 정리')

# ── 2) 나가기 버튼 ──────────────────────────────────────────────────────────
one('button[onclick^="leave"]{min-height:44px;padding:.6rem 1.4rem;font-size:.92rem;font-weight:700;color:#e0475a;background:#fff2f5;',
    'button[onclick^="leave"]{min-height:44px;padding:.6rem 1.4rem;font-size:.92rem;font-weight:700;color:#c62035;background:#fff2f5;',
    '나가기 버튼 글자색')

# ── 3) 틀린 그림 찾기 ───────────────────────────────────────────────────────
one(".df-tag.t1{background:#4f7cff}", ".df-tag.t1{background:#3367ff}   /* 흰 글자 3.71:1 → 4.64:1 */", '원본 태그')
one(".df-tag.t2{background:#b8661d}   /* 흰 글자 대비 2.67:1 → 4.6:1 */",
    ".df-tag.t2{background:#a85d15}   /* 흰 글자 2.67:1 → 4.7:1 */", '다른곳 태그')
one(".df-count{display:inline-flex;align-items:center;gap:.45rem;font-size:.92rem;font-weight:800;color:var(--text2);",
    ".df-count{display:inline-flex;align-items:center;gap:.45rem;font-size:.92rem;font-weight:800;color:var(--text);",
    '남은 개수 글자색')
one("'<span style=\"color:#8e99b8\">○</span>'",
    "'<span style=\"color:#7b87a8\">○</span>'", '남은 개수 표시')

# ── 4) 규칙 바꾸기 — '크기' 배너 ────────────────────────────────────────────
one(".sw-rule.mag{background:var(--teal3);color:var(--teal2)}",
    ".sw-rule.mag{background:var(--teal3);color:#0f6e4e}   /* #178a63 on #daf3ea 는 3.71:1 */",
    '규칙 배너')

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — 잉크 선택을 대비 비교로 · 나가기/태그/배너 색')
