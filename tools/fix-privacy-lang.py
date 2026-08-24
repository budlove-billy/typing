# -*- coding: utf-8 -*-
"""개인정보처리방침 페이지의 언어 처리 결함 수정.

네이버 서치어드바이저 지적 + 사용자 확인 사항:
  1) <H1>이 2개 — 한국어 블록과 영어 블록에 각각 h1이 있고, 보이지 않는 쪽은
     CSS로만 숨긴다. 크롤러는 HTML 소스를 보므로 둘 다 센다.
  2) 영어로 바꿔도 좌측 상단 마스코트 옆 문구가 한글로 남는다(하드코딩).
  3) 본문 상단이 "언어: 한국어 · English" — 라벨이 영어 모드에서도 한글.

추가로 발견:
  4) `/privacy/?lang=en`의 canonical이 언제나 ko 주소라 검색엔진이 ko로 통합한다.
     8/18에 다른 6개 페이지에서 고쳤던 것과 같은 병(이 페이지만 빠져 있었다).
     제목·설명·og도 언어를 따라가지 않는다. hreflang도 없다.

해결
  - h1을 언어 블록 밖으로 꺼내 **하나만** 두고, 안에 언어별 span을 넣는다.
  - 헤더 문구와 언어 라벨도 같은 방식으로 언어별 span.
  - setL()에서 canonical·og:url·title·description을 그 언어 주소로 맞추고
    주소창도 동기화한다(다른 페이지의 syncSEO와 같은 방식).

사이트맵은 건드리지 않는다 — 애드센스 심사 중이라 색인 대상 URL을 늘리지 않는다.
"""
import io, re

f = 'privacy/index.html'
s = io.open(f, encoding='utf-8', newline='').read()
assert 'privacy-lang-fixed' not in s, '이미 적용됨'
NL = '\r\n' if '\r\n' in s[:2000] else '\n'

# ---- 1) CSS: 인라인으로 보여야 하는 자리 확장 ----
old = 'h2 [data-lang]{display:none}h2 [data-lang].on{display:inline}'
assert old in s
new = ('h1 [data-lang],h2 [data-lang],nav [data-lang],.lang [data-lang]{display:none}'
       'h1 [data-lang].on,h2 [data-lang].on,nav [data-lang].on,.lang [data-lang].on{display:inline}'
       '/* privacy-lang-fixed */')
s = s.replace(old, new, 1)

# ---- 2) 헤더 문구 ----
old = '<img src="/mallow-logo.svg" alt="Mallow">Mallow <small>가볍게 즐기는 두뇌게임</small>'
assert old in s
s = s.replace(old,
              '<img src="/mallow-logo.svg" alt="Mallow">Mallow <small>'
              '<span data-lang="ko" class="on">가볍게 즐기는 두뇌게임</span>'
              '<span data-lang="en">light brain games</span></small>', 1)

# ---- 3) 언어 라벨 ----
old = ('  <div class="lang">언어: <a onclick="setL(\'ko\')"><b id="l-ko">한국어</b></a> · '
       '<a onclick="setL(\'en\')"><span id="l-en">English</span></a></div>')
assert old in s, '언어 선택 줄을 못 찾음'
s = s.replace(old,
              '  <div class="lang"><span data-lang="ko" class="on">언어</span>'
              '<span data-lang="en">Language</span>: '
              '<a onclick="setL(\'ko\')"><b id="l-ko">한국어</b></a> · '
              '<a onclick="setL(\'en\')"><span id="l-en">English</span></a></div>' + NL +
              '  <h1><span data-lang="ko" class="on">개인정보처리방침</span>'
              '<span data-lang="en">Privacy Policy</span></h1>', 1)

# ---- 4) 블록 안의 h1 두 개 제거 ----
for old in ('    <h1>개인정보처리방침</h1>' + NL, '    <h1>Privacy Policy</h1>' + NL):
    assert s.count(old) == 1, '블록 안 h1을 못 찾음: %r' % old
    s = s.replace(old, '', 1)
assert s.count('<h1') == 1, 'h1이 %d개 남음' % s.count('<h1')

# ---- 5) hreflang ----
old = '<link rel="canonical" href="https://playmallow.com/privacy/">'
assert old in s
s = s.replace(old, old + NL +
              '<link rel="alternate" hreflang="ko" href="https://playmallow.com/privacy/">' + NL +
              '<link rel="alternate" hreflang="en" href="https://playmallow.com/privacy/?lang=en">' + NL +
              '<link rel="alternate" hreflang="x-default" href="https://playmallow.com/privacy/">', 1)

# ---- 6) setL에서 언어별 SEO 동기화 ----
old = ("function setL(l){document.querySelectorAll('[data-lang]').forEach("
       "e=>e.classList.toggle('on',e.getAttribute('data-lang')===l));" + NL +
       "document.documentElement.lang=l;}")
assert old in s, 'setL을 못 찾음'
new = """/* 언어별 SEO 동기화 — canonical이 언어와 무관하게 ko 주소로 고정돼 있으면
   검색엔진이 ?lang=en 주소를 ko로 통합해 영어 페이지가 색인에서 사라진다. */
const SEO={
 ko:{t:'개인정보처리방침 | Mallow(플레이말로우)',d:'플레이말로우(playmallow.com) 개인정보처리방침 — 쿠키, Google Analytics·AdSense, 브라우저 저장 안내.'},
 en:{t:'Privacy Policy | Mallow',d:'Privacy policy for playmallow.com — cookies, Google Analytics, AdSense and browser storage.'}};
function setL(l){
  document.querySelectorAll('[data-lang]').forEach(e=>e.classList.toggle('on',e.getAttribute('data-lang')===l));
  document.documentElement.lang=l;
  const seo=SEO[l]||SEO.ko, url='https://playmallow.com/privacy/'+(l==='ko'?'':'?lang=en');
  document.title=seo.t;
  const set=(sel,attr,v)=>{const e=document.querySelector(sel); if(e&&v) e.setAttribute(attr,v);};
  set('link[rel="canonical"]','href',url);
  set('meta[property="og:url"]','content',url);
  set('meta[name="description"]','content',seo.d);
  set('meta[property="og:title"]','content',seo.t);
  set('meta[property="og:description"]','content',seo.d);
  try{ if(history.replaceState) history.replaceState(null,'','/privacy/'+(l==='ko'?'':'?lang=en')); }catch(e){}
}"""
s = s.replace(old, new.replace('\n', NL), 1)

io.open(f, 'w', encoding='utf-8', newline='').write(s)
print('ok privacy — h1 %d개 · hreflang %d개' % (s.count('<h1'), s.count('hreflang=')))
