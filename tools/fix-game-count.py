# -*- coding: utf-8 -*-
"""게임 수 표기를 실제와 맞춘다.

확인한 사실:
- 앱의 스킬 게임은 HOME_GAMES 기준 36개(cat.daily 3·cat.fun 7 제외), 36개 모두 screen-<id> 존재.
- guide/brain-games는 33개만 나열하고 제목도 '33종'이라 그 페이지 안에서는 맞지만
  홈(36가지)과 어긋난다. 빠진 셋은 말로우 런·영단어·한글 타자.
→ 가이드에 셋을 채워 넣고 제목·설명·JSON-LD·형제 링크의 33종을 36종으로 올린다.
  숫자만 고치면 목록과 어긋나므로 반드시 항목 추가가 먼저다.

sudoku FAQ의 '15종 이상'도 실제(36)와 동떨어져 있어 다른 페이지와 같은 '30종 이상'으로 맞춘다.
"""
import io, os, re, glob

# ---- 1) 가이드에 빠진 게임 3종 추가 ----
f = 'guide/brain-games/index.html'
s = io.open(f, encoding='utf-8', newline='').read()
assert '말로우 런' not in s, '이미 적용됨'

s = s.replace(
    '      <li><b>말로우 타워</b> — 포크를 피해 마시멜로 타워를 깨물어 내려가는 리듬 게임</li>\n',
    '      <li><b>말로우 타워</b> — 포크를 피해 마시멜로 타워를 깨물어 내려가는 리듬 게임</li>\n'
    '      <li><b>말로우 런</b> — 다가오는 장애물을 제때 뛰어넘는 달리기 게임. 속도가 점점 붙어 판단할 시간이 짧아집니다</li>\n', 1)

s = s.replace(
    '      <li><b>숨은 단어 찾기</b> — 글자 격자에서 숨은 단어를 드래그로 찾기</li>\n',
    '      <li><b>숨은 단어 찾기</b> — 글자 격자에서 숨은 단어를 드래그로 찾기</li>\n'
    '      <li><b>영단어</b> — 뜻을 보고 맞는 영어 단어를 고르는 어휘 게임</li>\n'
    '      <li><b>한글 타자</b> — 화면에 뜬 낱말을 정확하고 빠르게 입력하는 타자 연습</li>\n', 1)

n = len(re.findall(r'<li><b>', s[s.index('<main'):s.index('</main>')]))
assert n == 39, '항목 수가 예상과 다름: %d (게임 36 + 테스트/데일리/운세 3)' % n

s = s.replace('33종', '36종')
io.open(f, 'w', encoding='utf-8', newline='').write(s)
print('ok guide/brain-games — 3종 추가, 나열 36종, 제목·설명·JSON-LD 36종')

# ---- 2) 형제 페이지의 '33종 총정리' 링크 문구 ----
cnt = 0
for g in glob.glob('guide/*/index.html'):
    t = io.open(g, encoding='utf-8', newline='').read()
    if '33종' in t:
        io.open(g, 'w', encoding='utf-8', newline='').write(t.replace('33종', '36종'))
        cnt += 1
        print('   링크 문구 수정', g)
print('형제 페이지 %d곳' % cnt)

# ---- 3) sudoku FAQ의 '15종 이상' ----
f = 'sudoku/index.html'
s = io.open(f, encoding='utf-8', newline='').read()
assert '15종 이상' in s
io.open(f, 'w', encoding='utf-8', newline='').write(s.replace('15종 이상', '30종 이상', 1))
print('ok sudoku FAQ — 15종 이상 → 30종 이상')
