# -*- coding: utf-8 -*-
"""틀린 그림 찾기 — 판을 깰 때마다 타이머가 처음 값으로 완전히 리셋돼서 게임이 끝나지 않았다.

측정(.logs/dbg4.mjs): 정답만 계속 맞히면 남은 시간이 계속 37~39초에 머물고
      60초 시점에 레벨 28 · 7,112점, 그 뒤로도 5초마다 약 630점씩 무한히 올라간다.
      즉 이 게임의 점수는 실력이 아니라 '얼마나 오래 앉아 있었나'였고,
      기준점수(GAME_REF 600)는 애초에 의미가 없었다.

해결: 판을 깨면 시간을 '보너스'로 주되, 시작 시간을 넘지 못하게 상한을 둔다.
      보너스는 시작 시간의 25%. 판이 어려워질수록(찾을 곳이 1개 → 최대 n²/4개)
      한 판에 드는 시간이 보너스를 넘어서므로 시계가 서서히 줄어들어 반드시 끝난다.
      초반(찾을 곳 1~2개)에는 보너스가 소요 시간보다 커서 계속 최대치에 붙어 있는다.
      시간이 붙는 것이 보이도록 남은 개수 표시 위에 +N초를 띄운다.
"""
import io

SRC = 'index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'
assert 'DF_BONUS' not in s, '이미 적용됨'


def one(old, new, what):
    global s
    assert s.count(old) == 1, what + ' — 대상을 못 찾음(또는 여러 개)'
    s = s.replace(old, new, 1)


# 1) 보너스 표 — 시작 시간의 25%
one("const DF_TIME={easy:30, normal:40, hard:50};",
    "const DF_TIME={easy:30, normal:40, hard:50};",
    'DF_TIME 확인') if s.count("const DF_TIME={easy:30, normal:40, hard:50};") == 1 else None

# DF_TIME 선언 줄을 찾아 그 뒤에 보너스 표를 붙인다 (값이 다를 수 있으므로 접두만 매칭)
i = s.index('const DF_TIME=')
j = s.index(NL, i)
s = s[:j] + NL + NL.join([
    "/* 판을 깰 때 주는 시간 — 시작 시간의 25%. 판이 어려워지면 한 판에 드는 시간이",
    "   이 보너스를 넘어서므로 시계가 줄어들어 게임이 반드시 끝난다(예전엔 매판 완전 리셋이라 무한). */",
    "const DF_BONUS={easy:8, normal:10, hard:12};"]) + s[j:]

# 2) 새 판을 만들 때는 시간을 건드리지 않는다 (시작 시각은 startDiff가 정한다)
one("DF.g1=base; DF.g2=g2; DF.timeLeft=DF_TIME[DF.diff]; if(typeof dfTimer==='function') dfTimer(); dfRender(); dfCount();",
    "DF.g1=base; DF.g2=g2; if(typeof dfTimer==='function') dfTimer(); dfRender(); dfCount();",
    '새 판 생성 시 타이머 리셋 제거')

# 3) 판 클리어 → 완전 리셋 대신 상한 있는 보너스
one("if(DF.found>=DF.diffs.length){ DF.level++; DF.lock=true; DF.timeLeft=DF_TIME[DF.diff]; dfTimer();",
    "if(DF.found>=DF.diffs.length){ DF.level++; DF.lock=true;" + NL +
    "      const bonus=Math.min(DF_BONUS[DF.diff], DF_TIME[DF.diff]-DF.timeLeft);   // 시작 시간을 넘지 않게" + NL +
    "      DF.timeLeft+=bonus; dfTimer();" + NL +
    "      if(bonus>0){ const ce=document.getElementById('df-count'); if(ce) fxCelebrate(ce,'+'+bonus+'s'); }",
    '판 클리어 보너스')

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — 매판 완전 리셋 → 상한 있는 보너스(시작값의 25%)')
