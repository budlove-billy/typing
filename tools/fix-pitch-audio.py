# -*- coding: utf-8 -*-
"""높은음 찾기 — 소리가 꺼져 있으면 시작할 수 없게 막고, 그 자리에서 켤 수 있게 한다.

문제: 이 게임의 정답 단서는 '음높이' 하나뿐이다. 패드는 소리가 꺼져 있어도 순서대로
      불이 들어오지만 그 불빛에는 높낮이 정보가 없다. 즉 소리를 끈 사람은 찍기밖에
      할 수 없는데, 경고도 대체 수단도 없이 그냥 게임이 시작됐다.
      (멜로디·리듬은 불빛만으로도 풀리므로 해당 없음 — 이 게임만의 문제)
해결: 시작 시 소리 상태를 확인해서, 꺼져 있으면 게임 대신 안내를 띄우고
      '소리 켜고 시작' 버튼 하나로 바로 이어지게 한다.
"""
import io, re

SRC = 'index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
assert 'pt-noaudio' not in s, '이미 적용됨'
NL = '\r\n' if '\r\n' in s[:4000] else '\n'   # 이 파일은 CRLF — 삽입 문자열도 같은 줄바꿈을 써야 매칭된다

# ── 1) 안내 블록 (인트로 카드의 시작 버튼 바로 앞) ─────────────────────────────
btn = '    <button class="btn" onclick="startPitch()" data-i18n="pitch.startGame">게임 시작</button>' + NL
assert s.count(btn) == 1, '높은음 시작 버튼을 못 찾음'
notice = (
    '    <div class="pt-noaudio" id="pt-noaudio" style="display:none">\n'
    '      <div class="pt-noaudio-t">🔇 <span data-i18n="pitch.muteTitle">소리가 꺼져 있어요</span></div>\n'
    '      <p data-i18n="pitch.muteBody">이 게임은 음의 높낮이만으로 정답을 찾습니다. '
    '소리를 켜야 플레이할 수 있어요.</p>\n'
    '      <button class="btn" onclick="ptEnableSound()" data-i18n="pitch.muteBtn">소리 켜고 시작</button>\n'
    '    </div>\n')
s = s.replace(btn, notice + btn, 1)

# ── 2) 스타일 (.pt-pad 규칙 뒤에 붙인다) ──────────────────────────────────────
m = re.search(r'^\.pt-pad\{[^\n]*\n', s, re.M)
assert m, '.pt-pad 규칙 없음'
css = (".pt-noaudio{background:var(--red3);border:1.5px solid var(--red);border-radius:var(--radius2);"
       "padding:1rem;margin-bottom:1rem;text-align:center}\n"
       ".pt-noaudio-t{font-weight:800;color:var(--red2);margin-bottom:.35rem}\n"
       ".pt-noaudio p{font-size:.85rem;color:var(--text2);line-height:1.6;margin-bottom:.8rem}\n")
s = s[:m.end()] + css + s[m.end():]

# ── 3) 시작 시 소리 확인 ─────────────────────────────────────────────────────
old = "function startPitch(){ PT.score=0;"
assert s.count(old) == 1
new = (
    "/* 소리가 꺼져 있으면 이 게임은 찍기밖에 안 된다 — 시작을 막고 켜는 길을 준다 */\n"
    "function ptEnableSound(){ if(!sndOn()) toggleSound(); const n=document.getElementById('pt-noaudio');"
    " if(n) n.style.display='none'; startPitch(); }\n"
    "function startPitch(){\n"
    "  const notice=document.getElementById('pt-noaudio');\n"
    "  if(!sndOn()){ if(notice) notice.style.display='block'; return; }\n"
    "  if(notice) notice.style.display='none';\n"
    "  PT.score=0;")
s = s.replace(old, new, 1)

# ── 4) 번역 ─────────────────────────────────────────────────────────────────
anchor = '  "pitch.startGame": {ko:"게임 시작", en:"Start Game", th:"เริ่มเกม"},'
assert s.count(anchor) == 1
tr = (anchor + '\n'
      '  "pitch.muteTitle": {ko:"소리가 꺼져 있어요", en:"Sound is off", th:"เสียงปิดอยู่"},\n'
      '  "pitch.muteBody": {ko:"이 게임은 음의 높낮이만으로 정답을 찾습니다. 소리를 켜야 플레이할 수 있어요.",'
      ' en:"This game is decided by pitch alone. You need sound on to play.",'
      ' th:"เกมนี้ตัดสินด้วยระดับเสียงล้วน ต้องเปิดเสียงจึงจะเล่นได้"},\n'
      '  "pitch.muteBtn": {ko:"소리 켜고 시작", en:"Turn sound on & start", th:"เปิดเสียงแล้วเริ่ม"},')
s = s.replace(anchor, tr, 1)

# 줄바꿈 정규화 — 이 파일은 CRLF다. 삽입한 줄만 LF로 남으면 뒤섞이므로 통일한다.
s = '\r\n'.join(s.splitlines()) + '\r\n'
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — 안내 블록·스타일·가드·번역 3언어')
