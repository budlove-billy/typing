# -*- coding: utf-8 -*-
"""홈 로비 게임 표지 — assets/stage/<id>.jpg(게임 세계 그림)를 240×320 썸네일로 줄여 assets/cover/<id>.jpg에 둔다.
말로우 런은 세계 그림이 캔버스로 그려져 파일이 없어서 플레이 화면 캡처(generated_images/run-v2-play-390.png)를 쓴다. 여러 번 실행해도 된다."""
import os
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'assets', 'cover'); os.makedirs(OUT, exist_ok=True)
W, H = 240, 320
def cover(src, dst):
    im = Image.open(src).convert('RGB'); r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    im.crop((l, t, l + W, t + H)).save(dst, quality=72, optimize=True, progressive=True)
stage = os.path.join(ROOT, 'assets', 'stage')
for f in sorted(os.listdir(stage)):
    if f.endswith('.jpg'): cover(os.path.join(stage, f), os.path.join(OUT, f))
cover(os.path.join(ROOT, 'generated_images', 'run-v2-play-390.png'), os.path.join(OUT, 'run.jpg'))
print('covers', len(os.listdir(OUT)))
