# -*- coding: utf-8 -*-
"""밸런스 v2 적용 — docs/밸런스-분석-제안.md 의 제안을 index.html에 반영한다(1회용, 기록용).
수치 원본: tools/balance/calib.json (calibrate.mjs 산출). 게임 34종 + 기록 초기화 마이그레이션.
각 치환은 정확히 1회 일치해야 한다(아니면 중단)."""
import io, os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, 'index.html')
CAL = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calib.json'), encoding='utf-8'))
s = io.open(P, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s else '\n'

def R(a, b, n=1, label=''):
    global s
    a2, b2 = a.replace('\n', NL), b.replace('\n', NL)
    c = s.count(a2)
    assert c == n, (label or a[:70], c)
    s = s.replace(a2, b2)

def RX(pat, repl, n=1, label=''):
    global s
    new, c = re.subn(pat, repl, s)
    assert c == n, (label or pat[:70], c)
    s = new

r2 = lambda x: round(x, 2)
DM = {g: {d: r2(v) for d, v in m.items()} for g, m in CAL['dm'].items() if g not in ('fit', 'sort', 'slide', 'nono', 'sudoku')}
MED = dict(CAL['medals']); MED['iq'] = [100, 112, 122, 132]
K = CAL['K']

# ───────────── 1. 난이도 배수: 게임별 표 ─────────────
R("""const DMULT_GAME={ merge:{easy:1, normal:7, hard:70} };""",
  """/* 밸런스 v2(2026-09-27): 게임마다 '같은 사람이 쉬움 0.8 : 보통 1 : 어려움 1.25'를 받도록 시뮬레이션으로 산출한 배수.
   (tools/balance/calibrate.mjs → calib.json, 근거 docs/밸런스-분석-제안.md) 보통 규모는 예전과 같다. */
const DMULT_GAME=""" + json.dumps(DM, separators=(',', ':')) + ";", label='DMULT_GAME')
# 모든 dmScore 호출에 게임 id를 붙인다(접두어 → 게임)
PFX = {'FM':'flash','ST':'stroop','TR':'trail','CP':'chop','SP':'spot','OD':'odd','BB':'bubble','SW':'switch','NB':'nback','RT':'rotate',
       'CM':'cards','RC':'react','WK':'whack','ML':'melody','FK':'flank','GU':'guess','RV':'rev','RH':'rhythm','CA':'catch','WS':'wordsearch',
       'DF':'diff','PT':'pitch','TC':'trace'}
def _dms(m):
    p = m.group(1)
    return 'dmScore(%s.diff, %s, \'%s\')' % (p, m.group(2), PFX[p])
new, c = re.subn(r"dmScore\((FM|ST|TR|CP|SP|OD|BB|SW|NB|RT|CM|RC|WK|ML|FK|GU|RV|RH|CA|WS|DF|PT|TC)\.diff, ((?:[^()]|\([^()]*(?:\([^()]*\)[^()]*)*\))*?)\)", _dms, s)
assert c == 26, ('dmScore calls', c); s = new

# ───────────── 2. 메달·능력치 기준 ─────────────
RX(r"const GAME_REF=\{[^\n]*\};", lambda m: "const GAME_REF=" + re.sub(r'"([a-z]+)":', r'\1:', json.dumps(dict(vocab=100, typing=420, **{g: v[3] for g, v in MED.items()}), separators=(',', ':'))) +   # 키 따옴표 없이(quality-static 검사 형식)
   ";   // 밸런스 v2: 💎 목표 = 상위 1%의 중앙값 → 능력치 100%", label='GAME_REF')
R("""const MEDAL_GOALS={run:[600,1800,4000,8000]};""",
  """/* 밸런스 v2: 메달 = 플레이어 분포(시뮬레이션). 🥉 초보의 보통 중앙값 · 🥈 상위25% · 🥇 상위10% · 💎 상위1% 중앙값.
   예전 GAME_REF×0.6/1.8/4/8은 지수라 30개 게임에서 상위 1%도 💎이 불가능했고 몇 개는 공짜였다. IQ는 IQ 척도 그대로. */
const MEDAL_GOALS=""" + json.dumps(MED, separators=(',', ':')) + ";", label='MEDAL_GOALS')

# ───────────── 3. 기록 초기화(1회) ─────────────
R("""let _LR=null;
""", """/* ══════════ 밸런스 v2 — 기록 새로 시작(2026-09-27) ══════════
   점수 공식·배수·메달이 바뀌어 옛 기록과 비교할 수 없다(사용자 결정: 초기화). 최고 기록·봇 사다리·최근 판 비율·능력치 기준을 지운다.
   주간 포인트·미션·설정은 그대로 둔다. */
(function migrateBalanceV2(){
  try{
    if(localStorage.getItem('brain.balanceV2')==='1') return;
    const drop=[];
    for(let i=0;i<localStorage.length;i++){ const k=localStorage.key(i);
      if(/^brain\\.[a-z0-9]+\\.(best|flat)$/.test(k) || /^brain\\.bot\\./.test(k)) drop.push(k); }
    ['brain.recent','brain.ability.base','brain.ability.seen','brain.newRecords'].forEach(k=>drop.push(k));
    drop.forEach(k=>localStorage.removeItem(k));
    localStorage.setItem('brain.balanceV2','1');
  }catch(e){}
})();
let _LR=null;
""", label='migration')

# ───────────── 4. 어려움 문항 제한시간(60초 5종) ─────────────
R("""function dmScore(d,pts,game){ return Math.round(pts*dm(d,game)); }""",
  """function dmScore(d,pts,game){ return Math.round(pts*dm(d,game)); }
/* 어려움 전용 문항 제한시간 — 지금 어려움은 문항당 15% 느려질 뿐이라 '다른 게임'처럼 느껴지지 않았다.
   넘기면 오답처럼 콤보만 끊고(시간 감점 없음) 다음 문항. 남은 시간은 판 위 얇은 막대로 보인다. */
const QDL_MS={stroop:1500, flank:900, switch:1500, rotate:2200, guess:3200};
const _qdl={};
function qdlClear(id){ clearTimeout(_qdl[id]); _qdl[id]=0; }
function qdlArm(id, diff, onTimeout){
  qdlClear(id); const ms=(diff==='hard')&&QDL_MS[id]; const bar=document.getElementById('qdl-'+id);
  if(!ms){ if(bar) bar.style.display='none'; return; }
  if(bar){ bar.style.display='block'; const i=bar.firstElementChild; i.style.transition='none'; i.style.width='100%'; void i.offsetWidth; i.style.transition='width '+ms+'ms linear'; i.style.width='0%'; }
  _qdl[id]=setTimeout(()=>{ _qdl[id]=0; onTimeout(); }, ms);
}""", label='qdl helper')
BAR = lambda g: '<div class="qdl-bar" id="qdl-%s" style="display:none"><i></i></div>' % g
R('    <div class="st-word-wrap">', '    ' + BAR('stroop') + '\n    <div class="st-word-wrap">', label='bar stroop')
R('    <div class="fk-stage">', '    ' + BAR('flank') + '\n    <div class="fk-stage">', label='bar flank')
R('    <div style="text-align:center">\n      <div class="sw-rule" id="sw-rule"></div>', '    ' + BAR('switch') + '\n    <div style="text-align:center">\n      <div class="sw-rule" id="sw-rule"></div>', label='bar switch')
R('    <div class="rot-stage">', '    ' + BAR('rotate') + '\n    <div class="rot-stage">', label='bar rotate')
RX(r'(\r?\n    )(<div class="gu-q" id="gu-q")', lambda m: m.group(1) + BAR('guess') + m.group(1) + m.group(2), label='bar guess')
# stroop
R("""  w.textContent=t('color.'+wordKey);
  w.style.color=ink.hex;
}""", """  w.textContent=t('color.'+wordKey);
  w.style.color=ink.hex;
  qdlArm('stroop', ST.diff, ()=>{ if(!ST.running) return; ST.combo=0; sfx('bad'); stUpdateStats(); stNextTrial(); });
}""", label='stroop arm')
# switch
R("""    bA.textContent=t('switch.low');  bA.dataset.k='low';
    bB.textContent=t('switch.high'); bB.dataset.k='high';
  }
}""", """    bA.textContent=t('switch.low');  bA.dataset.k='low';
    bB.textContent=t('switch.high'); bB.dataset.k='high';
  }
  qdlArm('switch', SW.diff, ()=>{ if(!SW.running) return; SW.combo=0; sfx('bad'); swUpdateStats(); swNextTrial(false); });
}""", label='switch arm')
# rotate
R("""  document.getElementById('rot-opt-same').classList.remove('flash-wrong');
  document.getElementById('rot-opt-diff').classList.remove('flash-wrong');
}""", """  document.getElementById('rot-opt-same').classList.remove('flash-wrong');
  document.getElementById('rot-opt-diff').classList.remove('flash-wrong');
  qdlArm('rotate', RT.diff, ()=>{ if(!RT.running) return; RT.combo=0; sfx('bad'); rtUpdateStats(); rtNextTrial(); });
}""", label='rotate arm')
# flank
R("""  document.getElementById('fk-row').innerHTML=A(fl)+A(fl)+' <b>'+A(FK.cur)+'</b> '+A(fl)+A(fl); FK.lock=false; }""",
  """  document.getElementById('fk-row').innerHTML=A(fl)+A(fl)+' <b>'+A(FK.cur)+'</b> '+A(fl)+A(fl); FK.lock=false;
  qdlArm('flank', FK.diff, ()=>{ if(!FK.running) return; FK.combo=0; sfx('bad'); fkStats(); fkRound(); }); }""", label='flank arm')
# guess
R("""  order.forEach(v=>{ const b=document.createElement('button'); b.className='gu-choice'; b.textContent=v; b.onclick=()=>guAns(v,b); box.appendChild(b); }); GU.lock=false; }""",
  """  order.forEach(v=>{ const b=document.createElement('button'); b.className='gu-choice'; b.textContent=v; b.onclick=()=>guAns(v,b); box.appendChild(b); }); GU.lock=false;
  qdlArm('guess', GU.diff, ()=>{ if(!GU.running) return; GU.combo=0; sfx('bad'); guStats(); guRound(); }); }""", label='guess arm')
R("GU.score+=dmScore(GU.diff, comboPts(GU.combo), 'guess'); sfx('good'); guStats(); setTimeout(guRound,140); }",
  "GU.score+=dmScore(GU.diff, comboPts(GU.combo), 'guess'); sfx('good'); guStats(); qdlClear('guess'); setTimeout(guRound,140); }", label='guess clear on answer')
# 종료·리셋 시 해제
for fn, g in [('function finishStroop(){', 'stroop'), ('function finishSwitch(){', 'switch'), ('function finishRotate(){', 'rotate'),
              ('function finishFlank(){', 'flank'), ('function finishGuess(){', 'guess')]:
    R(fn, fn + " qdlClear('%s');" % g, label='qdl finish ' + g)
R("function haltRunningGames(){\n  stopRecordFx();", "function haltRunningGames(){\n  stopRecordFx();\n  try{ Object.keys(QDL_MS).forEach(qdlClear); }catch(e){}", label='qdl halt')
# 설명(어려움 칩)
for key, ko, en, th in [('stroop', '6색·문항당 1.5초', '6 colors · 1.5s each', '6 สี·ข้อละ 1.5 วิ'),
                        ('switch', '자주 전환·문항당 1.5초', 'Frequent switch · 1.5s each', 'สลับบ่อย·ข้อละ 1.5 วิ'),
                        ('rotate', '30° 단위·문항당 2.2초', '30° steps · 2.2s each', 'ทีละ 30°·ข้อละ 2.2 วิ')]:
    RX(r'"%s\.hardDesc": \{ko:"[^"]*", en:"[^"]*", th:"[^"]*"\}' % key, '"%s.hardDesc": {ko:"%s", en:"%s", th:"%s"}' % (key, ko, en, th), label='desc ' + key)
RX(r'"flank\.hardDesc": \{ko:"[^"]*", en:"[^"]*", th:"[^"]*"\}', '"flank.hardDesc": {ko:"함정 많음·0.9초", en:"Many decoys · 0.9s", th:"ตัวลวงเยอะ·0.9 วิ"}', n=2, label='desc flank')
RX(r'"guess\.hardDesc": \{ko:"[^"]*", en:"[^"]*", th:"[^"]*"\}', '"guess.hardDesc": {ko:"세 자리·문항당 3.2초", en:"3-digit · 3.2s each", th:"สามหลัก·ข้อละ 3.2 วิ"}', n=2, label='desc guess')

# ───────────── 5. 게임별 규칙 ─────────────
# 말로우 타워: 가속 = 깨문 횟수(배수가 가속에 곱해지던 이중 처벌 제거)
RX(r"const CP_CFG=\{[^\n]*\};", "const CP_CFG={ easy:{decay:2.6,gain:8,forkP:0.45,accel:0.13}, normal:{decay:3.4,gain:7,forkP:0.55,accel:0.2}, hard:{decay:4.2,gain:6.2,forkP:0.65,accel:0.28} };   // 밸런스 v2: accel은 '깨문 횟수'당", label='CP_CFG')
R("  CP.score=0; CP.gauge=100; CP.side='L'; CP.running=true;", "  CP.score=0; CP.chops=0; CP.gauge=100; CP.side='L'; CP.running=true;", label='chop reset')
R("    CP.gauge -= (cfg.decay + CP.score*cfg.accel)*0.1; // 100ms 틱", "    CP.gauge -= (cfg.decay + (CP.chops||0)*cfg.accel)*0.1; // 100ms 틱 — 가속은 깨문 횟수 기준(점수엔 난이도 배수가 곱해져 있다)", label='chop accel')
R("  CP.score += dmScore(CP.diff, 10, 'chop');", "  CP.score += dmScore(CP.diff, 10, 'chop'); CP.chops=(CP.chops||0)+1;", label='chop count')

# 인원수 세기: 연속 보너스 상한 +20, 4연속마다 이벤트 +1, 배수 적용
R("  HC.score=0; HC.lives=3; HC.streak=0; HC.maxStreak=0;", "  HC.score=0; HC.lives=3; HC.streak=0; HC.maxStreak=0; HC.ok=0;", label='count reset')
R("  const n=hc_randInt(cfg.events[0], cfg.events[1]);", "  const n=hc_randInt(cfg.events[0], cfg.events[1]) + Math.floor((HC.ok||0)/4);   // 4번 맞힐 때마다 이벤트 1개씩 늘어난다", label='count ramp')
R("    HC.score += cfg.pts + (HC.streak-1)*2;", "    HC.ok=(HC.ok||0)+1;\n    HC.score += dmScore(HC.diff, cfg.pts + Math.min(HC.streak-1,10)*2, 'count');   // 연속 보너스 상한 +20(예전엔 무한)", label='count score')

# 틀린 그림: 판 클리어 보너스가 레벨마다 줄어든다
R("      const bonus=Math.min(DF_BONUS[DF.diff], DF_TIME[DF.diff]-DF.timeLeft);   // 시작 시간을 넘지 않게",
  "      const bonus=Math.min(Math.max(2, Math.round(DF_BONUS[DF.diff]-0.6*(DF.level-2))), DF_TIME[DF.diff]-DF.timeLeft);   // 시작 시간을 넘지 않게 · 레벨마다 0.6초씩 줄어 상위권도 끝난다", label='diff bonus')

# 반응 속도: 실력 차가 점수에 드러나게
R("RC.score+=dmScore(RC.diff, 120, 'react');", "RC.score+=dmScore(RC.diff, 150, 'react');", label='react nogo')
R("sfx('good'); rcUpdateStats(); rcSetBox('good', t('react.goodNogo'), '+120');", "sfx('good'); rcUpdateStats(); rcSetBox('good', t('react.goodNogo'), '+150');", label='react nogo label')
R("    const pts=Math.max(20, Math.round(500 - rt*0.5)); RC.score+=dmScore(RC.diff, pts, 'react');",
  "    const pts=Math.max(20, Math.round(1000 - rt*2.2)); RC.score+=dmScore(RC.diff, pts, 'react');   // 예전 500-rt/2는 상위1%와 초보 차이가 19%뿐", label='react pts')

# 마시멜로 받기: 판 안에서 점점 빨라진다
R("function caTick(){ if(!CA.running) return; const a=caArea(); if(!a) return; const H=a.clientHeight||330, line=H-42, cfg=CA_CFG[CA.diff];\n  for(let i=CA.items.length-1;i>=0;i--){ const it=CA.items[i]; it.y+=cfg.spd*0.04;",
  "function caTick(){ if(!CA.running) return; const a=caArea(); if(!a) return; const H=a.clientHeight||330, line=H-42, cfg=CA_CFG[CA.diff]; CA.ticks=(CA.ticks||0)+1;\n  const ramp=1+0.012*CA.ticks*0.04;   // 1초에 1.2%씩 빨라진다(예전엔 60초 내내 같은 속도라 실력 차가 안 났다)\n  for(let i=CA.items.length-1;i>=0;i--){ const it=CA.items[i]; it.y+=cfg.spd*ramp*0.04;", label='catch ramp')
R("  CA.tickT=setInterval(caTick,40); CA.spawnT=setInterval(caSpawn,CA_CFG[CA.diff].spawn); caSpawn(); }",
  "  CA.ticks=0; CA.tickT=setInterval(caTick,40); caSpawnLoop(); }\n/* 생성 간격도 1초에 0.6%씩 줄어든다(최소 45%) */\nfunction caSpawnLoop(){ if(!CA.running) return; caSpawn(); const k=(CA.ticks||0)*0.04; CA.spawnT=setTimeout(caSpawnLoop, CA_CFG[CA.diff].spawn*Math.max(0.45,1-0.006*k)); }", label='catch spawn')

# 높은음 찾기: 음정차 하한을 낮춰 상위권 변별
RX(r"normal:\{nStart:4,nMax:6,c0:80,cStep:5,cMin:26\}, hard:\{nStart:5,nMax:7,c0:62,cStep:5,cMin:18\}", "normal:{nStart:4,nMax:6,c0:80,cStep:5,cMin:16}, hard:{nStart:5,nMax:7,c0:62,cStep:5,cMin:10}", label='pitch cMin')

# 글자 맞추기: 전용 배율을 보정값으로
R("const AG_MULT={ easy:1.0, normal:1.4, hard:2.0 }; // 난이도 점수 배율", "const AG_MULT=DMULT_GAME.anagram; // 난이도 점수 배율(밸런스 v2 보정값)", label='AG_MULT')

# 암산: 정답 수 → 콤보 점수 × 배수(다른 게임과 같은 눈금)
R("  highScore:{beginner:0, advanced:0, expert:0}, // 세션 중에만 유지되는 난이도별 최고점", "  highScore:{beginner:0, advanced:0, expert:0}, // 세션 중에만 유지되는 난이도별 최고점\n  combo:0,", label='math combo field')
R("function startMathGame(){\n  MG.score=0;", "function startMathGame(){\n  MG.score=0; MG.combo=0;", label='math reset')
R("  if(isCorrect){\n    MG.score++;", "  if(isCorrect){\n    MG.combo++; MG.score+=dmScore({beginner:'easy',advanced:'normal',expert:'hard'}[MG.diff], comboPts(MG.combo), 'math');   // 밸런스 v2: 정답 수 → 콤보 점수", label='math score')
R("  }else{\n    MG.wrongCount++;", "  }else{\n    MG.combo=0;\n    MG.wrongCount++;", label='math combo reset')

# 풀이형 4종: '기준점 − 시간' → 기준시간 대비 점수
R("function dmScore(d,pts,game){ return Math.round(pts*dm(d,game)); }",
  """function dmScore(d,pts,game){ return Math.round(pts*dm(d,game)); }
/* 풀이형(컬러 소트·슬라이딩·픽셀 로직·스도쿠) 점수: K × (기준시간/걸린시간)^0.8, 최저 0.15배.
   기준시간 = 보통 실력자의 풀이 시간. 예전 '기준점 − 시간'은 어려움이 거의 늘 바닥 점수였다. */
const PAR_SCORE=""" + json.dumps({
    'sort':   {d: {'K': K['sort'][d],   'par': {'easy': 45,  'normal': 110,  'hard': 220}[d]}  for d in ('easy', 'normal', 'hard')},
    'slide':  {d: {'K': K['slide'][d],  'par': {'easy': 70,  'normal': 330,  'hard': 900}[d]}  for d in ('easy', 'normal', 'hard')},
    'nono':   {d: {'K': K['nono'][d],   'par': {'easy': 60,  'normal': 280,  'hard': 560}[d]}  for d in ('easy', 'normal', 'hard')},
    'sudoku': {d: {'K': K['sudoku'][d], 'par': {'easy': 560, 'normal': 1150, 'hard': 2200}[d]} for d in ('easy', 'normal', 'hard')},
  }, separators=(',', ':')) + """;
function parScore(game, diff, sec, pen){ const c=PAR_SCORE[game][diff]; return Math.max(10, Math.round(c.K*Math.max(0.15, Math.pow(c.par/Math.max(1,sec),0.8))*(1-(pen||0)))); }""", label='parScore')
R("  SO.score=Math.max(10, SO_CFG[SO.diff].base - SO.sec*2 - SO.moves*3);", "  SO.score=parScore('sort', SO.diff, SO.sec);", label='sort score')
R("  SL.score=Math.max(10, SL_CFG[SL.diff].base - SL.sec*3 - SL.moves);", "  SL.score=parScore('slide', SL.diff, SL.sec);", label='slide score')
R("  const score=Math.max(50, NO_CFG[NO.diff].base - Math.round(secs*NO_CFG[NO.diff].rate)); sfx('win');", "  const score=parScore('nono', NO.diff, secs); sfx('win');", label='nono score')
R("  const skBase={easy:60,medium:85,expert:110};\n  const skScore=Math.max(30, Math.round((skBase[SK.diff]||60) - SK.mistakes*4 - SK.hintsUsed*6 - SK.timeSec/20));",
  "  const skScore=parScore('sudoku', {easy:'easy',medium:'normal',expert:'hard'}[SK.diff]||'easy', SK.timeSec, Math.min(0.6, SK.mistakes*0.04 + SK.hintsUsed*0.06));", label='sudoku score')

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('balance v2 applied (without run v2)')
