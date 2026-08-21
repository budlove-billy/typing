# -*- coding: utf-8 -*-
"""콤보 점수의 상한 — 16개 게임에 복사돼 있던 같은 식을 공통 helper 하나로 모은다.

문제(실측): 점수식이 `10 + (콤보-1)*2` 누적이라 총점이 '한 판에 처리한 문제 수의 제곱'으로
커졌다. 그 결과 (1) 같은 실력으로 5판을 돌려도 점수가 3.1~3.4배 흔들리고
(2) 기준점수(GAME_REF)를 한 판에 몇 배씩 넘겨 능력 레이더가 전부 100%로 평평해졌다.

해결: 콤보 보너스에 상한을 둔다. 콤보 11부터는 한 문제당 30점으로 고정 →
한 판 총점이 문제 수에 대해 선형에 가까워진다. 콤보를 쌓는 재미(10→30점, 3배)는 남는다.
"""
import io, re

SRC = 'index.html'

HELPER = """/* ───────── 콤보 보너스 상한 ─────────
   16개 게임이 같은 식 `10+(콤보-1)*2`를 각자 복사해 쓰고 있었다. 상한이 없어 총점이
   '판에서 처리한 문제 수의 제곱'으로 커졌고, 그래서 (a) 같은 실력의 점수 분산이 3.1~3.4배
   (b) 기준점수를 한 판에 몇 배씩 초과 → 능력 레이더가 전부 100%로 평평해졌다.
   (측정: .logs/balance_bot2.mjs · .logs/balance_var.mjs)
   콤보 11부터 보너스를 고정하면 총점이 문제 수에 선형이 되고, 쌓는 재미(10→30점)는 남는다.
   여기 한 곳만 고치면 16게임에 동시에 적용된다. */
const COMBO_CAP=10;
function comboBonus(c){ return Math.min(Math.max(0,(c|0)-1), COMBO_CAP)*2; }   // 0 ~ 20
function comboPts(c){ return 10 + comboBonus(c); }                             // 10 ~ 30
"""

s = io.open(SRC, encoding='utf-8', newline='').read()
assert 'function comboPts' not in s, '이미 적용됨'

# 1) helper 정의를 난이도 배수(dmScore) 바로 앞에 넣는다 — 둘 다 점수 계산의 공통부.
anchor = "/* ───────── 난이도 배수 ─────────"
assert s.count(anchor) == 1
s = s.replace(anchor, HELPER + anchor, 1)

# 2) 표준형 14곳: `10 + (XX.combo-1)*2` (공백 유무 무관) → comboPts(XX.combo)
pat_std = re.compile(r'10\s*\+\s*\(([A-Z]{2})\.combo\s*-\s*1\)\s*\*\s*2')
s, n_std = pat_std.subn(lambda m: 'comboPts(%s.combo)' % m.group(1), s)

# 3) anagram — 단어 길이가 기본점이라 보너스만 교체
old_ag = 'comboB=(AG.combo-1)*2'
assert s.count(old_ag) == 1, 'anagram 점수식 형태가 바뀜'
s = s.replace(old_ag, 'comboB=comboBonus(AG.combo)', 1)

# 4) wordsearch — 마찬가지로 보너스만 교체
old_ws = '[...tt.word].length*4+(WS.combo-1)*2'
assert s.count(old_ws) == 1, 'wordsearch 점수식 형태가 바뀜'
s = s.replace(old_ws, '[...tt.word].length*4+comboBonus(WS.combo)', 1)

# 줄바꿈 정규화 — 이 파일은 CRLF다. 삽입한 줄만 LF로 남으면 뒤섞이므로 통일한다.
s = '\r\n'.join(s.splitlines()) + '\r\n'
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('표준형 치환 %d곳 + anagram 1 + wordsearch 1 = %d곳' % (n_std, n_std + 2))
assert n_std == 14, '표준형이 14곳이어야 함 (실제 %d)' % n_std

# 검증: 옛 식이 남아있지 않은지
left = re.findall(r'\([A-Z]{2}\.combo\s*-\s*1\)\s*\*\s*2', s)
print('남은 옛 식:', len(left))
assert not left
