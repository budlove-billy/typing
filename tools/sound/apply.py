# -*- coding: utf-8 -*-
"""사운드 v2 적용(1회용, 기록용) — tools/sound/engine.js를 index.html에 넣고 게임별 훅을 연결한다.
각 치환은 정확히 1회 일치해야 한다(아니면 중단)."""
import io, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
P = os.path.join(ROOT, 'index.html')
s = io.open(P, encoding='utf-8', newline='').read(); NL = '\r\n' if '\r\n' in s else '\n'
ENG = io.open(os.path.join(HERE, 'engine.js'), encoding='utf-8').read().rstrip('\n') + '\n'
def R(a, b, n=1, label=''):
    global s
    a2, b2 = a.replace('\n', NL), b.replace('\n', NL); c = s.count(a2)
    if c == 0 and NL != '\n': a2, b2 = a, b; c = s.count(a2)   # 이전 패치가 LF로 넣은 구간
    assert c == n, (label or a[:70], c); s = s.replace(a2, b2)

# 1) 옛 sfx() 통째로 교체
a = s.index('function sfx(kind){'); b = s.index('// UI 버튼 탭 사운드', a)
s = s[:a] + ENG.replace('\n', NL) + s[b:]
# 2) 기존 _tone/_beep 출력을 새 버스로(시험음 _beep은 울림 없는 드라이 버스)
R("    o.connect(g); g.connect(_AC.destination);", "    o.connect(g); g.connect(_dryOut());", label='beep out')
R("    g.connect(_AC.destination);\n    // 메인 + 옥타브 위", "    g.connect(_sfxOut());\n    // 메인 + 옥타브 위", label='tone out')
R("      src.connect(nf); nf.connect(ng); ng.connect(_AC.destination);", "      src.connect(nf); nf.connect(ng); ng.connect(_sfxOut());", label='tone noise out')
# 3) 소리 끄기 → 음악도 멈춤, 🔊 버튼 → 음량 패널
R("  if(on) sfx('good');\n}", "  if(on) sfx('good'); else bgmStop();\n}", label='toggle')
R('<button class="snd-btn" id="snd-btn" onclick="toggleSound()" title="sound">', '<button class="snd-btn" id="snd-btn" onclick="openSndPanel(event)" title="sound">', label='snd btn')
R('  "nav.run": {', '  "snd.music": {ko:"음악", en:"Music", th:"เพลง"}, "snd.sfx": {ko:"효과음", en:"Effects", th:"เสียงเอฟเฟกต์"},\n  "snd.on": {ko:"소리 켜짐", en:"Sound on", th:"เปิดเสียง"}, "snd.off": {ko:"소리 꺼짐", en:"Sound off", th:"ปิดเสียง"},\n  "nav.run": {', label='i18n')
R(".snd-btn{", ".snd-panel{position:absolute;z-index:9999;display:flex;flex-direction:column;gap:.55rem;padding:.75rem .85rem;min-width:210px;border-radius:14px;background:#fff;border:1px solid var(--border);box-shadow:0 10px 28px rgba(20,20,60,.22)}\n.snd-panel label{display:flex;align-items:center;justify-content:space-between;gap:.6rem;font-size:.84rem;font-weight:700;color:var(--text)}\n.snd-panel input{width:110px}\n.snd-mute{font:inherit;font-weight:800;border:1px solid var(--border);background:var(--bg3);border-radius:10px;padding:.45rem;cursor:pointer}\n.snd-btn{", label='css')
# 4) 게임 전환·중단 시 음악 정지
R("  try{ Object.keys(QDL_MS).forEach(qdlClear); }catch(e){}", "  try{ Object.keys(QDL_MS).forEach(qdlClear); bgmStop(); SND.streak=0; }catch(e){}", label='halt')
# 5) 어려움 문항 제한시간 — 남은 30%에서 빠른 틱
R("function qdlClear(id){ clearTimeout(_qdl[id]); _qdl[id]=0; }", "function qdlClear(id){ clearTimeout(_qdl[id]); _qdl[id]=0; clearTimeout(_qdl[id+'_t']); }", label='qdl clear')
R("  _qdl[id]=setTimeout(()=>{ _qdl[id]=0; onTimeout(); }, ms);", "  _qdl[id]=setTimeout(()=>{ _qdl[id]=0; onTimeout(); }, ms);\n  _qdl[id+'_t']=setTimeout(()=>sfx('dltick'), ms*0.62);", label='qdl tick')
# 6) 자체 타이머를 쓰던 60초 게임에도 마지막 10초 심장박동 연결
for fn, st in [('fkTimer', 'FK'), ('guTimer', 'GU'), ('caTimer', 'CA'), ('agTimer', 'AG'), ('wsTimer', 'WS'), ('dfTimer', 'DF'), ('ptTimer', 'PT')]:
    R("el.style.color=%s.timeLeft<=10?'var(--red)':''; }" % st, "el.style.color=%s.timeLeft<=10?'var(--red)':''; sfx('__tick',%s); }" % (st, st), label='tick ' + fn)
R("  IQS.timeLeft--;\n  updateIQTimerDisplay();", "  IQS.timeLeft--;\n  if(IQS.timeLeft>0 && IQS.timeLeft<=30) sfx('tick');   // 마지막 30초\n  updateIQTimerDisplay();", label='iq tick')
# 7) 콤보 배지는 화면만(소리는 연속 성공 팡파르가 맡는다)
R("if(sndOn()){ try{ [880,1175,1568].forEach((f,i)=>_tone({freq:f,dur:0.07,type:'triangle',vol:0.11,when:i*0.05})); navigator.vibrate&&navigator.vibrate(18); }catch(_){} }",
  "try{ navigator.vibrate&&navigator.vibrate(18); }catch(_){}", label='fxCombo')

# ───── 게임별 시그니처 ─────
# 말로우 런
R("function rnSnd(kind){ try{ if(!sndOn()) return;\n  if(kind==='jump') _tone({freq:360,dur:0.13,type:'square',vol:0.05,glide:420});\n  else if(kind==='beat') [659,880,1175].forEach((f,i)=>_tone({freq:f,dur:0.1,type:'triangle',vol:0.11,when:i*0.07}));\n}catch(e){} }",
  "function rnSnd(kind){ sfx(kind); }   // jump · beat → 사운드 엔진 v2", label='rnSnd')
R("  if(!RN.grounded){ RN.py+=RN.vy; RN.vy-=RN_G; if(RN.py<=0){ RN.py=0; RN.vy=0; RN.grounded=true; RN.landT=8; rnPuff(RN,RN.px+RN_PW/2,RN.groundY-2,7,3); } }\n  for(const o of RN.obs) o.x-=RN_BASE;",
  "  if(!RN.grounded){ RN.py+=RN.vy; RN.vy-=RN_G; if(RN.py<=0){ RN.py=0; RN.vy=0; RN.grounded=true; RN.landT=8; rnPuff(RN,RN.px+RN_PW/2,RN.groundY-2,7,3); sfx('land'); } }\n  for(const o of RN.obs) o.x-=RN_BASE;", label='run land')
R("  try{sfx('bad');}catch(e){} try{if(navigator.vibrate)navigator.vibrate(60);}catch(e){}\n  const nr=bt_recordScore(RN.best",
  "  try{sfx('crash');}catch(e){}\n  const nr=bt_recordScore(RN.best", label='run crash')
R("  const m=Math.floor(RN.dist/RN_PX_PER_M); if(m!==RN.hudM){ RN.hudM=m; document.getElementById('rn-dist').textContent=m.toLocaleString(); }",
  "  const m=Math.floor(RN.dist/RN_PX_PER_M); if(m!==RN.hudM){ RN.hudM=m; document.getElementById('rn-dist').textContent=m.toLocaleString(); if(m>0&&m%100===0) sfx('milestone'); }\n  sndIntensity(RN.ts>1.45?2:RN.ts>1.15?1:0);   // 배속이 오르면 음악도 쌓인다", label='run hud')
# 말로우 타워
R("  _beep(700+Math.random()*80,0.05,'square',0.12);\n  try{ navigator.vibrate&&navigator.vibrate(10); }catch(_){}", "  sfx('bite');\n  try{ navigator.vibrate&&navigator.vibrate(10); }catch(_){}", label='chop bite')
R("    cpGaugeRender();\n    if(CP.gauge<=0) cpDie('time');", "    cpGaugeRender();\n    if(CP.gauge<30){ CP._hb=(CP._hb||0)+1; if(CP._hb%7===1) sfx('heart'); } else CP._hb=0;   // 게이지 30% 아래 심장박동\n    if(CP.gauge<=0) cpDie('time');", label='chop heart')
# 말로우 팡팡
R("    document.getElementById('wk-cell-'+idx).classList.add('up');", "    document.getElementById('wk-cell-'+idx).classList.add('up'); if(!bad) sfx('pop');", label='whack pop')
R("  if(sl.bad){\n    sfx('bad'); WK.combo=0;", "  if(sl.bad){\n    sfx('bomb'); WK.combo=0;", label='whack bomb')
R("    sfx('good'); WK.hits++; WK.combo++;", "    sfx('good'); sfx('bonk'); WK.hits++; WK.combo++;", label='whack bonk')
# 마시멜로 받기
R("caFlash(true); caStats(); caTimer(); sfx('bad');", "caFlash(true); caStats(); caTimer(); sfx('clang');", label='catch fork')
# 반응 속도 — GO 신호에는 소리를 내지 않는다(노고에는 없어 소리만으로 정답이 새기 때문). 누른 뒤 빠를수록 높은 차임
R("    sfx('good'); rcUpdateStats(); rcSetBox('good', rt+' ms', '+'+pts); rcSchedNext();", "    sfx('rt', rt); rcUpdateStats(); rcSetBox('good', rt+' ms', '+'+pts); rcSchedNext();", label='react rt')
# 순서 잇기 — 번호마다 음계 한 칸, 판 완료 팡파르
R("    node.classList.add('done'); node.onclick=null; TR.next++; sfx('good');", "    node.classList.add('done'); node.onclick=null; TR.next++; sfx('good', TR.next-2);", label='trail node')
R("      TR.boards++; TR.score+=dmScore(TR.diff, TR.n, 'trail'); TR.n++;", "      TR.boards++; TR.score+=dmScore(TR.diff, TR.n, 'trail'); TR.n++; sfx('win');", label='trail clear')
# 순간기억
R("    c.textContent=FM.expect; c.classList.remove('empty'); c.classList.add('done'); c.onclick=null; sfx('good');", "    c.textContent=FM.expect; c.classList.remove('empty'); c.classList.add('done'); c.onclick=null; sfx('good', FM.expect-1);", label='flash cell')
R("function fmClear(){\n  FM.phase='idle';", "function fmClear(){\n  FM.phase='idle'; sfx('win');", label='flash clear')
# 버블 톡톡
R("if(at>=0){ BB.sel.splice(at,1); el.classList.remove('sel'); _beep(420,0.05,'sine',0.12); bbCurrentLine(); return; }", "if(at>=0){ BB.sel.splice(at,1); el.classList.remove('sel'); sfx('bubble',0); bbCurrentLine(); return; }", label='bubble off')
R("  BB.sel.push(i); el.classList.add('sel'); _beep(660,0.05,'sine',0.15);", "  BB.sel.push(i); el.classList.add('sel'); sfx('bubble', BB.vals[i]);", label='bubble on')
# 블록 채우기
R("    sfx(lines>=2?'win':'good');\n  } else { FT.combo=0; sfx('good'); }", "    sfx('place'); sfx('lines', lines);\n  } else { FT.combo=0; sfx('place'); }", label='fit')
# 말랑 2048
R("  if(gain>0) sfx('good'); else sfx('whoosh');", "  sfx('whoosh'); if(gain>0) sfx('merge', gain);", label='merge')
# 엔백 — 글자마다 같은 중립음
R("  el.className='nb-stim'; el.textContent=letter;", "  el.className='nb-stim'; el.textContent=letter; sfx('blip');", label='nback blip')
# 스도쿠 — 틀리면 버즈, 행·열·박스 완성 차임, 완성 팡파르
R("  SK.board[r][c]=n;\n  SK.notes[r][c].clear();\n", "  SK.board[r][c]=n;\n  SK.notes[r][c].clear();\n  if(n===SK.solution[r][c]){ if(skUnitDone(r,c)) sfx('unit'); } else sfx('bad');\n", label='sudoku input')
R("  // 완성!\n  SK.running=false;", "  // 완성!\n  SK.running=false; sfx('win');", label='sudoku win')
# 픽셀 로직 — 칠하기 붓 소리 / X 틱(줄 완성 차임은 정답을 알려 주므로 넣지 않는다)
R("function noTap(r,c,cell){ if(!NO.running) return;", "function noTap(r,c,cell){ if(!NO.running) return; sfx(NO.mark==='fill'?'brush':'click');", label='nono')
# 컬러 소트
R("    SO.sel=ti; _beep(600,0.04,'sine',0.12); soRender(); return;", "    SO.sel=ti; sfx('click'); soRender(); return;", label='sort select')
R("  _beep(760,0.05,'sine',0.14);\n  if(soTubeDone(B)) sfx('good');", "  sfx('pour');\n  if(soTubeDone(B)) sfx('cork');", label='sort pour')
# 슬라이딩
a = s.index('function slTap(i){'); b = s.index("  sfx('whoosh');", a); assert b - a < 1200
s = s[:b] + "  sfx('click');" + s[b + len("  sfx('whoosh');"):]
# 글자 맞추기
R("AG.slots.push(idx); tile.used=true; agRender();", "AG.slots.push(idx); tile.used=true; sfx('letter', p); agRender();", label='anagram letter')
# 길 따라가기
R("      TC.cur=q; tcAddTrail(q);\n", "      TC.cur=q; tcAddTrail(q); if(TC.trail.length%45===0) sfx('trace', TC.trail.length);\n", label='trace progress')
R("TC.lives--; sfx('bad'); tcStats(); tcResetTrail();", "TC.lives--; sfx('scrape'); tcStats(); tcResetTrail();", label='trace scrape')

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('sound v2 applied')
