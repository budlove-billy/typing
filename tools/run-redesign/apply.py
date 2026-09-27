# -*- coding: utf-8 -*-
"""말로우 런 디자인 전면 개편 — index.html의 run 화면 HTML·CSS·JS·i18n 교체.
JS 본문은 tools/run-redesign/run.js (물리·히트박스는 기존 검증값 그대로).
2026-09-27 1회 적용 완료 — 기록용. 다시 실행하면 훅·번역·CSS가 중복되므로 이후 수정은 index.html에 직접 한다."""
import io, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, 'index.html')
s = io.open(P, encoding='utf-8').read()
js = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'run.js'), encoding='utf-8').read().rstrip('\n') + '\n'

def swap(start, end, new, label):
    global s
    a = s.index(start); b = s.index(end, a) + len(end)
    s = s[:a] + new + s[b:]
    print('ok', label)

# 1) HTML
HTML = '''<!-- ==================== RUN SCREEN (말로우 런 / 순발력) ==================== -->
<div class="screen" id="screen-run">
  <div class="card rn-card" id="run-intro-card">
    <div class="rn-stage rn-stage-intro" onclick="startRun()">
      <canvas id="rn-preview" aria-hidden="true"></canvas>
      <div class="rn-logo"><small>ENDLESS RUNNER</small><h2 data-i18n="run.title">말로우 런</h2></div>
    </div>
    <p class="rn-intro-text" data-i18n="run.intro">
      황혼의 숲을 달리는 말로우! 다가오는 <b>가시 울타리·바위·상자·수정</b>을 <b>점프</b>로 넘으세요. 갈수록 빨라집니다.<br>
      화면을 탭하거나 스페이스바로 점프. 얼마나 멀리 갈까요?
    </p>
    <div class="difficulty-row rn-diff">
      <div class="diff-btn" id="rn-diff-easy" onclick="setRunDiff('easy')"><h3>🌱 <span data-i18n="run.easy">쉬움</span></h3><p data-i18n="run.easyDesc">느긋하게</p></div>
      <div class="diff-btn active" id="rn-diff-normal" onclick="setRunDiff('normal')"><h3>⚡ <span data-i18n="run.normal">보통</span></h3><p data-i18n="run.normalDesc">기본</p></div>
      <div class="diff-btn" id="rn-diff-hard" onclick="setRunDiff('hard')"><h3>🔥 <span data-i18n="run.hard">어려움</span></h3><p data-i18n="run.hardDesc">빠르게</p></div>
    </div>
    <button class="btn rn-go" onclick="startRun()" data-i18n="run.startGame">게임 시작</button>
    <div class="best-line" id="rn-intro-best"></div>
  </div>
  <div class="card rn-card rn-dark" id="run-game-card" style="display:none">
    <div class="rn-stage" onpointerdown="rnJump()">
      <canvas id="rn-canvas"></canvas>
      <div class="rn-hud">
        <div class="rn-hud-r">
          <div class="rn-hud-row"><div class="rn-plate rn-dist"><b id="rn-dist">0</b><small>m</small></div><div class="rn-plate" id="rn-score-plate"><small data-i18n="run.score">점수</small><b id="rn-score">0</b></div></div>
          <div class="rn-best-mini"><span data-i18n="run.bestShort">최고</span> <b id="rn-hud-best">0</b></div>
          <div class="rn-speed" aria-hidden="true"><i id="rn-speed-fill"></i></div>
        </div>
      </div>
      <div class="rn-cue" id="rn-cue" data-i18n="run.tapHint">화면을 탭하면 점프!</div>
      <div class="rn-toast" id="rn-toast" data-i18n="run.newBest">신기록!</div>
    </div>
    <div class="rn-controls"><button class="btn rn-jump" onpointerdown="event.preventDefault();rnJump()" data-i18n="run.jump">⬆️ 점프</button><button class="btn rn-leave" onclick="leaveRun()" data-i18n="run.leave">나가기</button></div>
  </div>
  <div class="card rn-card" id="run-result-card" style="display:none;text-align:center">
    <div class="rn-board">
      <div class="rn-board-emoji" id="rn-result-emoji">🏃</div>
      <h2 id="rn-result-title">게임 오버!</h2>
      <div class="iq-result-score" id="rn-result-score">0</div>
      <div class="rn-board-sub" data-i18n="run.finalScore">최종 점수</div>
      <div class="rn-board-stats">
        <div><span data-i18n="run.distance">달린 거리</span><b id="rn-r-dist">0 m</b></div>
        <div><span data-i18n="run.difficulty">난이도</span><b id="rn-r-diff">보통</b></div>
        <div><span data-i18n="run.best">최고 기록</span><b id="rn-r-best">0</b></div>
      </div>
      <div class="rn-board-actions"><button class="btn rn-go" onclick="startRun()" data-i18n="run.newGame">새 게임</button><button class="btn rn-ghost" onclick="gameShare('run')" data-i18n="share.button">📷 결과 공유</button><button class="btn rn-ghost" onclick="sendChallenge('run')" data-i18n="ch.send">🎯 도전장</button></div>
    </div>
  </div>
</div>
'''
swap('<!-- ==================== RUN SCREEN (말로우 런 / 순발력) ==================== -->',
     '<!-- ==================== FIT SCREEN', HTML + '\n<!-- ==================== FIT SCREEN', 'html')

# 2) JS
swap('// ========== 말로우 런 (순발력·집중력 · 엔들리스 러너)',
     "document.addEventListener('keydown',e=>{ if((e.code==='Space'||e.code==='ArrowUp') && RN.running){ e.preventDefault(); rnJump(); } });\n",
     js, 'js')

# 3) 인트로 미리보기 시작 훅
hook = "  if(id==='records' && typeof renderRecords==='function'){ renderRecords(); markRecordsSeen(); }\n"
assert s.count(hook) == 1
s = s.replace(hook, hook + "  if(id==='run' && typeof rnPreviewStart==='function') rnPreviewStart();\n")
print('ok hook')

# 4) i18n
old_intro = re.search(r'  "run\.intro": \{[^\n]*\n', s).group(0)
s = s.replace(old_intro,
  '  "run.intro": {ko:"황혼의 숲을 달리는 말로우! 다가오는 <b>가시 울타리·바위·상자·수정</b>을 <b>점프</b>로 넘으세요. 갈수록 빨라집니다.<br>화면을 탭하거나 스페이스바로 점프. 얼마나 멀리 갈까요?", en:"Mallow dashes through a twilight forest! <b>Jump</b> over incoming <b>spike fences, rocks, crates and crystals</b> — it keeps getting faster.<br>Tap the screen or press Space to jump. How far can you run?", th:"มาโลว์วิ่งผ่านป่ายามพลบค่ำ! <b>กระโดด</b>ข้าม<b>รั้วหนาม หิน ลัง และคริสตัล</b>ที่พุ่งเข้ามา ยิ่งวิ่งยิ่งเร็ว!<br>แตะหน้าจอหรือกด Space เพื่อกระโดด วิ่งได้ไกลแค่ไหน?"},\n'
  '  "run.distance": {ko:"달린 거리", en:"Distance", th:"ระยะทาง"},\n'
  '  "run.bestShort": {ko:"최고", en:"BEST", th:"สถิติ"},\n'
  '  "run.newBest": {ko:"🏆 신기록 돌파!", en:"🏆 NEW BEST!", th:"🏆 ทำลายสถิติ!"},\n')
print('ok i18n')

# 5) CSS
CSS = '''/* ===== 말로우 런: 황혼 숲 횡스크롤 테마 (컨셉아트: canvas/ 무한 캔버스) ===== */
#screen-run .rn-card{padding:.75rem .75rem 1.1rem;overflow:hidden}
#screen-run .rn-stage{position:relative;border-radius:16px;overflow:hidden;background:#131238;box-shadow:inset 0 0 0 2px rgba(255,255,255,.07),0 10px 24px rgba(20,16,50,.28);touch-action:manipulation;user-select:none;-webkit-user-select:none;-webkit-tap-highlight-color:transparent;cursor:pointer}
#screen-run .rn-stage canvas{display:block;width:100%;height:228px}
#screen-run .rn-stage-intro canvas{height:232px}
#screen-run .rn-logo{position:absolute;right:14px;top:12px;text-align:right;pointer-events:none}
#screen-run .rn-logo small{display:block;font-size:.6rem;font-weight:800;letter-spacing:.24em;color:#ffcf7a;text-shadow:0 1px 3px rgba(0,0,0,.5)}
#screen-run .rn-logo h2{margin:0;font-size:1.75rem;font-weight:900;line-height:1.1;color:#fff;letter-spacing:-.02em;text-shadow:0 3px 0 #b8456f,0 6px 14px rgba(0,0,0,.45)}
#screen-run .rn-intro-text{font-size:.88rem;color:var(--text2);line-height:1.6;margin:.9rem .2rem 1rem}
#screen-run .rn-diff{gap:.5rem}
#screen-run .rn-diff .diff-btn{padding:.7rem .3rem;border:2px solid #e2dcf3;border-radius:14px;background:#fff;box-shadow:0 4px 0 #e2dcf3;transition:transform .12s,box-shadow .12s}
#screen-run .rn-diff .diff-btn:hover{transform:translateY(-1px)}
#screen-run .rn-diff .diff-btn.active{background:linear-gradient(180deg,#ffe39c,#ffbd4f);border-color:#d8891b;box-shadow:0 4px 0 #b36c0e;color:#5a3300}
#screen-run .rn-diff .diff-btn.active p{color:#7a4808}
#screen-run .rn-go{width:100%;padding:.85rem 1rem;font-size:1.05rem;font-weight:900;letter-spacing:.02em;border-radius:15px;background:linear-gradient(180deg,#ff8f5e,#ef4f6d);box-shadow:0 5px 0 #b3314b,0 10px 20px rgba(239,79,109,.28);transition:transform .08s,box-shadow .08s}
#screen-run .rn-go:active{transform:translateY(3px);box-shadow:0 2px 0 #b3314b,0 5px 10px rgba(239,79,109,.2)}
#screen-run .rn-dark{background:linear-gradient(180deg,#221d4f,#14112e);border-color:#2f2966}
#screen-run .rn-hud{position:absolute;left:8px;right:8px;top:8px;display:flex;justify-content:flex-end;align-items:flex-start;pointer-events:none}
#screen-run .rn-hud-row{display:flex;gap:6px}
#screen-run .rn-hud-r{display:flex;flex-direction:column;align-items:flex-end;gap:4px}
#screen-run .rn-plate{display:inline-flex;align-items:baseline;gap:.3rem;padding:.3rem .62rem .32rem;border-radius:10px;background:linear-gradient(180deg,rgba(44,48,64,.9),rgba(22,24,36,.9));border:2px solid #5d6275;box-shadow:inset 0 1px 0 rgba(255,255,255,.16),0 3px 0 rgba(0,0,0,.35);color:#fff;line-height:1;font-variant-numeric:tabular-nums;transition:border-color .3s,box-shadow .3s}
#screen-run .rn-plate b{font-size:1.15rem;font-weight:900}
#screen-run .rn-plate small{font-size:.66rem;font-weight:800;color:#ffcf7a}
#screen-run .rn-plate.beat{border-color:#ffcf5a;box-shadow:0 0 0 3px rgba(255,207,90,.3),0 0 16px rgba(255,200,90,.55),0 3px 0 rgba(0,0,0,.35)}
#screen-run .rn-best-mini{font-size:.62rem;font-weight:800;color:rgba(255,255,255,.8);text-shadow:0 1px 2px rgba(0,0,0,.6);letter-spacing:.04em}
#screen-run .rn-best-mini b{color:#ffe29a;font-variant-numeric:tabular-nums}
#screen-run .rn-speed{width:84px;height:8px;border-radius:6px;background:rgba(18,20,30,.85);border:2px solid #5d6275;overflow:hidden}
#screen-run .rn-speed i{display:block;height:100%;width:0;background:linear-gradient(90deg,#ffd35a,#ff7a3d,#ff3d6e);transition:width .25s}
#screen-run .rn-cue{position:absolute;left:50%;bottom:42px;transform:translateX(-50%);padding:.32rem .8rem;border-radius:999px;background:rgba(10,8,26,.55);color:#fff;font-size:.76rem;font-weight:700;white-space:nowrap;pointer-events:none;transition:opacity .4s;animation:rnCue 1.1s ease-in-out infinite}
#screen-run .rn-cue.hide{opacity:0;animation:none}
@keyframes rnCue{50%{transform:translateX(-50%) translateY(-3px)}}
#screen-run .rn-toast{position:absolute;left:50%;top:38%;transform:translate(-50%,-50%);opacity:0;font-size:1.35rem;font-weight:900;color:#fff3c4;white-space:nowrap;pointer-events:none;text-shadow:0 3px 0 #b8456f,0 0 16px rgba(255,200,90,.85)}
#screen-run .rn-toast.show{animation:rnToast 1.4s ease-out forwards}
@keyframes rnToast{0%{opacity:0;transform:translate(-50%,-50%) scale(.55)}14%{opacity:1;transform:translate(-50%,-50%) scale(1.1)}28%{transform:translate(-50%,-50%) scale(1)}78%{opacity:1}100%{opacity:0;transform:translate(-50%,-95%) scale(1)}}
#screen-run .rn-controls{display:flex;gap:.55rem;margin-top:.7rem}
#screen-run .rn-jump{flex:1;padding:.9rem 1rem;font-size:1.05rem;font-weight:900;border-radius:15px;background:linear-gradient(180deg,#5ee0a0,#22a86f);box-shadow:0 5px 0 #157049,0 10px 18px rgba(34,168,111,.25);touch-action:manipulation;transition:transform .06s,box-shadow .06s}
#screen-run .rn-jump:active{transform:translateY(3px);box-shadow:0 2px 0 #157049}
#screen-run .rn-leave{padding:.9rem 1rem;border-radius:15px;background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.18);color:#d9d5f2;box-shadow:none;font-weight:700}
#screen-run .rn-board{position:relative;overflow:hidden;padding:1.2rem 1rem 1.1rem;border-radius:16px;color:#fff;background:radial-gradient(120% 90% at 50% 0%,#46357a 0%,#1b1845 62%,#131238 100%);box-shadow:inset 0 0 0 2px rgba(255,255,255,.07)}
#screen-run .rn-board::before{content:'';position:absolute;left:0;right:0;bottom:0;height:34px;background:linear-gradient(180deg,#8ad65a 0 3px,#4f9b33 3px 11px,#6e4225 11px);opacity:.9}
#screen-run .rn-board>*{position:relative}
#screen-run .rn-board-emoji{font-size:2.8rem;line-height:1;margin-bottom:.3rem;filter:drop-shadow(0 4px 6px rgba(0,0,0,.4))}
#screen-run .rn-board h2{margin:0 0 .2rem;color:#fff;font-weight:900;text-shadow:0 2px 0 #b8456f}
#screen-run .rn-board .iq-result-score{color:#ffd66b;font-weight:900;font-variant-numeric:tabular-nums;text-shadow:0 4px 0 #a8431f,0 8px 18px rgba(0,0,0,.4)}
#screen-run .rn-board-sub{font-size:.82rem;color:rgba(255,255,255,.7);margin-bottom:.9rem}
#screen-run .rn-board-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:.4rem;margin-bottom:1rem}
#screen-run .rn-board-stats div{display:flex;flex-direction:column;gap:.2rem;padding:.55rem .3rem;border-radius:12px;background:rgba(10,8,30,.45);border:1px solid rgba(255,255,255,.1)}
#screen-run .rn-board-stats span{font-size:.68rem;color:rgba(255,255,255,.65)}
#screen-run .rn-board-stats b{font-size:.98rem;font-weight:900;color:#fff;font-variant-numeric:tabular-nums}
#screen-run .rn-board-actions{display:flex;flex-wrap:wrap;gap:.45rem;justify-content:center;padding-bottom:2.2rem}
#screen-run .rn-board-actions .rn-go{flex:1 1 100%}
#screen-run .rn-ghost{flex:1;background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.22);color:#fff;box-shadow:none;border-radius:13px;font-weight:700}
@media (prefers-reduced-motion:reduce){#screen-run .rn-cue{animation:none}#screen-run .rn-toast.show{animation-duration:.01s}}
'''
assert s.count('</style>') >= 1
i = s.index('</style>')
s = s[:i] + CSS + s[i:]
print('ok css')
io.open(P, 'w', encoding='utf-8', newline='').write(s)
