# -*- coding: utf-8 -*-
"""글자 대비 미달 교정 — .logs/design_audit3.mjs 로 34게임을 전수 계측해 나온 것들.

대체 색은 눈대중이 아니라 계산으로 골랐다(.logs/fix_colors.mjs):
색상(H)은 그대로 두고 명도만 낮춰 가며 기준(WCAG 본문 4.5:1 · 큰 글자 3:1)을 처음 넘는 값.

■ 색깔 맞추기 — 게임의 정답 단서 자체가 안 읽혔다
   큰 글자: 노랑 2.20:1 · 주황 2.80:1 (큰 글자 기준 3:1 미달). 나머지 4색은 통과.
     → 두 색만 명도를 조금 낮춘다. 정답 판단은 '아래 선택 버튼과 같은 색 고르기'라
       색 이름의 미묘한 어감보다 서로 구별되는 것이 중요하므로 안전한 교정이다.
   선택 버튼: 배경이 색인데 글자가 늘 흰색이라 노랑 2.20 · 주황 2.80 · 초록 3.29였다.
     → 배경 밝기에 따라 흰 글자/진한 글자를 고른다(컬러소트 기호와 같은 방식).
       노랑 7.81 · 주황 6.14 · 초록 5.21로 올라간다.

■ 틀린 그림 찾기
   '다른 곳 찾기' 태그가 흰 글자에 밝은 주황 배경이라 2.67:1.
   아직 못 찾은 개수 표시(○)가 1.36:1 — 남은 개수가 몇 개인지 사실상 안 보였다.

■ 모든 게임 공통 (한 곳만 고치면 34게임에 적용)
   게임 제목과 화면 안내문(.gm-status)이 3.71:1. 안내문은 지금 뭘 해야 하는지 알려주는
   글이라 가장 잘 읽혀야 한다. 강조색을 조금 진하게 한다 — 배경으로 쓰이는 자리에서는
   흰 글자와의 대비가 오히려 좋아지므로 손해가 없다.
   점수 라벨(SCORE/COMBO/LEVEL) 3.96:1, 헤더 나가기 3.48:1도 같이.

■ 컬러소트 기호
   색약 대비용으로 넣은 기호인데 정작 기호 자체가 3.69~3.76:1이었다. 잉크를 진하게.
"""
import io

SRC = 'index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'
assert 'stOptInk' not in s, '이미 적용됨'


def one(old, new, what):
    global s
    assert s.count(old) == 1, what + ' — 대상을 못 찾음(또는 여러 개)'
    s = s.replace(old, new, 1)


# ── 1) 색깔 맞추기 ──────────────────────────────────────────────────────────
one("  {key:'yellow',hex:'#e0a500'},{key:'purple',hex:'#7b4ff0'},{key:'orange',hex:'#f07a1f'}",
    "  {key:'yellow',hex:'#bc8b00'},{key:'purple',hex:'#7b4ff0'},{key:'orange',hex:'#eb6f10'}"
    "   /* 노랑 2.20:1 · 주황 2.80:1 → 3.08:1 (큰 글자 기준 3:1) */",
    '스트룹 잉크색')

one("function stUpdateBestLine(){",
    NL.join([
        "/* 선택 버튼의 글자색 — 배경이 색이라 흰 글자로 고정하면 노랑·주황에서 안 읽힌다.",
        "   배경의 밝기를 재서 밝으면 진한 글자, 어두우면 흰 글자를 쓴다. */",
        "function stOptInk(hex){",
        "  const v=i=>{ let c=parseInt(hex.slice(i,i+2),16)/255; return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4); };",
        "  const L=0.2126*v(1)+0.7152*v(3)+0.0722*v(5);",
        "  return L>0.30 ? {c:'#1a1a28', sh:'none'} : {c:'#ffffff', sh:'0 1px 2px rgba(0,0,0,.28)'};",
        "}",
        "function stUpdateBestLine(){"]),
    '스트룹 버튼 잉크 함수')

one("    b.className='st-opt'; b.style.background=c.hex; b.textContent=t('color.'+c.key);",
    "    b.className='st-opt'; b.style.background=c.hex; b.textContent=t('color.'+c.key);" + NL +
    "    const ink=stOptInk(c.hex); b.style.color=ink.c; b.style.textShadow=ink.sh;",
    '스트룹 버튼 글자색 적용')

# ── 2) 틀린 그림 찾기 ───────────────────────────────────────────────────────
one(".df-tag.t2{background:#e08a3c}",
    ".df-tag.t2{background:#b8661d}   /* 흰 글자 대비 2.67:1 → 4.6:1 */",
    '틀린그림 태그')

one("let pips=''; for(let i=0;i<total;i++){ pips += i<found ? '<span style=\"color:#f0b429\">●</span>' : '<span style=\"color:#c9d0e8\">○</span>'; }",
    "let pips=''; for(let i=0;i<total;i++){ pips += i<found ? '<span style=\"color:#b07d05\">●</span>'"
    " : '<span style=\"color:#8e99b8\">○</span>'; }   /* 아직 못 찾은 표시가 1.36:1이라 안 보였다 */",
    '틀린그림 남은 개수 표시')

# ── 3) 공통 — 강조색·보조 글자색·헤더 나가기 ───────────────────────────────
one("--purple:#4f7cff;--purple2:#6e92ff;--purple3:#e9f0ff;",
    "--purple:#3367ff;--purple2:#6e92ff;--purple3:#e9f0ff;"
    "   /* 제목·안내문이 흰 배경에서 3.71:1이라 4.64:1로. 배경으로 쓰일 땐 흰 글자 대비가 더 좋아진다 */",
    '강조색')

one("--text:#182235;--text2:#5a6683;--text3:#6b7794;",
    "--text:#182235;--text2:#5a6683;--text3:#616c87;   /* 점수 라벨이 3.96:1이라 4.62:1로 */",
    '보조 글자색')

one("border-radius:11px;cursor:pointer;flex-shrink:0;box-shadow:0 2px 6px rgba(224,71,90,.18);transition:.12s}",
    "border-radius:11px;cursor:pointer;flex-shrink:0;box-shadow:0 2px 6px rgba(224,71,90,.18);transition:.12s}",
    '헤더 나가기 확인') if False else None
one(".nav-exit{display:inline-flex;align-items:center;gap:.15rem;margin-left:.9rem;padding:.5rem .85rem;min-height:40px;font-family:inherit;font-size:.92rem;font-weight:800;color:#e0475a;",
    ".nav-exit{display:inline-flex;align-items:center;gap:.15rem;margin-left:.9rem;padding:.5rem .85rem;min-height:40px;font-family:inherit;font-size:.92rem;font-weight:800;color:#cf2338;",
    '헤더 나가기 글자색')

one(".tab-ico{font-size:1.4rem;line-height:1;filter:grayscale(.4);opacity:.75}",
    ".tab-ico{font-size:1.4rem;line-height:1;filter:grayscale(.4);opacity:.88}",
    '하단 탭 아이콘')

# ── 4) 컬러소트 기호 ────────────────────────────────────────────────────────
one("  return L>0.42 ? 'rgba(20,16,45,.5)' : 'rgba(255,255,255,.82)';",
    "  return L>0.42 ? 'rgba(20,16,45,.68)' : 'rgba(255,255,255,.92)';"
    "   /* 색약 대비용 기호인데 정작 기호가 3.7:1이었다 */",
    '컬러소트 기호 잉크')

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — 스트룹 · 틀린그림 · 공통 UI · 컬러소트 기호')
