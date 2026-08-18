# -*- coding: utf-8 -*-
"""한국어 전용 게임 랜딩 8곳의 영어판 생성 → <page>/en.html (vercel rewrite /:dir/en 로 서빙).
   랜딩은 정적 HTML이라 i18n 배선 없이 별도 파일이 가장 깔끔하고, 얇은 페이지·중복 문제도 없다.
   한국어 원본에서 <style>과 광고/애널리틱스 헤드를 그대로 재사용해 디자인 드리프트를 막는다."""
import io, os, re

# id = 메인 앱 딥링크 게임 id
PAGES = {}

PAGES['sudoku'] = dict(gid='sudoku', emoji='🔢',
 title="Free Sudoku Online — Play Instantly, No Sign-Up | Mallow",
 desc="Play free Sudoku online in your browser. 3 difficulties, notes, hints, undo.",
 ogd="Free Sudoku in your browser. No sign-up, no install — a new puzzle every game.",
 h1="Free Sudoku Online",
 lead="No install, no sign-up — open the link and you are playing Sudoku within seconds.",
 cta="Play now →",
 name="Free Sudoku Online",
 jd="Free online Sudoku with three difficulty levels, pencil notes, hints and undo. Runs in any browser with no sign-up.",
 body="""
  <section><h2>Why play here</h2>
    <ul>
      <li><b>No sign-up, no install</b> — it starts in the browser, and there is nothing to dismiss first.</li>
      <li><b>Three difficulties</b> — easy, medium and hard, with a freshly generated puzzle every game.</li>
      <li><b>The tools you expect</b> — pencil notes, three hints, undo, and a three-mistake limit.</li>
      <li><b>Built for phones</b> — large digits and a calm background, comfortable to play one-handed.</li>
      <li><b>Times kept</b> — your best is stored on your own device, so you can pick the challenge back up.</li>
    </ul>
  </section>
  <section><h2>How to play Sudoku</h2>
    <p>Fill the 9×9 grid with the digits 1 to 9. There is only one rule: <b>no digit may repeat within a row, a column, or a 3×3 box</b>. Every puzzle has exactly one solution and can be finished by reasoning alone — you never have to guess.</p>
    <p>Start with the cells you are certain about. When a cell has several candidates, write them in with the notes tool rather than holding them in your head; that is where most mistakes come from. Three mistakes end the game, so take the extra second.</p>
  </section>
  <section><h2>Frequently asked questions</h2>
    <dl class="faq">
      <dt>Is it really free?</dt><dd>Yes. Every game on the site is free and no account is needed.</dd>
      <dt>Do I need to install an app?</dt><dd>No, it runs in the browser. If you play often, "Add to Home Screen" makes it behave like an app.</dd>
      <dt>Are there other puzzles?</dt><dd>Yes — nonogram, water sort, 2048 and more than thirty other brain games, plus a new daily puzzle.</dd>
    </dl>
  </section>""",
 links=[('/nonogram/en','Nonogram'),('/water-sort/en','Water Sort'),('/2048/en','2048'),('/iq-test/en','IQ Test')])

PAGES['2048'] = dict(gid='merge', emoji='🍭',
 title="2048 Game Online Free — Play Instantly | Mallow",
 desc="Play 2048 free online. Merge matching tiles to reach 2048. Swipe or arrow keys.",
 ogd="Merge matching numbers to reach the 2048 tile. Free, in your browser, no sign-up.",
 h1="2048 Game Online Free",
 lead="Merge matching numbers and build the 2048 tile. Open the link and you are playing in three seconds.",
 cta="Play now →",
 name="2048 Game Online Free",
 jd="Free online 2048 puzzle in three board sizes with swipe and arrow-key control and one-move undo.",
 body="""
  <section><h2>Why play here</h2>
    <ul>
      <li><b>No sign-up, no install</b> — open the address and the board is already there.</li>
      <li><b>Three difficulties</b> — set by board size: easy 5×5, normal 4×4, hard 3×3.</li>
      <li><b>Swipe or arrow keys</b> — push tiles with a finger on a phone, with the keyboard on a desktop.</li>
      <li><b>Undo</b> — take one move back when a swipe goes somewhere you did not intend.</li>
      <li><b>Scores kept</b> — your best stays on your device, ready for the next attempt.</li>
    </ul>
  </section>
  <section><h2>How to play 2048</h2>
    <p>Push up, down, left or right and every tile on the board slides that way. When two tiles carrying the same number collide they merge into one tile of double the value, and a new tile appears after each move.</p>
    <p>2 becomes 4, 4 becomes 8, 8 becomes 16 — and the goal is to build a 2048 tile. The standard approach is to keep your largest tile pinned in a corner and never disturb the row it sits in; once the big number moves off the edge, the board tends to fall apart quickly.</p>
    <p class="note">Mallow's 2048 follows the rules of the original 2048 by Gabriele Cirulli (MIT open source).</p>
  </section>
  <section><h2>Frequently asked questions</h2>
    <dl class="faq">
      <dt>Is it really free?</dt><dd>Yes. Every game is free and no account is needed.</dd>
      <dt>Do I need an app?</dt><dd>No. It runs in the browser, and "Add to Home Screen" makes it feel like an app.</dd>
      <dt>Any tips for a higher score?</dt><dd>Keep the biggest tile in one corner, build a descending row alongside it, and avoid swiping in the direction that would move it out.</dd>
    </dl>
  </section>""",
 links=[('/water-sort/en','Water Sort'),('/nonogram/en','Nonogram'),('/sudoku/en','Sudoku'),('/memory-game/en','Memory Game')])

PAGES['water-sort'] = dict(gid='sort', emoji='🧪',
 title="Water Sort Puzzle Free Online — Color Sort | Mallow",
 desc="Free water sort puzzle online. Pour colours into matching bottles to sort.",
 ogd="Pour the colours until every bottle holds just one. Free, no sign-up, always solvable.",
 h1="Water Sort Puzzle (Color Sort)",
 lead="Pour the colours until every bottle holds only one. Open the link and start sorting.",
 cta="Play now →",
 name="Water Sort Puzzle Online",
 jd="Free water sort (colour sort) puzzle with 4, 6 and 8 colour difficulties. Every board is verified solvable before it is served.",
 body="""
  <section><h2>Why play here</h2>
    <ul>
      <li><b>No sign-up, no install</b> — straight into the browser, with nothing interrupting.</li>
      <li><b>Three difficulties</b> — 4, 6 or 8 colours.</li>
      <li><b>Always solvable</b> — each board is solved during generation, so a dead end is never dealt to you.</li>
      <li><b>Undo</b> — pour into the wrong bottle and you can simply take it back.</li>
      <li><b>Scores kept</b> — your best is stored on your own device.</li>
    </ul>
  </section>
  <section><h2>How to play water sort</h2>
    <p>You are given bottles with layers of mixed colours and two empty bottles. Tap one bottle then another to pour the top colour across — but only onto the same colour, or into an empty bottle, and only while there is room.</p>
    <p>Keep pouring until every bottle contains a single colour and the board is clear. Treat the empty bottles as temporary workspace rather than somewhere to dump a colour, and try to move a colour only when it can go somewhere it will stay.</p>
    <p class="note">Also known as water sort, colour sort, or the ball / liquid sorting puzzle.</p>
  </section>
  <section><h2>Frequently asked questions</h2>
    <dl class="faq">
      <dt>Is it really free?</dt><dd>Yes. Every game is free and no account is needed.</dd>
      <dt>Can I get an unsolvable board?</dt><dd>No. Every board is verified during generation, so if you are stuck the solution is still there — undo a few pours and free up an empty bottle.</dd>
      <dt>Any strategy?</dt><dd>Never split a colour across two bottles if you can avoid it, and keep at least one bottle genuinely empty for as long as possible.</dd>
    </dl>
  </section>""",
 links=[('/nonogram/en','Nonogram'),('/sudoku/en','Sudoku'),('/2048/en','2048'),('/stroop/en','Stroop Test')])

PAGES['nonogram'] = dict(gid='nono', emoji='🖼️',
 title="Nonogram Online Free — Picross Pixel Logic Puzzle | Mallow",
 desc="Free nonogram (picross) online. Solve number clues to reveal a pixel picture.",
 ogd="Read the number clues, fill the grid, and a pixel picture appears. Free, no guessing.",
 h1="Nonogram (Picross)",
 lead="Turn number clues into a pixel picture by pure logic. Open the link and start solving.",
 cta="Play now →",
 name="Nonogram Online Free",
 jd="Free online nonogram (picross) puzzle. Every board is generated with a unique solution reachable by logic alone.",
 body="""
  <section><h2>Why play here</h2>
    <ul>
      <li><b>No sign-up, no install</b> — quiet, immediate, and good for settling into.</li>
      <li><b>Unique solutions</b> — only boards with exactly one answer are served, so guessing is never required.</li>
      <li><b>Pick your size</b> — from small grids up to large ones as you improve.</li>
      <li><b>Fill and cross</b> — mark cells you have ruled out with an X and the board stops confusing you.</li>
      <li><b>Times kept</b> — your best is stored on your own device.</li>
    </ul>
  </section>
  <section><h2>How to play a nonogram</h2>
    <p>The numbers beside each row and above each column tell you how many cells in that line are filled, in consecutive runs. Several numbers mean several runs, in that order, with at least one empty cell between them.</p>
    <p>If a line of five cells is labelled "5", the whole line is filled — that is where to start. Work from the lines that are most constrained, cross out what is impossible, and let each certainty narrow its neighbours. Nothing here needs luck.</p>
    <p class="note">Nonograms also go by picross, griddlers, paint by numbers, or pixel puzzles. In the Mallow app this game is called <b>Pixel Logic</b>.</p>
  </section>
  <section><h2>Frequently asked questions</h2>
    <dl class="faq">
      <dt>Is it really free?</dt><dd>Yes. Every game is free and no account is needed.</dd>
      <dt>Will I have to guess?</dt><dd>No. Every board is generated to have a single logical solution, so it can always be finished by deduction.</dd>
      <dt>Are there other logic puzzles?</dt><dd>Yes — Sudoku, water sort, daily Queens and Tango puzzles, and more than thirty brain games.</dd>
    </dl>
  </section>""",
 links=[('/sudoku/en','Sudoku'),('/water-sort/en','Water Sort'),('/2048/en','2048'),('/queens/?lang=en','Daily Queens')])

PAGES['memory-game'] = dict(gid='cards', emoji='🃏',
 title="Memory Card Game Free Online — Match the Pairs | Mallow",
 desc="Free memory card matching game online. 60-second time attack with combo bonuses.",
 ogd="Flip the cards, remember where things are, and match every pair before the clock runs out.",
 h1="Memory Card Game (Match the Pairs)",
 lead="Flip two cards, remember what was where, and clear every pair before the clock runs out.",
 cta="Play now →",
 name="Memory Card Game Online",
 jd="Free online memory card matching game. Sixty-second time attack with combo bonuses and a board that grows as you clear it.",
 body="""
  <section><h2>Why play here</h2>
    <ul>
      <li><b>No sign-up, no install</b> — simple enough for children and adults alike.</li>
      <li><b>Sixty-second time attack</b> — short and sharp, made for an idle few minutes.</li>
      <li><b>It grows with you</b> — clear a board and the next one has more pairs.</li>
      <li><b>Combo bonus</b> — consecutive matches are worth progressively more.</li>
      <li><b>Scores kept</b> — your best stays on your device for the next attempt.</li>
    </ul>
  </section>
  <section><h2>How to play</h2>
    <p>Every card starts face down. Turn two over: if the pictures match, the pair is cleared; if not, both flip back — and the whole game is about remembering what you saw and where it was.</p>
    <p>Clear the board and the next one adds more pairs. Rather than flipping at random, it helps to sweep the board in a fixed order early on so the positions you have seen form a pattern you can recall.</p>
    <p class="note">This is the classic exercise for visual working memory — holding what you have just seen for a few seconds.</p>
  </section>
  <section><h2>Frequently asked questions</h2>
    <dl class="faq">
      <dt>Is it really free?</dt><dd>Yes. Every game is free and no account is needed.</dd>
      <dt>Do I need an app?</dt><dd>No, it runs in the browser. "Add to Home Screen" makes it behave like one.</dd>
      <dt>Are there other memory games?</dt><dd>Yes — flash memory, N-back, reverse recall and more than thirty brain games in total.</dd>
    </dl>
  </section>""",
 links=[('/reaction-time/en','Reaction Time'),('/2048/en','2048'),('/nonogram/en','Nonogram'),('/iq-test/en','IQ Test')])

PAGES['reaction-time'] = dict(gid='react', emoji='⏱️',
 title="Reaction Time Test — How Fast Are You? Free | Mallow",
 desc="Free reaction time test. Tap when the screen turns green, get your average ms.",
 ogd="Tap the moment the screen turns green. Find out your average reaction time in milliseconds.",
 h1="Reaction Time Test",
 lead="Tap the instant the screen turns green, and find out your average reaction time in milliseconds.",
 cta="Measure now →",
 name="Reaction Time Test",
 jd="Free online reaction time test measuring average visual reaction in milliseconds, including no-go trials that test response inhibition.",
 body="""
  <section><h2>Why test here</h2>
    <ul>
      <li><b>No sign-up, no install</b> — measured in the browser, results immediately.</li>
      <li><b>Average in milliseconds</b> — several trials are averaged rather than judging you on one lucky tap.</li>
      <li><b>Restraint is tested too</b> — red no-go trials require you <em>not</em> to tap, which measures response inhibition.</li>
      <li><b>Challenge a friend</b> — share your result and see who is quicker.</li>
      <li><b>Records kept</b> — your best stays on your device so you can watch it improve.</li>
    </ul>
  </section>
  <section><h2>How the test works</h2>
    <p>Tap as fast as you can the moment the screen turns green. Tapping before it changes counts as a false start.</p>
    <p>Occasionally the screen turns red instead — a no-go trial, where the correct response is to hold still. After several rounds your average reaction time in milliseconds is reported.</p>
    <p>You will be quicker when rested and focused, looking at the screen with your finger already hovering. <b>Typical simple visual reaction time is around 200–270 ms</b>; under 200 ms is genuinely fast.</p>
  </section>
  <section><h2>Frequently asked questions</h2>
    <dl class="faq">
      <dt>Is it really free?</dt><dd>Yes. Every game is free and no account is needed.</dd>
      <dt>What counts as a normal reaction time?</dt><dd>Simple reactions usually land between 200 and 270 ms. Age, alertness and your device's display latency all shift the number.</dd>
      <dt>Are there other brain games?</dt><dd>Yes — flash memory, the Stroop colour test, memory cards, 2048 and more than thirty others.</dd>
    </dl>
  </section>""",
 links=[('/stroop/en','Stroop Test'),('/memory-game/en','Memory Game'),('/iq-test/en','IQ Test'),('/2048/en','2048')])

PAGES['iq-test'] = dict(gid='iq', emoji='🧠',
 title="Free IQ Test Online — 30 Questions, 10 Minutes | Mallow",
 desc="Free IQ test online: 30 questions across sequences, verbal, shapes and logic.",
 ogd="Thirty questions in ten minutes across four areas, with a difficulty-weighted score.",
 h1="Free IQ Test (30 questions)",
 lead="Four areas, thirty questions, ten minutes — see how you score.",
 cta="Start now →",
 name="Free IQ Test Online",
 jd="Free online IQ-style test: 30 questions across number sequences, verbal analogies, shape patterns and logical reasoning, difficulty-weighted, for entertainment.",
 body="""
  <section><h2>What the test covers</h2>
    <ul>
      <li><b>Four areas, 30 questions</b> — number sequences, verbal analogies, shape patterns and logical reasoning.</li>
      <li><b>Ten-minute limit</b> — both speed and accuracy feed into the score.</li>
      <li><b>Difficulty weighting</b> — harder questions count for more, producing a score in the 55–145 range.</li>
      <li><b>Shareable result</b> — save the score card as an image and compare with friends.</li>
      <li>Questions are drawn at random from a bank, so a second attempt is a genuinely new set.</li>
    </ul>
    <p class="note">⚠️ This is a game-based score meant for entertainment, not a professionally administered intelligence assessment. Treat it as a light workout, not a diagnosis.</p>
  </section>
  <section><h2>Frequently asked questions</h2>
    <dl class="faq">
      <dt>Is this a real IQ score?</dt><dd>No. It is an entertainment score based on game performance. A formal assessment has to be administered by a qualified professional.</dd>
      <dt>Can I retake it?</dt><dd>As often as you like. The questions change every time, so you can practise against your own best.</dd>
      <dt>Is there a sign-up or payment?</dt><dd>Neither. Everything is free, including seeing your result.</dd>
    </dl>
  </section>""",
 links=[('/sudoku/en','Sudoku'),('/nonogram/en','Nonogram'),('/persona/?lang=en','Personality Test'),('/reaction-time/en','Reaction Time')])

PAGES['stroop'] = dict(gid='stroop', emoji='🎨',
 title="Stroop Test Online Free — Color Match Game | Mallow",
 desc="Free Stroop test online. Tap the ink colour, not the word. 60-second challenge.",
 ogd="The word says RED but the ink is blue — can you answer the colour? Sixty seconds, free.",
 h1="Stroop Test",
 lead="Answer the ink colour, not the word. Sixty seconds of holding back what your brain wants to say.",
 cta="Play now →",
 name="Stroop Test Online",
 jd="Free online Stroop test: name the ink colour rather than the written word, scored over sixty seconds. Measures inhibitory control and focus.",
 body="""
  <section><h2>What is the Stroop effect?</h2>
    <p>When the word "RED" is printed in blue ink, your brain reads the word before it registers the colour — and answering "blue" takes noticeably longer than it should.</p>
    <p>That slowdown, when meaning and colour conflict, is the <b>Stroop effect</b>, first described by the psychologist John Ridley Stroop in 1935. It is one of the most reproduced findings in cognitive psychology.</p>
    <p>The test measures how well you can override that automatic reading response — what psychologists call inhibitory control — along with sustained attention.</p>
  </section>
  <section><h2>How to play</h2>
    <ul>
      <li>A colour word appears on screen, printed in a different colour.</li>
      <li>Tap the button for <b>the colour the word is printed in</b>, not the colour it names.</li>
      <li>Score as many as you can in sixty seconds. Wrong answers cost you time, so stay calm and look only at the colour.</li>
    </ul>
    <p class="note">Tip: narrow your eyes slightly and treat the word as a block of colour rather than something to read — most people get noticeably faster.</p>
  </section>
  <section><h2>Why play here</h2>
    <ul>
      <li><b>No sign-up, no install</b> — open the link and you are playing in three seconds.</li>
      <li><b>Sixty-second time attack</b> — short and intense, with your best kept on your device.</li>
      <li><b>Built for phones</b> — large buttons that are comfortable to hit at speed.</li>
    </ul>
  </section>
  <section><h2>Frequently asked questions</h2>
    <dl class="faq">
      <dt>Is it really free?</dt><dd>Yes. Every game is free and no account is needed.</dd>
      <dt>What exactly am I answering?</dt><dd>The ink colour the word is printed in, never the colour the word spells out.</dd>
      <dt>Are there other focus games?</dt><dd>Yes — the reaction time test, memory games, the IQ test and more than thirty others.</dd>
    </dl>
  </section>""",
 links=[('/reaction-time/en','Reaction Time'),('/iq-test/en','IQ Test'),('/memory-game/en','Memory Game'),('/sudoku/en','Sudoku')])

SITE = 'https://playmallow.com'

for page, c in PAGES.items():
    src = os.path.join(page, 'index.html')
    s = io.open(src, encoding='utf-8', newline='').read()
    assert len(c['desc']) <= 80, (page, len(c['desc']))

    style = re.search(r'<style>.*?</style>', s, re.S).group(0)
    ads = re.search(r'<!-- Google AdSense -->.*?gtag\(\'config\', \'G-9EQEH5BF0C\'\);\n</script>', s, re.S).group(0)
    ogimg = re.search(r'<meta property="og:image" content="([^"]*)"', s).group(1)

    en_url = '%s/%s/en' % (SITE, page)
    ko_url = '%s/%s/' % (SITE, page)
    links = ' · '.join('<a href="%s">%s</a>' % (h, t) for h, t in c['links'])
    faq = re.findall(r'<dt>(.*?)</dt><dd>(.*?)</dd>', c['body'], re.S)
    faq_ld = ','.join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
                      % (__import__('json').dumps(re.sub('<[^>]+>', '', q)),
                         __import__('json').dumps(re.sub('<[^>]+>', '', a))) for q, a in faq)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{ogd}">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:url" content="{en_url}">
<meta property="og:image" content="{ogimg}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{ogimg}">
<link rel="canonical" href="{en_url}">
<link rel="alternate" hreflang="ko" href="{ko_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{ko_url}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[{{"@type":"WebApplication","name":"{name}","url":"{en_url}","applicationCategory":"GameApplication","operatingSystem":"Any","inLanguage":"en","isAccessibleForFree":true,"description":"{jd}"}},{{"@type":"FAQPage","mainEntity":[{faq_ld}]}},{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{SITE}/?lang=en"}},{{"@type":"ListItem","position":2,"name":"{name}","item":"{en_url}"}}]}}]}}
</script>
<link rel="icon" type="image/png" href="/favicon-32.png?v=2">
{ads}
{style}
</head>
<body>
<nav><a href="/?lang=en"><img src="/mallow-logo.svg" alt="Mallow mascot">Mallow <small>light brain games</small></a></nav>
<main>
  <div class="hero">
    <div class="emoji">{emoji}</div>
    <h1>{h1}</h1>
    <p>{lead}</p>
    <a class="cta" href="/?game={gid}&amp;lang=en">{cta}</a>
    <div class="sub">No sign-up · No install · 100% free</div>
  </div>
{body}
</main>
<footer><a href="/?lang=en">Mallow home</a>·{links}<br>© Mallow · playmallow.com · <a href="{ko_url}">한국어</a></footer>
</body>
</html>
""".format(SITE=SITE, en_url=en_url, ko_url=ko_url, ogimg=ogimg, ads=ads, style=style,
           links=links, faq_ld=faq_ld,
           **{k: v for k, v in c.items() if k != 'links'})

    io.open(os.path.join(page, 'en.html'), 'w', encoding='utf-8', newline='').write(html)

    # 한국어 원본에 hreflang 짝 추가 (양방향이어야 hreflang이 유효하다)
    if 'hreflang' not in s:
        can = '<link rel="canonical" href="%s">' % ko_url
        assert can in s, page
        s = s.replace(can, can
                      + '\n<link rel="alternate" hreflang="ko" href="%s">' % ko_url
                      + '\n<link rel="alternate" hreflang="en" href="%s">' % en_url
                      + '\n<link rel="alternate" hreflang="x-default" href="%s">' % ko_url, 1)
        io.open(src, 'w', encoding='utf-8', newline='').write(s)
    print('ok', page, '-> %s/en.html (desc %d자)' % (page, len(c['desc'])))
