# -*- coding: utf-8 -*-
"""영어 SEO 본문 주입 — en 모드에서 ko 섹션이 통째로 숨겨져 100~400자짜리 얇은 페이지가 되던 문제.
   기존 <section class="seo" data-lang-only="ko"> 뒤에 en 섹션을 형제로 붙인다."""
import io, os, re

EN = {}

EN['zodiac'] = """
  <section class="seo" data-lang-only="en">
    <div class="card">
      <h2>What is a daily horoscope?</h2>
      <p>A daily horoscope reads the day ahead through the twelve signs of the zodiac — the band of sky the Sun appears to travel through over a year. Your sign comes from your date of birth. Mallow Horoscope takes that sign, compares it with where the Moon actually is today, and turns the result into a score out of 100 with a short reading for love, money, health and work. It is free, needs no sign-up or installation, and runs in any browser.</p>
    </div>
    <div class="card">
      <h2>Zodiac sign dates</h2>
      <ul class="zlist">
        <li><b>Aries</b> Mar 21 – Apr 19 · Fire</li>
        <li><b>Taurus</b> Apr 20 – May 20 · Earth</li>
        <li><b>Gemini</b> May 21 – Jun 21 · Air</li>
        <li><b>Cancer</b> Jun 22 – Jul 22 · Water</li>
        <li><b>Leo</b> Jul 23 – Aug 22 · Fire</li>
        <li><b>Virgo</b> Aug 23 – Sep 22 · Earth</li>
        <li><b>Libra</b> Sep 23 – Oct 22 · Air</li>
        <li><b>Scorpio</b> Oct 23 – Nov 22 · Water</li>
        <li><b>Sagittarius</b> Nov 23 – Dec 24 · Fire</li>
        <li><b>Capricorn</b> Dec 25 – Jan 19 · Earth</li>
        <li><b>Aquarius</b> Jan 20 – Feb 18 · Air</li>
        <li><b>Pisces</b> Feb 19 – Mar 20 · Water</li>
      </ul>
      <p class="sub">Signs that share an element — fire, earth, air, water — are said to understand each other easily. If you were born on a cusp date, read both neighbouring signs.</p>
    </div>
    <div class="card">
      <h2>How today's reading is calculated</h2>
      <p>Nothing here is drawn at random. Mallow uses the method Western astrology actually uses for a <b>daily</b> reading: the transit of the Moon. The Moon crosses one sign roughly every two and a half days, and the angle between the sign it occupies today and your own sign is called an <b>aspect</b>. That aspect sets the tone of the day.</p>
      <p class="sub">There are seven of them. <b>Conjunction (0°)</b> the Moon is in your own sign · <b>Semi-sextile (30°)</b> half a beat out of step · <b>Sextile (60°)</b> an opening, if you reach for it · <b>Square (90°)</b> friction that pushes work forward · <b>Trine (120°)</b> the easiest angle there is · <b>Quincunx (150°)</b> two things that never quite fit · <b>Opposition (180°)</b> face to face, pulled both ways.</p>
      <p class="sub">The phase of the Moon then adjusts that base value — new moon, waxing crescent, first quarter and on to waning crescent, eight steps in all. The Moon's position comes from an astronomical formula (Meeus, low precision) that we checked against recorded solar and lunar eclipses; it agrees to within 0.2°. Your star rating and all four category scores are derived from that single number, so they never contradict each other, and the same sign on the same date always returns the same reading.</p>
    </div>
    <div class="card">
      <h2>What you get</h2>
      <ul class="zlist">
        <li><b>Today's Moon</b> the sign it sits in, and its phase</li>
        <li><b>Aspect</b> the exact angle to your sign, and what it means</li>
        <li><b>Score</b> out of 100, with a star rating</li>
        <li><b>Categories</b> love, money, health and work, each scored</li>
        <li><b>Guidance</b> one thing to do, one thing to watch</li>
        <li><b>Moon in your sign</b> the one date a month it comes home</li>
        <li><b>Your week</b> seven daily bars and the best day of them</li>
        <li><b>Tomorrow</b> a preview of the next aspect and score</li>
      </ul>
    </div>
    <div class="card">
      <h2>How to use it</h2>
      <ol>
        <li>Enter your date of birth.</li>
        <li>Your sign, its element and its temperament appear.</li>
        <li>Read today's score and categories, then share the card with a friend.</li>
      </ol>
    </div>
    <div class="card">
      <h2>Frequently asked questions</h2>
      <p><b>Is it free?</b><br>Yes. No sign-up, no installation — enter a birth date and read it straight away.</p>
      <p><b>Does it really change every day?</b><br>Yes. The Moon moves about 13° a day, so the aspect to your sign shifts every two or three days and the phase changes daily.</p>
      <p><b>How is my sign decided?</b><br>From your birth date, against the cusp dates in the table above.</p>
      <p><b>Where does the score come from?</b><br>The aspect between today's Moon sign and your sign sets a base value, the lunar phase adjusts it, and the result is a score out of 100. The stars and the four category scores all follow from it.</p>
      <p><b>Will I get the same result if I look twice?</b><br>Yes. Same sign, same date, same reading — every time.</p>
    </div>
    <div class="card">
      <h2>More free readings and games</h2>
      <p class="links"><a href="/luckycolor/?lang=en">Thai lucky colour</a> · <a href="/persona/?lang=en">Personality type test</a> · <a href="/queens/?lang=en">Daily Queens puzzle</a> · <a href="/?lang=en">Free brain games</a></p>
    </div>
    <p class="disc">Mallow Horoscope is entertainment built on astrological tradition. It is not a scientific or medical prediction.</p>
  </section>
"""

EN['persona'] = """
  <section class="seo" data-lang-only="en">
    <div class="card">
      <h2>What is Mallow Persona?</h2>
      <p>Mallow Persona is a free personality type test. Instead of asking you to rate abstract statements, it puts you in <b>24 everyday situations</b> — a weekend with nothing planned, a friend who has just made a mistake, a trip you are about to take — and asks which way you would actually lean. From your answers it works out four preference axes and places you in one of <b>16 personality types</b>. No sign-up, no installation, about three minutes.</p>
    </div>
    <div class="card">
      <h2>The four axes</h2>
      <ul>
        <li><b>Extravert / Introvert</b> — where your energy comes back: people, or quiet.</li>
        <li><b>Intuition / Sensing</b> — what you notice first: what something could become, or what it plainly is.</li>
        <li><b>Feeling / Thinking</b> — how you decide: by how people will feel, or by what makes sense.</li>
        <li><b>Prospecting / Judging</b> — how you like your days: open-ended, or settled in advance.</li>
      </ul>
      <p class="sub">Each axis is reported as a percentage rather than a yes-or-no, so a 55/45 split reads very differently from a 90/10 one. Being near the middle simply means both sides are available to you.</p>
    </div>
    <div class="card">
      <h2>The 16 types</h2>
      <ul class="tlist">
        <li>🗂️ ISTJ · The Steady Keeper</li><li>🧸 ISFJ · The Warm Caretaker</li>
        <li>🌙 INFJ · The Deep Dreamer</li><li>♟️ INTJ · The Lone Architect</li>
        <li>🛠️ ISTP · The Hands-on Fixer</li><li>🎨 ISFP · The Gentle Soul</li>
        <li>🌷 INFP · The Tender Idealist</li><li>🔬 INTP · The Curious Explorer</li>
        <li>🔥 ESTP · The Bold Adventurer</li><li>🎉 ESFP · The Life of the Party</li>
        <li>✨ ENFP · The Sparkling Enthusiast</li><li>💡 ENTP · The Idea Machine</li>
        <li>📊 ESTJ · The Driving Captain</li><li>🤗 ESFJ · The Caring Connector</li>
        <li>🌟 ENFJ · The People Grower</li><li>👑 ENTJ · The Grand Commander</li>
      </ul>
      <p class="sub">Every type comes with strengths, blind spots, how you show up in love and at work, what stress does to you, one growth tip, and the types you match with best.</p>
    </div>
    <div class="card">
      <h2>How to take it</h2>
      <ol>
        <li>Tap start — no account and nothing to install.</li>
        <li>Answer 24 situations with whichever option feels more like you.</li>
        <li>Read your type, your four percentages and the full profile, then share the result card.</li>
      </ol>
    </div>
    <div class="card">
      <h2>Frequently asked questions</h2>
      <p><b>Is it free?</b><br>Yes, completely. There is no sign-up and nothing is installed.</p>
      <p><b>How long does it take?</b><br>About three minutes for 24 questions. You can go back and change an answer.</p>
      <p><b>Is my data stored anywhere?</b><br>No. Answers stay in your browser and are never sent to a server.</p>
      <p><b>Is this the same as an official personality assessment?</b><br>No. It uses the same four-axis idea that many type tests share, but it is an original set of questions written for fun, not a clinical or professional instrument.</p>
      <p><b>Can I take it again?</b><br>Yes, as often as you like. Answer honestly rather than aspirationally and the result tends to stay stable.</p>
    </div>
    <div class="card">
      <h2>More free tests and games</h2>
      <p class="links"><a href="/zodiac/?lang=en">Daily horoscope</a> · <a href="/luckycolor/?lang=en">Thai lucky colour</a> · <a href="/tango/?lang=en">Daily Tango puzzle</a> · <a href="/?lang=en">Free brain games</a></p>
    </div>
    <p class="disc">Mallow Persona is made for entertainment. It is not a psychological diagnosis or a clinical assessment.</p>
  </section>
"""

EN['queens'] = """
  <section class="seo" data-lang-only="en">
    <div class="card">
      <h2>What is Mallow Crown?</h2>
      <p>Mallow Crown is a free daily logic puzzle, sometimes called a Queens puzzle. You are given a square board divided into coloured regions and you have to work out where the crowns go. There is never any guessing involved: every board is generated with exactly one solution, and pure reasoning always gets you there. A new puzzle appears each day, and it plays in the browser with no sign-up and nothing to install.</p>
    </div>
    <div class="card">
      <h2>The rules, in three lines</h2>
      <ul>
        <li><b>One crown per row</b> — no row may ever hold two.</li>
        <li><b>One crown per column</b> — the same going down.</li>
        <li><b>One crown per colour region</b> — each block of same-coloured cells gets exactly one.</li>
      </ul>
      <p class="sub">One more condition: crowns may not touch each other. Not side by side, not above or below, and not diagonally either — so placing a crown clears all eight neighbouring cells. Tapping a cell cycles it through 👑, ✕ and empty; the ✕ is your own note meaning "not here", and it is what keeps a hard board readable.</p>
    </div>
    <div class="card">
      <h2>If it is your first time</h2>
      <ol>
        <li><b>Start with the smallest colour region.</b> A region of two or three cells has very few places a crown can sit, so it usually resolves first.</li>
        <li><b>Look for a colour trapped in one line.</b> If a colour appears only within a single row, that row's crown must be inside it — which frees every other cell of that row.</li>
        <li><b>Clean up straight after each placement.</b> One crown eliminates its row, its column, its colour region and the eight cells around it, all at once.</li>
        <li><b>When stuck, mark ✕ instead of guessing.</b> Ruling cells out is faster than hunting for the right one; eventually a single cell is left standing.</li>
      </ol>
    </div>
    <div class="card">
      <h2>Board sizes: 6×6, 7×7, 8×8</h2>
      <p>The same day gives you three sizes. 6×6 is the one to learn the rules on, 7×7 is about right for a single daily sitting, and 8×8 has enough colour regions that you will need the elimination technique rather than sight-reading. Your time is kept for each size separately.</p>
    </div>
    <div class="card">
      <h2>Frequently asked questions</h2>
      <p><b>Is it really free?</b><br>Yes. No account, no app — open the page and today's puzzle is already there.</p>
      <p><b>Could a puzzle have more than one answer?</b><br>No. Every board is checked for a unique solution as it is generated, so logic alone always finishes it.</p>
      <p><b>Where are my times stored?</b><br>On this device only. Nothing is sent to a server, and finishing gives you a shareable result card.</p>
      <p><b>I have already solved today's puzzle.</b><br>Switch the board size for a different puzzle on the same day; the next daily set arrives at midnight.</p>
    </div>
    <div class="card">
      <h2>More daily puzzles</h2>
      <p class="links"><a href="/tango/?lang=en">Mallow Tango — sun &amp; moon puzzle</a> · <a href="/persona/?lang=en">Personality type test</a> · <a href="/zodiac/?lang=en">Daily horoscope</a> · <a href="/?lang=en">Free brain games</a></p>
    </div>
  </section>
"""

EN['tango'] = """
  <section class="seo" data-lang-only="en">
    <div class="card">
      <h2>What is Mallow Tango?</h2>
      <p>Mallow Tango is a free daily logic puzzle where every empty cell is filled with one of just two things: ☀️ a sun or 🌙 a moon. There is no arithmetic and only two rules, so you can start within seconds — but the boards still take real reasoning to finish. A new puzzle appears each day and it runs in the browser with no sign-up and nothing to install.</p>
    </div>
    <div class="card">
      <h2>Only two rules</h2>
      <ul>
        <li><b>Never three of the same in a row.</b> Neither across nor down may you produce ☀️☀️☀️ or 🌙🌙🌙. Two together is fine; three is not.</li>
        <li><b>Each line holds equal numbers.</b> On a 6×6 board every line has three suns and three moons; on 8×8 it is four and four. This applies to every row and every column.</li>
      </ul>
      <p class="sub">Tapping a cell cycles it through ☀️, 🌙 and empty. The cells that are filled in from the start never change — those are the anchors the whole solution hangs from.</p>
    </div>
    <div class="card">
      <h2>Three moves that solve most boards</h2>
      <ol>
        <li><b>A pair forces its neighbours.</b> If ☀️☀️ sit side by side, the cells on either end must both be moons, or you would make three in a row.</li>
        <li><b>A gap between twins is the opposite.</b> Given ☀️ ⬜ ☀️, the middle cell has to be 🌙 — filling it with a sun would make three.</li>
        <li><b>Once one symbol is used up, the rest are the other.</b> If a 6×6 row already holds three suns, every remaining cell in that row is a moon. No thinking required.</li>
      </ol>
      <p class="sub">Alternate between these three and most boards run all the way to the end. If you get stuck, there is almost always a row or column above or beside you that you have not re-read since your last placement.</p>
    </div>
    <div class="card">
      <h2>Board sizes: 6×6 and 8×8</h2>
      <p>6×6 is the size to learn on and takes a few minutes. 8×8 asks for more of each symbol per line and starts with proportionally fewer given cells, so the chains of deduction get noticeably longer. Your times are kept per size.</p>
    </div>
    <div class="card">
      <h2>Frequently asked questions</h2>
      <p><b>Is it really free?</b><br>Yes. No account, no app — open the page and today's puzzle is waiting.</p>
      <p><b>Will I ever have to guess?</b><br>No. Every board is checked for a unique solution as it is generated, so the two rules are always enough.</p>
      <p><b>How is it different from Sudoku?</b><br>Sudoku juggles nine digits; Tango has only two symbols. What replaces the difficulty is the "no three in a row" constraint, which lets one placement cascade across a whole line.</p>
      <p><b>Where are my times stored?</b><br>On this device only. Nothing goes to a server, and finishing gives you a shareable result card.</p>
    </div>
    <div class="card">
      <h2>More daily puzzles</h2>
      <p class="links"><a href="/queens/?lang=en">Mallow Crown — Queens puzzle</a> · <a href="/persona/?lang=en">Personality type test</a> · <a href="/zodiac/?lang=en">Daily horoscope</a> · <a href="/?lang=en">Free brain games</a></p>
    </div>
  </section>
"""

for page, block in EN.items():
    f = os.path.join(page, 'index.html')
    s = io.open(f, encoding='utf-8', newline='').read()
    if 'data-lang-only="en"' in s:
        print('skip (이미 있음)', page); continue
    m = re.search(r'<section class="seo" data-lang-only="ko">', s)
    assert m, f
    # ko 섹션의 짝이 되는 </section>을 찾아 그 뒤에 붙인다
    end = s.index('</section>', m.end()) + len('</section>')
    s = s[:end] + '\n' + block.strip('\n') + s[end:]
    io.open(f, 'w', encoding='utf-8', newline='').write(s)
    print('ok', page)
