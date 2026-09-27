# -*- coding: utf-8 -*-
"""멜로디 기억: 라운드 성공음을 음정 없는 박수(sfx('clap'))로 (1회용, 2026-09-28 사용자 선택).
예전 sfx('good')는 음계 플럭이라 다음 멜로디의 첫 음처럼 들렸다. engine.js와 index.html 둘 다 고친다."""
import io, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CASE = "    case 'clap': [0,0.16].forEach(o=>{ for(let k=0;k<3;k++) _hit(T0+o+k*0.011,0.5,_AM.sfx,1300,0.045,'bandpass'); _hit(T0+o+0.03,0.3,_AM.sfx,1300,0.14,'bandpass'); }); vib(15); break;   // 박수 — 음정이 없어 멜로디 기억의 다음 멜로디와 섞이지 않는다\n"
ANCH = "    case 'bite':"
BURST = "if(kind==='good'||kind==='merge'||kind==='cork'||kind==='lines'||kind==='rt') fxBurst"
for f in ['tools/sound/engine.js', 'index.html']:
    P = os.path.join(ROOT, f); s = io.open(P, encoding='utf-8', newline='').read(); nl = '\r\n' if '\r\n' in s else '\n'
    if "case 'clap':" in s: print('skip', f); continue
    assert s.count(ANCH) == 1 and s.count(BURST) == 1, f
    s = s.replace(ANCH, CASE.replace('\n', nl) + ANCH)
    s = s.replace(BURST, BURST.replace("kind==='rt')", "kind==='rt'||kind==='clap')"))   # 화면 불꽃은 정답과 같게(연속 성공 카운트에는 넣지 않음 — 끊길 때 음계 하강음이 나지 않게)
    if f == 'index.html':
        a = "      mlSetStatus('melody.goodRound','good'); mlUpdateStats(); sfx('good');"
        assert s.count(a) == 1; s = s.replace(a, a.replace("sfx('good')", "sfx('clap')"))
    io.open(P, 'w', encoding='utf-8', newline='').write(s); print('patched', f)
