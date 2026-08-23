# -*- coding: utf-8 -*-
"""영어 랜딩 8곳 보강 — 한국어판에 넣은 실질 내용을 영어로도 싣는다.

배경: 이 en.html 8개는 8/18에 생성기로 한 번에 찍어 낸 파일이라 구조가 전부 같고
      본문이 1,250~1,800자다. 한국어판만 두껍고 영어판은 얇은 상태로 두면
      '양산된 얇은 페이지'라는 인상이 그대로 남는다.
번역이 아니라 같은 내용을 영어로 다시 쓴다(직역 티가 나면 오히려 역효과).
주입 위치는 FAQ 바로 앞.
"""
import io, os, re

B = {}

B['sudoku'] = """
  <section><h2>Four techniques that remove all guessing</h2>
    <p>Sudoku is never solved by luck. These four carry you through easy and normal, and open the blocked spots on hard.</p>
    <ol>
      <li><b>Hidden single</b> — pick one row, column or 3×3 box and count the cells where a 7 could still go. If only one cell qualifies, that cell is a 7, no matter how many other candidates it also holds. This is the workhorse of the opening.</li>
      <li><b>Naked single</b> — the same idea turned around. Pick an empty cell and count the digits that could go in it. If only one survives, write it in. Turning notes on makes these jump out at you.</li>
      <li><b>Naked pair</b> — when two cells in the same row, column or box hold exactly the same two candidates, those two digits must split between them. So you can erase both digits from every other cell in that unit. It fills nothing directly, but it clears the way.</li>
      <li><b>Pointing pair</b> — if every candidate for a 3 inside one box sits in a single row, then the 3 comes from that row. You can therefore erase 3 from the cells of that row that lie outside the box. On hard puzzles this is usually the move that breaks the deadlock.</li>
    </ol>
  </section>
  <section><h2>What the difficulty levels actually change</h2>
    <p>The three levels differ less in how many digits you start with than in <b>which techniques you need to finish</b>.</p>
    <ul>
      <li><b>Easy</b> — hidden singles alone will carry you to the end. You never need notes.</li>
      <li><b>Normal</b> — expect to need naked singles along the way. Notes make it far more comfortable.</li>
      <li><b>Hard</b> — a naked pair or a pointing pair is required at least once. Scanning by eye will always stall somewhere.</li>
    </ul>
    <p class="note">When you feel stuck, stop hunting for a cell to fill and look for a candidate to <b>erase</b> instead. Sudoku rewards subtraction more than addition. And remember three mistakes end the round — if you cannot say in one sentence why a digit belongs there, it is not that cell yet.</p>
  </section>
"""

B['nonogram'] = """
  <section><h2>Overlap — the move that opens an empty row</h2>
    <p>There is a way to produce certain cells in a row you know nothing about. It is called <b>overlap</b>, and it works whenever a clue is large relative to the row.</p>
    <p>Take a row of 10 cells with a single clue of <b>8</b>. Push that block of eight as far left as it goes, then as far right as it goes. The <b>middle 6 cells are filled in both arrangements</b>, so they are certain right now. The arithmetic is simply <b>(clue × 2) − row length</b>; whenever that comes out above zero, the technique applies.</p>
    <p class="note">Rows with several clues work the same way. Sketch the leftmost possible packing and the rightmost possible packing, then keep only the cells that are filled in both.</p>
  </section>
  <section><h2>Count the slack before you touch a row</h2>
    <p>A row clued <b>3 2 4</b> needs 3+2+4 plus one gap between each block — <b>11 cells minimum</b>. If the row is 12 long, the slack is a single cell and almost everything is forced. If the slack is generous, that row has nothing to give you yet.</p>
    <p>So work in order of slack: <b>tightest rows first</b>, which usually means the rows with the largest clue sum or the most clues. Each cell you settle there tightens the crossing columns, and the chain starts.</p>
  </section>
  <section><h2>X marks are the real tool</h2>
    <ul>
      <li><b>Cap a finished block immediately.</b> Once a block of 3 is complete, the cells on either side must be empty. Mark them, or you will re-derive the same thing next time you read the row.</li>
      <li><b>Spent clue means the rest is empty.</b> If every filled cell a row calls for is placed, all remaining cells in it are blank — no reasoning needed.</li>
      <li><b>An X splits a row.</b> One empty cell in the middle divides the row into two shorter segments. Re-measure each, and clues that no longer fit are eliminated — which often reveals an overlap that was invisible a moment ago.</li>
    </ul>
    <p class="note">Every board is verified to have exactly one solution, so being stuck never means it is time to guess. It means a row you have not re-read since your last mark still has something in it. Start with the rows crossing the cell you just filled.</p>
  </section>
"""

B['2048'] = """
  <section><h2>Four habits that raise your score</h2>
    <ol>
      <li><b>Pin the largest tile to one corner.</b> Any corner will do, but once you choose it, never change your mind. The board collapses fast the moment your biggest tile leaves that corner.</li>
      <li><b>Never swipe in the direction that lifts that row.</b> With the big numbers along the bottom-left, swiping up is what breaks them apart. Cycle through the other three and use the forbidden direction only when nothing else moves.</li>
      <li><b>Keep the anchored row in descending order.</b> Lined up largest-to-smallest, one swipe merges neighbours all the way along it. The better sorted that row is, the more a single move pays.</li>
      <li><b>Do not let small tiles settle in the middle.</b> A stray 2 or 4 wedged between big tiles keeps them from ever meeting. Clear the small numbers between merges rather than after.</li>
    </ol>
  </section>
  <section><h2>What the board size changes</h2>
    <p>Difficulty here is board size. The rules stay identical; the feel does not.</p>
    <ul>
      <li><b>Easy 5×5</b> — plenty of room to recover from a bad swipe. The right size for making the corner strategy a habit.</li>
      <li><b>Normal 4×4</b> — the original 2048 board. You have to keep the row sorted while still clearing space.</li>
      <li><b>Hard 3×3</b> — each new tile takes up a ninth of the board. One careless swipe breaks your order and there is nowhere to rebuild. Here, <b>keeping cells free</b> matters more than growing the big number.</li>
    </ul>
  </section>
  <section><h2>Reading the collapse before it happens</h2>
    <p>A game never ends suddenly — it was decided several moves earlier. When you see these, stop chasing points and repair the board.</p>
    <ul>
      <li>Your largest tile has slipped one cell off the corner. This is the urgent one; fix it before anything else.</li>
      <li>No two equal numbers sit next to each other in your anchored row — nothing left to merge.</li>
      <li>You are down to two free cells or fewer. One badly placed new tile now removes your options entirely.</li>
    </ul>
    <p class="note">Undo works better as a <b>one-move preview</b> than as an eraser: try the swipe you are unsure about, look at the result, and take it back if the board got worse.</p>
  </section>
"""

B['water-sort'] = """
  <section><h2>The order you pour in decides the game</h2>
    <p>Most lost boards are lost to sequencing, not to picking the wrong colour. These four rules set the order.</p>
    <ol>
      <li><b>Empty tubes are currency.</b> You only get two. Spend one on a colour you have no plan for and your options vanish immediately. Use an empty tube when it enables a specific next move, and free it again as soon as you can.</li>
      <li><b>Move the thickest stack first.</b> Three of the same colour stacked together travel in a single pour. It costs one move, exactly like shifting a single unit, and gains three times as much.</li>
      <li><b>Finish the tube that is nearly done.</b> A tube filled with one colour is out of the way for good. Leave it half-finished and it keeps getting used as a dumping ground.</li>
      <li><b>Check what you are burying.</b> Pouring B onto A means A is unavailable until B moves again. Asking "can I afford to cover this colour?" before each pour prevents most dead ends.</li>
    </ol>
  </section>
  <section><h2>4, 6 and 8 colours</h2>
    <p>More colours means more tubes, but you still get only two empties. So the ratio of free space to possibilities gets worse quickly as the level rises.</p>
    <ul>
      <li><b>4 colours</b> — playing what you see in front of you usually works. This is where the rules become second nature.</li>
      <li><b>6 colours</b> — you need to see two or three moves ahead. Where you spend that first empty tube decides the board.</li>
      <li><b>8 colours</b> — each colour starts scattered across three or four tubes. Gathering one means clearing another first, and without planning that order you will stall in the middle every time.</li>
    </ul>
  </section>
  <section><h2>When you get stuck</h2>
    <p>Every board is checked for a solution as it is generated, so <b>an unsolvable level never appears</b>. Being stuck means an earlier move can be taken back.</p>
    <ul>
      <li>Are both empty tubes holding a colour with nowhere to go? This is the usual culprit.</li>
      <li>Is one colour spread over three or four tubes with none of it near the top?</li>
      <li>Did you pour something on top of a tube that was one step from finished?</li>
    </ul>
    <p class="note">Undo lets you take several moves back, so retrace to the point where it went wrong rather than restarting. It is almost always the move where you first used an empty tube.</p>
  </section>
"""

B['stroop'] = """
  <section><h2>Why naming a colour is the slower job</h2>
    <p>For anyone who reads fluently, <b>reading is automatic</b>. The meaning of a word arrives whether you want it or not. Naming a colour has never been practised to that degree, so it stays a deliberate act every single time.</p>
    <p>When the word RED is printed in blue ink, the fast answer <b>red</b> and the slower answer <b>blue</b> collide at the moment you choose a response. The time it takes to override the first one is exactly the slowdown this test measures. The gap between matching trials and conflicting trials is the number that matters.</p>
  </section>
  <section><h2>Four ways to score higher</h2>
    <ol>
      <li><b>Do not look straight at the word.</b> Resting your gaze slightly off-centre keeps the letterforms from resolving sharply, so reading intrudes less. Narrowing your eyes works for the same reason.</li>
      <li><b>Let your hand learn the buttons.</b> If you have to hunt for the right button after deciding, you pay twice. Go deliberately slowly for the first few seconds to fix the positions.</li>
      <li><b>Keep a rhythm rather than racing.</b> Wrong answers cost you time, so a steady run of correct ones beats a burst followed by a miss.</li>
      <li><b>Watch the trial right after an error.</b> People rush to make up the loss and miss again. Take the next one deliberately half a beat slower.</li>
    </ol>
  </section>
  <section><h2>How to read your score</h2>
    <p>The Stroop task has a long history in psychology, but <b>what you get here is a game score, not an assessment.</b> Screen size, lighting, how far your thumb travels and how tired you are all move it around.</p>
    <p>So compare your runs against <b>your own, taken on the same device</b>, rather than against anyone else. A few rounds at a similar time of day will tell you where you actually sit.</p>
  </section>
"""

B['iq-test'] = """
  <section><h2>What each of the four sections asks for</h2>
    <ul>
      <li><b>Number sequences</b> — find the rule behind a run of numbers. When you are stuck, write down the <b>differences</b> between neighbours first. A constant difference means arithmetic; differences that form their own pattern mean two rules stacked. Suspect multiplication or squares only after that.</li>
      <li><b>Verbal analogies</b> — carry the relationship between two words over to another pair. Do not hold the relationship in your head; <b>put it in a sentence</b>. Once you have "A is what B is made of", the answer narrows to one.</li>
      <li><b>Figure patterns</b> — decide whether rotation, reflection, count or colour is what changes. When several change at once, it is faster to find what <b>stays the same</b>.</li>
      <li><b>Logical reasoning</b> — pick what must be true given the premises, not what sounds likely. Jotting the conditions down in short form removes most of the confusion.</li>
    </ul>
  </section>
  <section><h2>Spending the ten minutes well</h2>
    <p>Thirty questions in ten minutes is twenty seconds each on average. Since both speed and accuracy count, nothing costs you more than one question you refuse to leave.</p>
    <ol>
      <li><b>Past twenty seconds, move on.</b> Missing easy questions later is a far bigger loss than solving one hard one now.</li>
      <li><b>Play to your own order.</b> People are fast in different sections. Clear the ones you find quick, then spend what is left on the rest.</li>
      <li><b>Never leave a blank.</b> Come back and mark something on skipped questions if any time remains.</li>
    </ol>
  </section>
  <section><h2>Reading the number you get</h2>
    <p>Scores are weighted by difficulty and mapped onto a 55–145 range. That shape looks familiar because real intelligence tests are built to cluster around 100, and this borrows the look. <b>It is not one of those tests.</b></p>
    <p>A genuine assessment is administered by a trained examiner under a standard procedure and scored against a large sample of the same age group. There is no such sample here and no controlled conditions. Questions are drawn at random from a pool each time, so a score that moves between attempts is expected, not a fault.</p>
    <p class="note">Treat the number as a record of how these thirty questions went today, not as a description of you. If you need a result for study or career decisions, take a proper test with a qualified provider.</p>
  </section>
"""

B['memory-game'] = """
  <section><h2>Your memory is not growing — your method is</h2>
    <p>People who get good at this rarely have more capacity than when they started. They changed <b>how</b> they remember. Three things account for most of the difference.</p>
    <ol>
      <li><b>Turn positions into words.</b> Trying to hold the picture itself blurs quickly. "Cat, top-left corner" survives far longer than a mental image.</li>
      <li><b>Fix your scanning order.</b> Flipping wherever your eye lands means checking the same card three times. Sweeping row by row from the top-left guarantees no overlap.</li>
      <li><b>Open unknown cards next to known ones.</b> Pairing a new card with one whose partner you are still missing means even a miss teaches you something. That beats flipping two random cards.</li>
    </ol>
  </section>
  <section><h2>Keeping a combo alive</h2>
    <p>Because consecutive matches are worth more, an unbroken run scores better than the same number of scattered matches.</p>
    <ul>
      <li><b>Save the pairs you are sure of.</b> Instead of cashing a known pair right away, hold it and play it straight after a card you have just discovered — that links the chain.</li>
      <li><b>The opening is for gathering, not scoring.</b> Chasing a combo from nothing almost always breaks. Spend the first flips filling in positions, then run.</li>
      <li><b>In the last seconds, only play what you know.</b> With little time left, stop exploring and cash the pairs already on your map.</li>
    </ul>
  </section>
  <section><h2>What changes as the board grows</h2>
    <p>Clear a board and the next one adds pairs. The extra difficulty is not only that there is more to hold — it is that <b>checking one card pushes earlier cards out</b> of your working memory.</p>
    <p>So "memorise everything" stops working at larger sizes. Divide the board into quarters, work only the quarter in front of you until its pairs are cleared, then move across. It holds up far better.</p>
  </section>
"""

B['reaction-time'] = """
  <section><h2>What a reaction time is made of</h2>
    <p>The gap between the screen changing and your finger landing is not one thing. It is several stages stacked together.</p>
    <ul>
      <li><b>Noticing</b> — the change reaching your eye and registering as a signal.</li>
      <li><b>Deciding</b> — telling a go signal from a stop signal. More options makes this longer.</li>
      <li><b>Moving</b> — the decision travelling to your finger and the finger reaching the screen.</li>
      <li><b>The machine's share</b> — how often the display redraws and how long touch input takes to arrive. Anything measured in a browser always includes this.</li>
    </ul>
    <p class="note">That is why the same person scores differently on different hardware. Simple visual reactions in adults are usually discussed in the 200–300 millisecond range, but that figure depends on how it was measured too — so <b>the change in your own scores on one device</b> is far more meaningful than a comparison with anyone else.</p>
  </section>
  <section><h2>Holding still on red is the harder test</h2>
    <p>If it were only about hitting green quickly, the trick would be simple. The difficult half is <b>not moving on red</b>.</p>
    <p>The more you prepare to fire, the further your hand has already committed, and from there a stop signal is hard to obey. Pressing when you should have waited is a false alarm, and the faster someone's average gets, the more of them tend to appear.</p>
    <p>So a good result is <b>a fast average with few false alarms</b>. Shaving the average by launching early always comes with that bill attached.</p>
  </section>
  <section><h2>Measuring yourself properly</h2>
    <ol>
      <li><b>Warm up before you count a run.</b> The first attempt or two goes to getting used to the screen and the button.</li>
      <li><b>Hold conditions steady.</b> Device, finger, posture and screen brightness all shift the number.</li>
      <li><b>Trust the average, not your best single try.</b> One lucky early press easily becomes your record; the average reflects your actual state.</li>
      <li><b>Compare tired against rested.</b> Sleep, caffeine and time of day move this measure noticeably.</li>
    </ol>
  </section>
"""


def inject(page, block, suffix):
    f = os.path.join(page, suffix)
    s = io.open(f, encoding='utf-8', newline='').read()
    key = re.search(r'<h2>([^<]+)</h2>', block).group(1)
    assert key not in s, '%s/%s: 이미 적용됨' % (page, suffix)
    m = re.search(r'\n  <section><h2>Frequently asked questions</h2>', s)
    i = m.start() + 1 if m else s.index('</main>')
    s = s[:i] + block.strip('\n') + '\n' + s[i:]
    io.open(f, 'w', encoding='utf-8', newline='').write(s)
    print('ok %-14s +%d자' % (page + '/en', len(re.sub(r'<[^>]*>', '', block).strip())))


for page, block in B.items():
    inject(page, block, 'en.html')
