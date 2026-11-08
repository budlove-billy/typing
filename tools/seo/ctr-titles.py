# -*- coding: utf-8 -*-
"""네이버 검색 클릭률 개선 (2026-11-08, 서치어드바이저 30일: 노출 많고 CTR 낮은 페이지).
- 스도쿠 공략: '스도쿠 푸는법' 노출 1,273·CTR 0.3% → 제목·설명에 '푸는법', 맨 위 3줄 요약 + 바로 하기 버튼
- 2048 공략: '2048 게임 공략' 노출 186·CTR 0.5% → 제목·설명 + 3줄 요약
- 네모로직: 노출 901·CTR 1.2% → '푸는 법' 추가
- 스트룹: 노출 837·CTR 2.0% → 설명 앞에 '스트룹 테스트란?' 한 줄
본문 내용과 다른 과장은 넣지 않는다. 한 번만 실행(이미 적용되면 건너뜀)."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'daily-redesign'))
from _patch import Patch

def run(rel, marker, pairs):
    p = Patch(os.path.join(ROOT, rel))
    if marker in p.s: print('skip', rel); return
    for a, b in pairs: p.R(a, b)
    p.save()

SUMMARY_CSS = '.sum{background:#eef4ff;border:1px solid #cfdcff;border-radius:14px;padding:.9rem 1rem;margin:.2rem 0 1rem}.sum b.h{display:block;font-size:.95rem;margin-bottom:.35rem}.sum ol{margin:0;padding-left:1.2rem}.sum li{margin:.2rem 0}.sum .cta{margin-top:.7rem}\n'

# 1) 스도쿠 공략
T1 = '스도쿠 푸는법 — 초보도 추측 없이 푸는 5단계'
D1 = '스도쿠 푸는법을 순서대로: ① 숫자별로 훑기(스캐닝) ② 이 칸엔 이것뿐(유일 후보) ③ 숨은 싱글 ④ 노트 ⑤ 쌍 소거. 초보부터 어려움 난이도까지 예시와 함께 정리.'
run('guide/sudoku/index.html', 'class="sum"', [
    ('<title>스도쿠 공략 — 추측 없이 푸는 5가지 기법 | Mallow</title>', f'<title>{T1} | Mallow</title>'),
    ('<meta name="description" content="스도쿠 초보부터 고수까지: 스캐닝, 유일 후보, 숨은 싱글, 노트 활용, 쌍 소거까지 추측 없이 푸는 기법을 예시와 함께 정리했습니다.">', f'<meta name="description" content="{D1}">'),
    ('<meta property="og:title" content="스도쿠 공략 — 추측 없이 푸는 5가지 기법 | Mallow">', f'<meta property="og:title" content="{T1} | Mallow">'),
    ('<meta property="og:description" content="스도쿠 초보부터 고수까지: 스캐닝, 유일 후보, 숨은 싱글, 노트 활용, 쌍 소거까지 추측 없이 푸는 기법을 예시와 함께 정리했습니다.">', f'<meta property="og:description" content="{D1}">'),
    ('"headline":"스도쿠 공략 — 추측 없이 푸는 5가지 기법"', f'"headline":"{T1}"'),
    ('› 스도쿠 공략 — 추측 없이 푸는 법</div>', '› 스도쿠 푸는법</div>'),
    ('<h1>스도쿠 공략 — 추측 없이 푸는 법</h1>', '<h1>스도쿠 푸는법 — 추측 없이 푸는 5단계</h1>'),
    ('.tip{', SUMMARY_CSS + '.tip{'),
    ('  <article>\n    <h2>기본 규칙 30초 요약</h2>',
     '  <div class="sum"><b class="h">스도쿠 푸는법 3줄 요약</b><ol>'
     '<li>규칙: 각 행·열·3×3 박스에 1~9가 한 번씩.</li>'
     '<li>숫자 하나를 골라 들어갈 자리가 한 곳뿐인 칸부터 채운다(스캐닝·숨은 싱글).</li>'
     '<li>막히면 찍지 말고 노트로 후보를 적어 지워 나간다.</li></ol>'
     '<a class="cta" data-seo-role="summary_cta" href="/?game=sudoku&amp;from=guide-sudoku-top">배운 대로 스도쿠 바로 해 보기 →</a></div>\n'
     '  <article>\n    <h2>기본 규칙 30초 요약</h2>'),
])

# 2) 2048 공략
T2 = '2048 게임 공략·잘하는 법 — 코너 하나로 2048 만드는 순서'
D2 = '2048 게임 공략: 가장 큰 타일을 한 코너에 고정하고, 위쪽 밀기를 봉인하고, ㄹ자(스네이크)로 쌓는 순서만 지키면 됩니다. 되돌리기 타이밍까지 정리.'
run('guide/2048/index.html', 'class="sum"', [
    ('<title>2048 게임 공략 — 코너 전략과 스네이크 배열 | Mallow</title>', f'<title>{T2} | Mallow</title>'),
    ('<meta property="og:title" content="2048 게임 공략 — 코너 전략과 스네이크 배열 | Mallow">', f'<meta property="og:title" content="{T2} | Mallow">'),
    ('"headline":"2048 게임 공략 — 코너 전략과 스네이크 배열"', f'"headline":"{T2}"'),
    ('.tip{', SUMMARY_CSS + '.tip{'),
    ('  <article>\n    <h2>원칙 1 — 최대 타일을 한 코너에 고정</h2>',
     '  <div class="sum"><b class="h">2048 공략 3줄 요약</b><ol>'
     '<li>가장 큰 타일을 한 구석(예: 왼쪽 아래)에 두고 절대 옮기지 않는다.</li>'
     '<li>그 코너 쪽 두 방향(왼쪽·아래)만 주로 쓰고, 위로 밀기는 하지 않는다.</li>'
     '<li>큰 수부터 ㄹ자로 줄 세워 한 번에 연쇄로 합친다.</li></ol></div>\n'
     '  <article>\n    <h2>원칙 1 — 최대 타일을 한 코너에 고정</h2>'),
])
# 2048 설명은 원문 길이가 달라 별도 처리
p = Patch(os.path.join(ROOT, 'guide/2048/index.html'))
import re
for tag in ('name="description"', 'property="og:description"'):
    m = re.search(r'<meta ' + tag + r' content="([^"]*)">', p.s)
    if m and '코너에 고정하고' not in m.group(1): p.s = p.s.replace(m.group(0), f'<meta {tag} content="{D2}">', 1)
p.save()

# 3) 네모로직
T3 = '네모로직 무료 게임 + 푸는 법 — 노노그램 바로 하기'
p = Patch(os.path.join(ROOT, 'nonogram/index.html'))
if T3 not in p.s:
    p.R('<title>네모로직 (노노그램) 무료 온라인 — 픽셀 로직 퍼즐 | Mallow</title>', f'<title>{T3} | Mallow</title>')
    p.R('<meta property="og:title" content="네모로직 (노노그램) 무료 온라인 — 픽셀 로직 퍼즐 | Mallow">', f'<meta property="og:title" content="{T3} | Mallow">')
    m = re.search(r'<meta name="description" content="([^"]*)">', p.s)
    p.s = p.s.replace(m.group(0), '<meta name="description" content="네모로직(노노그램)을 무료로 바로 하고, 푸는 법도 함께: 줄 앞 숫자만큼 연속으로 칠하고, 확실한 칸부터 칠하고 아닌 칸은 X. 가입·설치 없음, 답이 하나뿐인 판만 출제.">', 1)
    p.save()

# 4) 스트룹
p = Patch(os.path.join(ROOT, 'stroop/index.html'))
m = re.search(r'<meta name="description" content="([^"]*)">', p.s)
if m and not m.group(1).startswith('스트룹 테스트란'):
    p.s = p.s.replace(m.group(0), '<meta name="description" content="스트룹 테스트란? 글자 뜻과 색이 다를 때(빨강이라고 쓴 파란 글자) 뇌가 헷갈리는 현상을 이용한 집중력 테스트입니다. 잉크 색을 맞히는 60초 게임으로 무료로 바로 해 보세요.">', 1)
    p.save()
