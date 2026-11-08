# -*- coding: utf-8 -*-
"""쉬어가는 게임(/arcade/) 빌드 — assets/playgama-config.js(켜기·끄기) + tools/playgama/content.py(원문) → 정적 HTML.
  python tools/playgama/build.py            사이트용: arcade/index.html·en.html·th.html + sitemap.xml·llms.txt·개인정보처리방침 반영
  python tools/playgama/build.py --preview  미리보기: .logs/arcade-preview/ (켜진 상태로 강제, 배포되지 않음)
설정이 꺼져 있거나 clid가 비어 있으면: 게임 목록을 아예 만들지 않고 '준비 중' 화면 + noindex, 사이트맵·llms·개인정보 문구에서 뺀다.
여러 번 실행해도 된다. (docs/playgama-plan.md)"""
import io, json, os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from content import PAGE, GAMES

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PREVIEW = '--preview' in sys.argv
LANGS = ['ko', 'en', 'th']
URL = {'ko': '/arcade/', 'en': '/arcade/en', 'th': '/arcade/th'}
FILE = {'ko': 'index.html', 'en': 'en.html', 'th': 'th.html'}
OURS_NAME = {  # index.html I18N nav.<id> 와 같게
  'merge': {'ko': '말랑 2048', 'en': 'Mallow 2048', 'th': 'มัลโลว์ 2048'}, 'spot': {'ko': '다른 색 찾기', 'en': 'Odd Color Out', 'th': 'หาสีที่ต่าง'},
  'cards': {'ko': '카드 짝', 'en': 'Card Match', 'th': 'จับคู่การ์ด'}, 'diff': {'ko': '틀린 그림 찾기', 'en': 'Spot the Difference', 'th': 'หาจุดต่าง'},
  'sort': {'ko': '컬러 소트', 'en': 'Color Sort', 'th': 'เรียงสี'}, 'slide': {'ko': '슬라이딩 퍼즐', 'en': 'Slide Puzzle', 'th': 'พัซเซิลเลื่อน'},
  'fit': {'ko': '블록 채우기', 'en': 'Block Fit', 'th': 'ต่อบล็อก'}, 'run': {'ko': '말로우 런', 'en': 'Mallow Run', 'th': 'มาโลว์รัน'}}
e = lambda s: html.escape(str(s), quote=True)

def rd(p): return io.open(p, encoding='utf-8', newline='').read()
def wr(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True); io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

def config():
    s = rd(os.path.join(ROOT, 'assets', 'playgama-config.js'))
    a = s.index('= /*CONFIG*/') + 12  # 머리 주석에도 표시 글자가 있어서 '= '까지 붙여 찾는다
    return json.loads(s[a:s.index('/*END*/', a)])

CFG = config()
LIVE = PREVIEW or bool(CFG.get('enabled') and CFG.get('clid'))
CGAMES = {g['id']: g for g in CFG.get('games', [])}

CSS = '''*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{margin:0;background:radial-gradient(120% 80% at 50% 0%,#e7f3ff 0%,#f5f7fb 55%);color:#1f2a44;font-family:'Pretendard Variable',Pretendard,-apple-system,'Apple SD Gothic Neo','Malgun Gothic','Noto Sans KR',system-ui,sans-serif;line-height:1.65;display:flex;flex-direction:column;align-items:center;min-height:100vh}
header{width:100%;max-width:640px;padding:14px 16px 4px;text-align:center}
h1{margin:6px 0 0;font-size:25px;font-weight:900;letter-spacing:-.4px}
.tag{margin:2px 0 0;color:#5a6683;font-size:14px}
main{width:100%;max-width:640px;padding:10px 14px 36px}
.card{background:#fff;border:1px solid #e4e9f2;border-radius:18px;padding:18px 16px;margin-bottom:14px;box-shadow:0 6px 20px rgba(40,60,110,.06)}
.intro p{margin:0 0 8px;font-size:15.5px}
.notice{font-size:13.5px;color:#4a5570;background:#f2f6fc;border-radius:12px;padding:10px 12px;margin:10px 0 0}
.pg-card h3{margin:0;font-size:19px;font-weight:900;letter-spacing:-.3px}
.pg-meta{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 12px}
.pg-meta span{font-size:12.5px;font-weight:700;background:#eef3ff;color:#3756b8;border-radius:999px;padding:3px 10px}
.pg-poster{position:relative;display:block;width:100%;aspect-ratio:16/9;border:0;padding:0;border-radius:14px;overflow:hidden;cursor:pointer;background:#dde5f2}
.pg-poster img{display:block;width:100%;height:100%;object-fit:cover}
.pg-poster b{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-size:18px;font-weight:900;color:#fff;background:rgba(40,70,200,.88);border-radius:999px;padding:10px 26px;box-shadow:0 6px 18px rgba(0,0,0,.3);white-space:nowrap}
.pg-poster:focus-visible{outline:3px solid #4f7cff;outline-offset:3px}
.pg-stage{margin-top:0}
.pg-bar{display:flex;justify-content:flex-end;margin:0 0 30px}
.pg-close,.pg-btn{font-family:inherit;font-size:15px;font-weight:800;border:1.5px solid #c9d4ea;background:#fff;color:#33415f;border-radius:10px;padding:8px 14px;cursor:pointer}
.pg-frame-wrap{position:relative;width:100%;height:min(78vh,640px);border-radius:12px;overflow:hidden;background:#111}
.pg-frame-wrap iframe{display:block;width:100%;height:100%;border:0}
.pg-wait{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#cfd8ee;font-size:15px}
.pg-fail{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:20px;background:#f7f9fd;text-align:center;font-size:15px}
.pg-body{margin-top:12px;font-size:15px}
.pg-body p{margin:0 0 8px}
.pg-body h4{margin:12px 0 4px;font-size:14.5px;color:#3756b8}
.pg-body ul{margin:0;padding-left:20px}
.pg-ours{display:inline-block;margin-top:10px;font-weight:800;color:#2c6e49;text-decoration:none;background:#eaf7ef;border-radius:10px;padding:7px 12px;font-size:14px}
.off{text-align:center}
.off a{display:inline-block;margin-top:8px;font-weight:900;color:#fff;background:#4f7cff;border-radius:12px;padding:11px 18px;text-decoration:none}
.faq h2{margin:0 0 6px;font-size:18px}
.faq h3{margin:12px 0 2px;font-size:15.5px}
.faq p{margin:0;font-size:14.5px;color:#3a4560}
.back{display:block;text-align:center;margin:6px 0 0;font-weight:800;color:#3756b8;text-decoration:none}
footer{text-align:center;padding:1rem .8rem 1.6rem;font-size:13px;line-height:1.9;color:#6b7794}
footer a{color:inherit;text-decoration:underline;text-underline-offset:2px}
@media (max-width:360px){h1{font-size:22px}.pg-poster b{font-size:16px;padding:9px 20px}}'''

LEGAL = {'ko': ['소개', '문의', '이용약관', '개인정보처리방침', '업데이트 소식'], 'en': ['About', 'Contact', 'Terms', 'Privacy', 'Updates'],
         'th': ['เกี่ยวกับเรา', 'ติดต่อ', 'ข้อกำหนด', 'ความเป็นส่วนตัว', 'อัปเดต']}
def footer(l):
    q = '' if l == 'ko' else '?lang=en'
    links = ' · '.join(f'<a href="/{s}/{q}">{w}</a>' for s, w in zip(['about', 'contact', 'terms', 'privacy', 'updates'], LEGAL[l]))
    return f'<footer><!--mlegal-->{links}<br>© Mallow · playmallow.com</footer>'

def card(g, l):
    t, P = g[l], PAGE[l]
    cg = CGAMES.get(g['id'])
    if not cg or cg.get('enabled') is False: return ''
    home = '/' if l == 'ko' else f'/?lang={l}&'
    ours = f'{home}?game={g["ours"]}'.replace('/??', '/?').replace('&?', '&')
    tips = ''.join(f'<li>{e(x)}</li>' for x in t['tips'])
    return f'''  <article class="card pg-card" data-id="{e(g['id'])}">
    <h3>{e(t['name'])}</h3>
    <div class="pg-meta"><span>{e(g['tags'][l])}</span><span>{e(P['mins'].format(m=g['mins']))}</span></div>
    <button type="button" class="pg-poster" aria-label="{e(t['name'])} {e(P['play'])}"><img src="{e(cg['thumb'])}" alt="" width="480" height="270" loading="lazy" decoding="async"><b>{e(P['play'])}</b></button>
    <div class="pg-stage" hidden></div>
    <div class="pg-body">
      <p>{e(t['intro'])}</p>
      <h4>{e(P['how'])}</h4><p>{e(t['how'])}</p>
      <h4>{e(P['tips'])}</h4><ul>{tips}</ul>
      <h4>{e(P['for'])}</h4><p>{e(t['for'])}</p>
      <a class="pg-ours" href="{e(ours)}">🧠 {e(P['ours'])}: {e(OURS_NAME[g['ours']][l])} →</a>
    </div>
  </article>'''

def page(l):
    P = PAGE[l]; url = 'https://playmallow.com' + URL[l]
    alts = ''.join(f'<link rel="alternate" hreflang="{x}" href="https://playmallow.com{URL[x]}">' for x in LANGS) + \
           '<link rel="alternate" hreflang="x-default" href="https://playmallow.com/arcade/">'
    faq_ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': l, 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in P['faq']]}, ensure_ascii=False)
    home = '/' if l == 'ko' else f'/?lang={l}'
    games = '\n'.join(x for x in (card(g, l) for g in GAMES) if x)
    body_games = f'<section id="pg-games" aria-label="{e(P["h1"])}">\n{games}\n  </section>' if LIVE else ''
    off = f'''  <div class="card off" id="pg-off"{' hidden' if LIVE else ''}><h2 style="margin:0 0 4px;font-size:18px">{e(P['off_h'])}</h2><p style="margin:0">{e(P['off_p'])}</p><a href="{home}">{e(P['off_btn'])}</a></div>'''
    faq = ''.join(f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q, a in P['faq'])
    cfg_src = '/assets/playgama-config.js?v=2'
    preview_override = ('<script>window.PLAYGAMA=Object.assign({},window.PLAYGAMA,{enabled:true,clid:"PREVIEW"});</script>' if PREVIEW else '')
    return f'''<!DOCTYPE html>
<html lang="{l}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{e(P['title'])}</title>
<meta name="description" content="{e(P['desc'])}">
<meta name="robots" content="{'index,follow' if LIVE and not PREVIEW else 'noindex,follow'}">
<meta property="og:title" content="{e(P['title'])}">
<meta property="og:description" content="{e(P['desc'])}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://playmallow.com/og/home.png">
<link rel="canonical" href="{url}">
{alts}
{('<script type="application/ld+json">' + faq_ld + '</script>') if LIVE else ''}
<link rel="icon" type="image/png" href="/favicon-32.png?v=2">
<!-- 이 페이지에는 AdSense를 넣지 않는다(외부 게임 안 광고와 겹침·실수 클릭 방지, 2026-11-08 결정) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9EQEH5BF0C"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9EQEH5BF0C');</script>
<style>{CSS}</style>
<link rel="stylesheet" href="/assets/topbar.css?v=1">
</head>
<body>
<header>
  <a id="backHome" href="{home}">← 홈</a>
  <h1>{e(P['h1'])}</h1>
  <p class="tag">{e(P['tag'])}</p>
</header>
<script src="/assets/topbar.js?v=4"></script>
<main>
  <div class="card intro">{''.join(f'<p>{e(x)}</p>' for x in P['intro'])}<p class="notice">ⓘ {e(P['notice'])}</p></div>
{off}
  {body_games}
  <div class="card faq"><h2>{e(P['faq_h'])}</h2>{faq}</div>
  <a class="back" href="{home}">{e(P['back'])}</a>
</main>
{footer(l)}
<script src="{cfg_src}"></script>
{preview_override}
<script src="/assets/playgama.js?v=2" defer></script>
<script defer src="/seo-events.js"></script>
</body>
</html>
'''

def toggle_block(path, start, end, block, on, anchor):
    """start~end 표시로 감싼 블록을 켜면 anchor 앞에 넣고, 끄면 지운다. 파일의 줄바꿈(CRLF/LF)을 따른다."""
    p = os.path.join(ROOT, path); s = rd(p); nl = '\r\n' if '\r\n' in s else '\n'
    if start in s:
        a = s.index(start); b = s.index(end, a) + len(end)
        if s[b:b + len(nl)] == nl: b += len(nl)
        s = s[:a] + s[b:]
    if on:
        anchor = anchor.replace('\n', nl)
        assert s.count(anchor) == 1, (path, anchor)
        s = s.replace(anchor, (start + '\n' + block + '\n' + end + '\n').replace('\n', nl) + anchor, 1)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)

PRIV_KO = '''    <section>
      <h2>4-1. 외부 게임 (Playgama)</h2>
      <p><a class="inline" href="/arcade/">쉬어가는 게임</a> 페이지의 게임은 외부 게임 플랫폼 <b>Playgama</b>(LeadToChanges L.L.C-FZ)가 제공합니다. 이용자가 <b>플레이 버튼을 누르기 전에는</b> 게임을 불러오지 않습니다.</p>
      <ul>
        <li>플레이를 누르면 게임이 Playgama 서버에서 열리며, Playgama와 그 광고 파트너가 게임 안에서 쿠키·기기 정보를 사용하고 광고를 보여 주거나 선택 구매 화면을 제공할 수 있습니다.</li>
        <li>이 과정의 정보 처리는 Playgama의 정책을 따릅니다. 말로우는 이 게임들을 통해 이용자 개인정보를 따로 수집하지 않습니다.</li>
        <li>외부 게임 이용 기록은 말로우의 기록·미션·연속 기록에 저장되거나 반영되지 않습니다.</li>
      </ul>
    </section>'''
PRIV_EN = '''    <section>
      <h2>4-1. External Games (Playgama)</h2>
      <p>Games on the <a class="inline" href="/arcade/en">Take a Break</a> page are provided by the external game platform <b>Playgama</b> (LeadToChanges L.L.C-FZ). Nothing is loaded from Playgama <b>until you press Play</b>.</p>
      <ul>
        <li>After you press Play, the game opens from Playgama's servers, and Playgama and its advertising partners may use cookies and device information inside the game, show ads, or offer optional purchases.</li>
        <li>That processing is governed by Playgama's policies. Mallow does not collect any personal information through these games.</li>
        <li>Activity in external games is not stored in or counted toward your Mallow records, missions or streaks.</li>
      </ul>
    </section>'''

def sync_names():
    """홈 선반용 게임 이름(ko/en/th)을 설정 파일의 NAMES 칸에 채운다 — 문구 원본은 content.py 하나."""
    p = os.path.join(ROOT, 'assets', 'playgama-config.js'); s = rd(p)
    a = s.index('/*NAMES*/') + 9; b = s.index('/*NAMES_END*/', a)
    names = json.dumps({g['id']: {l: g[l]['name'] for l in LANGS} for g in GAMES}, ensure_ascii=False)
    if s[a:b] != names: io.open(p, 'w', encoding='utf-8', newline='').write(s[:a] + names + s[b:])

def main():
    out = os.path.join(ROOT, '.logs', 'arcade-preview') if PREVIEW else os.path.join(ROOT, 'arcade')
    for l in LANGS: wr(os.path.join(out, FILE[l]), page(l))
    print(('preview' if PREVIEW else 'site'), 'live' if LIVE else 'off', '→', out)
    if PREVIEW: return
    sync_names()
    # 사이트맵·llms·개인정보처리방침: 켜졌을 때만
    toggle_block('sitemap.xml', '  <!--arcade-->', '  <!--/arcade-->',
                 '\n'.join(f'  <url><loc>https://playmallow.com{URL[l]}</loc><lastmod>2026-11-08</lastmod><changefreq>weekly</changefreq><priority>0.5</priority></url>' for l in LANGS),
                 LIVE, '</urlset>')
    toggle_block('llms.txt', '<!--arcade-->', '<!--/arcade-->',
                 '- [쉬어가는 게임](https://playmallow.com/arcade/): 말로우가 고른 외부 웹게임 9가지(Playgama 제공) — 게임별 직접 쓴 소개·요령, 플레이 버튼을 눌러야 열림\n',
                 LIVE, '## 사이트 정보')
    toggle_block('privacy/index.html', '    <!--pg-ko-->', '    <!--/pg-ko-->', PRIV_KO, LIVE, '    <section>\n      <h2>5. 쿠키 거부 방법</h2>')
    toggle_block('privacy/index.html', '    <!--pg-en-->', '    <!--/pg-en-->', PRIV_EN, LIVE, '    <section>\n      <h2>5. How to Refuse Cookies</h2>')

if __name__ == '__main__':
    main()
