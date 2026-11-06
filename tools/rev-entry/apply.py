# -*- coding: utf-8 -*-
"""거꾸로 기억: 입력한 숫자를 '?' 칸(흰 상자) 안에 보여 준다 (2026-10-16, 사용자 제보, 1회용·기록용).
원인: 입력 숫자는 상자 아래 별도 줄(#rv-entry)에 어두운 글자색(var(--text))으로 찍혀 어두운 게임 배경에 묻혔다.
수정: 입력 단계에서 상자 안에 [입력한 숫자 + 남은 빈칸] 슬롯을 그린다. 아래 줄은 쓰지 않는다. 판정·점수 그대로."""
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'daily-redesign')); from _patch import Patch
p = Patch(os.path.join(os.path.dirname(__file__), '..', '..', 'index.html')); R = p.R

R('.rv-key.empty{border:none;background:none;pointer-events:none}', '''.rv-key.empty{border:none;background:none;pointer-events:none}
/* 입력 칸: 상자 안에 입력한 숫자 + 남은 빈칸 */
.rv-slots{display:flex;gap:.3rem;justify-content:center;flex-wrap:nowrap;letter-spacing:0}
.rv-slot{display:flex;align-items:flex-end;justify-content:center;width:1.9rem;height:2.6rem;font-size:2rem;line-height:1;font-weight:900;color:var(--purple);border-bottom:3px solid #c9d2e6}
.rv-slot.f{border-bottom-color:var(--purple)}
.rv-slot.n{border-bottom-color:var(--purple);animation:mrPop .15s ease}
.rv-slots.long .rv-slot{width:1.45rem;font-size:1.55rem}
.rv-slots.xl{gap:.18rem}.rv-slots.xl .rv-slot{width:1.05rem;font-size:1.2rem}
#rv-entry{display:none}''')

R("""function rvKey(n){""", """// 입력 단계 상자: 입력한 숫자는 보라색, 남은 자리는 빈 밑줄 칸
function rvSlots(){ const d=document.getElementById('rv-display'); let h='';
  for(let i=0;i<RV.len;i++){ const v=RV.entry[i]; h+='<span class="rv-slot'+(v!=null?' f'+(i===RV.entry.length-1?' n':''):'')+'">'+(v!=null?v:'')+'</span>'; }
  d.innerHTML='<span class="rv-slots'+(RV.len>10?' xl':RV.len>7?' long':'')+'">'+h+'</span>'; }
function rvKey(n){""")
R("""RV.phase='input'; disp.textContent='?'; rvStatus('rev.input','turn');""", """RV.phase='input'; rvSlots(); rvStatus('rev.input','turn');""")
R("""document.getElementById('rv-entry').textContent=RV.entry.join(' '); if(RV.entry.length===RV.len) rvCheck(); }""",
  """rvSlots(); if(RV.entry.length===RV.len) rvCheck(); }""")
R("""document.getElementById('rv-entry').textContent=RV.entry.join(' '); }""", """rvSlots(); }""")
p.save()
