# -*- coding: utf-8 -*-
"""한국어 랜딩의 화면 FAQ를 FAQPage JSON-LD로도 싣는다 (SEO 진단 2026-09-28, 3순위). 여러 번 실행해도 된다(이미 있으면 건너뜀).
- 질문·답은 화면 글자를 그대로 옮긴다(태그만 걷어냄) — 화면과 다른 구조화 데이터는 스팸 판정 위험.
- 화면 형식 두 가지: <dl class="faq"><dt>질문</dt><dd>답</dd> / <p><b>Q. 질문</b><br>답</p>(크라운·탱고·성격유형 한국어 섹션)
- 파일 안의 첫 '자주 묻는 질문' 블록 = 한국어(기본 언어) FAQ."""
import io, os, re, json, html
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = ['sudoku', '2048', 'iq-test', 'reaction-time', 'memory-game', 'nonogram', 'water-sort', 'braintype', 'persona', 'queens', 'tango']
def text(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()
for pg in PAGES:
    P = os.path.join(ROOT, pg, 'index.html'); s = io.open(P, encoding='utf-8', newline='').read()
    if '"FAQPage"' in s: print('skip (있음)', pg); continue
    i = s.index('자주 묻는 질문')
    if '<dl class="faq">' in s[i:i + 200]:
        block = s[i:s.index('</dl>', i)]
        qa = re.findall(r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>', block, re.S)
    else:
        block = s[i:s.index('</div>', i)]
        qa = re.findall(r'<p><b>Q\.\s*(.*?)</b><br>(.*?)</p>', block, re.S)
    qa = [(text(q), text(a)) for q, a in qa]
    assert len(qa) >= 2, (pg, qa)
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    ld = json.loads(m.group(2)); url = next(n['url'] for n in ld['@graph'] if n.get('url'))
    ld['@graph'].append({'@type': 'FAQPage', '@id': url + '#faq', 'inLanguage': 'ko',
        'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in qa]})
    nl = m.group(2)[len(m.group(2).rstrip()):]  # 원래 줄바꿈 유지
    lead = m.group(2)[:len(m.group(2)) - len(m.group(2).lstrip())]
    s = s[:m.start(2)] + lead + json.dumps(ld, ensure_ascii=False, separators=(',', ':')) + nl + s[m.end(2):]
    io.open(P, 'w', encoding='utf-8', newline='').write(s); print('FAQPage', pg, len(qa))
