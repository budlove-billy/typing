# -*- coding: utf-8 -*-
"""홈 로비 게임 표지 — assets/cover/<id>.jpg (360×480, 카드 비율 3:4). 여러 번 실행해도 된다.
1순위: 무한 캔버스(canvas/graph.json)에서 프롬프트가 'cover-<id> —'로 시작하는 가장 최근 이미지
       (게임 세계 그림을 참조해 게임의 대표 물건을 장면 안에 그려 넣은 표지 — 2026-09-28 사용자 승인 A안)
2순위: assets/stage/<id>.jpg(세계 그림만) — 새 게임은 우선 이것으로 나가고, 캔버스에서 cover-<id>를 만들면 바뀐다."""
import os, json, re
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'assets', 'cover'); os.makedirs(OUT, exist_ok=True)
W, H = 360, 480
def cover(src, dst):
    im = Image.open(src).convert('RGB'); r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    im.crop((l, t, l + W, t + H)).save(dst, quality=74, optimize=True, progressive=True)
art = {}
g = json.load(open(os.path.join(ROOT, 'canvas', 'graph.json'), encoding='utf-8'))
for order, n in enumerate(g['nodes']):   # 캔버스 노드는 만든 순서대로 쌓인다(createdAt이 비어 있을 때가 있어 순서를 쓴다)
    d = n.get('data', {}); m = re.match(r'cover-(\w+) —', d.get('prompt', '')); u = d.get('url', '')
    if m and u and not d.get('error'):
        f = os.path.join(ROOT, 'canvas', 'pages', 'main', 'assets', u.split('/')[-1])
        if os.path.exists(f) and (m.group(1) not in art or order > art[m.group(1)][0]):
            art[m.group(1)] = (order, f)
art = {('chop' if k == 'tower' else k): v for k, v in art.items()}   # 시안 때 말로우 타워는 'cover-tower'로 만들었다
stage = os.path.join(ROOT, 'assets', 'stage')
ids = sorted(set(f[:-4] for f in os.listdir(stage) if f.endswith('.jpg')) | set(art))
for i in ids:
    cover(art[i][1] if i in art else os.path.join(stage, i + '.jpg'), os.path.join(OUT, i + '.jpg'))
print('covers', len(ids), '· 새 표지', len(art), '· 세계 그림만', sorted(set(ids) - set(art)))
