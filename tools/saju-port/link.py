# -*- coding: utf-8 -*-
"""말로우 사주(/saju/) 연결 (2026-11-07, 1회용·기록용).
- 홈 로비 '오늘의 운세' 바로가기 4칸: 띠별 순위 자리를 말로우 사주로(띠별 순위는 운세 탭에 그대로 있다).
- 운세 탭 목록 맨 앞에 말로우 사주.
- /unse/ 결과 아래와 '다른 운세도 보기'에 깊이 보기 안내.
- sitemap.xml · llms.txt · /updates/ 에 추가."""
import os, sys, io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'daily-redesign')); from _patch import Patch
ROOT = os.path.join(os.path.dirname(__file__), '..', '..')

p = Patch(os.path.join(ROOT, 'index.html')); R = p.R
R("""  {id:'unse', emoji:'🌙', key:'nav.unse', grp:'cat.fun', koOnly:true, external:'unse/'},""",
  """  {id:'unse', emoji:'🌙', key:'nav.unse', grp:'cat.fun', koOnly:true, external:'unse/'},
  {id:'saju', emoji:'🧭', key:'nav.saju', grp:'cat.fun', koOnly:true, external:'saju/'},   // 깊은 사주(2026-11-07, D:\\claude\\saju 엔진)""")
R('''  "nav.unse": {ko:"오늘의 운세", en:"Fortune", th:"ดวงวันนี้"},''',
  '''  "nav.unse": {ko:"오늘의 운세", en:"Fortune", th:"ดวงวันนี้"},
  "nav.saju": {ko:"말로우 사주", en:"Saju", th:"ดวงสี่เสา"},''')
R('''  "lb.f.unse": {ko:"생년월일로 보는 오늘 하루의 흐름", en:"Your day by birth date", th:"ดวงรายวันตามวันเกิด"},''',
  '''  "lb.f.unse": {ko:"생년월일로 보는 오늘 하루의 흐름", en:"Your day by birth date", th:"ดวงรายวันตามวันเกิด"},
  "lb.f.saju": {ko:"사주팔자·대운·월운까지 깊게, 매일 바뀌는 내 운세", en:"In-depth Four Pillars reading", th:"ดวงสี่เสาแบบละเอียด"},''')
R("""({ko:['unse','zodiac','ttirank','tarot'],""", """({ko:['saju','unse','zodiac','tarot'],""")
R("""const ids={ko:['unse','zodiac','ttirank','tarot','luckycolor','persona','braintype'],""",
  """const ids={ko:['saju','unse','zodiac','ttirank','tarot','luckycolor','persona','braintype'],""")
p.save()

p = Patch(os.path.join(ROOT, 'unse', 'index.html')); R = p.R
R('''      <p class="links"><a href="/zodiac/">별자리 운세</a>''', '''      <p class="links"><a href="/saju/"><b>말로우 사주 (깊이 보기)</b></a> · <a href="/zodiac/">별자리 운세</a>''')
R('''    <p class="disc">※ 말로우 운세는''', '''    <a href="/saju/" style="display:block;margin:0 0 14px;padding:16px 18px;border-radius:18px;background:linear-gradient(135deg,#7b5ce8,#ff6f9c);color:#fff;text-decoration:none;box-shadow:0 8px 20px rgba(123,92,232,.28)"><b style="font-size:17px">🧭 내 사주 깊이 보기 →</b><br><span style="font-size:14px;opacity:.95">사주팔자 명식 · 오행·십성 · 격국·용신 · 10년 대운 · 12달 월운 · 이번 달 좋은 날 달력</span></a>
    <p class="disc">※ 말로우 운세는''')
p.save()

def add(path, old, new):
    f = os.path.join(ROOT, path); s = io.open(f, encoding='utf-8', newline='').read(); nl = '\r\n' if '\r\n' in s else '\n'
    if new.split('\n')[0] in s: return
    assert s.count(old) == 1, (path, old[:40]); s = s.replace(old, new.replace('\n', nl) + old, 1)
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('patched', path)
add('sitemap.xml', '</urlset>', '  <url><loc>https://playmallow.com/saju/</loc><lastmod>2026-11-07</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>\n')
f = os.path.join(ROOT, 'llms.txt'); s = io.open(f, encoding='utf-8', newline='').read()
if '/saju/' not in s:
    nl = '\r\n' if '\r\n' in s else '\n'
    s = s.replace('## 사이트 정보', '- [말로우 사주](https://playmallow.com/saju/): 절기·경도 보정 만세력 사주팔자, 오행·십성·신강약·격국·용신·합충·신살, 대운·세운·월운·일운 점수와 풀이(브라우저 안 계산)' + nl + nl + '## 사이트 정보', 1)
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('patched llms.txt')
