# -*- coding: utf-8 -*-
"""FAQ 섹션을 main의 맨 끝으로 옮긴다.

보강 섹션을 </main> 앞에 붙였더니 FAQ 뒤에 본문이 오는 순서가 됐다.
FAQ는 관례상 마지막에 오는 게 읽기 자연스러우므로 통째로 뒤로 보낸다.
"""
import io, os, re

def move_faq(page):
    f = os.path.join(page, 'index.html')
    s = io.open(f, encoding='utf-8', newline='').read()
    m = re.search(r'\n  <section><h2>자주 묻는 질문</h2>.*?\n  </section>', s, re.S)
    if not m:
        print('skip (FAQ 못 찾음)', page); return
    end = s.index('</main>')
    if m.end() > end:
        print('skip (이미 뒤에 있음)', page); return
    faq = m.group(0)
    s = s[:m.start()] + s[m.end():]
    end = s.index('</main>')          # 잘라낸 뒤 위치가 밀리므로 다시 계산
    s = s[:end] + faq.lstrip('\n') + '\n' + s[end:]
    io.open(f, 'w', encoding='utf-8', newline='').write(s)
    print('ok', page)

for p in ['sudoku', 'nonogram', '2048', 'water-sort']:
    move_faq(p)
