# -*- coding: utf-8 -*-
"""사이트 전체에서 Google AdSense 제거 (2026-11-08, 사용자 결정: 여러 번 반려되어 더 신청하지 않음).
- 모든 HTML 머리의 '<!-- Google AdSense -->' + 계정 meta + adsbygoogle 스크립트 3줄을 지운다.
- 개인정보처리방침 4장(광고)을 '지금은 광고 프로그램을 쓰지 않음'으로 바꾼다.
- 신뢰 페이지(소개·문의·약관·업데이트)는 tools/trust-pages/build.py가 만들므로 그쪽을 고친 뒤 다시 빌드한다.
여러 번 실행해도 된다. ads.txt는 남겨 둔다(광고가 없으면 아무 영향 없음)."""
import io, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP = {'.git', '.logs', 'generated_images', 'canvas', 'node_modules', '.claude', '.claudecrab', '.omc'}
PAT = re.compile(r'[ \t]*<!-- Google AdSense -->\r?\n|[ \t]*<meta name="google-adsense-account"[^>]*>\r?\n|[ \t]*<script async src="https://pagead2\.googlesyndication\.com/[^"]*"[^>]*></script>\r?\n')

n = 0
for d, dirs, files in os.walk(ROOT):
    dirs[:] = [x for x in dirs if x not in SKIP]
    for f in files:
        if not f.endswith('.html'): continue
        p = os.path.join(d, f); s = io.open(p, encoding='utf-8', newline='').read()
        t = PAT.sub('', s)
        if t != s: io.open(p, 'w', encoding='utf-8', newline='').write(t); n += 1
print('adsense removed from', n, 'html files')

# 개인정보처리방침 4장
p = os.path.join(ROOT, 'privacy', 'index.html'); s = io.open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
KO = ('      <h2>4. 광고</h2>' + nl +
      '      <p>현재 사이트는 Google AdSense 등 광고 프로그램을 사용하지 않으며, 광고용 쿠키를 심지 않습니다. 광고를 다시 싣게 되면 이 방침을 먼저 고쳐 알리겠습니다.</p>' + nl +
      '      <p>단, 아래 4-1의 외부 게임은 게임 안에서 그 제공자가 광고를 보여 줄 수 있습니다.</p>' + nl)
EN = ('      <h2>4. Advertising</h2>' + nl +
      '      <p>The site currently does not use Google AdSense or any other ad program and sets no advertising cookies. If we start showing ads again, we will update this policy first.</p>' + nl +
      '      <p>External games described in 4-1 below may show ads inside the game, served by their provider.</p>' + nl)
for head, new in (('      <h2>4. 광고 (Google AdSense)</h2>', KO), ('      <h2>4. Advertising (Google AdSense)</h2>', EN)):
    if head in s:
        a = s.index(head); b = s.index('    </section>', a)
        s = s[:a] + new + s[b:]
s = s.replace('쿠키, Google Analytics·AdSense, 브라우저 저장 안내', '쿠키, Google Analytics, 외부 게임, 브라우저 저장 안내')
s = s.replace('cookies, Google Analytics, AdSense and browser storage', 'cookies, Google Analytics, external games and browser storage')
s = s.replace('다만 서비스 품질 개선과 광고 게재를 위해', '다만 서비스 품질 개선을 위해')
io.open(p, 'w', encoding='utf-8', newline='').write(s); print('privacy updated')
