# -*- coding: utf-8 -*-
"""끝나지 않는 두 게임 — 높은음 찾기(버그)와 길 따라가기(난이도 정체).

■ 높은음 찾기 — 타이머가 영구히 멈추는 버그
   정답을 맞히면 PT.pause=true로 타이머를 잠깐 세우고, 다음 라운드(ptRound)에서
   300ms 뒤에 풀도록 setTimeout을 PT.timers에 넣는다. 그런데 바로 다음 줄의
   ptPlaySeq()가 첫 줄에서 ptClear()로 PT.timers를 통째로 지운다.
   → 그 '풀어주는 타이머'까지 같이 지워져 PT.pause가 true로 굳는다.
   측정(.logs/dbg2.mjs): 남은 시간이 40초 내내 72에서 1도 줄지 않았다. 게임이 안 끝난다.
   고침: pause 해제를 ptPlaySeq 안(ptClear 직후)으로 옮긴다. 어떤 경로로 들어와도
        시퀀스를 재생하는 순간 타이머가 반드시 다시 흐른다. 다시 듣기에도 안전해진다.

■ 길 따라가기 — 레벨 11부터 난이도가 멈춘다
   길 폭 w는 레벨마다 좁아지지만 12px 바닥이 있어 보통 난이도 기준 레벨 11에서 멈추고,
   판정 여유 tol = w/2 + 11 도 17px에서 그대로다. 그 뒤로는 길이만 길어질 뿐
   요구 정밀도가 오르지 않아, 손이 안정된 사람에게는 사실상 끝나지 않는 인내 게임이 된다.
   (측정: 봇이 레벨 46 · 17,010점까지 갔고 3판 중 2판은 4분을 넘겨 중단)
   고침: 길은 손가락에 가리지 않게 12px를 유지하되, 판정 여유만 레벨에 따라 계속 좁힌다.
        11 → 최소 3까지. 초반(레벨 1~5)은 사실상 그대로다.
   주의: 이 수정은 봇으로 검증하지 못했다. 스크립트 포인터는 경로 중심선을 사람 손보다
        훨씬 정확히 따라가서 사람 난이도를 대표하지 못한다. 실제 플레이 확인이 필요하다.
"""
import io

SRC = 'index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'


def one(old, new, what):
    global s
    assert s.count(old) == 1, what + ' — 대상을 못 찾음(또는 여러 개)'
    s = s.replace(old, new, 1)


# ── 1) pitch: pause 해제를 ptPlaySeq 안으로 ─────────────────────────────────
assert 'PT.pause=false;   // ptClear' not in s, 'pitch 이미 적용됨'

one("function ptPlaySeq(done){ ptClear();",
    "function ptPlaySeq(done){ ptClear();" + NL +
    "  /* ptClear()가 PT.timers를 비우므로, 예전처럼 여기 바깥에서 setTimeout으로 pause를 풀면"
    " 그 타이머까지 지워져 타이머가 영구히 멈췄다. 재생을 시작하는 이 지점에서 직접 푼다. */" + NL +
    "  PT.pause=false;   /* ptClear 직후여야 안전 — 이 함수는 한 줄이라 // 주석을 쓰면 뒤 코드가 통째로 죽는다 */",
    'pitch pause 해제 위치')

# 이제 ptRound의 300ms 타이머는 불필요하고 위험(같은 방식으로 지워짐)
one("PT.lock=true; ptStatus('pitch.listen'); PT.timers.push(setTimeout(()=>{ PT.pause=false; },300)); ptPlaySeq(()=>{ PT.lock=false; ptStatus('pitch.find','turn'); }); }",
    "PT.lock=true; ptStatus('pitch.listen'); ptPlaySeq(()=>{ PT.lock=false; ptStatus('pitch.find','turn'); }); }",
    'pitch 낡은 pause 타이머 제거')

# ── 2) trace: 판정 여유를 레벨에 따라 계속 좁힌다 ───────────────────────────
one("const w=Math.max(12, cfg.w-(TC.level-1)*1.2); TC.tol=w/2+11;",
    "const w=Math.max(12, cfg.w-(TC.level-1)*1.2);" + NL +
    "  /* 길 폭은 12px에서 멈춘다(더 좁으면 손가락에 가려 보이지 않는다). 대신 판정 여유를"
    "     계속 좁혀 난이도가 이어지게 한다 — 예전엔 레벨 11 이후 난이도가 그대로여서"
    "     손이 안정된 사람에게는 길이만 길어지는 인내 게임이었다. */" + NL +
    "  TC.tol=w/2+Math.max(3, 11-(TC.level-1)*0.4);",
    'trace 판정 여유 램프')

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — pitch 타이머 정지 버그 · trace 난이도 램프')
