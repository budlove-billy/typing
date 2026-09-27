# -*- coding: utf-8 -*-
"""상단바 통일 (1회용, 기록용, 2026-09-28 사용자 승인) — 오늘의 퍼즐·운세 9개 페이지에 공통 상단바(/assets/topbar.css·js)를 붙이고,
사이트 본체 게임 화면의 '← 나가기'를 '← 홈'으로 바꾼다. 여러 번 실행해도 된다."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'daily-redesign')); from _patch import Patch
PAGES = ['moamoa', 'queens', 'tango', 'unse', 'zodiac', 'ttirank', 'tarot', 'luckycolor', 'persona']
V = '?v=1'
for pg in PAGES:
    p = Patch(os.path.join(ROOT, pg, 'index.html'))
    if '/assets/topbar.js' in p.s: print('skip', pg); continue
    p.R('</head>', '<link rel="stylesheet" href="/assets/topbar.css%s">\n</head>' % V)
    p.R('</header>', '</header>\n<script src="/assets/topbar.js%s"></script>' % V)
    p.save()
p = Patch(os.path.join(ROOT, 'index.html'))
if '"nav.exit": {ko:"홈"' not in p.s:
    p.R('"nav.exit": {ko:"나가기", en:"Exit", th:"ออก"},', '"nav.exit": {ko:"홈", en:"Home", th:"หน้าแรก"},')
    p.R('<span data-i18n="nav.exit">나가기</span>', '<span data-i18n="nav.exit">홈</span>')
    p.save()
