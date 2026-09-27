# -*- coding: utf-8 -*-
"""오늘의 퍼즐 리디자인 패치 도우미 — 각 치환은 정확히 1회 일치해야 한다(아니면 중단, 파일 미변경)."""
import io
class Patch:
    def __init__(self, path):
        self.path = path; self.s = io.open(path, encoding='utf-8', newline='').read()
        self.nl = '\r\n' if '\r\n' in self.s else '\n'
    def R(self, a, b):
        a2, b2 = a.replace('\n', self.nl), b.replace('\n', self.nl); c = self.s.count(a2)
        assert c == 1, (a[:70], c); self.s = self.s.replace(a2, b2)
    def between(self, start, end, new):
        a = self.s.index(start); b = self.s.index(end, a)
        self.s = self.s[:a] + new.replace('\n', self.nl) + self.s[b:]
    def save(self):
        io.open(self.path, 'w', encoding='utf-8', newline='').write(self.s); print('patched', self.path)
