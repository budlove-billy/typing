# -*- coding: utf-8 -*-
"""길 따라가기 — 난이도에 '숨 돌리는 구간'을 의도적으로 넣는다.

사용자 관찰: "8까지 점점 어려워지다가 9에 쉬워지고 10에 다시 어려워지는 게 좋다.
             계속 어려워지면 스트레스가 높아진다."

계측해 보니(.logs/trace_difficulty.mjs, 40판) 그 관찰은 **운이었다**:
  - 쉬워지는 레벨 전환은 전체의 8%뿐
  - 연속으로 어려워지는 구간이 중앙값 16판, 최악 19판
  - 난이도 지표(길이÷여유폭)는 20.7 → 94.8로 거의 매 레벨 단조 상승
경로가 무작위라 판마다 폭이 조금씩 흔들리는데, 사용자는 그 흔들림이 크게 나온 판을 만난 것이다.
즉 지금 설계는 사용자가 싫다고 한 '계속 어려워짐' 쪽이고, 대부분의 플레이가 그렇게 된다.

그래서 난이도를 정하는 값을 레벨이 아니라 **'난이도 단계'**로 바꾼다.
4레벨마다 한 판은 두 단계 낮은 난이도로 돌아갔다가 다시 오른다 — 톱니 모양.
  레벨 1 2 3 4 5 6 7 8 9 10 11 12 …
  단계 1 2 3 2 5 6 7 6 9 10 11 10 …
길이·폭·판정 여유가 모두 이 단계를 따르므로, 쉬는 판은 '짧고 넓고 너그럽게' 느껴진다.
레벨 자체는 계속 오르고 점수도 레벨을 따르므로(30+레벨×10) 나아가는 감각은 그대로다.
"""
import io

SRC = 'index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'
assert 'tcStage' not in s, '이미 적용됨'


def one(old, new, what):
    global s
    assert s.count(old) == 1, what + ' — 대상을 못 찾음(또는 여러 개)'
    s = s.replace(old, new, 1)


# ── 1) 난이도 단계 ──────────────────────────────────────────────────────────
one("function tcRender(){",
    NL.join([
        "/* 난이도를 정하는 값 — 레벨을 그대로 쓰지 않는다.",
        "   4레벨마다 한 판은 두 단계 낮은 난이도로 돌아갔다가 다시 오른다(톱니).",
        "   계속 조여 올리기만 하면 지치기 때문에, 중간중간 숨을 돌리게 하려는 것이다.",
        "   레벨과 점수는 계속 오르므로 나아가는 감각은 그대로다. */",
        "const TC_BREATH_EVERY=4, TC_BREATH_BACK=2;",
        "function tcStage(lv){ return Math.max(1, lv - ((lv%TC_BREATH_EVERY===0)?TC_BREATH_BACK:0)); }",
        "function tcRender(){",
        "  const stage=tcStage(TC.level);"]),
    'tcStage 신설')

# ── 2) 길이·폭·여유가 모두 단계를 따르게 ────────────────────────────────────
one("  const steps=Math.min(cfg.steps+(TC.level-1)*2, 44);",
    "  const steps=Math.min(cfg.steps+(stage-1)*2, 44);",
    '길이')
one("  const w=Math.max(11, Math.min(cfg.w-(TC.level-1)*1.6, Math.round(TC.cell*0.68)));",
    "  const w=Math.max(11, Math.min(cfg.w-(stage-1)*1.6, Math.round(TC.cell*0.68)));",
    '폭')
one("  const slack=Math.max(4, 12-(TC.level-1)*0.5);",
    "  const slack=Math.max(4, 12-(stage-1)*0.5);",
    '판정 여유')

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — 4레벨마다 두 단계 되돌아가는 톱니 난이도')
