# -*- coding: utf-8 -*-
"""Playgama 게임 고르기 화면 만들기 — 인기순(평가 수) 목록 + 그림 + 체크박스 → 고른 목록 복사.
입력: .logs/pg/all2.json (python .logs/pg/fetch2.py 로 카탈로그 페이지에서 수집)
출력: generated_images/playgama-picker.html (내부 검토용, 배포하지 않음)"""
import io, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
L = json.load(io.open(os.path.join(ROOT, '.logs', 'pg', 'all2.json'), encoding='utf-8'))
src = io.open(os.path.join(ROOT, 'assets', 'playgama-config.js'), encoding='utf-8').read()
have = set(re.findall(r'export/game/([a-z0-9-]+)', src))

CATS = [  # (키, 한글, 이 태그 중 하나라도 있으면)
    ('puzzle', '퍼즐', {'Puzzle', 'Logic', 'Brain', 'Brain Training', 'Mind Games', 'Tiles Games', 'Jigsaw'}),
    ('match', '매치·짝맞추기', {'Matching', 'Match 3', 'Mahjong', 'Bubble Shooter', 'Color Match Games', 'Hidden Object'}),
    ('casual', '캐주얼', {'Casual Games', 'Relaxing Games', 'Cozy', 'Hyper Casual Games', 'Merge', 'Idle'}),
    ('arcade', '아케이드', {'Arcade', 'Skill', 'Fast-Paced Games', 'Physics'}),
    ('racing', '레이싱', {'Racing', 'Driving', 'Car', 'Race Games'}),
    ('strategy', '전략·디펜스', {'Strategy', 'Tower Defense', 'Defense Games'}),
    ('sim', '경영·시뮬', {'Simulation', 'Tycoon', 'Management', 'Business Games'}),
    ('sports', '스포츠', {'Sports', 'Soccer', 'Basketball'}),
    ('girls', '꾸미기', {'For Girls', 'Dress Up', 'Fashion', 'Make Up', 'Decoration', 'Beauty Games'}),
    ('card', '카드·보드', {'Card', 'Solitaire', 'Board'}),
    ('kids', '어린이', {'Kids', 'Educational'}),
]
RISK = {'Horror': '공포', 'Zombie': '좀비', 'Shooting': '총', 'First Person Shooter': '총', 'Gun': '총', 'Sniper': '총',
        'Casino': '도박', 'Gambling': '도박', 'Slots': '도박', 'Blood': '잔혹', 'Multiplayer': '멀티', 'Obby': '오비'}
IP = re.compile(r'(?i)plants.?vs|minecraft|roblox|pok[eé]mon|sonic|mario|squid game|grand.?(theft|shift).?auto|gta|fortnite|among us|huggy|skibidi|brainrot|kpop.?demon|tralal|naruto|spider.?man|barbie|disney|frozen|peppa')

rows = []
for g in L:
    if not g.get('count') or not g.get('img'): continue
    tags = set(g.get('genre') or [])
    cats = [k for k, _, s in CATS if tags & s] or ['etc']
    risk = sorted({v for k, v in RISK.items() if k in tags})
    if IP.search(g['slug'] + ' ' + (g.get('name') or '') + ' ' + ' '.join(tags)): risk.append('IP의심')
    rows.append({'s': g['slug'], 'n': g.get('name') or g['slug'], 'c': int(g['count']), 'r': g.get('rating'),
                 'm': 'Mobile' in (g.get('devices') or []), 'k': cats, 'x': risk, 'h': g['slug'] in have,
                 'i': re.sub(r'\?width=\d+', '', g['img']) + '?width=360', 'd': (g.get('desc') or '')[:150],
                 't': [t for t in (g.get('genre') or []) if t not in ('New', '1 Player Games', 'Mobile', 'Top Playgama', 'Trending now')][:4]})
rows.sort(key=lambda r: -r['c'])

HTML = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Playgama 게임 고르기 (인기순)</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#0f1020;color:#eee;font-family:'Pretendard','Malgun Gothic',system-ui,sans-serif;font-size:16px}
header{position:sticky;top:0;z-index:5;background:#15162b;padding:12px 14px;border-bottom:1px solid #2a2c4a}
h1{margin:0 0 6px;font-size:20px}.sub{color:#aab;font-size:14px;margin:0 0 8px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px}.chip{border:1px solid #3a3c63;background:#1d1f38;color:#ddd;border-radius:999px;padding:6px 13px;font-size:14px;cursor:pointer}
.chip.on{background:#7c4dff;border-color:#7c4dff;color:#fff;font-weight:800}
.opts{display:flex;flex-wrap:wrap;gap:12px;align-items:center;font-size:14px;color:#ccd}
.opts input[type=search]{background:#0f1020;border:1px solid #3a3c63;color:#fff;border-radius:8px;padding:7px 10px;font-size:15px;width:200px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:12px;padding:14px}
.card{position:relative;background:#1a1b31;border:2px solid #26284a;border-radius:14px;overflow:hidden;cursor:pointer}
.card.sel{border-color:#7c4dff;box-shadow:0 0 0 2px #7c4dff inset}.card.have{opacity:.55}
.card img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;background:#222}
.rank{position:absolute;top:6px;left:6px;background:rgba(0,0,0,.7);border-radius:8px;padding:2px 8px;font-weight:800;font-size:13px}
.ck{position:absolute;top:6px;right:6px;width:26px;height:26px;border-radius:7px;background:rgba(0,0,0,.6);border:2px solid #fff;display:grid;place-items:center;font-weight:900}
.card.sel .ck{background:#7c4dff}
.b{padding:8px 10px 10px}.nm{font-weight:800;font-size:15px;line-height:1.3;margin-bottom:4px}
.st{font-size:13px;color:#c9c9e8}.tg{font-size:12px;color:#9a9cc0;margin-top:3px}
.flag{display:inline-block;font-size:11.5px;font-weight:800;border-radius:6px;padding:1px 6px;margin:4px 3px 0 0;background:#5a1f2a;color:#ffb3c0}
.flag.ok{background:#1f4a35;color:#9ff0c4}.flag.nm{background:#4a3c1f;color:#ffe0a0}
.d{font-size:12.5px;color:#a9abc9;margin-top:5px;line-height:1.45}
footer{position:sticky;bottom:0;background:#15162b;border-top:1px solid #2a2c4a;padding:10px 14px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
footer b{font-size:16px}button.go{background:#7c4dff;color:#fff;border:0;border-radius:10px;padding:10px 16px;font-size:15px;font-weight:800;cursor:pointer}
button.cl{background:#2a2c4a;color:#ddd;border:0;border-radius:10px;padding:10px 14px;font-size:14px;cursor:pointer}
#out{flex:1 1 100%;display:none;width:100%;height:90px;background:#0f1020;color:#cfe;border:1px solid #3a3c63;border-radius:8px;font-size:13px}
</style></head><body>
<header><h1>Playgama 게임 고르기 — 인기순</h1>
<p class="sub">평가 수가 많은 순서예요. 카드를 눌러 고르고, 아래 <b>「고른 목록 복사」</b>를 눌러 채팅에 붙여 넣어 주세요. 흐린 카드는 이미 사이트에 있는 게임이에요. 빨간 표시는 넣기 전에 주의할 점이에요.</p>
<div class="chips" id="chips"></div>
<div class="opts"><input type="search" id="q" placeholder="이름 검색"><label><input type="checkbox" id="mob" checked> 휴대폰 되는 게임만</label>
<label><input type="checkbox" id="safe"> 주의 표시 없는 것만</label><label><input type="checkbox" id="selOnly"> 고른 것만 보기</label><span id="cnt"></span></div></header>
<div class="grid" id="grid"></div>
<footer><b id="selN">0개 고름</b><button class="go" id="copy">고른 목록 복사</button><button class="cl" id="clear">모두 해제</button><textarea id="out" readonly></textarea></footer>
<script>
const G=__DATA__, CATS=__CATS__;
const sel=new Set(JSON.parse(localStorage.getItem('pgpick')||'[]'));
let cat='all', shown=120;
const chips=document.getElementById('chips');
[['all','전체']].concat(CATS,[['etc','기타']]).forEach(([k,n])=>{const b=document.createElement('button');b.className='chip'+(k==='all'?' on':'');b.textContent=n;b.onclick=()=>{cat=k;shown=120;chips.querySelectorAll('.chip').forEach(c=>c.classList.toggle('on',c===b));draw();};chips.appendChild(b);});
const $=id=>document.getElementById(id);
function list(){const q=$('q').value.trim().toLowerCase();return G.filter(g=>(cat==='all'||g.k.includes(cat))&&(!$('mob').checked||g.m)&&(!$('safe').checked||!g.x.length)&&(!$('selOnly').checked||sel.has(g.s))&&(!q||g.n.toLowerCase().includes(q)||g.s.includes(q)));}
function card(g){const rank=G.indexOf(g)+1;const d=document.createElement('div');d.className='card'+(sel.has(g.s)?' sel':'')+(g.h?' have':'');
 d.innerHTML='<img loading="lazy" alt="" src="'+g.i+'"><span class="rank">#'+rank+'</span><span class="ck">'+(sel.has(g.s)?'✓':'')+'</span><div class="b"><div class="nm"></div><div class="st">평가 '+g.c.toLocaleString()+' · ★'+g.r+'</div><div class="tg"></div><div class="fl"></div><div class="d"></div></div>';
 d.querySelector('.nm').textContent=g.n; d.querySelector('.tg').textContent=g.t.join(' · '); d.querySelector('.d').textContent=g.d;
 const fl=d.querySelector('.fl'); if(g.h) fl.innerHTML+='<span class="flag ok">사이트에 있음</span>'; if(!g.m) fl.innerHTML+='<span class="flag nm">PC 전용</span>'; g.x.forEach(x=>fl.innerHTML+='<span class="flag">'+x+'</span>');
 d.onclick=()=>{sel.has(g.s)?sel.delete(g.s):sel.add(g.s);localStorage.setItem('pgpick',JSON.stringify([...sel]));d.classList.toggle('sel');d.querySelector('.ck').textContent=sel.has(g.s)?'✓':'';$('selN').textContent=sel.size+'개 고름';};
 return d;}
function draw(){const L=list();const gr=$('grid');gr.innerHTML='';L.slice(0,shown).forEach(g=>gr.appendChild(card(g)));
 if(L.length>shown){const m=document.createElement('button');m.className='go';m.style.gridColumn='1/-1';m.textContent='더 보기 ('+(L.length-shown)+'개 남음)';m.onclick=()=>{shown+=120;draw();};gr.appendChild(m);}
 $('cnt').textContent=L.length+'개'; $('selN').textContent=sel.size+'개 고름';}
['q','mob','safe','selOnly'].forEach(id=>$(id).addEventListener('input',()=>{shown=120;draw();}));
$('copy').onclick=()=>{const t='Playgama 고른 게임('+sel.size+'개): '+[...sel].join(', ');const o=$('out');o.style.display='block';o.value=t;o.select();try{navigator.clipboard.writeText(t);$('copy').textContent='복사됨 ✓';}catch(e){}};
$('clear').onclick=()=>{if(confirm('모두 해제할까요?')){sel.clear();localStorage.setItem('pgpick','[]');draw();}};
draw();
</script></body></html>'''
out = HTML.replace('__DATA__', json.dumps(rows, ensure_ascii=False, separators=(',', ':'))).replace('__CATS__', json.dumps([[k, n] for k, n, _ in CATS], ensure_ascii=False))
p = os.path.join(ROOT, 'generated_images', 'playgama-picker.html')
io.open(p, 'w', encoding='utf-8').write(out)
print(len(rows), 'games →', p, round(len(out) / 1024), 'KB')
