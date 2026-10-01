# -*- coding: utf-8 -*-
"""모든 공개 페이지 하단에 소개·문의·이용약관·개인정보처리방침·업데이트 소식 링크를 단다(2026-10-02).
전에는 개인정보처리방침이 홈에서만 링크됐다. 다시 실행해도 된다(<!--mlegal--> 표시로 한 번만 넣는다).
- 페이지에 <footer>가 있으면 그 안 끝에, 없으면 </body> 앞에 작은 footer를 새로 만든다.
- en.html → 영어, th.html → 태국어, 나머지 → 한국어 낱말. 링크 대상 페이지는 ko·en만 있다(태국어는 영어판).
- noindex 리다이렉트 스텁은 건너뛴다.
- index.html은 언어 전환 사전(I18N) 키로 넣고, sitemap.xml·llms.txt에 새 페이지 4개를 추가한다."""
import os, io, re, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MARK = '<!--mlegal-->'
WORDS = {
  'ko': ['소개', '문의', '이용약관', '개인정보처리방침', '업데이트 소식'],
  'en': ['About', 'Contact', 'Terms', 'Privacy', 'Updates'],
  'th': ['เกี่ยวกับเรา', 'ติดต่อ', 'ข้อกำหนด', 'ความเป็นส่วนตัว', 'อัปเดต'],
}
SLUGS = ['about', 'contact', 'terms', 'privacy', 'updates']
def links(lang):
    q = '' if lang == 'ko' else '?lang=en'
    return ' · '.join(f'<a href="/{s}/{q}" style="color:inherit;text-decoration:underline;text-underline-offset:2px">{w}</a>' for s, w in zip(SLUGS, WORDS[lang]))   # 어두운 배경 페이지에서도 읽히게 푸터 글자색을 따른다
def rd(p): return io.open(p, encoding='utf-8', newline='').read()
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='').write(s)

files = subprocess.run(['git', 'ls-files', '*.html'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8').stdout.split()
skip = ('tools/', 'generated_images/', 'docs/', 'canvas/', 'mobile/', 'og/', 'shared/', 'assets/')
done, skipped = [], []
for f in files:
    if f.startswith(skip) or '/' not in f and f not in ('en.html', 'th.html') or f in ('index.html',) or f.startswith(tuple(s + '/' for s in SLUGS)):
        continue
    p = os.path.join(ROOT, f); s = rd(p)
    if MARK in s: continue
    if re.search(r'<meta name="robots" content="noindex', s): skipped.append(f); continue
    lang = 'en' if f.endswith('en.html') else 'th' if f.endswith('th.html') else 'ko'
    nl = '\r\n' if '\r\n' in s else '\n'
    i = s.rfind('</footer>')
    if i >= 0:
        s = s[:i] + f'{MARK}<div class="mlegal" style="margin-top:.45rem;font-size:.8rem;line-height:1.9">{links(lang)}</div>' + s[i:]
    else:
        j = s.rfind('</body>'); assert j >= 0, f
        s = s[:j] + f'{MARK}<footer class="mlegal" style="text-align:center;padding:1.2rem .8rem 1.6rem;font-size:.8rem;line-height:1.9;color:#6b7794">{links(lang)}<br>© Mallow · playmallow.com</footer>{nl}' + s[j:]
    wr(p, s); done.append(f)

# privacy: 기존 푸터를 신뢰 페이지와 같은 전체 목록으로
p = os.path.join(ROOT, 'privacy', 'index.html'); s = rd(p)
if MARK not in s:
    ko = ['소개', '문의', '이용약관', '개인정보처리방침', '업데이트 소식']; en = ['About', 'Contact', 'Terms', 'Privacy Policy', 'Updates']
    full = ' · '.join(f'<a href="/{sl}/"><span data-lang="ko" class="on">{k}</span><span data-lang="en">{e}</span></a>' for sl, k, e in zip(SLUGS, ko, en))
    old = re.search(r'<a href="/privacy/"><span data-lang="ko" class="on">개인정보처리방침</span><span data-lang="en">Privacy Policy</span></a>', s)
    s = s[:old.start()] + MARK + full + s[old.end():]
    s = s.replace('© 2026 Mallow · playmallow.com', '© 2026 Mallow · playmallow.com · Billy Lee', 1)
    wr(p, s); done.append('privacy/index.html')

# index.html: 홈 아래 안내 링크 줄(언어 전환 사전 키)
p = os.path.join(ROOT, 'index.html'); s = rd(p); nl = '\r\n' if '\r\n' in s else '\n'
if MARK not in s:
    a = s.index('<div class="site-footer" id="site-footer">'); b = s.index('</div>', a) + len('</div>')
    row = ' · '.join(f'<a href="/{sl}/" data-i18n="legal.{sl}">{k}</a>' for sl, k in zip(SLUGS, WORDS['ko']))
    s = s[:b] + f'{nl}  {MARK}<div class="site-footer site-legal">{row}</div>' + s[b:]
    keys = ''.join(f'{nl}  "legal.{sl}": {{ko:"{k}", en:"{e}", th:"{t}"}},' for sl, k, e, t in zip(SLUGS, WORDS['ko'], WORDS['en'], WORDS['th']))
    anchor = '  "nav.exit": {ko:"홈", en:"Home", th:"หน้าแรก"},'
    assert s.count(anchor) == 1; s = s.replace(anchor, anchor + keys)
    wr(p, s); done.append('index.html')

# sitemap + llms.txt
p = os.path.join(ROOT, 'sitemap.xml'); s = rd(p); nl = '\r\n' if '\r\n' in s else '\n'
add = ''
for sl in ['about', 'contact', 'terms', 'updates']:
    if f'https://playmallow.com/{sl}/<' not in s:
        add += f'  <url><loc>https://playmallow.com/{sl}/</loc><lastmod>2026-10-02</lastmod><changefreq>{"weekly" if sl == "updates" else "monthly"}</changefreq><priority>0.4</priority></url>{nl}'
if add: s = s.replace('</urlset>', add + '</urlset>'); wr(p, s); done.append('sitemap.xml')
p = os.path.join(ROOT, 'llms.txt'); s = rd(p); nl = '\r\n' if '\r\n' in s else '\n'
if '/about/' not in s:
    s = s.rstrip() + nl + nl + '## 사이트 정보' + nl + \
        '- [소개](https://playmallow.com/about/): 운영자(필명 Billy Lee), 만든 이유, 게임 설계 원칙' + nl + \
        '- [업데이트 소식](https://playmallow.com/updates/): 날짜별 변경 기록' + nl + \
        '- [문의](https://playmallow.com/contact/): contact@playmallow.com' + nl + \
        '- [이용약관](https://playmallow.com/terms/) · [개인정보처리방침](https://playmallow.com/privacy/)' + nl
    wr(p, s); done.append('llms.txt')
print('updated', len(done), '· skipped noindex', len(skipped))
