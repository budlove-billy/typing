# -*- coding: utf-8 -*-
"""글자 맞추기: 보통·어려움에서 글자 하나를 '?'로 가린다 (2026-09-30, 1회용·기록용).
- 가린 글자판은 '?'로 보이고, 칸에 넣어도 '?' — 나머지 글자로 단어를 추리해 빈자리에 넣는다.
- 되도록 단어에 한 번만 나오는 글자를 가린다(두 번 나오면 가려도 보이므로).
- 힌트가 가린 글자를 넣으면 그 글자는 드러난다. 맞히면 0.45초 동안 정답을 초록색으로 보여 주고 다음 단어.
- 판정·점수·시간은 그대로."""
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'daily-redesign')); from _patch import Patch
p = Patch(os.path.join(os.path.dirname(__file__), '..', '..', 'index.html')); R = p.R

R('.ag-tile.used{opacity:.24;box-shadow:none;pointer-events:none;background:var(--purple)}',
  '''.ag-tile.used{opacity:.24;box-shadow:none;pointer-events:none;background:var(--purple)}
/* 가린 글자(보통·어려움) */
.ag-tile.q{background:linear-gradient(180deg,#ffd46b 0%,#f39a1e 75%);color:#6b3a00;box-shadow:0 3px 8px rgba(220,130,20,.38),inset 0 1px 0 rgba(255,255,255,.5)}
.ag-tile.q.used{background:#f39a1e}
.ag-slot.filled.q{border-color:#f39a1e;background:#fff3d6;color:#b86400}
.ag-slots.ok .ag-slot{border-style:solid;border-color:#21a67a;background:#e3f7ee;color:#137a57;animation:mrPop .18s ease}''')

R("""const AG_PENALTY={ easy:0, normal:1, hard:2 };""",
  """const AG_PENALTY={ easy:0, normal:1, hard:2 };
const AG_HIDE={ easy:0, normal:1, hard:1 };        // 가리는 글자 수('?' 글자판)""")

R("""  AG.tiles=order.map(i=>({ch:chars[i],used:false})); AG.slots=[]; AG.wordStart=Date.now(); }""",
  """  AG.tiles=order.map(i=>({ch:chars[i],used:false,hidden:false})); AG.slots=[]; AG.wordStart=Date.now();
  if(AG_HIDE[AG.diff]){ let cand=AG.tiles.map((t,i)=>i).filter(i=>chars.filter(c=>c===AG.tiles[i].ch).length===1);   // 한 번만 나오는 글자를 가린다
    if(!cand.length) cand=AG.tiles.map((t,i)=>i); AG.tiles[cand[Math.floor(Math.random()*cand.length)]].hidden=true; } }""")

R("""d.className='ag-slot'+(ti!=null?' filled':''); d.textContent=ti!=null?AG.tiles[ti].ch:'';""",
  """d.className='ag-slot'+(ti!=null?' filled':'')+(ti!=null&&AG.tiles[ti].hidden?' q':''); d.textContent=ti!=null?(AG.tiles[ti].hidden?'?':AG.tiles[ti].ch):'';""")
R("""b.className='ag-tile'+(tile.used?' used':''); b.textContent=tile.ch;""",
  """b.className='ag-tile'+(tile.used?' used':'')+(tile.hidden?' q':''); b.textContent=tile.hidden?'?':tile.ch;""")
R("""ts.appendChild(b); }); agStats(); }""",
  """ts.appendChild(b); });
  const pr=document.querySelector('#anagram-game-card .ag-prompt'), pk=AG.tiles.some(x=>x.hidden)?'anagram.promptHidden':'anagram.prompt';
  if(pr&&pr.getAttribute('data-i18n')!==pk){ pr.setAttribute('data-i18n',pk); pr.textContent=t(pk); }
  agStats(); }""")

R("""function agTapTile(idx){ if(!AG.running) return;""", """function agTapTile(idx){ if(!AG.running||AG.lock) return;""")
R("""function agUnplace(i){ if(!AG.running||AG.slots[i]==null) return;""", """function agUnplace(i){ if(!AG.running||AG.lock||AG.slots[i]==null) return;""")
R("""AG.score+=Math.round((base+speed+comboB)*AG_MULT[AG.diff]); sfx('good'); agStats(); agPick(); agRender(); }""",
  """AG.score+=Math.round((base+speed+comboB)*AG_MULT[AG.diff]); sfx('good'); agStats();
    if(AG.tiles.some(x=>x.hidden)){   // 가린 글자가 있었으면 정답을 잠깐 보여 준다
      const ss=document.getElementById('ag-slots'); ss.classList.add('ok'); [...ss.children].forEach((d,i)=>{ d.textContent=AG.tiles[AG.slots[i]].ch; d.classList.remove('q'); });
      AG.lock=true; setTimeout(()=>{ AG.lock=false; ss.classList.remove('ok'); if(AG.running){ agPick(); agRender(); } },450); }
    else{ agPick(); agRender(); } }""")
R("""function agHint(){ if(!AG.running||AG.hints<=0) return;""", """function agHint(){ if(!AG.running||AG.lock||AG.hints<=0) return;""")
R("""  AG.hints--; AG.slots.push(found); AG.tiles[found].used=true; agRender();""",
  """  AG.hints--; AG.slots.push(found); AG.tiles[found].used=true; AG.tiles[found].hidden=false; agRender();""")
R("""function startAnagram(){ AG.score=0;""", """function startAnagram(){ AG.lock=false; AG.score=0;""")

# 난이도 설명 + 안내 문구 (사전이 두 곳 — 뒤의 것이 이긴다. 둘 다 맞춘다)
s = p.s
s = s.replace('"anagram.normalDesc": {ko:"4글자 · 힌트2", en:"4 letters · 2 hints", th:"4 ตัว · ใบ้2"}',
              '"anagram.normalDesc": {ko:"4글자 · 1글자 가림 · 힌트2", en:"4 letters · 1 hidden · 2 hints", th:"4 ตัว · ซ่อน1 · ใบ้2"}')
s = s.replace('"anagram.hardDesc": {ko:"5~6글자 · 힌트1 · 점수2배", en:"5-6 letters · 1 hint · x2", th:"5-6 ตัว · ใบ้1 · x2"}',
              '"anagram.hardDesc": {ko:"5~6글자 · 1글자 가림 · 힌트1 · 점수2배", en:"5-6 letters · 1 hidden · 1 hint · x2", th:"5-6 ตัว · ซ่อน1 · ใบ้1 · x2"}')
assert s.count('1글자 가림') == 4, s.count('1글자 가림')
p.s = s
R('''  "anagram.prompt": {ko:"글자를 순서대로 눌러 단어를 완성하세요", en:"Tap the letters in order to spell the word", th:"แตะตัวอักษรตามลำดับเพื่อสะกดคำ"},''',
  '''  "anagram.prompt": {ko:"글자를 순서대로 눌러 단어를 완성하세요", en:"Tap the letters in order to spell the word", th:"แตะตัวอักษรตามลำดับเพื่อสะกดคำ"},
  "anagram.promptHidden": {ko:"? 는 가려진 글자예요 — 단어를 추리해 채우세요", en:"? is a hidden letter — guess the word to place it", th:"? คือตัวอักษรที่ซ่อนไว้ — เดาคำแล้ววางให้ถูก"},''')
p.save()
