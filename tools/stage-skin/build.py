# -*- coding: utf-8 -*-
"""스킬 게임 33종 '게임 월드' 스킨 — index.html의 <style> 끝에 표시된 블록을 (재)생성한다.
기획: docs/게임-디자인-리뉴얼-기획.md · 아트: assets/stage/<id>.jpg (원본은 canvas/ 무한 캔버스)
여러 번 실행해도 된다(STAGE-SKIN 표시 사이만 교체). 게임 로직은 건드리지 않는다."""
import io, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, 'index.html')

# id: (강조색, 판 처리)  판 처리 — light: 밝은 유리 / clear: 투명(세계가 놀이판) / dark: 어두운 유리 / keep: 기존 유지
G = {
 'whack':('#ffb23f','clear'), 'catch':('#ff8fb1','clear'), 'chop':('#ff7ab8','clear'), 'react':('#35e0ff','keep'),
 'trail':('#ffd66b','dark'),  'bubble':('#3fe0d0','clear'),'fit':('#3fe8c4','dark'),   'merge':('#ff8fa8','light'),
 'flash':('#ffcf5a','light'), 'count':('#ffb35c','light'), 'nback':('#ff4fd8','dark'),  'cards':('#ffd66b','clear'),
 'rev':('#3fe0d0','light'),   'melody':('#8dff9a','clear'),'rhythm':('#ff9a3f','keep'),'pitch':('#7dffc4','clear'),
 'stroop':('#ff6b8b','light'),'switch':('#b98cff','light'),'flank':('#ffcf5a','light'), 'spot':('#ff5fd2','clear'),
 'odd':('#ffc15a','light'),   'diff':('#ffc15a','keep'),   'rotate':('#9fb4ff','light'),'slide':('#7fe6ff','clear'),
 'math':('#ffa94d','light'),  'guess':('#ffb35c','light'), 'sudoku':('#ff9fc0','light'),'sort':('#c79bff','clear'),
 'nono':('#ffcf5a','light'),  'iq':('#ffd66b','light'),    'anagram':('#ffb38a','light'),'wordsearch':('#b6f05a','light'),
 'trace':('#8ee06a','light'),
}
# 게임 판(보드) 요소 — 판 처리 방식이 적용되는 대상
BOARD = {
 'whack':'.wk-wrap', 'catch':'.ca-area', 'chop':'.cp-stage', 'react':'.rc-box', 'trail':'.tr-board', 'bubble':'.bb-grid',
 'fit':'.ft-board', 'merge':'.mr-board-wrap', 'flash':'.fm-board', 'count':'.hc-stage', 'nback':'.nb-stim',
 'cards':'.cm-board', 'rev':'.rv-display', 'melody':'.ml-pads', 'rhythm':'.rh-pad', 'pitch':'.pt-pads',
 'stroop':'.st-word-wrap', 'switch':'> div:has(> .sw-num)', 'flank':'.fk-stage', 'spot':'.sp-grid', 'odd':'.od-grid',
 'diff':'.df-grids', 'rotate':'.rot-stage', 'slide':'.sl-board', 'math':'.mg-board', 'guess':'.gu-q',
 'sudoku':'.sk-board', 'sort':'.so-tubes', 'nono':'.no-wrap', 'iq':'.iq-question', 'anagram':'.ag-assemble',
 'wordsearch':'.ws-wrap', 'trace':'.tc-area',
}

ids = list(G)
CARD = {'iq': {'game': 'test'}}   # IQ 테스트는 플레이 카드 id가 iq-test-card
def cid(g, part): return '%s-%s-card' % (g, CARD.get(g, {}).get(part, part))
def sel(part, only=None):
    return ':is(' + ','.join('#' + cid(g, part) for g in (only or ids)) + ')'
GC, IC, RC = sel('game'), sel('intro'), sel('result')
RC_BADGE = sel('result', [g for g in ids if g != 'iq'])   # IQ 결과는 첫 요소가 점수 블록

css = []
A = css.append
A('/* ===== STAGE-SKIN START — tools/stage-skin/build.py가 생성(직접 수정 금지) ===== */')
# 게임별 변수: 세계 그림 + 강조색
for g,(acc,_) in G.items():
    A('#screen-%s{--stage:url(assets/stage/%s.jpg);--acc:%s}' % (g, g, acc))

# ---------- 플레이 카드 ----------
A(GC + '{position:relative;background:linear-gradient(180deg,rgba(10,8,30,.34) 0%,rgba(10,8,30,.06) 26%,rgba(10,8,30,.06) 70%,rgba(10,8,30,.42) 100%),var(--stage) center/cover no-repeat,#1c1a3c;'
  'border:3px solid rgba(255,255,255,.16);border-radius:22px;box-shadow:0 16px 34px rgba(18,14,48,.34),inset 0 0 0 1px rgba(0,0,0,.35);padding:.85rem .85rem 1rem}')
# HUD: 통계 박스 → 금속 명판
A(GC + ' .mg-top-stats{background:none;padding:0;gap:.4rem;margin-bottom:.8rem;box-shadow:none;border:none}')
A(GC + ' .mg-stat-divider{display:none}')
A(GC + ' .mg-stat-box{padding:.42rem .3rem .46rem;border-radius:13px;background:linear-gradient(180deg,rgba(52,56,76,.94),rgba(22,24,38,.94));'
  'border:2px solid #686e84;box-shadow:inset 0 1px 0 rgba(255,255,255,.18),0 3px 0 rgba(0,0,0,.4),0 6px 12px rgba(0,0,0,.2)}')
A(GC + ' .mg-stat-label{color:#ffd27a;font-size:.62rem;font-weight:800;letter-spacing:.1em;margin-bottom:.12rem;text-transform:uppercase}')
A(GC + ' .mg-stat-value{color:#fff;font-size:1.45rem;font-weight:900;line-height:1.1;font-variant-numeric:tabular-nums;text-shadow:0 2px 0 rgba(0,0,0,.35)}')
A('#fm-life,#rv-life,#rh-life,#tc-life,#ml-life,#hc-life,#ft-life{color:#ff5f7e!important;letter-spacing:.04em}')
# 타이머 캡슐
A(GC + ' .mg-timer{background:linear-gradient(180deg,#3a3350,#1b1830);color:#fff;border:2px solid #e9b54a;box-shadow:inset 0 1px 0 rgba(255,255,255,.2),0 3px 0 rgba(0,0,0,.4),0 0 14px rgba(255,200,90,.28);'
  'font-size:1.35rem;font-weight:900;padding:.3rem 1.3rem;border-radius:999px;text-shadow:0 2px 0 rgba(0,0,0,.4)}')
A(GC + ' .mg-timer.warn{background:linear-gradient(180deg,#ff5a6e,#c8173a);border-color:#ffd0d6;box-shadow:0 3px 0 #7a0a20,0 0 18px rgba(255,70,100,.65)}')
# 안내문: 그림 위 글자 금지 → 알약
A(GC + ' .gm-status{display:table;margin:.55rem auto .65rem;padding:.38rem .95rem;border-radius:999px;background:rgba(255,255,255,.93);color:#2b2350!important;'
  'font-weight:800;box-shadow:0 3px 0 rgba(0,0,0,.22),0 6px 14px rgba(0,0,0,.14);max-width:100%;text-align:center;line-height:1.35}')
# 판 처리
for g,(acc,mode) in G.items():
    b = '#%s %s' % (cid(g, 'game'), BOARD[g])
    if mode == 'light':
        A(b + '{background:rgba(250,251,255,.97);border-color:transparent;border-radius:18px;box-shadow:0 0 0 3px rgba(255,255,255,.96),0 7px 0 rgba(0,0,0,.18),0 12px 26px rgba(0,0,0,.2)}')   # 테두리 대신 링 — 판 크기(JS가 폭으로 계산) 불변
    elif mode == 'dark':
        A(b + '{background:rgba(12,12,34,.62);border-color:rgba(255,255,255,.22);border-radius:18px;box-shadow:inset 0 0 24px rgba(0,0,0,.35),0 8px 22px rgba(0,0,0,.25);backdrop-filter:blur(2px)}')
    elif mode == 'clear':
        A(b + '{background:transparent;border-color:transparent;box-shadow:none}')
# IQ 상단 줄(타이머·문항 번호)도 그림 위 글자 → 명판
A('#iq-test-card .iq-timer,#iq-test-card .iq-qnum{display:inline-block;padding:.3rem .8rem;border-radius:999px;background:rgba(14,12,34,.66);color:#fff!important;border:2px solid rgba(255,255,255,.28)}')
# 버튼: 입체 / 나가기는 어두운 반투명
A(GC + ' .btn:not(.btn-outline){box-shadow:0 4px 0 rgba(20,40,120,.55),0 8px 16px rgba(0,0,0,.2);font-weight:800}')
A(GC + ' .btn:not(.btn-outline):active{transform:translateY(3px);box-shadow:0 1px 0 rgba(20,40,120,.55)}')
A(GC + ' .btn-outline{background:rgba(255,255,255,.93);border:2px solid rgba(255,255,255,.96);color:#2b2350;box-shadow:0 3px 0 rgba(0,0,0,.25);font-weight:700}')
A(GC + ' .btn-outline[onclick^="leave"]{background:rgba(14,12,34,.58);border:2px solid rgba(255,255,255,.34);color:#fff;box-shadow:0 3px 0 rgba(0,0,0,.3);backdrop-filter:blur(3px)}')

# ---------- 게임별 보정 ----------
# 방향 버튼(받기·화살표·타워): 입체 게임 버튼
A('#catch-game-card .ca-btn,#flank-game-card .fk-btn,#chop-game-card .cp-side-btn{background:linear-gradient(180deg,#6f9bff,#3d62f0);color:#fff;border:2px solid rgba(255,255,255,.35);box-shadow:0 5px 0 #2238a0,0 10px 18px rgba(0,0,0,.25);text-shadow:0 2px 0 rgba(0,0,0,.25)}')
A('#catch-game-card .ca-btn:active,#flank-game-card .fk-btn:active,#chop-game-card .cp-side-btn:active{transform:translateY(4px);box-shadow:0 1px 0 #2238a0;background:linear-gradient(180deg,#6f9bff,#3d62f0);color:#fff}')
# 두더지: 들판 위 흙구덩이(칸 배경을 없애고 구멍을 흙으로)
A('#whack-game-card .wk-cell{background:transparent;border:none;overflow:visible}')
A('#whack-game-card .wk-hole{background:radial-gradient(ellipse at 50% 38%,#2a1608 0%,#3e2412 55%,#5a3a1e 72%,#7a5530 100%);box-shadow:inset 0 7px 9px rgba(0,0,0,.55),0 3px 0 #8a6a3a,0 0 0 4px rgba(120,86,44,.55)}')
A('#whack-game-card .wk-count{background:rgba(14,12,34,.45);color:#fff;text-shadow:0 3px 0 rgba(0,0,0,.4);border-radius:18px}')
# 멜로디·높은음·리듬 패드: 반투명(그림이 비침) 대신 불투명하게 두고 어둡게↔빛남으로 구분
A('#melody-game-card .ml-pad,#pitch-game-card .pt-pad,#rhythm-game-card .rh-pad{opacity:1;filter:saturate(.6) brightness(.58);border:3px solid rgba(255,255,255,.28);box-shadow:0 5px 0 rgba(0,0,0,.35)}')
A('#melody-game-card .ml-pad.lit,#pitch-game-card .pt-pad.lit,#rhythm-game-card .rh-pad.lit{filter:saturate(1.1) brightness(1.15);border-color:#fff;box-shadow:0 0 0 3px rgba(255,255,255,.5),0 0 28px 6px rgba(255,255,255,.55)}')
# 엔백: 어두운 네온 패널 위 글자는 흰 네온
A('#nback-game-card .nb-stim{color:#f4fbff;text-shadow:0 0 12px #3fe6ff,0 0 26px rgba(255,79,216,.7)}')
A('#nback-game-card .nb-stim.hit{background:rgba(20,120,110,.7);border-color:#5fffd8;color:#fff}')
A('#nback-game-card .nb-stim.miss{background:rgba(150,20,50,.7);border-color:#ff7a95;color:#fff}')
# 카드 짝: 초록 펠트 위 카지노풍 카드 뒷면
A('#cards-game-card .cm-card.back{background:repeating-linear-gradient(45deg,rgba(255,255,255,.1) 0 6px,transparent 6px 12px),linear-gradient(160deg,#d8344e,#8e1430);border:3px solid #fff;box-shadow:inset 0 0 0 3px #f2c14e,0 4px 0 rgba(0,0,0,.35)}')
A('#cards-game-card .cm-card.back::after{content:"★";color:#f6d27a;text-shadow:0 2px 0 rgba(0,0,0,.3)}')
A('#cards-game-card .cm-card.up{background:#fffdf6;border:3px solid #f2c14e;box-shadow:0 4px 0 rgba(0,0,0,.3)}')
A('#cards-game-card .cm-card.done{box-shadow:0 4px 0 rgba(0,0,0,.25)}')
# 그림 위에 놓이던 글자들 → 알약/패널
A('#sudoku-game-card .sk-top-row{background:rgba(250,251,255,.94);border-radius:14px;padding:.45rem .7rem;box-shadow:0 3px 0 rgba(0,0,0,.18)}')
A('#wordsearch-game-card #ws-theme{display:table;margin:0 auto .55rem!important;padding:.3rem .9rem;border-radius:999px;background:rgba(255,255,255,.93);box-shadow:0 3px 0 rgba(0,0,0,.2)}')

# ---------- 시작 카드: 세계 배너 + 로고 제목 ----------
A(IC + '{position:relative;overflow:hidden;padding-top:168px}')
A(IC + '::before{content:"";position:absolute;left:0;right:0;top:0;height:152px;background:linear-gradient(180deg,rgba(10,8,30,0) 35%,rgba(10,8,30,.62) 100%),var(--stage) center 42%/cover no-repeat;'
  'border-bottom:3px solid var(--acc);box-shadow:inset 0 -12px 22px rgba(0,0,0,.18)}')
A(IC + ' > .section-head{max-width:none;position:absolute;left:1.1rem;right:6.2rem;top:0;height:152px;margin:0;z-index:2;display:flex;align-items:flex-end;padding-bottom:13px}')   # 긴 제목(영/태)은 위로 자란다
A(IC + ' .section-head h2{min-width:0;flex:1;overflow-wrap:anywhere;color:#fff;font-size:clamp(1.3rem,6.4vw,1.72rem);font-weight:900;letter-spacing:-.02em;line-height:1.12;margin:0;'
  'text-shadow:0 3px 0 rgba(0,0,0,.45),0 0 18px rgba(0,0,0,.35);-webkit-text-stroke:0}')
A(IC + ' .game-scene{top:14px;bottom:auto;right:12px;opacity:1;transform:none;z-index:2;filter:drop-shadow(0 4px 6px rgba(0,0,0,.35))}')
A(IC + ' > p{max-width:none}')   # 마스코트가 배너로 올라갔으니 본문은 전체 폭
A(IC + ' .difficulty-row{gap:.5rem}')
A(IC + ' .diff-btn{padding:.7rem .3rem;border:2px solid #e2dcf3;border-radius:14px;background:#fff;box-shadow:0 4px 0 #e2dcf3;transition:transform .12s,box-shadow .12s}')
A(IC + ' .diff-btn:hover{transform:translateY(-1px);background:#fff}')
A(IC + ' .diff-btn.active{background:linear-gradient(180deg,#ffe39c,#ffbd4f);border-color:#d8891b;box-shadow:0 4px 0 #b36c0e;color:#5a3300}')
A(IC + ' .diff-btn.active p{color:#7a4808}')
A(IC + ' > .btn:not(.btn-outline){display:block;width:100%;padding:.85rem 1rem;font-size:1.05rem;font-weight:900;border-radius:15px;background:linear-gradient(180deg,#ff8f5e,#ef4f6d);'
  'box-shadow:0 5px 0 #b3314b,0 10px 20px rgba(239,79,109,.26);transition:transform .08s,box-shadow .08s}')
A(IC + ' > .btn:not(.btn-outline):active{transform:translateY(3px);box-shadow:0 2px 0 #b3314b}')
A('@media (max-width:480px){' + IC + ' .game-scene{transform:scale(.82);transform-origin:top right}}')

# ---------- 결과 카드: 배너 + 메달 배지 + 금색 점수 ----------
A(RC + '{position:relative;overflow:hidden;padding-top:92px}')
A(RC + '::before{content:"";position:absolute;left:0;right:0;top:0;height:128px;background:linear-gradient(180deg,rgba(10,8,30,.05),rgba(10,8,30,.45)),var(--stage) center 40%/cover no-repeat;border-bottom:3px solid var(--acc)}')
A(RC_BADGE + ' > div:first-child{position:relative;z-index:1;width:84px;height:84px;margin:0 auto .55rem!important;display:flex;align-items:center;justify-content:center;font-size:2.7rem!important;line-height:1;'
  'border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,#fff4dc 70%);border:4px solid var(--acc);box-shadow:0 5px 0 rgba(0,0,0,.2),0 10px 22px rgba(0,0,0,.22)}')
A(RC + ' > h2{position:relative;z-index:1;font-weight:900}')
A('#iq-result-card{padding-top:146px}')   # 배지 없이 점수 블록이 먼저 → 배너 아래에서 시작
A(RC + ' .iq-result-score{background:linear-gradient(180deg,#ffd35a,#ff9a2f);-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:900;'
  'filter:drop-shadow(0 3px 0 rgba(160,70,20,.45));font-variant-numeric:tabular-nums}')
A(RC + ' .btn:not(.btn-outline){background:linear-gradient(180deg,#ff8f5e,#ef4f6d);box-shadow:0 4px 0 #b3314b,0 8px 16px rgba(239,79,109,.22);font-weight:900}')
A(RC + ' .btn:not(.btn-outline):active{transform:translateY(3px);box-shadow:0 1px 0 #b3314b}')
A(RC + ' .btn-outline{border-width:2px;box-shadow:0 3px 0 #dcd6ee;font-weight:700}')
A('/* ===== STAGE-SKIN END ===== */')
block = '\n'.join(css) + '\n'

s = io.open(P, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
block = block.replace('\n', nl)
m = re.search(r'/\* ===== STAGE-SKIN START.*?STAGE-SKIN END ===== \*/' + re.escape(nl), s, re.S)
if m:
    s = s[:m.start()] + block + s[m.end():]
else:
    i = s.index('</style>')
    s = s[:i] + block + s[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('stage skin: %d rules, %d games' % (len(css), len(G)))
