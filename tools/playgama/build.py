# -*- coding: utf-8 -*-
"""말로우 아케이드(/arcade/) 빌드 — assets/playgama-config.js(켜기·끄기) + tools/playgama/content.py(원문) → 정적 HTML.
  python tools/playgama/build.py            사이트용: arcade/index.html·en.html·th.html + sitemap.xml·llms.txt·개인정보처리방침 반영
  python tools/playgama/build.py --preview  미리보기: .logs/arcade-preview/ (켜진 상태로 강제, 배포되지 않음)
설정이 꺼져 있거나 clid가 비어 있으면: 게임 목록을 아예 만들지 않고 '준비 중' 화면 + noindex, 사이트맵·llms·개인정보 문구에서 뺀다.
여러 번 실행해도 된다. (docs/playgama-plan.md)"""
import io, json, os, sys, html, shutil
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
  'fit': {'ko': '블록 채우기', 'en': 'Block Fit', 'th': 'ต่อบล็อก'}, 'run': {'ko': '말로우 런', 'en': 'Mallow Run', 'th': 'มาโลว์รัน'},
  'chop': {'ko': '말로우 타워', 'en': 'Mallow Tower', 'th': 'หอมัลโลว์'}, 'trace': {'ko': '길 따라가기', 'en': 'Path Trace', 'th': 'ลากตามทาง'},
  'react': {'ko': '반응 속도', 'en': 'Reaction', 'th': 'ความไว'}, 'math': {'ko': '암산 게임', 'en': 'Math Game', 'th': 'เกมคำนวณ'},
  'whack': {'ko': '말로우 팡팡', 'en': 'Mallow Pop', 'th': 'ตีมัลโลว์'}, 'flank': {'ko': '화살표 집중', 'en': 'Arrow Focus', 'th': 'ลูกศรโฟกัส'},
  'catch': {'ko': '마시멜로 받기', 'en': 'Catch Mallow', 'th': 'รับมาร์ชเมลโล่'}}
e = lambda s: html.escape(str(s), quote=True)

def rd(p): return io.open(p, encoding='utf-8', newline='').read()
def wr(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True); io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

def config():
    s = rd(os.path.join(ROOT, 'assets', 'playgama-config.js'))
    a = s.index('= /*CONFIG*/') + 12  # 머리 주석에도 표시 글자가 있어서 '= '까지 붙여 찾는다
    return json.loads(s[a:s.index('/*END*/', a)])

CFG = config()
TODAY = '2026-11-08'  # 사이트맵 lastmod — 페이지 구조를 크게 바꿀 때 고친다
LIVE = PREVIEW or bool(CFG.get('enabled') and CFG.get('clid'))
CGAMES = {g['id']: g for g in CFG.get('games', [])}

LEGAL = {'ko': ['소개', '문의', '이용약관', '개인정보처리방침', '업데이트 소식'], 'en': ['About', 'Contact', 'Terms', 'Privacy', 'Updates'],
         'th': ['เกี่ยวกับเรา', 'ติดต่อ', 'ข้อกำหนด', 'ความเป็นส่วนตัว', 'อัปเดต']}
def footer(l):
    q = '' if l == 'ko' else '?lang=en'
    links = ' · '.join(f'<a href="/{s}/{q}">{w}</a>' for s, w in zip(['about', 'contact', 'terms', 'privacy', 'updates'], LEGAL[l]))
    return f'<footer><!--mlegal-->{links}<br>© Mallow · playmallow.com</footer>'

CSS = '''*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{margin:0;background:#12122a;color:#ecebff;font-family:'Pretendard Variable',Pretendard,-apple-system,'Apple SD Gothic Neo','Malgun Gothic','Noto Sans KR',system-ui,sans-serif;line-height:1.65;display:flex;flex-direction:column;align-items:center;min-height:100vh}
header{width:100%;max-width:960px;padding:14px 16px 4px;text-align:center}
h1{margin:6px 0 0;font-size:25px;font-weight:900;letter-spacing:-.4px}
.tag{margin:2px 0 0;color:#b9b6e6;font-size:14.5px}
.crumb{display:inline-block;font-size:14.5px;font-weight:800;color:#b9a8ff;text-decoration:none;margin-bottom:2px}
main{width:100%;max-width:960px;padding:10px 14px 36px}
.card{background:#1c1c3a;border:1px solid #2e2d5a;border-radius:18px;padding:16px;margin-bottom:14px}
.intro p{margin:0 0 8px;font-size:15.5px}
.notice{font-size:13.5px;color:#cfcdf2;background:#262552;border-radius:12px;padding:10px 12px;margin:10px 0 0}
.ag-h{display:flex;align-items:center;gap:8px;margin:18px 2px 10px;font-size:19px;font-weight:900}
.chips{display:flex;gap:7px;overflow-x:auto;padding:2px 2px 10px;scrollbar-width:none}.chips::-webkit-scrollbar{display:none}
.chip{flex-shrink:0;font-family:inherit;font-size:14.5px;font-weight:800;color:#d9d7ff;background:#24234a;border:1px solid #3a3970;border-radius:999px;padding:7px 15px;cursor:pointer}
.chip.on{background:#7c4dff;border-color:#7c4dff;color:#fff}
.ag-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
@media (min-width:600px){.ag-grid{grid-template-columns:repeat(3,1fr)}}
@media (min-width:860px){.ag-grid{grid-template-columns:repeat(4,1fr)}}
.ag-card{position:relative;display:block;background:#1c1c3a;border:1.5px solid #2e2d5a;border-radius:16px;overflow:hidden;color:inherit;text-decoration:none;transition:transform .12s,border-color .12s}
.ag-card:hover,.ag-card:focus-visible{border-color:#8f6bff;transform:translateY(-2px);outline:none}
.ag-card[hidden]{display:none}
.ag-th{display:block;aspect-ratio:16/10;background:#2a2950;overflow:hidden}
.ag-th img{display:block;width:100%;height:100%;object-fit:cover}
.ag-hot{position:absolute;top:8px;left:8px;font-style:normal;font-size:12.5px;font-weight:900;color:#fff;background:#ff7a1a;border-radius:8px;padding:2px 9px;box-shadow:0 2px 6px rgba(0,0,0,.35)}
.ag-tx{display:block;padding:9px 11px 12px}
.ag-tx b{display:block;font-size:15.5px;font-weight:900;line-height:1.3;word-break:keep-all}
.ag-tx small{display:block;margin-top:3px;font-size:12.5px;color:#a8a6d8}
.pg-meta{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px}
.pg-meta span{font-size:12.5px;font-weight:800;background:#2c2a5e;color:#cfc6ff;border-radius:999px;padding:3px 10px}
.pg-poster{position:relative;display:block;width:100%;aspect-ratio:16/9;border:0;padding:0;border-radius:14px;overflow:hidden;cursor:pointer;background:#2a2950}
.pg-poster img{display:block;width:100%;height:100%;object-fit:cover}
.pg-poster b{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-size:19px;font-weight:900;color:#fff;background:rgba(124,77,255,.92);border-radius:999px;padding:11px 30px;box-shadow:0 6px 18px rgba(0,0,0,.4);white-space:nowrap}
.pg-poster:focus-visible{outline:3px solid #a58bff;outline-offset:3px}
.pg-bar{display:flex;justify-content:flex-end;margin:0 0 10px}
.pg-close,.pg-btn{font-family:inherit;font-size:15px;font-weight:800;border:1.5px solid #4a4890;background:#24234a;color:#ecebff;border-radius:10px;padding:8px 14px;cursor:pointer}
.pg-frame-wrap{position:relative;width:100%;height:min(80vh,680px);border-radius:12px;overflow:hidden;background:#000}
.pg-frame-wrap iframe{display:block;width:100%;height:100%;border:0}
.pg-wait{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#cfd8ee;font-size:15px}
.pg-fail{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:20px;background:#1c1c3a;text-align:center;font-size:15px}
.pg-body{font-size:15.5px}
.pg-body p{margin:0 0 8px}
.pg-body h3{margin:14px 0 4px;font-size:16px;color:#b9a8ff}
.pg-body ul{margin:0;padding-left:20px}
.pg-ours{display:inline-block;margin-top:12px;font-weight:800;color:#0f3d26;text-decoration:none;background:#9ff0c4;border-radius:10px;padding:8px 13px;font-size:14.5px}
.off{text-align:center}
.off a{display:inline-block;margin-top:8px;font-weight:900;color:#fff;background:#7c4dff;border-radius:12px;padding:11px 18px;text-decoration:none}
.faq h2{margin:0 0 6px;font-size:18px}
.faq h3{margin:12px 0 2px;font-size:15.5px}
.faq p{margin:0;font-size:14.5px;color:#cfcdf2}
.back{display:block;text-align:center;margin:14px 0 0;font-weight:800;color:#b9a8ff;text-decoration:none}
footer{text-align:center;padding:1rem .8rem 1.6rem;font-size:13px;line-height:1.9;color:#9896c8}
footer a{color:inherit;text-decoration:underline;text-underline-offset:2px}
@media (max-width:360px){h1{font-size:22px}.ag-grid{gap:9px}.ag-tx b{font-size:14.5px}}'''

CAT = {'puzzle': {'ko': '퍼즐', 'en': 'Puzzle', 'th': 'พัซเซิล'}, 'match': {'ko': '매치·짝맞추기', 'en': 'Match', 'th': 'จับคู่'},
       'casual': {'ko': '캐주얼', 'en': 'Casual', 'th': 'สบาย ๆ'}, 'arcade': {'ko': '아케이드', 'en': 'Arcade', 'th': 'อาร์เคด'},
       'action': {'ko': '액션', 'en': 'Action', 'th': 'แอ็กชัน'}, 'racing': {'ko': '레이싱', 'en': 'Racing', 'th': 'แข่งรถ'},
       'strategy': {'ko': '전략·디펜스', 'en': 'Strategy', 'th': 'กลยุทธ์'}, 'sim': {'ko': '경영·시뮬', 'en': 'Simulation', 'th': 'จำลอง'},
       'sports': {'ko': '스포츠', 'en': 'Sports', 'th': 'กีฬา'}, 'girls': {'ko': '꾸미기', 'en': 'Dress up', 'th': 'แต่งตัว'},
       'card': {'ko': '카드·보드', 'en': 'Card & board', 'th': 'การ์ด·บอร์ด'}, 'kids': {'ko': '어린이', 'en': 'Kids', 'th': 'เด็ก'}}
UI = {'ko': {'all': '전체', 'hot': 'Hot', 'list': '게임 목록', 'more': '다른 게임도 해 보세요', 'back_list': '← 말로우 아케이드 목록',
             'title': '{n} 무료 웹게임 — 게임방법·게임TIP | 말로우 아케이드 | Mallow', 'crumb': '말로우 아케이드'},
      'en': {'all': 'All', 'hot': 'Hot', 'list': 'Games', 'more': 'Try another game', 'back_list': '← All Mallow Arcade games',
             'title': '{n} — free web game, how to play & tips | Mallow', 'crumb': 'Mallow Arcade'},
      'th': {'all': 'ทั้งหมด', 'hot': 'Hot', 'list': 'รายการเกม', 'more': 'ลองเกมอื่นด้วย', 'back_list': '← รายการมาโลว์อาร์เคด',
             'title': '{n} เกมเว็บฟรี — วิธีเล่นและเคล็ดลับ | Mallow', 'crumb': 'มาโลว์อาร์เคด'}}
GAME_MARK = '<!--pg-game-->'
BASE = '/.logs/arcade-preview/' if PREVIEW else '/arcade/'

def hub_url(l):
    return BASE + FILE[l] if PREVIEW else URL[l]
def gurl(gid, l):
    if PREVIEW: return f'{BASE}{gid}/{FILE[l]}'
    return f'/arcade/{gid}/' if l == 'ko' else f'/arcade/{gid}/{l}'
def live_games():
    return [g for g in GAMES if CGAMES.get(g['id']) and CGAMES[g['id']].get('enabled') is not False and CGAMES[g['id']].get('url')]

def tile(g, l, i=0):
    t = g[l]; cg = CGAMES[g['id']]
    hot = f'<i class="ag-hot">{UI[l]["hot"]}</i>' if g.get('hot') else ''
    lazy = ' loading="lazy"' if i > 3 else ''
    return (f'<a class="ag-card" data-id="{e(g["id"])}" data-cat="{e(g["cat"])}" href="{e(gurl(g["id"], l))}#play">'
            f'<span class="ag-th"><img src="{e(cg["thumb"])}" alt="" width="480" height="300"{lazy} decoding="async"></span>{hot}'
            f'<span class="ag-tx"><b>{e(t["name"])}</b><small>{e(CAT[g["cat"]][l])} · {e(PAGE[l]["mins"].format(m=g["mins"]))}</small></span></a>')

def head(l, title, desc, url, alts, ld, og_img='https://playmallow.com/og/home.png'):
    robots = 'index,follow' if LIVE and not PREVIEW else 'noindex,follow'
    ldtag = ('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>') if LIVE and ld else ''
    return f'''<!DOCTYPE html>
<html lang="{l}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://playmallow.com{url}">
<meta property="og:image" content="{e(og_img)}">
<link rel="canonical" href="https://playmallow.com{url}">
{alts}
{ldtag}
<link rel="icon" type="image/png" href="/favicon-32.png?v=2">
<!-- AdSense 없음(사이트 전체 제거, 2026-11-08) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9EQEH5BF0C"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9EQEH5BF0C');</script>
<style>{CSS}</style>
<link rel="stylesheet" href="/assets/topbar.css?v=2">
</head>'''

def tail(l):
    pv = '<script>window.PLAYGAMA=Object.assign({},window.PLAYGAMA,{enabled:true,clid:"PREVIEW"});</script>' if PREVIEW else ''
    return f'''{footer(l)}
<script src="/assets/playgama-config.js?v=3"></script>
{pv}
<script src="/assets/playgama.js?v=3" defer></script>
<script defer src="/seo-events.js"></script>
</body>
</html>
'''

def off_box(l):
    P = PAGE[l]; home = '/' if l == 'ko' else f'/?lang={l}'
    return f'''  <div class="card off" id="pg-off"{' hidden' if LIVE else ''}><h2 style="margin:0 0 4px;font-size:18px">{e(P['off_h'])}</h2><p style="margin:0">{e(P['off_p'])}</p><a href="{home}">{e(P['off_btn'])}</a></div>'''

def page(l):
    """허브: 분류 칩 + 게임 그림 카드 목록. 카드를 누르면 게임별 하위 페이지로 가서 바로 열린다."""
    P = PAGE[l]; U = UI[l]; home = '/' if l == 'ko' else f'/?lang={l}'
    alts = ''.join(f'<link rel="alternate" hreflang="{x}" href="https://playmallow.com{URL[x]}">' for x in LANGS) + \
           '<link rel="alternate" hreflang="x-default" href="https://playmallow.com/arcade/">'
    games = live_games()
    P = {k: (v.replace('{n}', str(len(games))) if isinstance(v, str) else v) for k, v in P.items()}  # 게임 수는 설정에서 센다
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'FAQPage', 'inLanguage': l, 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in P['faq']]},
        {'@type': 'ItemList', 'name': P['h1'], 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': 'https://playmallow.com' + gurl(g['id'], l), 'name': g[l]['name']} for i, g in enumerate(games)]}]}
    cats = [c for c in CAT if any(g['cat'] == c for g in games)]
    chips = f'<button type="button" class="chip on" data-cat="all">{U["all"]}</button>' + ''.join(f'<button type="button" class="chip" data-cat="{c}">{e(CAT[c][l])}</button>' for c in cats)
    grid = ''.join(tile(g, l, i) for i, g in enumerate(games))
    body = f'''<section id="pg-games" aria-label="{e(U['list'])}">
    <h2 class="ag-h">🎮 {e(U['list'])}</h2>
    <div class="chips">{chips}</div>
    <div class="ag-grid">{grid}</div>
  </section>''' if LIVE else ''
    faq = ''.join(f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q, a in P['faq'])
    return head(l, P['title'], P['desc'], URL[l], alts, ld) + f'''
<body>
<header>
  <a id="backHome" href="{home}">← 홈</a>
  <h1>{e(P['h1'])}</h1>
  <p class="tag">{e(P['tag'])}</p>
</header>
<script src="/assets/topbar.js?v=5"></script>
<main>
  {body}
{off_box(l)}
  <div class="card intro">{''.join(f'<p>{e(x)}</p>' for x in P['intro'])}<p class="notice">ⓘ {e(P['notice'])}</p></div>
  <div class="card faq"><h2>{e(P['faq_h'])}</h2>{faq}</div>
  <a class="back" href="{home}">{e(P['back'])}</a>
</main>
''' + tail(l)

def game_page(g, l):
    """게임별 하위 페이지: 플레이(누를 때만 로드) + 직접 쓴 소개·게임방법·게임TIP + 다른 게임."""
    P = PAGE[l]; U = UI[l]; t = g[l]; cg = CGAMES[g['id']]; gid = g['id']
    home = '/' if l == 'ko' else f'/?lang={l}&'
    ours = f'{home}?game={g["ours"]}'.replace('/??', '/?').replace('&?', '&')
    real = {x: (f'/arcade/{gid}/' if x == 'ko' else f'/arcade/{gid}/{x}') for x in LANGS}
    alts = ''.join(f'<link rel="alternate" hreflang="{x}" href="https://playmallow.com{real[x]}">' for x in LANGS) + \
           f'<link rel="alternate" hreflang="x-default" href="https://playmallow.com{real["ko"]}">'
    title = U['title'].format(n=t['name'])
    desc = (t['intro'] + ' ' + t['how'])[:150]
    ld = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Mallow', 'item': 'https://playmallow.com/'},
        {'@type': 'ListItem', 'position': 2, 'name': U['crumb'], 'item': 'https://playmallow.com' + URL[l]},
        {'@type': 'ListItem', 'position': 3, 'name': t['name'], 'item': 'https://playmallow.com' + real[l]}]}
    tips = ''.join(f'<li>{e(x)}</li>' for x in t['tips'])
    others = sorted([o for o in live_games() if o['id'] != gid], key=lambda o: o['cat'] != g['cat'])[:6]  # 같은 분류 먼저
    more = ''.join(tile(o, l, 9) for o in others)
    return head(l, title, desc, real[l], alts, ld, cg['thumb'].split('?')[0] + '?width=1200') + f'''
<body>
{GAME_MARK}
<header>
  <a class="crumb" href="{e(hub_url(l))}">← {e(U['crumb'])}</a>
  <h1>{e(t['name'])}</h1>
  <p class="tag">{e(CAT[g['cat']][l])} · {e(P['mins'].format(m=g['mins']))}</p>
</header>
<script src="/assets/topbar.js?v=5"></script>
<main>
  <article class="card pg-card" data-id="{e(gid)}">
    <h3 hidden>{e(t['name'])}</h3>
    <button type="button" class="pg-poster" aria-label="{e(t['name'])} {e(P['play'])}"><img src="{e(cg['thumb'])}" alt="" width="480" height="270" decoding="async"><b>{e(P['play'])}</b></button>
    <div class="pg-stage" hidden></div>
  </article>
{off_box(l)}
  <section class="card pg-body">
    <div class="pg-meta"><span>{e(g['tags'][l])}</span><span>{e(P['mins'].format(m=g['mins']))}</span></div>
    <p>{e(t['intro'])}</p>
    <h3>{e(P['how'])}</h3><p>{e(t['how'])}</p>
    <h3>{e(P['tips'])}</h3><ul>{tips}</ul>
    <h3>{e(P['for'])}</h3><p>{e(t['for'])}</p>
    <a class="pg-ours" href="{e(ours)}">🧠 {e(P['ours'])}: {e(OURS_NAME[g['ours']][l])} →</a>
    <p class="notice">ⓘ {e(P['notice'])}</p>
  </section>
  <h2 class="ag-h">🎮 {e(U['more'])}</h2>
  <div class="ag-grid">{more}</div>
  <a class="back" href="{e(hub_url(l))}">{e(U['back_list'])}</a>
</main>
''' + tail(l)


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
      <p><a class="inline" href="/arcade/">말로우 아케이드</a> 페이지의 게임은 외부 게임 플랫폼 <b>Playgama</b>(LeadToChanges L.L.C-FZ)가 제공합니다. 이용자가 <b>플레이 버튼을 누르기 전에는</b> 게임을 불러오지 않습니다.</p>
      <ul>
        <li>플레이를 누르면 게임이 Playgama 서버에서 열리며, Playgama와 그 광고 파트너가 게임 안에서 쿠키·기기 정보를 사용하고 광고를 보여 주거나 선택 구매 화면을 제공할 수 있습니다.</li>
        <li>이 과정의 정보 처리는 Playgama의 정책을 따릅니다. 말로우는 이 게임들을 통해 이용자 개인정보를 따로 수집하지 않습니다.</li>
        <li>외부 게임 이용 기록은 말로우의 기록·미션·연속 기록에 저장되거나 반영되지 않습니다.</li>
      </ul>
    </section>'''
PRIV_EN = '''    <section>
      <h2>4-1. External Games (Playgama)</h2>
      <p>Games on the <a class="inline" href="/arcade/en">Mallow Arcade</a> page are provided by the external game platform <b>Playgama</b> (LeadToChanges L.L.C-FZ). Nothing is loaded from Playgama <b>until you press Play</b>.</p>
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
    os.makedirs(out, exist_ok=True)
    for l in LANGS: wr(os.path.join(out, FILE[l]), page(l))
    keep = {g['id'] for g in live_games()} if LIVE else set()
    for d in os.listdir(out):   # 빠진 게임의 하위 페이지는 지운다(우리가 만든 것만)
        f = os.path.join(out, d, 'index.html')
        if d not in keep and os.path.isfile(f) and GAME_MARK in rd(f): shutil.rmtree(os.path.join(out, d))
    for g in (live_games() if LIVE else []):
        for l in LANGS: wr(os.path.join(out, g['id'], FILE[l]), game_page(g, l))
    print(('preview' if PREVIEW else 'site'), 'live' if LIVE else 'off', len(keep), 'games ->', out)
    if PREVIEW: return
    sync_names()
    # 사이트맵·llms·개인정보처리방침: 켜졌을 때만
    toggle_block('sitemap.xml', '  <!--arcade-->', '  <!--/arcade-->',
                 '\n'.join([f'  <url><loc>https://playmallow.com{URL[l]}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>0.5</priority></url>' for l in LANGS] +
                           [f'  <url><loc>https://playmallow.com{gurl(g["id"], l)}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.4</priority></url>' for g in live_games() for l in LANGS]),
                 LIVE, '</urlset>')
    toggle_block('llms.txt', '<!--arcade-->', '<!--/arcade-->',
                 '- [말로우 아케이드](https://playmallow.com/arcade/): 말로우가 고른 외부 웹게임 목록(Playgama 제공) — 게임마다 따로 된 페이지에 직접 쓴 소개·게임방법·게임TIP, 플레이 버튼을 눌러야 열림\n',
                 LIVE, '## 사이트 정보')
    toggle_block('privacy/index.html', '    <!--pg-ko-->', '    <!--/pg-ko-->', PRIV_KO, LIVE, '    <section>\n      <h2>5. 쿠키 거부 방법</h2>')
    toggle_block('privacy/index.html', '    <!--pg-en-->', '    <!--/pg-en-->', PRIV_EN, LIVE, '    <section>\n      <h2>5. How to Refuse Cookies</h2>')

if __name__ == '__main__':
    main()
