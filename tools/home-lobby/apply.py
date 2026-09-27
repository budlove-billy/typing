# -*- coding: utf-8 -*-
"""홈 로비 개편 (1회용, 기록용) — docs/홈-개편-제안.md, 시안 generated_images/home-mock.html (사용자 승인 2026-09-28)
- 홈: 어두운 게임 로비 톤. 오늘의 두뇌 3판(→ 다 하면 '오늘의 행운 카드') · 오늘의 퍼즐 · 오늘의 운세 · 추천/능력별 선반 · 이번 주 나 · 소개·FAQ(그대로)
- 게임은 세계 그림 표지(assets/cover/<id>.jpg, tools/home-lobby/covers.py)
- 아래 탭에 '운세' 화면 추가, 전체 게임 화면도 표지 카드로
- 모든 칸은 CSS로 크기를 미리 잡아 늦게 채워도 화면이 밀리지 않게(CLS)
각 치환은 정확히 1회 일치해야 한다(아니면 중단, 파일 미변경)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'daily-redesign')); from _patch import Patch
p = Patch(os.path.join(ROOT, 'index.html')); R = p.R
COVERS = sorted(f[:-4] for f in os.listdir(os.path.join(ROOT, 'assets', 'cover')) if f.endswith('.jpg'))

# ───── 1. 홈 마크업 ─────
p.between('<div class="screen active" id="screen-home">', '  <div class="home-about" aria-labelledby="about-title">', '''<div class="screen active" id="screen-home">
 <div class="lb">
  <div class="lb-head">
    <div class="lb-head-t"><p class="lb-greet" id="lb-greet">&nbsp;</p><h1 class="lb-h1" data-i18n="home.title">오늘의 두뇌 체조</h1></div>
    <span class="lb-streak" id="lb-streak">🔥 1</span>
  </div>
  <section class="lb-d3" aria-labelledby="lb-d3-title">
    <div class="lb-d3head">
      <div class="lb-ring" id="lb-ring"><i id="lb-ring-n">0/3</i></div>
      <div><b id="lb-d3-title" data-i18n="lb.d3.title">오늘의 두뇌 3판</b><span id="lb-d3-sub">&nbsp;</span></div>
    </div>
    <div class="lb-row3" id="lb-d3-cards"><button class="lb-card" tabindex="-1" aria-hidden="true"></button><button class="lb-card" tabindex="-1" aria-hidden="true"></button><button class="lb-card" tabindex="-1" aria-hidden="true"></button></div>
    <button class="lb-gift" id="lb-gift" onclick="lbGoLucky()">&nbsp;</button>
    <button class="lb-play" id="lb-play" onclick="lbPlay()">&nbsp;</button>
  </section>
  <h2 class="lb-h2">🧩 <span data-i18n="cat.daily">오늘의 퍼즐</span><small data-i18n="lb.puz.sub">하루 한 판</small></h2>
  <div class="lb-row3 lb-puz" id="lb-puz"><button class="lb-card" tabindex="-1" aria-hidden="true"></button><button class="lb-card" tabindex="-1" aria-hidden="true"></button><button class="lb-card" tabindex="-1" aria-hidden="true"></button></div>
  <p class="lb-count" id="lb-count">&nbsp;</p>
  <h2 class="lb-h2">🔮 <span data-i18n="lb.fortune.title">오늘의 운세</span><button class="lb-more" onclick="showScreen('fortune')" data-i18n="lb.more">더 보기 ›</button></h2>
  <div id="lb-lucky" class="lb-lucky-wrap"></div>
  <div class="lb-fchips" id="lb-fchips"></div>
  <h2 class="lb-h2">🔥 <span data-i18n="home.foryou">추천 게임</span><button class="lb-more" onclick="showScreen('games')" data-i18n="lb.all">전체 보기 ›</button></h2>
  <div class="lb-shelf" id="lb-rec"></div>
  <h2 class="lb-h2">🧠 <span data-i18n="lb.abil.title">능력별로 골라 하기</span></h2>
  <div class="lb-chips" id="lb-chips"></div>
  <div class="lb-shelf" id="lb-abil"></div>
  <h2 class="lb-h2">🏅 <span data-i18n="lb.me.title">이번 주 나</span><button class="lb-more" onclick="showScreen('records')" data-i18n="lb.records">내 기록 ›</button></h2>
  <div class="lb-me">
    <button class="lb-tile" id="home-week" onclick="showScreen('records')"></button>
    <button class="lb-tile" id="home-collection" onclick="showScreen('records')" aria-label="Mallow medal collection"></button>
  </div>
  <button class="card home-install" id="pwa-install" style="display:none" onclick="pwaInstall()">📲 <span data-i18n="install.button">홈 화면에 앱으로 설치</span></button>
  <div class="card home-ios-hint" id="ios-hint" style="display:none"><span data-i18n="install.ios">iPhone은 Safari 공유 버튼 → '홈 화면에 추가'로 앱처럼 설치할 수 있어요</span><button class="ios-hint-x" onclick="dismissIosHint()">✕</button></div>
 </div>
''')

# ───── 2. 운세 화면 + 탭 ─────
R('''<!-- ==================== ALL GAMES SCREEN (전체 게임) ==================== -->''', '''<!-- ==================== FORTUNE SCREEN (운세 — 홈 로비 탭) ==================== -->
<div class="screen" id="screen-fortune">
 <div class="lb">
  <h2 class="lb-title" data-i18n="home.fun">재미로 보는 운세</h2>
  <p class="lb-lead" data-i18n="lb.ft.lead">오늘의 행운 카드와 운세·성격 테스트를 모았어요. 모두 재미로 보는 내용이에요.</p>
  <div id="ft-lucky" class="lb-lucky-wrap"></div>
  <div class="ft-list" id="ft-list"></div>
 </div>
</div>

<!-- ==================== ALL GAMES SCREEN (전체 게임) ==================== -->''')
R('''  <button class="tab-btn" id="tab-records" onclick="navTo('records')">''', '''  <button class="tab-btn" id="tab-fortune" onclick="navTo('fortune')">
    <span class="tab-ico">🔮</span><span class="tab-label" data-i18n="tab.fortune">운세</span>
  </button>
  <button class="tab-btn" id="tab-records" onclick="navTo('records')">''')
R('<body>\n\n<nav>', '<body class="lobby">\n\n<nav>')   # 첫 화면이 홈이라 처음부터 로비 톤(JS 전에 색이 바뀌지 않게)

# ───── 3. CSS ─────
R('/* ===== STAGE-SKIN END ===== */\n</style>', '''/* ===== STAGE-SKIN END ===== */
/* ===== HOME-LOBBY (2026-09-28) — tools/home-lobby/apply.py. 홈·전체 게임·운세 = 어두운 게임 로비 톤 ===== */
body.lobby,body.lobby[data-axis]{background:#16122e radial-gradient(120% 55% at 50% 0%,#3a2a7a 0%,#1d1740 45%,#16122e 100%) fixed;color:#fff}
body.lobby nav{background:rgba(22,18,46,.94);border-bottom-color:rgba(255,255,255,.1);box-shadow:none}
body.lobby .nav-brand{color:#a9c4ff}
body.lobby .snd-btn{border-color:rgba(255,255,255,.25);color:#fff}
body.lobby .lang-select{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.22);color:#fff}
body.lobby .lang-select option{color:#1a1a2e}
body.lobby .tabbar{background:rgba(18,14,40,.97);border-top-color:rgba(255,255,255,.12);box-shadow:none}
body.lobby .tab-btn{color:#a49cd0} body.lobby .tab-btn.active{color:#fff}
body.lobby .home-section-title,body.lobby .home-grp{color:#e6e0ff;font-size:1rem;font-weight:900}
body.lobby .site-footer,body.lobby .site-footer a{color:#aaa2d8}
.lb{max-width:620px;margin:0 auto}
.lb-head{display:flex;align-items:flex-end;gap:.6rem;margin:.2rem .15rem .8rem}
.lb-head-t{flex:1;min-width:0}
.lb-greet{margin:0;color:#cfc7ff;font-size:.95rem;min-height:1.4em}
.lb-h1{margin:.1rem 0 0;font-size:1.45rem;font-weight:900;letter-spacing:-.02em;color:#fff}
.lb-streak{flex-shrink:0;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);border-radius:999px;padding:.4rem .75rem;font-size:.92rem;font-weight:900}
.lb-h2{display:flex;align-items:center;gap:.45rem;margin:1.6rem .15rem .7rem;font-size:1.12rem;font-weight:900;color:#fff;letter-spacing:-.02em}
.lb-h2 small,.lb-more{margin-left:auto;font-size:.85rem;font-weight:800;color:#b9b0e6}
.lb-more{background:none;border:none;font-family:inherit;cursor:pointer;padding:.3rem 0}
.lb-title{margin:.2rem .15rem .4rem;font-size:1.4rem;font-weight:900;color:#fff}
.lb-lead{margin:0 .15rem 1rem;color:#cfc7ff;font-size:.95rem;line-height:1.6}
/* 게임 표지 카드 */
.lb-card{position:relative;display:block;width:100%;aspect-ratio:3/4;padding:0;border-radius:16px;overflow:hidden;border:2px solid rgba(255,255,255,.22);box-shadow:0 5px 0 rgba(0,0,0,.35);background:linear-gradient(160deg,#4b3a9a,#231a52);color:#fff;font-family:inherit;text-align:left;cursor:pointer;transition:transform .12s}
.lb-card:active{transform:translateY(3px);box-shadow:0 2px 0 rgba(0,0,0,.35)}
.lb-card .lb-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.lb-card::after{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(10,6,30,0) 42%,rgba(10,6,30,.88))}
.lb-emoji{position:absolute;left:50%;top:42%;z-index:2;transform:translate(-50%,-50%);font-size:2.5rem;line-height:1;filter:drop-shadow(0 4px 6px rgba(0,0,0,.55))}
.lb-name{position:absolute;left:.5rem;right:.5rem;bottom:.5rem;z-index:2;font-size:.98rem;font-weight:900;line-height:1.25;text-shadow:0 2px 3px #000;word-break:keep-all}
.lb-tag{position:absolute;top:.4rem;left:.4rem;z-index:2;font-style:normal;font-size:.74rem;font-weight:800;background:rgba(0,0,0,.6);border-radius:999px;padding:.18rem .52rem}
.lb-tag.ok{background:#2fbf71}
.lb-dot{position:absolute;top:.5rem;right:.5rem;z-index:2;width:.65rem;height:.65rem;border-radius:50%;background:#ff4d6a;box-shadow:0 0 0 2px rgba(0,0,0,.35)}
.lb-card.done .lb-img,.lb-card.done .lb-emoji{filter:saturate(.45) brightness(.72)}
.lb-card.nocover{background:linear-gradient(160deg,#5a2f86,#2a1552)}
.lb-card.nocover .lb-emoji{font-size:3rem}
.lb-row3{display:flex;justify-content:center;gap:.6rem}
.lb-row3>.lb-card{flex:0 0 calc((100% - 1.2rem)/3);width:auto}
/* 오늘의 3판 */
.lb-d3{border-radius:24px;padding:1rem;background:linear-gradient(160deg,#5b3fd1,#2d1f6e);border:2px solid rgba(255,214,107,.55);box-shadow:0 14px 30px rgba(0,0,0,.4)}
.lb-d3head{display:flex;align-items:center;gap:.8rem;margin-bottom:.8rem}
.lb-d3head b{display:block;font-size:1.15rem;font-weight:900}
.lb-d3head span{display:block;color:#e4dcff;font-size:.9rem;margin-top:.1rem;min-height:1.35em}
.lb-ring{--p:0%;width:58px;height:58px;flex-shrink:0;border-radius:50%;background:conic-gradient(#ffd66b 0 var(--p),rgba(255,255,255,.15) 0);display:grid;place-items:center}
.lb-ring i{width:46px;height:46px;border-radius:50%;background:#3a288f;display:grid;place-items:center;font-style:normal;font-weight:900;font-size:1.05rem}
.lb-gift{display:block;width:100%;margin-top:.75rem;border:none;text-align:left;font-family:inherit;cursor:pointer;background:rgba(0,0,0,.25);border-radius:14px;padding:.65rem .8rem;font-size:.92rem;color:#ffe7a8;font-weight:800;min-height:2.6rem}
.lb-play{display:block;width:100%;margin-top:.75rem;border:none;font-family:inherit;cursor:pointer;font-weight:900;font-size:1.08rem;color:#3a1a08;background:linear-gradient(180deg,#ffd66b,#ff9f43);border-radius:16px;padding:.9rem;box-shadow:0 5px 0 #a8561c;min-height:3.2rem}
.lb-play:active{transform:translateY(3px);box-shadow:0 2px 0 #a8561c}
.lb-count{text-align:center;color:#b9b0e6;font-size:.88rem;margin:.6rem 0 0;min-height:1.35em}
/* 행운 카드 */
.lb-lucky{position:relative;overflow:hidden;min-height:8.2rem;border-radius:22px;padding:1rem 1.1rem;background:linear-gradient(150deg,#1b0f3a,#3b1650 60%,#5a1f4c);border:1.5px solid rgba(255,160,220,.4);box-shadow:0 10px 24px rgba(0,0,0,.35)}
.lb-lucky::before{content:"✦ ✧ ✦";position:absolute;right:.9rem;top:.6rem;color:rgba(255,220,255,.5);letter-spacing:.35rem}
.lk-k{font-size:.88rem;color:#ffc6ec;font-weight:800}
.lk-line{margin:.35rem 0 .45rem;font-size:1.15rem;font-weight:900;line-height:1.45;word-break:keep-all}
.lk-meta{display:flex;align-items:center;flex-wrap:wrap;gap:.35rem .6rem;font-size:.9rem;color:#f0e2fa}
.lk-sw{display:inline-block;width:1rem;height:1rem;border-radius:50%;border:2px solid rgba(255,255,255,.7);vertical-align:-.15rem;margin-right:.25rem}
.lb-lucky.locked{display:flex;align-items:center;gap:1rem;cursor:pointer;border-style:dashed}
.lk-back{flex:0 0 4.2rem;height:5.6rem;border-radius:12px;display:grid;place-items:center;font-size:1.8rem;background:repeating-linear-gradient(45deg,#6b2f8f 0 8px,#58247a 8px 16px);border:2px solid #ffd66b;box-shadow:0 4px 0 rgba(0,0,0,.35)}
.lk-txt b{display:block;font-size:1.1rem;font-weight:900}
.lk-txt span{display:block;margin-top:.25rem;color:#f0e2fa;font-size:.9rem;line-height:1.5}
.lb-lucky.reveal{animation:lkFlip .9s cubic-bezier(.3,1.3,.5,1)}
@keyframes lkFlip{0%{transform:perspective(600px) rotateY(90deg) scale(.9);opacity:.3}60%{transform:perspective(600px) rotateY(-8deg) scale(1.02)}100%{transform:none;opacity:1}}
@media (prefers-reduced-motion:reduce){.lb-lucky.reveal{animation:none}}
.lb-fchips{display:grid;grid-template-columns:repeat(4,1fr);gap:.5rem;margin-top:.7rem;min-height:4.6rem}
.lb-fchip{position:relative;border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.09);border-radius:14px;padding:.6rem .15rem;color:#fff;font-family:inherit;font-size:.84rem;font-weight:800;line-height:1.4;cursor:pointer;word-break:keep-all}
.lb-fchip b{display:block;font-size:1.45rem;line-height:1.2}
.lb-fchip .lb-dot{top:.35rem;right:.35rem}
/* 선반 */
.lb-shelf{display:flex;gap:.6rem;overflow-x:auto;padding:0 .1rem .45rem;min-height:calc(150px + .45rem);scroll-snap-type:x mandatory;scrollbar-width:none}
.lb-shelf::-webkit-scrollbar{display:none}
.lb-shelf>.lb-card{flex:0 0 112px;width:112px;height:150px;aspect-ratio:auto;scroll-snap-align:start}
.lb-chips{display:flex;gap:.45rem;overflow-x:auto;padding:0 .1rem .7rem;min-height:3rem;scrollbar-width:none}
.lb-chips::-webkit-scrollbar{display:none}
.lb-chip{flex-shrink:0;padding:.5rem .95rem;border-radius:999px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);color:#fff;font-family:inherit;font-size:.9rem;font-weight:800;cursor:pointer}
.lb-chip.on{background:#8fd3ff;color:#10204a;border-color:#8fd3ff}
/* 이번 주 나 */
.lb-me{display:grid;grid-template-columns:1fr 1fr;gap:.6rem}
.lb-tile{min-height:7.4rem;text-align:left;font-family:inherit;cursor:pointer;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);border-radius:16px;padding:.8rem;color:#cfc7ff;font-size:.86rem;line-height:1.5}
.lb-tile-k{font-weight:800;color:#e6e0ff}
.lb-tile-v{display:block;margin:.2rem 0;color:#fff;font-size:1.3rem;font-weight:900}
.lb-bar{height:8px;border-radius:9px;background:rgba(255,255,255,.14);margin-top:.45rem;overflow:hidden}
.lb-bar i{display:block;height:100%;background:linear-gradient(90deg,#8fd3ff,#b98cff)}
body.lobby #screen-home .home-install,body.lobby #screen-home .home-ios-hint{margin-top:1rem}
/* 전체 게임 · 운세 */
.lb-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(104px,1fr));gap:.65rem}
.ft-list{display:grid;gap:.6rem;margin-top:1rem}
.ft-item{position:relative;display:flex;align-items:center;gap:.85rem;width:100%;text-align:left;font-family:inherit;cursor:pointer;color:#fff;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:18px;padding:.85rem 1rem}
.ft-item>b{flex:0 0 3.1rem;height:3.1rem;border-radius:14px;display:grid;place-items:center;font-size:1.7rem;background:linear-gradient(160deg,#5a2f86,#2a1552)}
.ft-item span{display:block}
.ft-item .ft-n{font-size:1.02rem;font-weight:900}
.ft-item .ft-d{margin-top:.15rem;font-size:.88rem;color:#cfc7ff;line-height:1.45}
@media(max-width:360px){.lb-name{font-size:.86rem}.lb-emoji{font-size:2.1rem}.lb-fchip{font-size:.78rem}}
/* ===== HOME-LOBBY END ===== */
</style>''')

# ───── 4. 번역 ─────
I18N_ADD = r'''  "tab.fortune": {ko:"운세", en:"Fortune", th:"ดูดวง"},
  "lb.greet.m": {ko:"좋은 아침이에요 👋", en:"Good morning 👋", th:"อรุณสวัสดิ์ 👋"},
  "lb.greet.a": {ko:"좋은 오후예요 👋", en:"Good afternoon 👋", th:"สวัสดีตอนบ่าย 👋"},
  "lb.greet.e": {ko:"좋은 저녁이에요 👋", en:"Good evening 👋", th:"สวัสดีตอนเย็น 👋"},
  "lb.greet.n": {ko:"늦은 밤이에요 🌙", en:"Late night 🌙", th:"ดึกแล้วนะ 🌙"},
  "lb.streak": {ko:"{n}일 연속 방문", en:"{n}-day streak", th:"เข้าต่อเนื่อง {n} วัน"},
  "lb.d3.title": {ko:"오늘의 두뇌 3판", en:"Today's Brain 3", th:"สมอง 3 เกมวันนี้"},
  "lb.d3.left": {ko:"{n}판 남았어요 · 한 판 약 1분", en:"{n} to go · about 1 min each", th:"เหลืออีก {n} เกม · เกมละราว 1 นาที"},
  "lb.d3.done": {ko:"오늘의 3판 완료! 🎉", en:"All 3 done today! 🎉", th:"ครบ 3 เกมแล้ววันนี้! 🎉"},
  "lb.d3.prog": {ko:"오늘의 두뇌 3판 {d}/3 · 다음 판: {g}", en:"Today's Brain 3: {d}/3 · Next: {g}", th:"สมอง 3 เกมวันนี้ {d}/3 · ถัดไป: {g}"},
  "lb.done": {ko:"완료", en:"Done", th:"เสร็จ"},
  "lb.gift.lock": {ko:"🎁 3판 모두 하면 <u>오늘의 행운 카드</u>가 열려요", en:"🎁 Finish all 3 to open <u>today's lucky card</u>", th:"🎁 เล่นครบ 3 เกมเพื่อเปิด<u>การ์ดนำโชควันนี้</u>"},
  "lb.gift.open": {ko:"🎁 오늘의 행운 카드가 열렸어요 ›", en:"🎁 Your lucky card is open ›", th:"🎁 การ์ดนำโชคเปิดแล้ว ›"},
  "lb.play.next": {ko:"▶ 다음 판 시작", en:"▶ Play next", th:"▶ เล่นเกมถัดไป"},
  "lb.play.lucky": {ko:"🎁 행운 카드 보기", en:"🎁 See my lucky card", th:"🎁 ดูการ์ดนำโชค"},
  "lb.puz.sub": {ko:"하루 한 판", en:"one a day", th:"วันละหนึ่งเกม"},
  "lb.puz.next": {ko:"⏰ 새 퍼즐까지 {t}", en:"⏰ New puzzles in {t}", th:"⏰ ปริศนาใหม่ใน {t}"},
  "lb.new": {ko:"NEW", en:"NEW", th:"ใหม่"},
  "lb.fortune.title": {ko:"오늘의 운세", en:"Today's Fortune", th:"ดวงวันนี้"},
  "lb.more": {ko:"더 보기 ›", en:"More ›", th:"เพิ่มเติม ›"},
  "lb.all": {ko:"전체 보기 ›", en:"See all ›", th:"ดูทั้งหมด ›"},
  "lb.records": {ko:"내 기록 ›", en:"Records ›", th:"สถิติ ›"},
  "lb.abil.title": {ko:"능력별로 골라 하기", en:"Pick by skill", th:"เลือกตามทักษะ"},
  "lb.me.title": {ko:"이번 주 나", en:"My week", th:"สัปดาห์นี้ของฉัน"},
  "lb.lucky.title": {ko:"오늘의 행운 카드", en:"Today's Lucky Card", th:"การ์ดนำโชควันนี้"},
  "lb.lucky.lock": {ko:"두뇌 3판을 끝내면 열려요 · {d}/3", en:"Opens after today's 3 games · {d}/3", th:"เปิดได้เมื่อเล่นครบ 3 เกม · {d}/3"},
  "lb.lucky.color": {ko:"행운의 색", en:"Lucky color", th:"สีนำโชค"},
  "lb.lucky.num": {ko:"행운의 숫자", en:"Lucky number", th:"เลขนำโชค"},
  "lb.lucky.unlocked": {ko:"오늘의 3판 완료! 홈에서 행운 카드를 열어 보세요", en:"All 3 done! Open your lucky card on Home", th:"ครบ 3 เกมแล้ว! เปิดการ์ดนำโชคที่หน้าแรก"},
  "lb.go.home": {ko:"🎁 열어 보기", en:"🎁 Open", th:"🎁 เปิดดู"},
  "lb.go.next": {ko:"▶ 다음 판", en:"▶ Next", th:"▶ ถัดไป"},
  "lb.ft.lead": {ko:"오늘의 행운 카드와 운세·성격 테스트를 모았어요. 모두 재미로 보는 내용이에요.", en:"Your lucky card plus horoscopes and personality tests. All just for fun.", th:"รวมการ์ดนำโชค ดูดวง และแบบทดสอบบุคลิกภาพไว้ที่นี่ ทั้งหมดดูเพื่อความสนุก"},
  "lb.f.unse": {ko:"생년월일로 보는 오늘 하루의 흐름", en:"Your day by birth date", th:"ดวงรายวันตามวันเกิด"},
  "lb.f.zodiac": {ko:"12별자리 오늘의 운세", en:"Today's horoscope for the 12 signs", th:"ดวงวันนี้ของ 12 ราศี"},
  "lb.f.ttirank": {ko:"오늘 가장 운 좋은 띠 순위", en:"Today's luckiest zodiac animals", th:"อันดับปีนักษัตรที่โชคดีที่สุดวันนี้"},
  "lb.f.tarot": {ko:"카드 한 장으로 보는 오늘의 메시지", en:"One card, one message for today", th:"ไพ่หนึ่งใบ ข้อความหนึ่งข้อสำหรับวันนี้"},
  "lb.f.luckycolor": {ko:"태어난 요일로 보는 행운의 색", en:"Your lucky colours by birth weekday", th:"สีมงคลตามวันเกิด"},
  "lb.f.persona": {ko:"질문에 답하고 나의 성격 유형 알아보기", en:"Answer a few questions, find your type", th:"ตอบคำถามแล้วรู้จักบุคลิกของคุณ"},
  "lb.f.braintype": {ko:"나는 어떤 두뇌 유형일까?", en:"What kind of brain do you have?", th:"สมองของคุณเป็นแบบไหน?"},
'''
R('  "nav.run": {', I18N_ADD + '  "nav.run": {')

# ───── 5. 화면 전환 ─────
R("const TAB_FOR={home:'home', games:'games', records:'records'};",
  "const TAB_FOR={home:'home', games:'games', records:'records', fortune:'fortune'};\nconst NAV_SCREENS={home:1, games:1, records:1, fortune:1};   // 게임이 아닌 화면(하단 탭)")
R("  document.body.dataset.axis = ((id==='home'||id==='games'||id==='records') ? 'home' : (_gameAxis(id)||'home'));",
  "  document.body.dataset.axis = (NAV_SCREENS[id] ? 'home' : (_gameAxis(id)||'home'));\n  document.body.classList.toggle('lobby', id==='home'||id==='games'||id==='fortune');   // 홈 로비 톤")
R("  const isGameScreen = !(id==='home'||id==='games'||id==='records');", "  const isGameScreen = !NAV_SCREENS[id];")
R("  if(id==='games' && typeof renderGames==='function') renderGames();",
  "  if(id==='games' && typeof renderGames==='function') renderGames();\n  if(id==='fortune' && typeof renderFortune==='function') renderFortune();")
R("  const id=s.id.replace('screen-',''); if(['home','games','records'].includes(id)) return false;",
  "  const id=s.id.replace('screen-',''); if(NAV_SCREENS[id]) return false;")
R("""  ['home','games','records'].forEach(s=>{
    const el=document.getElementById('screen-'+s);
    if(el && el.classList.contains('active')){
      const fn={home:'renderHome',games:'renderGames',records:'renderRecords'}[s];""",
  """  ['home','games','records','fortune'].forEach(s=>{
    const el=document.getElementById('screen-'+s);
    if(el && el.classList.contains('active')){
      const fn={home:'renderHome',games:'renderGames',records:'renderRecords',fortune:'renderFortune'}[s];""")

# ───── 6. 결과 화면: 오늘의 3판 진행·행운 카드 알림 ─────
R("""  if(!m.done.includes(id)){
    m.done.push(id); missionSave(m);
    if(missionToday().every(g=>m.done.includes(g))){ track('mission_complete', {}); sfx('win'); }
  }
}""", """  if(!m.done.includes(id)){
    m.done.push(id); missionSave(m);
    if(missionToday().every(g=>m.done.includes(g))){ track('mission_complete', {}); sfx('win'); }
  }
  lbResultLine(id, m);
}""")

# ───── 7. 주간 챌린지·메달 타일(짧게) ─────
R("""  el.innerHTML='<div class="wk-top"><span class="wk-title">📅 '+t('wk.title')+'</span><span class="wk-tier">'+tr.e+' '+t(tr.k)+'</span></div>'+
    '<div class="wk-pts"><b>'+o.pts+'</b><span>'+t('wk.unit')+'</span><em>'+t('wk.plays').replace('{n}',(o.plays|0))+'</em></div>'+
    '<div class="wk-bar"><i style="width:'+pct+'%"></i></div>'+
    '<div class="wk-sub">'+goal+' · '+sub+'</div>';""",
  """  el.title=sub;
  el.innerHTML='<span class="lb-tile-k">📅 '+t('wk.title')+'</span><b class="lb-tile-v">'+tr.e+' '+o.pts+' '+t('wk.unit')+'</b>'+
    '<span>'+goal+'</span><div class="lb-bar"><i style="width:'+pct+'%"></i></div>';""")
a = p.s.index("  el.innerHTML='<span class=\"collection-mallow\">")
b = p.s.index('\n', a)
p.s = p.s[:a] + """  el.innerHTML='<span class="lb-tile-k">🏅 '+medalCopy('collection')+'</span><b class="lb-tile-v">🥉🥈🥇💎 '+total+'</b><span>'+(total?'💎 '+diamond+' · ':'')+goal+'</span>';""" + p.s[b:]

# ───── 8. 홈 렌더(교체) + 전체 게임 표지 + 운세 화면 ─────
a = p.s.index('// 홈: 오늘의 추천(미션 다음 게임) + 목표 + 카테고리 칩 + 인기게임\nfunction renderHome(){'.replace('\n', p.nl))
b = p.s.index('// 전체 게임: 카테고리별 통일 카드', a)
HOME_JS = r'''/* ===== 홈 로비 (2026-09-28) — docs/홈-개편-제안.md. 게임은 세계 그림 표지, 오늘의 두뇌 3판 → 행운 카드.
   칸 크기는 CSS로 미리 잡혀 있어 여기서 늦게 채워도 화면이 밀리지 않는다(CLS). ===== */
const LB_COVERS=new Set(%COVERS%);
const LB_NO_EMOJI={run:1};   // 표지가 이미 플레이 화면 캡처라 이모지를 얹지 않는다
function lbKst(){ return new Date(Date.now()+9*3600*1000).toISOString().slice(0,10); }
// 데일리 퍼즐(KST 자정 리셋)·운세를 오늘 이미 했는지 — 빨간 점/NEW 표시용
function lbSeen(id){ try{ const k=lbKst();
  if(id==='moamoa'){ const st=JSON.parse(localStorage.getItem('moamoa_state_v1')||'null'); return !!(st&&st.date===k&&st.done); }
  if(id==='queens'||id==='tango') return localStorage.getItem(id+'_done')===k;
  if(id==='persona') return !!localStorage.getItem('persona_seen');
  if(id==='braintype') return true;
  return localStorage.getItem(id+'_seen')===k; }catch(e){ return true; } }
function lbVisible(g){ return (!g.koOnly||CURRENT_LANG==='ko') && (!g.langs||g.langs.includes(CURRENT_LANG)); }
function lbOpen(g){ if(g.external){ goExternal(g); return; } showScreen(g.id); }
function lbCard(g, o){ o=o||{}; const b=document.createElement('button'); const cov=LB_COVERS.has(g.id);
  b.className='lb-card'+(cov?'':' nocover')+(o.done?' done':''); b.onclick=()=>{ track('home_card',{game:g.id,from:o.from||''}); lbOpen(g); };
  b.innerHTML=(cov?'<img class="lb-img" src="assets/cover/'+g.id+'.jpg" alt="" width="240" height="320" decoding="async"'+(o.lazy?' loading="lazy"':'')+'>':'')+
    (LB_NO_EMOJI[g.id]&&cov?'':'<span class="lb-emoji">'+g.emoji+'</span>')+
    (o.tag?'<em class="lb-tag'+(o.done?' ok':'')+'">'+o.tag+'</em>':'')+(o.dot?'<i class="lb-dot"></i>':'')+
    '<span class="lb-name">'+t(g.key)+'</span>';
  return b; }
function lbFill(el, cards){ if(!el) return; el.innerHTML=''; cards.forEach(c=>el.appendChild(c)); }
// 오늘의 행운 카드 — 오늘의 두뇌 3판을 다 하면 열린다. 모두에게 같은 날 같은 카드(날짜 시드)
const LB_LUCKY={
 ko:['미뤄 둔 일을 끝내기 좋은 날','오랜만에 반가운 연락이 닿는 날','작은 친절이 크게 돌아오는 날','새로운 걸 배우기 좋은 날','천천히 가도 늦지 않은 날','뜻밖의 칭찬을 듣는 날','정리하면 운이 트이는 날','첫 느낌을 믿어도 좋은 날','웃을 일이 하나 더 생기는 날','산책이 좋은 생각을 주는 날','말보다 행동이 빛나는 날','좋아하는 음식이 행운을 부르는 날','기다리던 소식이 가까워지는 날','오늘 한 약속이 오래 가는 날','가벼운 도전이 잘 풀리는 날','쉬어 가는 것도 실력인 날','집중력이 평소보다 좋은 날','누군가에게 힘이 되어 주는 날','계획대로 착착 풀리는 날','사소한 행운을 줍는 날','마음이 넓어지는 날','기억력이 반짝이는 날','새로운 인연이 가까워지는 날','오늘 고른 길이 맞는 날'],
 en:['A good day to finish what you put off','Someone you miss may reach out','A small kindness comes back bigger','A great day to learn something new','Going slowly is still going forward','Unexpected praise is on its way','Tidying up opens the way for luck','Trust your first instinct today','One more reason to smile today','A walk brings a good idea','Actions speak louder than words today','Your favourite food brings luck','The news you are waiting for is getting closer','A promise made today will last','Small challenges go your way','Resting well is a skill today','Your focus is sharper than usual','You will be someone\'s source of strength','Things go according to plan','You will pick up a little luck','Your heart feels wider today','Your memory shines today','A new connection is close','The path you choose today is the right one'],
 th:['วันดีที่จะทำเรื่องที่ค้างไว้ให้เสร็จ','อาจมีคนที่คิดถึงติดต่อมา','น้ำใจเล็ก ๆ จะย้อนกลับมาอย่างยิ่งใหญ่','วันดีสำหรับการเรียนรู้สิ่งใหม่','ค่อย ๆ ไปก็ไม่สายเกินไป','จะได้รับคำชมที่ไม่คาดคิด','จัดระเบียบแล้วโชคจะเปิดทาง','เชื่อความรู้สึกแรกของคุณได้เลย','จะมีเรื่องให้ยิ้มเพิ่มอีกหนึ่งเรื่อง','การเดินเล่นจะนำความคิดดี ๆ มาให้','วันนี้การกระทำมีค่ามากกว่าคำพูด','อาหารจานโปรดจะนำโชคมาให้','ข่าวที่รอคอยใกล้เข้ามาแล้ว','สัญญาที่ให้ไว้วันนี้จะยั่งยืน','ความท้าทายเล็ก ๆ จะผ่านไปได้ด้วยดี','การพักผ่อนให้ดีก็เป็นฝีมืออย่างหนึ่ง','สมาธิดีกว่าปกติ','คุณจะเป็นกำลังใจให้ใครบางคน','ทุกอย่างเป็นไปตามแผน','จะได้รับโชคเล็ก ๆ น้อย ๆ','ใจกว้างขึ้นในวันนี้','ความจำเฉียบคมเป็นพิเศษ','สายสัมพันธ์ใหม่อยู่ใกล้แค่เอื้อม','เส้นทางที่เลือกวันนี้คือทางที่ใช่']};
const LB_COLORS=[['#b98cff','보라','Purple','ม่วง'],['#6fc3ff','하늘색','Sky blue','ฟ้า'],['#4fe0b5','민트','Mint','มิ้นต์'],['#ffd23f','노랑','Yellow','เหลือง'],['#ff9f43','주황','Orange','ส้ม'],['#ff7eb6','분홍','Pink','ชมพู'],['#ff5a5a','빨강','Red','แดง'],['#6fd36f','초록','Green','เขียว'],['#ffffff','흰색','White','ขาว'],['#5b6cff','남색','Indigo','คราม']];
function lbLuckyToday(){ const d=bt_today(); let h=2166136261>>>0; for(let i=0;i<d.length;i++){ h^=d.charCodeAt(i); h=Math.imul(h,16777619)>>>0; }
  const L=LB_LUCKY[CURRENT_LANG]||LB_LUCKY.ko, c=LB_COLORS[(h>>>8)%LB_COLORS.length];
  return { line:L[h%L.length], color:c[0], cname:c[{ko:1,en:2,th:3}[CURRENT_LANG]||1], num:1+((h>>>16)%9) }; }
function lbMission(){ const set=missionToday(), m=missionLoad(); const done=set.filter(id=>m.done.includes(id)).length;
  return { set, m, done, next:set.find(id=>!m.done.includes(id)), all:done>=set.length }; }
function lbLuckyHTML(ms){
  if(!ms.all) return '<div class="lb-lucky locked" onclick="lbPlay()"><div class="lk-back">🔒</div><div class="lk-txt"><b>'+t('lb.lucky.title')+'</b><span>'+t('lb.lucky.lock').replace('{d}',ms.done)+'</span></div></div>';
  const L=lbLuckyToday(), loc={ko:'ko-KR',en:'en-US',th:'th-TH'}[CURRENT_LANG]||'ko-KR';
  let day=''; try{ day=new Date().toLocaleDateString(loc,{month:'short',day:'numeric'})+' · '; }catch(e){}
  return '<div class="lb-lucky open"><div class="lk-k">'+day+t('lb.lucky.title')+'</div><div class="lk-line">“'+L.line+'”</div>'+
    '<div class="lk-meta"><span><i class="lk-sw" style="background:'+L.color+'"></i>'+t('lb.lucky.color')+' <b>'+L.cname+'</b></span><span>'+t('lb.lucky.num')+' <b>'+L.num+'</b></span></div></div>'; }
function lbRenderLucky(elId){ const el=document.getElementById(elId); if(!el) return; const ms=lbMission(); el.innerHTML=lbLuckyHTML(ms);
  // 처음 열리는 순간만 뒤집히며 등장(하루 한 번)
  if(ms.all && el.offsetParent){ let seen=null; try{ seen=localStorage.getItem('brain.lucky.seen'); }catch(e){}
    if(seen!==bt_today()){ try{ localStorage.setItem('brain.lucky.seen',bt_today()); }catch(e){}
      const c=el.firstChild; if(c) c.classList.add('reveal'); track('lucky_open',{}); setTimeout(()=>{ try{ sfx('medal','gold'); }catch(e){} },250); } } }
function lbGoLucky(){ const ms=lbMission(); if(!ms.all){ lbPlay(); return; } const el=document.getElementById('lb-lucky'); if(el) el.scrollIntoView({behavior:'smooth',block:'center'}); }
function lbPlay(){ const ms=lbMission(); if(ms.next){ track('home_play',{game:ms.next}); showScreen(ms.next); } else lbGoLucky(); }
function lbGreet(){ const h=new Date().getHours(); return t(h<5?'lb.greet.n':h<12?'lb.greet.m':h<18?'lb.greet.a':h<23?'lb.greet.e':'lb.greet.n'); }
// 결과 화면: 오늘의 3판이면 진행도와 다음 판, 3판을 다 했으면 행운 카드 알림
function lbResultLine(id, m){ try{
  const set=missionToday(); if(!set.includes(id)) return;
  const card=document.getElementById(id+'-result-card'), box=card&&card.querySelector('.pg-box'); if(!box) return;
  const old=box.querySelector('.lb-res'); if(old) old.remove();
  const done=set.filter(g=>m.done.includes(g)).length, next=set.find(g=>!m.done.includes(g));
  const html= next ? '<div class="pg-line pg-good lb-res">🧠 '+t('lb.d3.prog').replace('{d}',done).replace('{g}',t(gameMeta(next).key))+' <button class="pg-btn" onclick="showScreen(\''+next+'\')">'+t('lb.go.next')+'</button></div>'
                   : '<div class="pg-line pg-good lb-res">🎁 '+t('lb.lucky.unlocked')+' <button class="pg-btn" onclick="showScreen(\'home\')">'+t('lb.go.home')+'</button></div>';
  box.insertAdjacentHTML('afterbegin', html); }catch(e){} }
let _lbTimer=0, _lbGrp=null;
function lbTick(){ const home=document.getElementById('screen-home'); if(!home||!home.classList.contains('active')) return;
  const n=new Date(Date.now()+9*3600*1000), ms=86400000-(n.getUTCHours()*3600000+n.getUTCMinutes()*60000+n.getUTCSeconds()*1000+n.getUTCMilliseconds());
  const s=Math.floor(ms/1000), p2=v=>String(v).padStart(2,'0');
  setTxt('lb-count', t('lb.puz.next').replace('{t}', p2(Math.floor(s/3600))+':'+p2(Math.floor(s%3600/60))+':'+p2(s%60))); }
function lbAbilShelf(){ const el=document.getElementById('lb-abil'); if(!el) return;
  const ids=trainingIds(); lbFill(el, HOME_GAMES.filter(g=>g.grp===_lbGrp && ids.includes(g.id) && lbVisible(g)).map(g=>lbCard(g,{lazy:true,from:'abil',tag:gameBestVal(g.id)>0?'🏆 '+gameBestVal(g.id):''})));
  document.querySelectorAll('#lb-chips .lb-chip').forEach(c=>c.classList.toggle('on', c.dataset.g===_lbGrp)); }
function renderHome(){
  const v=homeVisit(), ms=lbMission();
  _featureId=ms.next||'games';
  setTxt('lb-greet', lbGreet());
  const sk=document.getElementById('lb-streak'); if(sk){ sk.textContent='🔥 '+v.streak; sk.title=t('lb.streak').replace('{n}',v.streak); }
  // ① 오늘의 두뇌 3판
  const ring=document.getElementById('lb-ring'); if(ring) ring.style.setProperty('--p', Math.round(ms.done/ms.set.length*100)+'%');
  setTxt('lb-ring-n', ms.done+'/'+ms.set.length);
  setTxt('lb-d3-sub', ms.all ? t('lb.d3.done') : t('lb.d3.left').replace('{n}', ms.set.length-ms.done));
  lbFill(document.getElementById('lb-d3-cards'), ms.set.map(id=>{ const g=gameMeta(id), d=ms.m.done.includes(id);
    return lbCard(g,{done:d, tag:d?'✓ '+t('lb.done'):t(g.grp), from:'d3'}); }));
  const gift=document.getElementById('lb-gift'); if(gift) gift.innerHTML=t(ms.all?'lb.gift.open':'lb.gift.lock');
  setTxt('lb-play', t(ms.all?'lb.play.lucky':'lb.play.next'));
  // ② 오늘의 퍼즐
  lbFill(document.getElementById('lb-puz'), ['moamoa','queens','tango'].map(gameMeta).filter(lbVisible).map(g=>{ const d=lbSeen(g.id);
    return lbCard(g,{done:d, tag:d?'✓ '+t('lb.done'):t('lb.new'), from:'puzzle'}); }));
  lbTick(); if(!_lbTimer) _lbTimer=setInterval(lbTick,1000);
  // ③ 오늘의 운세 — 행운 카드 + 운세 바로가기
  lbRenderLucky('lb-lucky');
  const fc=document.getElementById('lb-fchips');
  if(fc){ fc.innerHTML=''; ({ko:['unse','zodiac','ttirank','tarot'], en:['zodiac','persona','luckycolor'], th:['luckycolor','zodiac','tarot','persona']}[CURRENT_LANG]||[]).forEach(id=>{
    const g=gameMeta(id); if(!lbVisible(g)) return; const b=document.createElement('button'); b.className='lb-fchip';
    b.innerHTML='<b>'+g.emoji+'</b>'+t(g.key)+(lbSeen(id)?'':'<i class="lb-dot"></i>'); b.onclick=()=>lbOpen(g); fc.appendChild(b); }); }
  // ④ 추천 선반(약점·안 해본 게임 우선) + 능력별 선반
  let picks=[]; try{ picks=recommendGames('home',8); }catch(e){}
  ['iq','sudoku','merge','run','stroop','whack'].forEach(id=>{ if(picks.length<8 && !picks.some(g=>g.id===id)) picks.push(gameMeta(id)); });
  lbFill(document.getElementById('lb-rec'), picks.slice(0,8).map(g=>lbCard(g,{lazy:true,from:'rec',tag:gameBestVal(g.id)>0?'🏆 '+gameBestVal(g.id):''})));
  const ids=trainingIds(), grps=[]; HOME_GAMES.forEach(g=>{ if(ids.includes(g.id) && lbVisible(g) && !grps.includes(g.grp)) grps.push(g.grp); });
  if(!grps.includes(_lbGrp)) _lbGrp=grps[0];
  const chips=document.getElementById('lb-chips');
  if(chips){ chips.innerHTML=''; grps.forEach(k=>{ const c=document.createElement('button'); c.className='lb-chip'; c.dataset.g=k; c.textContent=t(k); c.onclick=()=>{ _lbGrp=k; lbAbilShelf(); }; chips.appendChild(c); }); }
  lbAbilShelf();
  // ⑤ 이번 주 나
  try{ renderWeek(); renderCollection(); }catch(e){}
  // 랜딩 내부링크 푸터는 언어별
  const ftr=document.getElementById('site-footer');
  if(ftr){
    if(!ftr.dataset.ko) ftr.dataset.ko=ftr.innerHTML; // ko 원본 보존(언어 전환 시 복원용)
    ftr.style.display='';
    if(CURRENT_LANG==='en'||CURRENT_LANG==='th'){
      const L=CURRENT_LANG;
%FOOTER%
    } else {
      ftr.innerHTML=ftr.dataset.ko;
    }
  }
}
// 운세 화면(하단 탭) — 행운 카드 + 운세·성격 테스트 목록
function renderFortune(){
  lbRenderLucky('ft-lucky');
  const el=document.getElementById('ft-list'); if(!el) return; el.innerHTML='';
  const ids={ko:['unse','zodiac','ttirank','tarot','luckycolor','persona','braintype'], en:['zodiac','persona','luckycolor','braintype'], th:['luckycolor','zodiac','tarot','persona','braintype']}[CURRENT_LANG]||[];
  ids.forEach(id=>{ const g=gameMeta(id); if(!lbVisible(g)) return; const b=document.createElement('button'); b.className='ft-item';
    b.innerHTML='<b>'+g.emoji+'</b><span><span class="ft-n">'+t(g.key)+'</span><span class="ft-d">'+t('lb.f.'+id)+'</span></span>'+(lbSeen(id)?'':'<i class="lb-dot"></i>');
    b.onclick=()=>lbOpen(g); el.appendChild(b); });
}
'''
old_home = p.s[a:b]
fa = old_home.index("      ftr.innerHTML='<a href=\"sudoku/?lang=en\">")
footer_line = old_home[fa:old_home.index(p.nl, fa)]
HOME_JS = HOME_JS.replace('%COVERS%', repr(COVERS).replace("'", '"')).replace('%FOOTER%', footer_line)
p.s = p.s[:a] + HOME_JS.replace('\n', p.nl) + p.s[b:]

# 전체 게임 화면: 표지 카드
R("""    const grid=document.createElement('div'); grid.className='home-grid'; body.appendChild(grid);
    byGrp[grp].forEach(g=>{
      const card=document.createElement('button'); card.className='home-card';
      card.onclick=()=>{ if(g.external){ goExternal(g); return; } showScreen(g.id); };
      card.innerHTML=gameCardHTML(g); grid.appendChild(card);
    });""", """    const grid=document.createElement('div'); grid.className='lb-grid'; body.appendChild(grid);
    byGrp[grp].forEach(g=>{
      const daily=g.grp==='cat.daily'||g.grp==='cat.fun', best=(!g.external&&g.id!=='braintype')?gameBestVal(g.id):0;
      grid.appendChild(lbCard(g,{lazy:true, from:'games', tag:best>0?'🏆 '+best:'', dot:daily&&!lbSeen(g.id)}));
    });""")
p.save()
