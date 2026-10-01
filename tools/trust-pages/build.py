# -*- coding: utf-8 -*-
"""신뢰 페이지 4종 — /about/ /contact/ /terms/ /updates/ (ko·en, 2026-10-02 애드센스 2차 반려 대응).
개인정보처리방침(/privacy/)과 같은 틀·글꼴·언어 전환(?lang=en). 여러 번 실행해도 된다(덮어씀).
운영자 표기: 필명 Billy Lee (사용자 블로그 mallow.kr과 같은 이름). 연락처: contact@playmallow.com."""
import os, io
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPDATED = '2026-10-02'
LEGAL = [('about', '소개', 'About'), ('contact', '문의', 'Contact'), ('terms', '이용약관', 'Terms'),
         ('privacy', '개인정보처리방침', 'Privacy Policy'), ('updates', '업데이트 소식', 'Updates')]

def footer():
    links = ' · '.join(f'<a href="/{s}/"><span data-lang="ko" class="on">{k}</span><span data-lang="en">{e}</span></a>' for s, k, e in LEGAL)
    return f'''  <footer>
    <a href="/"><span data-lang="ko" class="on">홈</span><span data-lang="en">Home</span></a> · {links}<br>
    © 2026 Mallow · playmallow.com · Billy Lee
  </footer>'''

CSS = '''*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Pretendard Variable',Pretendard,-apple-system,BlinkMacSystemFont,system-ui,Roboto,'Helvetica Neue','Segoe UI','Apple SD Gothic Neo','Noto Sans KR','Malgun Gothic',sans-serif;background:#f5f7fb;color:#182235;line-height:1.75}
nav{background:#fff;border-bottom:1px solid #e4e9f2;height:54px;display:flex;align-items:center;padding:0 1.1rem;position:sticky;top:0;z-index:5}
nav a{display:flex;align-items:center;gap:.45rem;font-weight:700;color:#4f7cff;text-decoration:none;font-size:1.05rem}
nav img{height:28px}
nav a small{color:#21a67a;font-weight:600;font-size:.8rem}
main{max-width:680px;margin:0 auto;padding:1.6rem 1.1rem 3rem}
h1{font-size:1.5rem;margin:.2rem 0 .3rem}
.updated{color:#6b7794;font-size:.85rem;margin-bottom:1.2rem}
.lead{background:#fff;border:1px solid #e4e9f2;border-radius:14px;padding:1.1rem 1.3rem;margin-bottom:1rem;font-size:.97rem;color:#3a4560}
section{background:#fff;border:1px solid #e4e9f2;border-radius:14px;padding:1.2rem 1.3rem;margin-bottom:.9rem}
h2{font-size:1.07rem;margin-bottom:.6rem;color:#4f7cff}
h3{font-size:.98rem;margin:.9rem 0 .35rem}
p{font-size:.95rem;margin-bottom:.55rem}
ul{padding-left:1.15rem;margin:.3rem 0}
li{margin-bottom:.45rem;font-size:.94rem}
a.inline{color:#4f7cff}
.mail{display:inline-block;font-size:1.1rem;font-weight:800;color:#4f7cff;text-decoration:none;background:#eef3ff;border:1px solid #cfdcff;border-radius:10px;padding:.55rem .9rem;margin:.3rem 0 .5rem}
.note{font-size:.88rem;color:#5a6683;background:#f5f7fb;border-radius:8px;padding:.7rem .9rem;margin-top:.6rem}
.log{list-style:none;padding:0}
.log li{border-left:3px solid #cfdcff;padding:.1rem 0 .1rem .8rem;margin-bottom:.8rem}
.log time{display:block;font-size:.8rem;font-weight:700;color:#6b7794}
footer{text-align:center;padding:1.5rem 0;color:#6b7794;font-size:.84rem;line-height:2}
footer a{color:#4f7cff;text-decoration:none;margin:0 .2rem}
.lang{font-size:.85rem;margin-bottom:1rem}
.lang a{color:#4f7cff;text-decoration:none;cursor:pointer}
[data-lang]{display:none}
[data-lang].on{display:block}
h1 [data-lang],h2 [data-lang],nav [data-lang],.lang [data-lang],footer [data-lang]{display:none}
h1 [data-lang].on,h2 [data-lang].on,nav [data-lang].on,.lang [data-lang].on,footer [data-lang].on{display:inline}'''

def page(slug, tko, ten, dko, den, ko, en, jsonld=''):
    url = f'https://playmallow.com/{slug}/'
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{tko} | Mallow(플레이말로우)</title>
<meta name="description" content="{dko}">
<meta name="robots" content="index,follow">
<meta name="author" content="Billy Lee">
<meta property="og:title" content="{tko} | Mallow">
<meta property="og:description" content="{dko}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Mallow">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ko" href="{url}">
<link rel="alternate" hreflang="en" href="{url}?lang=en">
<link rel="alternate" hreflang="x-default" href="{url}">
<link rel="icon" type="image/png" href="/favicon-32.png?v=2">
<!-- Google AdSense -->
<meta name="google-adsense-account" content="ca-pub-8615421634491307">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8615421634491307" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9EQEH5BF0C"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-9EQEH5BF0C');
</script>{jsonld}
<style>{CSS}</style>
</head>
<body>
<nav><a href="/"><img src="/mallow-logo.svg" alt="Mallow">Mallow <small><span data-lang="ko" class="on">가볍게 즐기는 두뇌게임</span><span data-lang="en">light brain games</span></small></a></nav>
<main>
  <div class="lang"><span data-lang="ko" class="on">언어</span><span data-lang="en">Language</span>: <a onclick="setL('ko')">한국어</a> · <a onclick="setL('en')">English</a></div>
  <h1><span data-lang="ko" class="on">{tko}</span><span data-lang="en">{ten}</span></h1>
  <p class="updated"><span data-lang="ko" class="on">최종 수정 {UPDATED} · 작성 Billy Lee</span><span data-lang="en">Last updated {UPDATED} · by Billy Lee</span></p>

  <!-- ================= 한국어 ================= -->
  <div data-lang="ko" class="on">
{ko}
  </div>

  <!-- ================= English ================= -->
  <div data-lang="en">
{en}
  </div>

{footer()}
</main>
<script>
/* 언어별 SEO 동기화(개인정보처리방침과 같은 방식) — ?lang=en이면 영어, 주소가 없으면 사이트에서 고른 언어(en·th → 영어) */
const SEO={{ko:{{t:'{tko} | Mallow(플레이말로우)',d:'{dko}'}},en:{{t:'{ten} | Mallow',d:'{den}'}}}};
function setL(l){{
  document.querySelectorAll('[data-lang]').forEach(e=>e.classList.toggle('on',e.getAttribute('data-lang')===l));
  document.documentElement.lang=l;
  const seo=SEO[l]||SEO.ko, url='{url}'+(l==='ko'?'':'?lang=en');
  document.title=seo.t;
  const set=(sel,attr,v)=>{{const e=document.querySelector(sel); if(e&&v) e.setAttribute(attr,v);}};
  set('link[rel="canonical"]','href',url);
  set('meta[property="og:url"]','content',url);
  set('meta[name="description"]','content',seo.d);
  set('meta[property="og:title"]','content',seo.t);
  set('meta[property="og:description"]','content',seo.d);
  try{{ if(history.replaceState) history.replaceState(null,'','/{slug}/'+(l==='ko'?'':'?lang=en')); }}catch(e){{}}
}}
(function(){{var p=new URLSearchParams(location.search).get('lang'),s='';try{{s=localStorage.getItem('brain.lang')||'';}}catch(e){{}}
  if(p==='en'||(!p&&(s==='en'||s==='th')))setL('en');}})();
</script>
<script defer src="/seo-events.js"></script>
</body>
</html>
'''

MAIL = '<a class="mail" href="mailto:contact@playmallow.com">contact@playmallow.com</a>'

# ---------------------------------------------------------------- 소개
ABOUT_KO = '''    <div class="lead"><b>플레이말로우(Mallow)</b>는 가입·설치 없이 브라우저에서 바로 하는 무료 두뇌게임 사이트입니다. 기억력·집중력·순발력·논리·언어 감각을 쓰는 게임 34종과, 매일 자정에 새 문제가 열리는 오늘의 퍼즐 3종(모아모아·말로우 크라운·말로우 탱고), 재미로 보는 운세 콘텐츠를 한국어·영어·태국어로 제공합니다.</div>
    <section>
      <h2>누가 만드나요</h2>
      <p>플레이말로우는 필명 <b>Billy Lee</b>가 기획하고 만들고 운영합니다. 게임 규칙과 난이도 설계, 퍼즐 검수, 화면·소리 다듬기, 사용자 문의 답변까지 직접 합니다. 같은 필명으로 개인 블로그도 운영하고 있습니다.</p>
      <p>2026년 6월에 만들기 시작해 7월에 문을 열었고, 그 뒤로 꾸준히 게임을 고치고 새로 더하고 있습니다. 주요 변경은 <a class="inline" href="/updates/">업데이트 소식</a>에 모두 공개합니다.</p>
    </section>
    <section>
      <h2>왜 만들었나요</h2>
      <p>두뇌게임이라고 하면 가입을 요구하거나, 앱을 깔아야 하거나, 몇 판 하고 나면 결제를 권하는 경우가 많습니다. 플레이말로우는 <b>잠깐 짬이 날 때 바로 열어서 한두 판 하고 닫을 수 있는 곳</b>을 목표로 합니다. 대신 한 판 한 판이 가볍지만 허술하지 않도록, 규칙과 난이도와 손맛에 시간을 가장 많이 씁니다.</p>
    </section>
    <section>
      <h2>게임을 만드는 원칙</h2>
      <ul>
        <li><b>쉬움·보통·어려움이 게임마다 같은 뜻이 되도록</b> — 모든 게임을 가상 플레이어로 반복해서 돌려 보고, 난이도마다 버티는 시간과 점수 분포가 비슷한 폭이 되도록 맞춥니다(2026년 9월 전체 재조정).</li>
        <li><b>운이 아니라 실력으로</b> — 막다른 판이나 풀 수 없는 퍼즐이 나오지 않게 생성 규칙을 검사합니다. 오늘의 퍼즐은 공개 전에 자동 검사로 문제와 정답에 오류가 없는지 확인합니다.</li>
        <li><b>손이 먼저 이해하도록</b> — 게임마다 전용 배경 그림과 오브젝트, 브라우저에서 직접 합성한 효과음을 넣어 결과를 눈과 귀로 바로 알 수 있게 했습니다.</li>
        <li><b>누구나 읽을 수 있게</b> — 글자 대비를 전 게임에서 측정해 기준에 못 미치는 곳을 없앴고, 320px 폭의 작은 폰에서도 화면이 넘치지 않는지 확인합니다.</li>
      </ul>
    </section>
    <section>
      <h2>기록과 개인정보</h2>
      <p>계정이 없으므로 점수와 기록은 서버가 아니라 <b>여러분의 브라우저 안</b>에만 저장됩니다. 기기를 바꿀 때는 '내 기록'의 백업 기능으로 옮길 수 있습니다. 방문 통계(Google Analytics)와 광고(Google AdSense)에 쓰이는 쿠키는 <a class="inline" href="/privacy/">개인정보처리방침</a>에 정리해 두었습니다.</p>
    </section>
    <section>
      <h2>만드는 방식에 대해 솔직하게</h2>
      <p>개발에는 AI 코딩 도구를 함께 쓰고, 게임 배경과 표지 그림은 이미지 생성 도구로 만든 뒤 게임에 맞게 고르고 손봤습니다. 다만 규칙·난이도·퍼즐 정답은 자동 검사와 직접 플레이로 확인하고, 잘못이 발견되면 고친 내용을 업데이트 소식에 남깁니다.</p>
      <p>플레이말로우의 게임은 가볍게 즐기는 오락이며, 의학적 진단이나 치료·인지 훈련 효과를 약속하지 않습니다. 운세 콘텐츠도 재미로 보는 내용입니다.</p>
    </section>
    <section>
      <h2>연락하기</h2>
      <p>버그, 틀린 퍼즐, 게임 제안, 제휴 문의는 언제든 환영합니다. <a class="inline" href="/contact/">문의 페이지</a>를 보시거나 아래 주소로 메일을 보내 주세요.</p>
      ''' + MAIL + '''
    </section>'''
ABOUT_EN = '''    <div class="lead"><b>Mallow (playmallow.com)</b> is a free brain-game site that runs right in your browser — no sign-up, no install. It offers 34 games for memory, focus, reaction, logic and language, three daily puzzles that refresh at midnight (Moamoa, Mallow Crown, Mallow Tango), and just-for-fun fortune pages, in Korean, English and Thai.</div>
    <section>
      <h2>Who makes it</h2>
      <p>Mallow is designed, built and run by <b>Billy Lee</b> (pen name). That covers game rules and difficulty design, puzzle checking, art and sound polish, and answering your messages. I also write a personal blog under the same name.</p>
      <p>Work began in June 2026 and the site opened in July. Since then games have been fixed, tuned and added regularly — major changes are listed on the <a class="inline" href="/updates/?lang=en">Updates</a> page.</p>
    </section>
    <section>
      <h2>Why it exists</h2>
      <p>Brain-game sites often ask you to register, install an app, or pay after a few rounds. Mallow aims to be <b>the place you open for a couple of quick rounds and close again</b>. To keep each round light but never sloppy, most of the time goes into rules, difficulty and game feel.</p>
    </section>
    <section>
      <h2>How the games are made</h2>
      <ul>
        <li><b>Easy, Normal and Hard mean the same thing in every game</b> — each game is played over and over by simulated players so that survival time and score spread line up across difficulties (full re-tune in September 2026).</li>
        <li><b>Skill, not luck</b> — generators are checked so you never get a dead-end board or an unsolvable puzzle. Daily puzzles are checked automatically for errors in the puzzle and its answer before they go live.</li>
        <li><b>Feel it immediately</b> — every game has its own background art, game objects and sound effects synthesised in the browser, so you can see and hear what happened.</li>
        <li><b>Readable for everyone</b> — text contrast was measured in every game and fixed where it fell short; layouts are checked down to 320 px wide phones.</li>
      </ul>
    </section>
    <section>
      <h2>Your records and privacy</h2>
      <p>There are no accounts, so scores and records are stored <b>only in your own browser</b>, not on a server. Use the backup option in “My Records” to move them to a new device. Cookies used for visit statistics (Google Analytics) and ads (Google AdSense) are explained in the <a class="inline" href="/privacy/?lang=en">Privacy Policy</a>.</p>
    </section>
    <section>
      <h2>An honest note on how it's built</h2>
      <p>I use AI coding tools during development, and the game backgrounds and covers were made with image-generation tools, then selected and adjusted for each game. Rules, difficulty and puzzle answers are checked with automated tests and by playing; when a mistake is found, the fix is recorded on the Updates page.</p>
      <p>Mallow's games are light entertainment. They do not diagnose, treat or promise any cognitive-training effect. Fortune content is for fun only.</p>
    </section>
    <section>
      <h2>Get in touch</h2>
      <p>Bug reports, wrong puzzles, game ideas and partnership requests are all welcome — see the <a class="inline" href="/contact/?lang=en">Contact</a> page or email:</p>
      ''' + MAIL + '''
    </section>'''
ABOUT_LD = '''
<script type="application/ld+json">{"@context":"https://schema.org","@type":"AboutPage","url":"https://playmallow.com/about/","name":"플레이말로우 소개","mainEntity":{"@type":"WebSite","name":"Mallow","alternateName":"플레이말로우","url":"https://playmallow.com/","inLanguage":["ko","en","th"],"author":{"@type":"Person","name":"Billy Lee","email":"contact@playmallow.com"}}}</script>'''

# ---------------------------------------------------------------- 문의
CONTACT_KO = '''    <div class="lead">플레이말로우는 Billy Lee가 혼자 운영하는 사이트라, 보내 주신 메일은 제가 직접 읽고 답합니다. 아래 주소로 편하게 보내 주세요.</div>
    <section>
      <h2>메일 주소</h2>
      ''' + MAIL + '''
      <p>확인하는 대로 답장드립니다. 주말·휴일에는 조금 늦어질 수 있습니다.</p>
    </section>
    <section>
      <h2>이런 내용을 받습니다</h2>
      <ul>
        <li><b>버그·오류</b> — 게임이 멈추거나, 버튼이 눌리지 않거나, 점수가 이상하게 나올 때</li>
        <li><b>퍼즐 오류</b> — 오늘의 퍼즐(모아모아·말로우 크라운·말로우 탱고)에서 답이 이상하거나 뜻이 애매한 낱말이 있을 때</li>
        <li><b>난이도·조작 의견</b> — 너무 어렵거나 쉬운 게임, 손에 잘 안 맞는 조작</li>
        <li><b>번역</b> — 영어·태국어 문장이 어색한 곳</li>
        <li><b>개인정보 관련 요청</b> — 쿠키·광고 설정에 대한 질문(<a class="inline" href="/privacy/">개인정보처리방침</a> 참고)</li>
        <li><b>제휴·기타 문의</b></li>
      </ul>
    </section>
    <section>
      <h2>빨리 고치려면 이렇게 알려 주세요</h2>
      <ul>
        <li>게임 이름과 난이도</li>
        <li>기기와 브라우저(예: 갤럭시 S23 · 삼성 인터넷, 아이폰 · 사파리, PC · 크롬)</li>
        <li>무엇을 했을 때 어떤 일이 생겼는지, 가능하면 화면 캡처</li>
        <li>오늘의 퍼즐이라면 날짜</li>
      </ul>
      <p class="note">플레이말로우는 계정이 없어 기록이 브라우저에만 저장됩니다. 그래서 메일로 기록을 복구해 드릴 수는 없습니다. 기기를 바꾸기 전에 '내 기록'의 백업 기능을 써 주세요.</p>
    </section>
    <section>
      <h2>보내 주신 의견은 이렇게 쓰입니다</h2>
      <p>실제로 받은 피드백으로 고친 것들이 많습니다 — 길 따라가기에서 손가락이 길을 가리는 문제, 멜로디 기억의 정답음이 다음 멜로디처럼 들리던 문제, 리듬 게임 터치 패드 위치 등. 고친 내용은 <a class="inline" href="/updates/">업데이트 소식</a>에 남깁니다. 메일 주소는 답장에만 쓰고 다른 곳에 공유하지 않습니다.</p>
    </section>'''
CONTACT_EN = '''    <div class="lead">Mallow is run by one person, Billy Lee, so every email is read and answered by me. Feel free to write to the address below.</div>
    <section>
      <h2>Email</h2>
      ''' + MAIL + '''
      <p>I reply as soon as I can; weekends and holidays may take a little longer. Korean or English are both fine.</p>
    </section>
    <section>
      <h2>What you can write about</h2>
      <ul>
        <li><b>Bugs</b> — a game freezes, a button doesn't respond, a score looks wrong</li>
        <li><b>Puzzle errors</b> — a strange answer or an ambiguous word in a daily puzzle</li>
        <li><b>Difficulty and controls</b> — a game that's too hard or easy, controls that feel off</li>
        <li><b>Translation</b> — awkward English or Thai text</li>
        <li><b>Privacy requests</b> — questions about cookies and ads (see the <a class="inline" href="/privacy/?lang=en">Privacy Policy</a>)</li>
        <li><b>Partnerships and anything else</b></li>
      </ul>
    </section>
    <section>
      <h2>Help me fix it faster</h2>
      <ul>
        <li>Game name and difficulty</li>
        <li>Device and browser (e.g. iPhone · Safari, PC · Chrome)</li>
        <li>What you did and what happened — a screenshot helps a lot</li>
        <li>For a daily puzzle, the date</li>
      </ul>
      <p class="note">Mallow has no accounts and keeps records only in your browser, so records can't be restored by email. Please use the backup option in “My Records” before switching devices.</p>
    </section>
    <section>
      <h2>How your feedback is used</h2>
      <p>Many fixes came straight from player feedback — the finger hiding the path in Trace, the Melody Memory success sound that sounded like the next melody, the rhythm game's tap-pad position, and more. Fixes are listed on the <a class="inline" href="/updates/?lang=en">Updates</a> page. Your email address is used only to reply and is never shared.</p>
    </section>'''

# ---------------------------------------------------------------- 이용약관
TERMS_KO = '''    <div class="lead">이 약관은 플레이말로우(playmallow.com, 이하 '사이트')를 이용할 때의 기본 규칙입니다. 사이트를 이용하면 이 약관에 동의한 것으로 봅니다. 시행일: 2026년 10월 2일.</div>
    <section>
      <h2>1. 서비스</h2>
      <p>사이트는 브라우저에서 하는 두뇌게임, 오늘의 퍼즐, 재미로 보는 운세 콘텐츠와 관련 안내 글을 무료로 제공합니다. 운영자는 필명 Billy Lee입니다. 게임과 기능은 예고 없이 추가·변경·중단될 수 있으며, 주요 변경은 <a class="inline" href="/updates/">업데이트 소식</a>에 알립니다.</p>
    </section>
    <section>
      <h2>2. 계정과 기록</h2>
      <p>사이트에는 회원 가입이 없습니다. 점수·기록·설정은 이용자의 브라우저 저장소(localStorage)에만 저장되며, 브라우저 데이터를 지우거나 기기를 바꾸면 사라질 수 있습니다. 운영자는 서버에 기록을 보관하지 않으므로 사라진 기록을 복구할 수 없습니다. 백업 기능으로 직접 보관해 주세요.</p>
    </section>
    <section>
      <h2>3. 이용자가 지켜야 할 것</h2>
      <ul>
        <li>자동화 프로그램이나 스크립트로 점수를 조작하거나, 사이트에 과도한 요청을 보내 서비스를 방해하지 않습니다.</li>
        <li>광고를 부정하게 클릭하거나 클릭을 유도하지 않습니다.</li>
        <li>사이트의 그림·퍼즐·글·코드를 허락 없이 복제해 다른 곳에 게시하거나 판매하지 않습니다.</li>
        <li>공유 기능(결과 이미지·도전장)을 다른 사람을 괴롭히거나 속이는 데 쓰지 않습니다.</li>
      </ul>
    </section>
    <section>
      <h2>4. 권리</h2>
      <p>사이트의 게임 설계, 퍼즐, 글, 그림, 캐릭터(말로우), 소리와 코드에 대한 권리는 운영자에게 있습니다. 개인적·비상업적 목적으로 결과 화면을 캡처해 공유하는 것은 자유롭게 할 수 있습니다. 스도쿠·2048처럼 널리 알려진 게임 방식 자체에 대한 권리를 주장하지는 않습니다.</p>
    </section>
    <section>
      <h2>5. 광고와 외부 링크</h2>
      <p>사이트는 운영비를 위해 Google AdSense 광고를 게재할 수 있습니다. 광고 내용과 광고주가 제공하는 상품·서비스는 운영자가 보증하지 않습니다. 쿠키 사용은 <a class="inline" href="/privacy/">개인정보처리방침</a>을 따릅니다.</p>
    </section>
    <section>
      <h2>6. 책임의 한계</h2>
      <p>두뇌게임은 오락이며 의학적 진단·치료나 지능 측정을 대신하지 않습니다. IQ 테스트·두뇌 유형·성격 유형 결과는 재미와 참고용입니다. 운세·타로·행운색은 재미로 보는 콘텐츠이며, 이를 근거로 한 투자·건강·법률 등 중요한 결정에 대해 운영자는 책임지지 않습니다. 운영자는 사이트를 안정적으로 유지하려 노력하지만, 일시적인 중단이나 오류가 없음을 보장하지는 않습니다.</p>
    </section>
    <section>
      <h2>7. 약관 변경과 문의</h2>
      <p>약관을 바꿀 때는 이 페이지의 시행일을 고치고 업데이트 소식에 알립니다. 약관에 대한 문의는 <a class="inline" href="/contact/">문의 페이지</a> 또는 contact@playmallow.com으로 보내 주세요. 이 약관은 대한민국 법을 따릅니다.</p>
    </section>'''
TERMS_EN = '''    <div class="lead">These terms are the basic rules for using Mallow (playmallow.com, “the site”). By using the site you agree to them. Effective date: 2 October 2026.</div>
    <section>
      <h2>1. The service</h2>
      <p>The site provides free browser brain games, daily puzzles, just-for-fun fortune content and related guides. It is run by Billy Lee (pen name). Games and features may be added, changed or removed without notice; major changes are announced on the <a class="inline" href="/updates/?lang=en">Updates</a> page.</p>
    </section>
    <section>
      <h2>2. Accounts and records</h2>
      <p>There is no registration. Scores, records and settings are stored only in your browser (localStorage) and may be lost if you clear browser data or change devices. The operator keeps no records on a server and cannot restore lost records — please use the backup option.</p>
    </section>
    <section>
      <h2>3. Your responsibilities</h2>
      <ul>
        <li>Do not manipulate scores with bots or scripts, or disrupt the service with excessive requests.</li>
        <li>Do not click ads fraudulently or encourage others to do so.</li>
        <li>Do not copy and republish or sell the site's art, puzzles, text or code without permission.</li>
        <li>Do not use sharing features (result images, challenges) to harass or deceive others.</li>
      </ul>
    </section>
    <section>
      <h2>4. Ownership</h2>
      <p>Rights to the site's game designs, puzzles, text, art, the Mallow character, sounds and code belong to the operator. You are free to capture and share result screens for personal, non-commercial use. No claim is made to well-known game formats themselves, such as Sudoku or 2048.</p>
    </section>
    <section>
      <h2>5. Ads and external links</h2>
      <p>The site may show Google AdSense ads to cover running costs. The operator does not endorse advertised products or services. Cookie use follows the <a class="inline" href="/privacy/?lang=en">Privacy Policy</a>.</p>
    </section>
    <section>
      <h2>6. Limitation of liability</h2>
      <p>The games are entertainment and do not replace medical diagnosis, treatment or intelligence testing. IQ test, brain-type and personality results are for fun and reference. Fortune, tarot and lucky-colour content is for fun only; the operator is not responsible for investment, health, legal or other important decisions based on it. The operator tries to keep the site running smoothly but does not guarantee it will be free of interruptions or errors.</p>
    </section>
    <section>
      <h2>7. Changes and contact</h2>
      <p>When these terms change, the effective date on this page is updated and the change is announced on the Updates page. Questions about these terms can be sent via the <a class="inline" href="/contact/?lang=en">Contact</a> page or to contact@playmallow.com. These terms are governed by the laws of the Republic of Korea.</p>
    </section>'''

# ---------------------------------------------------------------- 업데이트 소식 (docs/CHANGELOG.md에서 이용자에게 보이는 변화만 골라 쉬운 말로)
LOG = [
 ('2026-09-30', '글자 맞추기 보통·어려움에서 한 글자를 "?"로 가림', 'Word Scramble: one letter now hidden as "?" on Normal and Hard', '나머지 글자로 단어를 추리해 빈자리에 넣어야 합니다. 맞히면 정답 단어를 잠깐 보여 줍니다.', 'You deduce the word from the other letters to place it; the full word is shown briefly when you solve it.'),
 ('2026-09-30', '말로우 타워 새 그림', 'Mallow Tower redrawn', '탑 블록을 파스텔 마시멜로 큐브로, 장애물을 은빛 포크로 바꾸고, 깨물 때 이빨 자국이 남으며 블록이 날아가는 연출을 더했습니다.', 'Tower blocks are now pastel marshmallow cubes and the obstacles silver forks; each bite leaves a tooth mark as the block flies off.'),
 ('2026-09-30', '리듬 게임 터치 패드를 화면 가운데로', 'Rhythm game tap pad centred', '패드가 한쪽으로 치우쳐 보이던 문제를 고쳤습니다(이용자 제보).', 'Fixed the pad sitting off-centre (player report).'),
 ('2026-09-28', '홈 화면 새 단장과 오늘의 행운 카드', 'New home screen and the daily lucky card', '오늘의 두뇌 3판을 모두 하면 행운 카드가 열립니다. 게임 표지 37장을 각 게임의 대표 물건이 들어간 그림으로 새로 그렸고, 운세 탭을 따로 만들었습니다.', 'Finish today\'s three brain games to flip a lucky card. All 37 game covers were redrawn around each game\'s key object, and fortune got its own tab.'),
 ('2026-09-28', '상단바와 "← 홈" 버튼 통일', 'Unified top bar and "← Home" button', '페이지마다 세 가지로 달랐던 돌아가기 버튼을 하나로 맞췄습니다.', 'The back button, which came in three different styles, is now the same everywhere.'),
 ('2026-09-28', '멜로디 기억 성공음을 박수로', 'Melody Memory success sound is now a clap', '정답음이 다음 멜로디의 첫 음처럼 들려 헷갈린다는 의견을 반영했습니다.', 'Players said the old chime sounded like the first note of the next melody.'),
 ('2026-09-28', '오늘의 퍼즐 3종 디자인·소리 개편', 'Daily puzzles: new look and sound', '모아모아·말로우 크라운·말로우 탱고에 전용 배경과 효과음을 넣었습니다.', 'Moamoa, Mallow Crown and Mallow Tango got their own art and sound effects.'),
 ('2026-09-27', '모든 게임의 난이도 다시 맞춤', 'Difficulty re-tuned across every game', '가상 플레이어로 게임마다 반복해서 돌려 보고, 쉬움·보통·어려움이 어느 게임에서나 비슷한 무게가 되도록 고쳤습니다.', 'Every game was played repeatedly by simulated players so that Easy, Normal and Hard feel equally weighted in every game.'),
 ('2026-09-27', '효과음 전면 교체', 'All sound effects replaced', '삐 소리 수준이던 효과음을 게임마다 어울리는 소리로 바꿨습니다.', 'Beep-like sounds were replaced with effects designed for each game.'),
 ('2026-09-27', '스킬 게임 33종 "게임 월드" 디자인', 'A "game world" look for 33 skill games', '게임마다 고유한 배경 세계와 화면 꾸밈을 입혔고, 말로우 런은 황혼 숲 횡스크롤로 새로 만들었습니다.', 'Each game got its own background world; Mallow Run was rebuilt as a twilight-forest side-scroller.'),
 ('2026-08-23', '게임 안내 글 보강', 'Game guides expanded', '스도쿠·네모로직·2048·반응속도 등 안내 페이지에 실제 풀이 기법과 흔한 실수를 더했습니다.', 'Guide pages for Sudoku, Nonogram, 2048, reaction time and more now include real solving techniques and common mistakes.'),
 ('2026-08-22', '글자 대비 전수 점검', 'Text contrast checked in every game', '읽기 어려운 글자색을 모든 게임에서 찾아 고쳤습니다.', 'Hard-to-read text colours were found and fixed in all games.'),
 ('2026-08-22', '길 따라가기 조작 개선', 'Trace: better controls', '손가락이 길을 가리지 않도록 트랙패드 방식으로 바꾸고, 벗어남 판정을 하나의 규칙으로 정리했습니다(이용자 피드백).', 'Switched to trackpad-style control so your finger no longer hides the path, and simplified the off-path rule (player feedback).'),
 ('2026-08-18', '태국어 콘텐츠 확대', 'More Thai content', '태국어 안내와 랜딩 페이지를 영어와 같은 수준으로 채웠습니다.', 'Thai guides and landing pages brought up to the same level as English.'),
 ('2026-08-05', '오늘의 운세 풀이 방식 개선', 'Daily fortune reworked', '무작위 문장 대신 생년월일과 날짜로 십성(十星)을 계산해 풀이합니다.', 'Readings are now derived from your birth date and today\'s date instead of random lines.'),
 ('2026-08-01', '요일별 행운색 페이지', 'Lucky colour by day', '태국 이용자 요청으로 요일별 행운색 페이지를 만들었습니다.', 'Added at the request of Thai players.'),
 ('2026-07-30', '점수 공정성과 기록 구조 개편', 'Fairer scoring and records', '지인 테스트 피드백 다섯 가지를 반영해 난이도별 점수와 최고 기록 방식을 고쳤습니다.', 'Five pieces of tester feedback led to fairer difficulty scoring and best-record tracking.'),
 ('2026-07-27', '글자 맞추기 개선', 'Word Scramble improved', '같은 단어 반복, 힌트, 오답 처리 등 일곱 가지를 고쳤습니다.', 'Seven fixes including repeated words, hints and wrong-answer handling.'),
 ('2026-07-17', '오늘의 논리 퍼즐 2종', 'Two daily logic puzzles', '말로우 크라운과 말로우 탱고를 열었습니다. 매일 자정 새 문제가 나옵니다.', 'Launched Mallow Crown and Mallow Tango, with a new puzzle every midnight.'),
 ('2026-07-16', '말로우 성격 유형', 'Mallow persona test', '성격 유형 테스트를 더했습니다(한국어·영어·태국어).', 'Added a personality test in Korean, English and Thai.'),
 ('2026-07-12', '오늘의 운세와 새 게임 7종', 'Daily fortune and seven new games', '생년월일로 보는 오늘의 운세와 함께 리듬·블록 맞추기·네모로직·글자 맞추기 등 게임 7종을 한꺼번에 추가했습니다.', 'A birth-date daily fortune, plus seven new games at once including Rhythm, Block Fit, Nonogram and Word Scramble.'),
 ('2026-07-11', '말로우 타워·컬러 소트·말랑 2048·다른 모양 찾기', 'Mallow Tower, Color Sort, Mallow 2048, Odd Shape', '새 게임 네 가지와 공략 가이드 6편을 추가했습니다.', 'Four new games and six strategy guides.'),
 ('2026-07-10', '플레이말로우라는 이름으로 출발', 'Launched as Mallow', 'Mallow라는 이름과 로고를 정하고, 기기를 바꿔도 기록을 옮길 수 있는 백업 기능을 넣었습니다.', 'The site took the name and logo Mallow, and gained a backup feature to move your records between devices.'),
]
def log_html(lang):
    i, j = (1, 3) if lang == 'ko' else (2, 4)
    return '\n'.join(f'        <li><time datetime="{r[0]}">{r[0]}</time><b>{r[i]}</b><br>{r[j]}</li>' for r in LOG)
UPD_KO = '''    <div class="lead">플레이말로우에서 무엇이 언제 바뀌었는지 기록합니다. 이용자 의견으로 고친 것도 함께 적습니다. 의견은 <a class="inline" href="/contact/">문의 페이지</a>로 보내 주세요.</div>
    <section>
      <h2>최근 소식</h2>
      <ul class="log">
''' + log_html('ko') + '''
      </ul>
    </section>'''
UPD_EN = '''    <div class="lead">A record of what changed on Mallow and when, including fixes made from player feedback. Send yours via the <a class="inline" href="/contact/?lang=en">Contact</a> page.</div>
    <section>
      <h2>Latest changes</h2>
      <ul class="log">
''' + log_html('en') + '''
      </ul>
    </section>'''

PAGES = [
 ('about', '플레이말로우 소개', 'About Mallow', '플레이말로우(playmallow.com)는 Billy Lee가 만들고 운영하는 무료 두뇌게임 사이트입니다. 만든 이유, 게임 설계 원칙, 기록과 개인정보 안내.', 'Mallow (playmallow.com) is a free brain-game site made and run by Billy Lee — why it exists, how the games are designed, and how your records are kept.', ABOUT_KO, ABOUT_EN, ABOUT_LD),
 ('contact', '문의하기', 'Contact', '플레이말로우 문의 — 버그, 퍼즐 오류, 게임 제안, 제휴 문의는 contact@playmallow.com으로 보내 주세요.', 'Contact Mallow — send bug reports, puzzle errors, game ideas and partnership requests to contact@playmallow.com.', CONTACT_KO, CONTACT_EN, ''),
 ('terms', '이용약관', 'Terms of Use', '플레이말로우(playmallow.com) 이용약관 — 서비스, 기록 저장, 이용자 의무, 권리, 광고, 책임의 한계.', 'Terms of use for playmallow.com — the service, record storage, your responsibilities, ownership, ads and liability.', TERMS_KO, TERMS_EN, ''),
 ('updates', '업데이트 소식', 'Updates', '플레이말로우 업데이트 기록 — 새 게임, 난이도 조정, 디자인·소리 개선, 이용자 의견으로 고친 내용.', 'Mallow update log — new games, difficulty tuning, art and sound improvements, and fixes from player feedback.', UPD_KO, UPD_EN, ''),
]
for slug, tko, ten, dko, den, ko, en, ld in PAGES:
    d = os.path.join(ROOT, slug); os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n').write(page(slug, tko, ten, dko, den, ko, en, ld))
    print('wrote', slug + '/index.html')
