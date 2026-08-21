# -*- coding: utf-8 -*-
"""넓은 화면에서 판이 작게 고정돼 있던 게임들 — 퍼즐 계열만 키운다.

측정(.logs/space_audit.mjs, 1280×900): 게임 카드는 812px인데 판은 270~480px에 묶여 있어
활용률이 33~59%였다. 길 따라가기·틀린 그림에서 지적된 것과 같은 문제다.

다만 전부 키우면 안 된다. **반응속도·협응 계열은 판 크기가 곧 난이도**다 —
두더지(whack)·다른색 찾기(spot)·다른모양(odd)·받기(catch)·반응속도(react)·순간기억(flash)·
순서잇기(trail)는 판이 커지면 눈·손이 움직일 거리가 늘어 체감 난이도와 점수가 달라진다.
방금 봇으로 재보정한 GAME_REF가 무효가 되므로 손대지 않는다.

여기서 키우는 건 '크기가 난이도를 바꾸지 않는' 것들뿐이다:
  스도쿠 · 슬라이딩 퍼즐 · 2048 · 컬러소트 · 블록 채우기 — 수·이동 횟수·논리로 점수가 나므로
  판이 커져도 난이도가 그대로다. 읽기만 편해진다.
높은음 찾기 패드도 같이 키운다 — 소리로 푸는 게임이라 패드 크기는 난이도와 무관한데
화면 절반이 비어 있었다(모바일에서 카드가 432/844에서 끝났다).

`min()`을 써서 좁은 화면에서는 지금 값 그대로 유지된다.
"""
import io

SRC = 'index.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s[:4000] else '\n'
assert '/* 넓은 화면에서만 커진다' not in s, '이미 적용됨'


def one(old, new, what):
    global s
    assert s.count(old) == 1, what + ' — 대상을 못 찾음(또는 여러 개)'
    s = s.replace(old, new, 1)


NOTE = '/* 넓은 화면에서만 커진다 — 크기가 난이도를 바꾸지 않는 퍼즐 계열만 */' + NL

# 스도쿠 — 9×9라 커질수록 숫자가 잘 보인다. 숫자패드도 같이 맞춘다.
one(".sk-board{display:grid;grid-template-columns:repeat(9,1fr);grid-template-rows:repeat(9,1fr);width:100%;max-width:480px;",
    NOTE + ".sk-board{display:grid;grid-template-columns:repeat(9,1fr);grid-template-rows:repeat(9,1fr);width:100%;max-width:min(100%,560px);",
    '스도쿠 판')
one(".sk-numpad{display:grid;grid-template-columns:repeat(9,1fr);gap:.4rem;max-width:480px;",
    ".sk-numpad{display:grid;grid-template-columns:repeat(9,1fr);gap:.4rem;max-width:min(100%,560px);",
    '스도쿠 숫자패드')

# 슬라이딩 퍼즐 · 2048 — 타일 수가 정해져 있어 크기가 난이도와 무관
one(".sl-board{position:relative;width:100%;max-width:380px;",
    ".sl-board{position:relative;width:100%;max-width:min(100%,500px);",
    '슬라이딩 판')
one(".mr-board-wrap{max-width:380px;",
    ".mr-board-wrap{max-width:min(100%,500px);",
    '2048 판')

# 컬러소트 — 병이 커지면 색·기호가 잘 보인다(점수는 시간·이동수 기준이라 무관)
one(".so-tubes{display:flex;flex-wrap:wrap;gap:.9rem 1rem;justify-content:center;max-width:420px;",
    ".so-tubes{display:flex;flex-wrap:wrap;gap:.9rem 1rem;justify-content:center;max-width:min(100%,560px);",
    '컬러소트 병')

# 블록 채우기 — 조각을 끌어다 놓는 게임이라 판이 크면 조작이 쉬워진다(논리는 그대로)
one(".ft-board{display:grid;gap:2px;justify-content:center;max-width:360px;",
    ".ft-board{display:grid;gap:2px;justify-content:center;max-width:min(100%,500px);",
    '블록 판')

# 높은음 찾기 — 소리로 푸는 게임이라 패드 크기는 난이도와 무관. 화면이 비어 있었다.
one(".pt-pads{display:flex;flex-wrap:wrap;gap:.7rem;justify-content:center;max-width:330px;margin:1.1rem auto}",
    NL.join([
        ".pt-pads{display:flex;flex-wrap:wrap;gap:.8rem;justify-content:center;max-width:min(100%,520px);margin:1.4rem auto}",
        "/* 패드는 화면 폭을 따라 커진다 — 소리로 푸는 게임이라 크기가 난이도를 바꾸지 않는다 */"]),
    '높은음 패드 영역')
one(".pt-pad{width:74px;height:74px;border:none;border-radius:16px;background:#7e57f0;opacity:.58;cursor:pointer;font-size:1.5rem;",
    ".pt-pad{width:clamp(74px,20vw,116px);height:clamp(74px,20vw,116px);border:none;border-radius:20px;background:#7e57f0;opacity:.58;cursor:pointer;font-size:1.9rem;",
    '높은음 패드 크기')

s = NL.join(s.splitlines()) + NL
io.open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('ok — 스도쿠·슬라이딩·2048·컬러소트·블록·높은음 (반응속도 계열은 의도적으로 제외)')
