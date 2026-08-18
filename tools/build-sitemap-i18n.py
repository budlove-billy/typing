# -*- coding: utf-8 -*-
"""sitemap.xml에 언어 변형 URL을 hreflang과 함께 등록.
   sitemap의 hreflang은 렌더링 없이도 읽히므로, 다국어 페이지 발견의 가장 확실한 경로다."""
import io, re

MULTI = {                     # 경로 -> 지원 언어
 '': ['ko','en','th'],
 'zodiac/': ['ko','en','th'],
 'persona/': ['ko','en','th'],
 'queens/': ['ko','en','th'],
 'tango/': ['ko','en','th'],
 'luckycolor/': ['ko','en','th'],
 'tarot/': ['ko','th'],
}
SITE = 'https://playmallow.com/'
FREQ = {'': ('weekly','1.0')}

s = io.open('sitemap.xml', encoding='utf-8').read()
blocks = re.findall(r'  <url>.*?</url>\n', s, re.S)
assert blocks, 'no url blocks'

out = []
for b in blocks:
    loc = re.search(r'<loc>(.*?)</loc>', b).group(1)
    path = loc[len(SITE):]
    if path not in MULTI:
        out.append(b)
        continue
    langs = MULTI[path]
    changefreq = re.search(r'<changefreq>(.*?)</changefreq>', b)
    priority = re.search(r'<priority>(.*?)</priority>', b)
    cf = changefreq.group(1) if changefreq else 'weekly'
    pr = priority.group(1) if priority else '0.8'
    alts = ''.join('\n    <xhtml:link rel="alternate" hreflang="%s" href="%s%s%s"/>'
                   % (l, SITE, path, '' if l == 'ko' else '?lang='+l) for l in langs)
    alts += '\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>' % (SITE, path)
    # 언어마다 하나씩 <url> 엔트리를 만들고, 각 엔트리가 같은 대체 목록을 갖게 한다(상호 참조 필수)
    for l in langs:
        u = SITE + path + ('' if l == 'ko' else '?lang='+l)
        # XML에서 & 는 이스케이프가 필요하지만 여기 URL엔 쿼리가 하나뿐이라 &가 없다
        out.append('  <url>\n    <loc>%s</loc>\n    <changefreq>%s</changefreq>\n    <priority>%s</priority>%s\n  </url>\n'
                   % (u, cf, '1.0' if (path == '' and l == 'ko') else ('0.7' if l != 'ko' else pr), alts))

head = s[:s.index('  <url>')]
tail = s[s.rindex('</url>\n')+len('</url>\n'):]
io.open('sitemap.xml', 'w', encoding='utf-8').write(head + ''.join(out) + tail)
print('url 개수:', len(out))
