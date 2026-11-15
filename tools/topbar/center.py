# -*- coding: utf-8 -*-
"""게임 화면 상단바: 게임 이름을 화면 정가운데로(3칸 격자) + 휴대폰 바 높이 58→48px (2026-11-16, 사용자 요청).
홈 화면 상단(로고·소개 문구)은 그대로 둔다. 따로 만든 페이지 상단바는 assets/topbar.css에서 같은 방식으로 고쳤다. 여러 번 실행해도 된다."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'daily-redesign'))
from _patch import Patch
p = Patch(os.path.join(ROOT, 'index.html'))
if '/* 게임 화면 상단바 가운데 정렬' in p.s: print('already'); sys.exit()
a = "@media (max-width:480px){ body.ingame .nav-brand,body.ingame .nav-mascot{display:none} body.ingame .nav-logo{padding-left:.55rem} body.ingame .lang-select{max-width:76px} }"
p.R(a, a + "\n/* 게임 화면 상단바 가운데 정렬(2026-11-16): 왼쪽 홈 · 가운데 게임 이름 · 오른쪽 소리/언어 */\n"
    "body.ingame nav{display:grid;grid-template-columns:1fr minmax(0,auto) 1fr}\n"
    "body.ingame .nav-exit{justify-self:start}\n"
    "body.ingame .nav-logo{justify-self:center;padding:0 .4rem}\n"
    "body.ingame .lang-select-wrap{justify-self:end}\n"
    "@media (max-width:640px){ body.ingame nav{height:48px} body.ingame .nav-exit{min-height:34px;padding:.35rem .7rem;font-size:.86rem;border-radius:10px} body.ingame .lang-select-wrap{padding-right:.6rem} }")
p.save()
