# -*- coding: utf-8 -*-
"""길 따라가기 — 손가락이 길을 가리는 문제. 조작을 '트랙패드 방식'으로 바꾼다.

문제(실제 플레이 피드백): 휴대폰에서 길 위를 직접 문지르니 손가락이 그 길을 덮어
      어디로 가야 하는지 안 보인다. 길을 아무리 넓혀도 손가락이 더 넓어서 해결되지 않는다.
      직접 터치 방식의 근본 한계다.

해결: 손가락 위치를 그대로 쓰지 않고 **움직인 거리만** 쓴다(노트북 트랙패드와 같은 방식).
      - 그리기 영역 아무 곳이나 누르면 표식이 초록 점에서 출발한다.
      - 손가락을 움직인 만큼 표식이 따라 움직인다(1:1). 손가락은 길에서 떨어진 곳에 두면 되니
        길이 가려지지 않는다.
      - 이탈 판정은 손가락이 아니라 **표식** 위치로 한다.
      - 손을 떼도 표식은 그 자리에 남는다 → 화면 끝에 닿으면 손을 떼고 다시 잡으면 이어진다
        (트랙패드에서 손을 들어 옮겨 잡는 것과 같다). 이게 없으면 경로가 긴 판에서
        손가락이 화면 밖으로 나가 버린다.
      - 길을 벗어나거나 판을 깨면 표식은 초록 점으로 돌아간다.

이 방식은 마우스에서도 그대로 동작한다(누른 채 끌면 된다). 조작이 하나뿐이라
기기별로 다르게 설명할 필요도 없다.
"""
import io

SRC = 'index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'
assert 'TC.grip' not in s, '이미 적용됨'


def one(old, new, what):
    global s
    assert s.count(old) == 1, what + ' — 대상을 못 찾음(또는 여러 개)'
    s = s.replace(old, new, 1)


# ── 1) 상태에 표식 위치와 잡은 지점 ─────────────────────────────────────────
one("MARGIN:33, cell:40, startR:28, endR:22,",
    "MARGIN:33, cell:40, startR:28, endR:22, cur:null, grip:null,",
    'TC 상태 필드')

# ── 2) 조작 — 절대 위치 대신 이동량 ─────────────────────────────────────────
old_down = "  area.onpointerdown=e=>{ if(!TC.running)return; const p=tcPoint(e); const s=TC.path[0]; if(Math.hypot(p.x-s.x,p.y-s.y)<=(TC.startR||28)){ TC.active=true; try{area.setPointerCapture(e.pointerId);}catch(_){} TC.trail=[{x:s.x,y:s.y}]; tcAddTrail(p); tcStatus('trace.guide'); e.preventDefault(); } };"
old_move = "  area.onpointermove=e=>{ if(!TC.running||!TC.active)return; const p=tcPoint(e); if(tcDist(p)>TC.tol){ tcStray(); return; } tcAddTrail(p); const en=TC.path[TC.path.length-1]; if(Math.hypot(p.x-en.x,p.y-en.y)<=(TC.endR||22)){ tcClearLevel(); } };"
old_up = "  area.onpointerup=()=>{ if(TC.active){ TC.active=false; tcResetTrail(); } };"
for o, w in [(old_down, 'pointerdown'), (old_move, 'pointermove'), (old_up, 'pointerup')]:
    assert s.count(o) == 1, w + ' 핸들러를 못 찾음'

new_handlers = NL.join([
    "  /* 트랙패드 방식 — 손가락의 '위치'가 아니라 '움직인 거리'를 쓴다.",
    "     손가락을 길에서 떨어진 곳에 두어도 되므로 길이 가려지지 않는다. */",
    "  area.onpointerdown=e=>{ if(!TC.running)return;",
    "    TC.grip=tcPoint(e);",
    "    if(!TC.active){                                   // 새로 시작 — 표식은 초록 점에서",
    "      TC.active=true; const st=TC.path[0];",
    "      TC.cur={x:st.x,y:st.y}; TC.trail=[{x:st.x,y:st.y}];",
    "      tcAddTrail(TC.cur); tcStatus('trace.guide');",
    "    }",
    "    try{area.setPointerCapture(e.pointerId);}catch(_){}",
    "    e.preventDefault(); };",
    "  area.onpointermove=e=>{ if(!TC.running||!TC.active||!TC.grip)return;",
    "    const p=tcPoint(e);",
    "    const nx=Math.max(0,Math.min(TC.W, TC.cur.x+(p.x-TC.grip.x)));",
    "    const ny=Math.max(0,Math.min(TC.H, TC.cur.y+(p.y-TC.grip.y)));",
    "    TC.grip=p; TC.cur={x:nx,y:ny};",
    "    if(tcDist(TC.cur)>TC.tol){ tcStray(); return; }",
    "    tcAddTrail(TC.cur);",
    "    const en=TC.path[TC.path.length-1];",
    "    if(Math.hypot(nx-en.x,ny-en.y)<=(TC.endR||22)) tcClearLevel(); };",
    "  /* 손을 떼도 표식은 그대로 둔다 — 화면 끝에 닿으면 떼고 다시 잡아 이어갈 수 있어야 한다",
    "     (트랙패드에서 손을 들어 옮겨 잡는 것과 같다). 경로가 긴 판에서는 이게 없으면 막힌다. */",
    "  area.onpointerup=()=>{ TC.grip=null; };",
    "  area.onpointercancel=()=>{ TC.grip=null; };"])
s = s.replace(old_down + NL + old_move + NL + old_up, new_handlers, 1)
assert 'TC.grip=tcPoint(e)' in s, '핸들러 교체 실패'

# ── 3) 이탈·클리어·새 판에서 표식 초기화 ────────────────────────────────────
one("function tcStray(){ if(!TC.active) return; TC.active=false; TC.lives--;",
    "function tcStray(){ if(!TC.active) return; TC.active=false; TC.cur=null; TC.grip=null; TC.lives--;",
    'tcStray 표식 초기화')
one("function tcClearLevel(){ TC.active=false;",
    "function tcClearLevel(){ TC.active=false; TC.cur=null; TC.grip=null;",
    'tcClearLevel 표식 초기화')
one("  TC.active=false; tcStatus('trace.guide'); }",
    "  TC.active=false; TC.cur=null; TC.grip=null; tcStatus('trace.guide'); }",
    'tcRender 표식 초기화')

# ── 4) 표식을 잘 보이게 — 이제 이걸 보고 조작한다 ───────────────────────────
one("+'<circle id=\"tc-cursor\" r=\"'+cr+'\" fill=\"#4f7cff\" opacity=\"0\"/></svg>';",
    "+'<circle id=\"tc-cursor\" r=\"'+cr+'\" fill=\"#4f7cff\" stroke=\"#fff\" stroke-width=\"3\" opacity=\"0\"/></svg>';",
    '표식 테두리')

# ── 5) 안내 문구 ────────────────────────────────────────────────────────────
one('"trace.guide": {ko:"초록 점에서 시작하세요", en:"Start at the green dot", th:"เริ่มที่จุดเขียว"}',
    '"trace.guide": {ko:"아무 곳이나 누른 채 움직이세요", en:"Press anywhere and move", '
    'th:"แตะตรงไหนก็ได้แล้วลาก"}',
    'trace.guide 문구')

old_intro = ('"trace.intro": {ko:"<b>초록 점</b>에서 출발해 길을 벗어나지 않고 손가락(마우스)으로 '
             '<b>빨간 점</b>까지 이어보세요!<br>길을 벗어나면 생명이 줄어요. 레벨이 오를수록 길이 좁고 길어집니다.", '
             'en:"Start at the <b>green dot</b> and drag to the <b>red dot</b> without leaving the path!'
             '<br>Straying costs a life. Higher levels make the path narrower and longer.", '
             'th:"เริ่มที่<b>จุดเขียว</b> แล้วลากไปยัง<b>จุดแดง</b>โดยไม่ออกนอกทาง!'
             '<br>ออกนอกทางเสียชีวิต เลเวลสูงขึ้นทางแคบและยาวขึ้น"}')
new_intro = ('"trace.intro": {ko:"<b>아무 곳</b>이나 누른 채 움직이면 표식이 <b>초록 점</b>에서 출발해 '
             '손가락을 따라와요. 길을 벗어나지 않고 <b>빨간 점</b>까지 데려가세요!'
             '<br>손가락은 길에서 <b>떨어진 곳</b>을 잡으세요 — 그래야 길이 가려지지 않아요. '
             '손을 떼도 표식은 그대로 있으니 자리를 옮겨 다시 잡아도 됩니다.", '
             'en:"Press <b>anywhere</b> and move — the marker starts at the <b>green dot</b> and follows '
             'your finger. Guide it to the <b>red dot</b> without leaving the path!'
             '<br>Hold <b>away from the marker</b> so your finger never covers the path. '
             'Lift and re-grip whenever you run out of room.", '
             'th:"แตะ<b>ตรงไหนก็ได้</b>แล้วลาก เครื่องหมายจะเริ่มที่<b>จุดเขียว</b>และตามนิ้วคุณไป '
             'พาไปให้ถึง<b>จุดแดง</b>โดยไม่ออกนอกทาง!'
             '<br>จับให้<b>ห่างจากเครื่องหมาย</b> นิ้วจะได้ไม่บังทาง ยกนิ้วแล้วจับใหม่ได้ตลอด"}')
one(old_intro, new_intro, 'trace.intro 문구')

# HTML의 기본 문구(번역 적용 전에 보이는 것)도 맞춘다
one("      <b>초록 점</b>에서 출발해 길을 벗어나지 않고 손가락(마우스)으로 <b>빨간 점</b>까지 이어보세요!<br>",
    "      <b>아무 곳</b>이나 누른 채 움직이면 표식이 <b>초록 점</b>에서 출발해 손가락을 따라와요. "
    "길을 벗어나지 않고 <b>빨간 점</b>까지 데려가세요!<br>",
    'HTML 기본 문구 1')
one("      길을 벗어나면 생명이 줄어요. 레벨이 오를수록 길이 좁고 길어집니다.",
    "      손가락은 길에서 <b>떨어진 곳</b>을 잡으세요 — 그래야 길이 가려지지 않아요. "
    "손을 떼도 표식은 그대로 있으니 자리를 옮겨 다시 잡아도 됩니다.",
    'HTML 기본 문구 2')

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — 트랙패드 방식 조작 · 손 떼고 다시 잡기 · 안내 3언어')
