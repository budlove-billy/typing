# -*- coding: utf-8 -*-
"""사이트맵에 <lastmod>를 넣는다 — 재제출의 목적이 '이것들이 새/변경됐다'를 알리는 것이므로
   날짜 신호가 있어야 구글이 재크롤 우선순위를 매길 수 있다.
   날짜는 지어내지 않고 git이 기록한 해당 소스 파일의 마지막 커밋 날짜를 쓴다."""
import io, re, os, subprocess

SITE = 'https://playmallow.com/'

def src_of(loc):
    """사이트맵 URL -> 실제 소스 파일"""
    p = loc[len(SITE):].split('?')[0]
    if p == '':
        return 'index.html'
    if p.endswith('/en'):
        return p[:-3] + '/en.html'
    if p.endswith('/th'):
        return p[:-3] + '/th.html'
    return p.rstrip('/') + '/index.html'

def last_commit_date(path):
    try:
        out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', path],
                             capture_output=True, text=True, check=True).stdout.strip()
        return out or None
    except Exception:
        return None

s = io.open('sitemap.xml', encoding='utf-8', newline='').read()
locs = re.findall(r'<loc>(.*?)</loc>', s)

missing = [(l, src_of(l)) for l in locs if not os.path.exists(src_of(l))]
print('URL %d개 · 소스 파일 없는 것 %d개' % (len(locs), len(missing)))
for l, f in missing:
    print('   x', l, '->', f)
assert not missing, '매핑 실패 — 위 URL은 사이트맵에서 빼거나 매핑을 고쳐야 함'

def add_lastmod(m):
    block = m.group(0)
    if '<lastmod>' in block:
        return block
    loc = re.search(r'<loc>(.*?)</loc>', block).group(1)
    d = last_commit_date(src_of(loc))
    if not d:
        return block
    return block.replace('</loc>', '</loc>\n    <lastmod>%s</lastmod>' % d, 1)

out = re.sub(r'  <url>.*?</url>', add_lastmod, s, flags=re.S)
io.open('sitemap.xml', 'w', encoding='utf-8', newline='').write(out)

# 검증
import xml.etree.ElementTree as ET
r = ET.parse('sitemap.xml').getroot()
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = r.findall('s:url', ns)
lm = [u.find('s:lastmod', ns) for u in urls]
print('lastmod 채워진 URL: %d / %d' % (sum(1 for x in lm if x is not None), len(urls)))
from collections import Counter
print('날짜 분포:', dict(Counter(x.text for x in lm if x is not None)))
