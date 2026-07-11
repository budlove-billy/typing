# MEMORY.md — Long-Term Memory
> Project: brain

_Write important context, decisions, and lessons here so future sessions can pick up where you left off._

## 디자인 시스템 (2026-07-12 상용화 리프트 — 캐릭터/오브젝트/손맛/입체/테마)
- **Mallow 마스코트 = 인라인 SVG**. `mallowSVG(mood,{size,variant,cls,attrs,standalone})` → SVG 문자열.
  mood: `default|happy|success|sad|focus`. variant(몸통색): `cream(기본)|pink|mint|sky|lemon|grape` (MALLOW_VARIANTS).
  **얼굴 = 원본 mallow-chan.png 마시멜로 감성**(네모 둥근사각 눈 `_EYES` + 작은 'w' 입 + 핑크 볼 `_mCheeks`). 동그란 아기눈은 "무섭다" 피드백으로 폐기(2026-07-12). 몸통=살짝 눌린 필로우형.
  공유 그라데이션 defs는 `_mgDefs()`가 body에 1회 주입(id=`mg_<variant>`). **캔버스/데이터URL용은 `standalone:true`**(defs 인라인). 픽셀 PNG(mallow-chan.png)는 **폐기**.
  HTML 자리표시는 `data-mallow="happy" data-mallow-size="30" data-mallow-variant="mint"` → `initMallowUI()`가 렌더. 로고/공유카드/bubble·catch·chop·whack·count 전부 SVG.
- **오브젝트 헬퍼**: `forkSVG(size)`(catch 장애물·금속 포크), `basketSVG(size)`(catch 바구니·위커). whack 팝업/count 인원=Mallow SVG.
- **손맛 FX 레이어**(음소거와 무관): `sfx('good')`/`sfx('win')`가 **sndOn() 게이트 앞에서** `fxBurst(_fxXY,...)` 호출 → **정답 시 sfx 부르는 38개 지점 전 게임 자동 파티클**. `_fxXY`=마지막 pointerdown 좌표.
  API: `fxBurst(x,y,{count,spread,color})` `fxScorePop(x,y,'+N',color)` `fxCombo('xN COMBO!')` `fxCelebrate(el,text,color)`. prefers-reduced-motion 존중. whack·catch는 +점수/콤보 배지 명시 호출.
- **입체 토큰**: `.btn/.ca-btn/.fk-btn`=그라데이션+그림자+누름, `.diff-btn`=화이트 그라데 카드+호버 리프트, `.fm-cell/.df-cell`=타일감. **텍스트 격자(sudoku/nono/wordsearch)·색구분(spot/odd)은 평면 유지**(가독성).
- **축별 테마 배경**: `body[data-axis="<axis>"]` 상단 글로우 그라데(--glow). `showScreen`이 `_gameAxis(id)`(HOME_GAMES grp 기반+vocab/typing/braintype/moamoa 보정)로 설정. 홈/게임/기록=`home`(브랜드 틴트). 12축: memory/focus/speed/coord/sound/sight/space/calc/logic/lang/daily/fun.
- 검증: `.logs/errcheck.mjs`(playwright, 34종 start 후 pageerror 0 확인), `.logs/shots.mjs`+`sheet.mjs`(콘택트시트). playwright는 npx캐시 경로 import(`_npx/e41f203.../playwright`).

## 앱 구조
- **`index.html` = `brain_app.html`** (바이트 동일 유지). "말랑말랑 두뇌체조" — **서버 없는 단일 HTML SPA**.
  게임 수정 시 **두 파일 모두 동기화**할 것 (`cp index.html brain_app.html`).
- **네비(2026-07-06 개편, Phase2)**: 상단 `<nav>`=로고+언어만. **하단 탭바 `.tabbar`**=홈/게임/내기록 3탭(랭킹은 서버 없어 보류).
  `showScreen(id)`: `.screen` 토글 + **하단 탭 활성**(`TAB_FOR[id]||'games'`, 게임 id는 '게임' 탭). `nav-<id>` 참조 없음(제거됨).
  `haltRunningGames()`가 showScreen마다 전 게임 reset(타이머 정리·intro 복귀). `window.scrollTo(0,0)`.
- **홈**: `renderHome` = 오늘의 추천 큰 카드(`#home-feature`, 미션 다음 게임 → `featureStart`) + 오늘의 목표(hg-plays/streak/records)
  + 게임 모음 카테고리 칩(`#home-cats`→게임탭) + 인기 게임(`#home-popular`, 큐레이션 flash/stroop/react/rotate).
- **전체 게임**: `#screen-games`/`renderGames` = 카테고리별 통일 카드. **내 기록**: `#screen-records`/`renderRecords` = 통계+게임별 최고점.
- 게임 1개 = intro/game/result 3카드 패턴. **다국어**: `I18N`(각 키 {ko,en,th}) + `t(key)` + `applyLanguage()`.
  동적 문자열은 `refreshDynamicTexts()`에 갱신 훅(home/games/records 활성 시 재렌더).
- **통일 카드**: `gameCardHTML(g)` = 이모지/이름/카테고리(`t(g.grp)`)/🏆기록. HOME_GAMES 각 항목 `grp`='cat.*'(소프트 카테고리).
- 재사용 CSS: `.card .btn .btn-outline .difficulty-row .diff-btn(3열) .result-row .section-head .mg-timer .home-card .home-grid`.
- 색(차분): `:root` 포인트 `--purple`=#4F7CFF(파랑), 성공 `--teal`=#21A67A, 배경 #F5F7FB, 텍스트 #182235. 게임 이모지·공유카드 강조색은 컬러 유지.

## 게임 목록 (인지 축)
- 기존: 한글타자·영단어·IQ·스도쿠·암산 → 계산/타이핑/논리 축.
- **신규(2026-07-06 추가): 순간기억(flash), 인원수 세기(count)** → **기억 축**을 채움.
  - 순간기억: 5×5 격자 숫자 순간표시→순서탭. 적응형(성공 N+1/실패 N−1), lives 3. `FM` 객체.
  - 인원수 세기: 집에 입/출(들어가면 숨김) 애니메이션 후 "몇 명?" 4지선다. streak 점수, lives 3. `HC` 객체.
  - 둘 다 **localStorage** 최고기록 영속화: 키 `brain.flash.best` / `brain.count.best`,
    스키마 `{easy|normal|hard:{all,day,date}}`. 헬퍼 `bt_*`. "오늘 최고 · 전체 최고" 표시(데일리 재방문 훅).
- **신규(2026-07-06 추가): 색깔 맞추기/스트룹(stroop), 순서 잇기/Trail(trail)** → **주의·속도 축**을 채움.
  - 스트룹: 색이름 글자를 다른 잉크색으로 표시 → 잉크색 버튼 탭. 60초 타임어택, combo, 부조화확률 난이도. `ST` 객체.
  - 순서 잇기: 흩어진 1..N 순서대로 탭, 판 클리어마다 N+1. 60초 최다 판. `TR` 객체.
  - 오답 페널티 = 시간 −2초. localStorage: `brain.stroop.best` / `brain.trail.best`.
- **신규(2026-07-06 추가): 두뇌 유형 테스트(braintype)** → **바이럴 축**. 게임 아님, 유입·공유 엔진.
  - 6문항 성향 테스트 → 6유형(calc/word/memory/focus/quick/logic) argmax(동점=BT_ORDER 순).
  - 각 유형이 앱 내 게임 추천으로 연결(math/vocab/flash/stroop/trail/iq) → 테스트→플레이 유입 루프.
  - **canvas 공유카드**(600×800): `btDrawCard`→미리보기, `btShare`→Web Share(files)/PNG 다운로드 폴백.
  - 문항/유형은 `BT_QUESTIONS`/`BT_TYPES`에 {ko,en,th} 인라인(IQ 방식), `btL()`로 언어 선택.
- **신규(2026-07-06 추가): 규칙 바꾸기(switch)** → **유연성 축**(인지 전환/set-shifting).
  - 규칙(홀짝 ↔ 5보다 크기)이 확률로 전환, 지금 규칙에 맞게 판단. 60초 타임어택, combo, 오답 −2초. `SW` 객체.
  - 숫자는 5 제외(SW_NUMS). localStorage `brain.switch.best`.
- **신규(2026-07-06 추가): 엔백(nback)** → **기억 축**(작업기억 업데이트). 글자 서열에서 N칸 전과 같으면 [일치].
  60초, 난이도=N(1/2/3)+속도, 일치율 0.30·우연일치 방지. `NB` 객체(timer+step 2개 인터벌). `brain.nback.best`.
- **신규(2026-07-06 추가): 도형 회전(rotate)** → **새 공간지각 축(home.grpSpace)**. 두 글자도형 비교, 오른쪽이
  회전만이면 '같다'/거울상이면 '다르다'. CSS transform rotate+scaleX(-1). 각도 0° 제외. `RT` 객체. `brain.rotate.best`.
  주의: 상태객체 `RT`(회전)와 trail의 `TR`(순서잇기)는 다름. rotate DOM id는 `rt2-*`/`rot-*`.
- **신규(2026-07-06 추가): 카드 짝 맞추기(cards)** → **기억 축**(시각기억). 뒤집힌 카드 짝 맞추기, 판 클리어 시 쌍+1.
  60초, combo, `shuffleArr` 재사용, 덱=각 그림 2장. `CM` 객체(timer+flipT). `brain.cards.best`.
- **신규(2026-07-06 추가): 반응 속도(react)** → **주의·속도 축**(Go/No-Go, 반응억제). 초록에 빠르게 탭/빨강 참기.
  **시행 기반(60초 아님)**, `performance.now()`로 RT 측정, 점수=빠를수록↑(하한20)/No-Go 참기 +120, 반칙 combo리셋.
  결과에 평균 RT 표시. `RC` 객체(waitT/nogoT/fbT 3타이머, state머신 waiting/go/nogo/resolved). `brain.react.best`.
- **공유카드 일반화(2026-07-06)**: `makeShareCard(...)` + `shareOrDownload()`. 점수게임 9종 `gameShare('<id>')`
  (flash/count/nback/cards/stroop/trail/react/switch/rotate). braintype도 이 헬퍼로 통일.
- **홈/대시보드(2026-07-06)**: `#screen-home` 기본 랜딩. `HOME_GAMES`(grp별, 15항목) 그리드 + 최고기록 뱃지.
  히어로 통계 3종 + **오늘의 미션(Daily Workout)**. 연속 출석 `homeVisit()`/`brain.visit`.
  nav는 아이콘+라벨 세로 칩(모바일도 라벨). 모바일 @media 640/360.
- **오늘의 미션(2026-07-06, Lumosity Daily Workout 참고)**: 매일 축 섞은 3게임을 날짜 시드로 선정
  (`missionToday()` = 기억A/주의·속도B/유연·공간C 풀에서 1개씩). 홈 미션카드(3칩+진행 n/3), 각 게임 `finishXXX`가
  `missionMark(id)` 호출→localStorage `brain.mission`{date,done} 체크. 3개 완료 시 카드 완료상태.
  톤: **재미/휴식**("머리 식힐 겸 3판") — FTC 교훈대로 효능 단정 없음.
- 게임/콘텐츠 **활성 16종(2026-07-10 버블 포함)**(2026-07-10 vocab/typing 소프트 비활성 — HOME_GAMES 주석 처리, 화면/JS/i18n은 보존, 재활성=주석 해제).
  비활성 사유: 두뇌게임 포지셔닝 불일치 + en/th 미대응. braintype 언어가형 추천은 vocab→nback으로 변경됨.
  축: 계산·타이핑·논리 / 기억(순간·인원·엔백·카드) / 주의·속도(스트룹·순서·반응) / 유연성 / 공간지각 / 언어 / 바이럴 + 홈.
- **두뇌 능력치(2026-07-06)**: 내 기록에 7능력 레이더+막대(ABILITY_MAP 가중치·GAME_REF 정규화, brain.ability.base 주간성장). 막대 탭→기여게임. saveFlatBest로 math/iq/vocab/sudoku/typing 최고점 저장(brain.<id>.flat). IQ점수=55+정답률^1.3*75+속도*15(55~145). FTC: '게임 수행 기반·실제 지능 아님'.
- **신규(2026-07-10): 말로우 팡팡(whack)** → 협응 축(cat.coord). 3x3 구멍에서 마스코트 탭/💣 참기(탭 시 시간-3s),
  60초, WK_CFG(win/gap/badP), 못 잡으면 콤보 리셋. `WK` 객체(timer+spawnT+hideT). `brain.whack.best`. 마스코트 활용 1호 게임.
- **신규(2026-07-10): 멜로디 기억(melody)** → 청각 축(cat.sound). 사이먼류 4패드(C4/E4/G4/B4, _beep 재사용),
  재생 중 입력 잠금(playing), 성공 len+1/실패 lives-1(3). `ML` 객체(timers[]). `brain.melody.best`.
- 미션 풀: A=[flash,count,nback,cards,melody], B=[stroop,trail,react,whack,spot,chop], C=[switch,rotate,slide].
- **신규(2026-07-10): 모아모아(moamoa)** — 한국어 Connections류 데일리 낱말 퍼즐. **SPA 편입 아님**: `/moamoa/index.html` 별도 정적 페이지
  (자체 header/모달·KST 데일리·이모지 공유·streak·localStorage `moamoa_state_v1`/`moamoa_stats_v1`).
  HOME_GAMES에 `{id:'moamoa', koOnly:true, external:'moamoa/'}` — **ko에서만 노출**(renderGames/홈 칩 필터), 카드 클릭=location.href.
  홈 카드에 오늘 미완료 ● 뱃지(.home-card-dot). 내기록/능력치/미션에서는 제외. 퍼즐 30일치 내장(EPOCH 2026-07-10),
  **D+25쯤 추가 제작 필요** — moamoa/validate_puzzles.cjs로 검증, 제작 원칙은 moamoa/README.md. 원본 드롭은 shared/(gitignore).
- **도전장 링크(2026-07-10)**: 아케이드 11종 결과에 sendChallenge(game) 버튼 → `?c=game.score.diff` URL 공유.
  수신 chReceive()(파라미터 검증+난이도 세터+인트로 배너+화면 직행), 판정 chCheck(id)는 missionMark 관문에서 호출(이기면 CH=null).
  GA: challenge_send/open/result.
- **가이드 페이지(2026-07-11)**: `/guide/` 6종 — brain-games(허브)/sudoku/2048/iq-test/color-sort/slide-puzzle.
  실전 공략 콘텐츠(양산형 아님), 생성기 .logs/gen_guides.py(gitignore), 랜딩과 동일 스타일+crumb.
  홈 푸터·랜딩 3종에서 링크, sitemap 등재. 신규 게임 추가 시 검색 수요 있으면 가이드도 함께 검토.
- **키워드 랜딩(2026-07-10)**: `/sudoku/` `/iq-test/` `/braintype/` 정적 페이지(특징·방법·FAQ·canonical·GA4).
  본체 진입은 `?game=<id>` 딥링크(screen-<id> 존재 검증). 홈 하단 .site-footer 내부링크(ko에서만 표시). sitemap 등재.
- **공유카드 v2(2026-07-10)**: makeShareCard = 그라데이션 배경+흰 카드+다크 텍스트, 상단 마스코트(_mascotImg 프리로드,
  pixelated)+Mallow, lines[0]=포인트색 대형 점수, 하단 playmallow.com 워터마크 강조. API(o.emoji/title/lines/desc/note) 불변.
- **신규(2026-07-10): 버블 톡톡(bubble)** → 계산 축(cat.calc) 2호. 파스텔 버블 탭으로 목표 합 만들기(Number Sum류, 토스 금고팡 참고).
  60초, 정답 부분집합 선생성으로 목표 항상 달성 가능(54,000판 시뮬 검증), 3판마다 조합 길이+1·판마다 숫자+2 난이도 상승,
  초과=콤보 리셋(시간 페널티 없음). `BB` 객체, `brain.bubble.best`, 도전장(CH_GAMES)·공유·능력치(calc60/logic25/speed15, REF 350) 연동. 활성 16종.
- **기록 백업(2026-07-10)**: 내 기록 화면 하단 backupExport/backupImport — `brain.*`+`moamoa_*` 키를 `MLW1.`+base64(JSON) 코드로
  내보내기(클립보드)/가져오기(prompt). 병합: `.best`=난이도별 all max·최신 date의 day, `.flat`=max, 그 외는 기존 기기 값 유지.
  로그인 없는 기기 이전용 — 로그인(Supabase+카카오, 백업 전용)은 리텐션 신호 후 Phase C 검토로 결정(2026-07-10 논의).
  ⚠️ 사용자 Supabase 무료 계정은 프로젝트 2/2 슬롯 사용 중(하나는 flipper용) — 로그인 착수 시
  flipper 프로젝트 정리 또는 새 계정 필요. 이 준비 비용까지 감안해 로그인은 보류, 신호 확인 후 진행(2026-07-10 사용자 결정).
- **신규(2026-07-10): 다른 색 찾기(spot)** → 관찰력 축(cat.sight) 신설(앱인토스 '절대 색감' 포맷 검증 후 제작).
  n×n 중 명도만 다른 타일 1개 탭. 3레벨마다 판+1(상한 6/7/8), 레벨마다 색차 감소(하한 Δ5/4/3%p — 시뮬 검증).
  60초·오답 -2s. `SP` 객체, `brain.spot.best`, 도전장·공유·능력치(focus50/speed30/space20, REF 400)·미션 풀 B 연동. 활성 17종.
- **신규(2026-07-10): 슬라이딩 퍼즐(slide)** → 공간지각 축(cat.space) 2호. 3×3/4×4/5×5, 완성형(타임어택 아님).
  셔플=풀린 상태에서 유효 이동 K회(60/150/300, 직전 되돌리기 금지) → 항상 해결 가능(9,000판 시뮬 검증).
  점수=base(600/1200/2000)−초×3−이동수(하한 10). 제자리 타일 teal 링, 값 기반 파스텔 그라데이션, 절대배치+CSS 슬라이드.
  `SL` 객체, `brain.slide.best`, 도전장·공유·능력치(space60/logic25/focus15, REF 700)·미션 풀 C 연동. 활성 18종.
- **신규(2026-07-11): 말랑 2048(merge)** → 계산 축 3호(hi5games '매치냥' 검토 후 원작 MIT 규칙 재구현).
  난이도=판 크기(easy 5×5/normal 4×4/hard 3×3), 스와이프(touch, .mr-board-wrap touch-action:none)+방향키, 되돌리기 1회(MR.prev 1슬롯),
  2048 도달 시 win 팡파르 후 계속, '기록하고 끝내기' 버튼. 순수 mrMoveLine(압축→1회 병합→압축, 시뮬 9케이스+999판 검증).
  `MR` 객체, `brain.merge.best`, 도전장·공유·능력치(calc50/logic30/space20, REF 6000) 연동. 미션 풀 제외(계산 축 관례). 활성 19종.
- **신규(2026-07-11): 말로우 타워(chop)** → 순발력 축 3호(팀버맨류, hi5games '숲속의 나무꾼' 검토 후 마시멜로 깨물기로 재테마).
  좌/우 탭(버튼+방향키)으로 타워 깨물기, 포크(🍴) 쪽=아웃(바닥 포크 쪽 이동도 아웃), 시간 게이지 상시 감소+깨물면 회복,
  점수 오를수록 감소 가속(accel). 생성 규칙: 포크 다음 칸은 반드시 빈 칸(완벽 플레이 무한 생존 시뮬 검증).
  `CP` 객체, `brain.chop.best`, 도전장·공유·능력치(speed70/focus30, REF 130)·미션 풀 B 연동. 활성 20종.
- **신규(2026-07-11): 컬러 소트(sort)** → 논리 축 3호(워터소트류, hi5games 소트 3종 검토 후 재구현). 4/6/8색+빈 병 2,
  용량 4, 같은 색 위에만 붓기(연속 런 일괄). 생성마다 내장 솔버(soSolvable, 메모 DFS 6만 노드 캡)로 해결 가능 보증
  +시작부터 완성된 병 배제. 되돌리기 3회(undo도 move+1), 점수=base(500/1000/1600)−초×2−이동×3.
  `SO` 객체, `brain.sort.best`, 도전장·공유·능력치(logic60/space20/focus20, REF 650) 연동. 미션 풀 제외. 활성 21종.
- **신규(2026-07-11): 다른 모양 찾기(odd)** → 관찰력 축(cat.sight) 2호. spot(색차)과 대비되는 **형태(회전)차** — n×n 화살표 중 1개만 각도 다름, 탭.
  spot 로직 미러링(3레벨마다 판+1 상한 6/7/8, 레벨마다 각도차 감소 하한 aMin 20/15/11°), 유일성=delta>0 보장(SVG 화살표 비대칭). 60초·오답 -2s.
  `OD` 객체, `brain.odd.best`, ABILITY_MAP odd={focus:40,space:30,speed:30} REF 400, 공유·도전장·미션 풀 B 연동. 활성 22종. Wave1 1호.
- **신규(2026-07-12): Wave2-3 7종 일괄 배포** → 활성 **30종**. 로드맵(`신규게임-기획-능력영역별.md`) 나머지 전부 구현, 한 번에 라이브.
  - **flank(화살표 집중/집중)**: 플랭커 과제. 가운데 화살표 방향 답(◀▶), 양옆 무시. 60s·오답-2s. FK. incong 확률 난이도. ABILITY {focus:60,speed:30,logic:10}, 미션B.
  - **guess(어림 계산/계산)**: 식의 근사값 3택(유일 최근접 보장, 보기간격≥unit*0.42). 60s. GU. maxOperand 30/90/400. {calc:70,speed:20,focus:10}. 미션 제외.
  - **rev(거꾸로 기억/기억)**: backward digit span. 숫자 순차표시→키패드 역순입력. len+lives. RV. {memory:70,focus:30}, 미션A.
  - **rhythm(리듬 따라하기/청각)**: 박자 재생→탭 재현. 템포정규화 판정(min기준 비 1.7 임계, ≥1 short). len+lives, performance.now. RH. {memory:50,focus:30,speed:20}, 미션A.
  - **catch(마시멜로 받기/협응)**: 4레인 낙하물 바구니로 받기(🍡 받고 🍴 피함). 60s, tick 40ms·spawn간격. CA. {speed:50,focus:30,space:20}, 미션B. 포크는 내 레인일 때만 페널티(-3s)→불가피 손해 없음.
  - **fit(블록 채우기/공간)**: 폴리오미노 3조각 탭선택→탭배치, 줄 소거. 데드락 시 종료(그리디 6×6 최소16조각 검증). FT. {space:60,logic:25,focus:15}, 미션C.
  - **nono(픽셀 로직/논리)**: 노노그램. 라인솔버 유일해 생성(무추론 보장, 5/8/10 즉시생성 검증). 카운트업, base-시간. 칠하기/X 토글. NO. {logic:60,focus:25,space:15}. 미션 제외.
  - **anagram(글자 맞추기/언어)**: vocab/typing 대체(언어 축 0→채움). 셔플 글자 재배열, 정답선지정→사전검증불요. **ko+en 동시**(음절/알파벳 타일), th 숨김(langs:['ko','en'] 필터). 힌트3. 60s. AG. {lang:70,memory:20,focus:10}. 미션 제외.
  - 선검증: `.logs/gen_sim.mjs`(nono유일해/fit생존/guess보기/rhythm판정/anagram셔플), 배선정합성 `.logs/wire_check.mjs`. 미션풀 A+rev,rhythm / B+flank,catch / C+fit.
  - ⚠️ 라이브 스모크 테스트 미완(이 환경 playwright/webread 없음) — 각 게임 실제 플레이 확인 필요(특히 nono 클루 레이아웃, catch 낙하 타이밍, rhythm 오디오 resume).
- **결과 화면 추천(2026-07-12)**: 모든 게임 결과카드 하단에 **약점 보완 추천 3종**. `missionMark(id)`에서 `renderRecs(id)` 호출(공통 훅) →
  `recommendGames(cur,3)`: need = 0.55*(100-gameLevel) + 0.45*(약한 능력축 가중) + 미플레이 가점22 + 소량 랜덤. 자기자신/external/braintype/lang필터 제외, ABILITY_MAP 있는 게임만.
  `<id>-result-card`에 `.rec-box` append(중복 제거). i18n `rec.title`. 결과카드 없는 게임(iq/math 등 일부)은 자동 skip. 검증 `.logs/runtime_probe.mjs`.
- **신규(2026-07-12): 얇은 영역 4종(2차) 배포** → 활성 **33종**. 모든 인지 영역 ≥2종 달성.
  - **wordsearch(숨은 단어 찾기/언어)**: 글자 격자서 단어 드래그 탐색(anagram=재배열과 구분). AG_WORDS 재활용, ko+en(langs), th 숨김. pointer 드래그+elementFromPoint. wsPlace 500/500 검증. WS. {lang:55,focus:30,space:15}. 미션B.
  - **diff(틀린 그림 찾기/관찰)**: 두 이모지 격자 비교, 다른 칸 모두 탭(spot 색·odd 회전과 구분). 60s·오답-2s. DF. {focus:45,space:30,speed:25}. 미션B.
  - **pitch(높은음 찾기/청각)**: n패드 중 살짝 높은 음 찾기(melody 순서·rhythm 박자와 구분=변별). 순차 자동재생+다시듣기. cents 축소 난이도. PT. {focus:50,memory:30,speed:20}. 미션A. 소리 필수.
  - **trace(길 따라가기/협응)**: 초록점→빨간점 경로 이탈 없이 드래그(whack 탭·catch 이동과 구분=연속 정밀). SVG path+point-segment 히트테스트, tol=폭/2+11. lives3·레벨↑. TC. {focus:40,space:35,speed:25}. 미션C.
  - 선검증 `.logs/gen_sim2.mjs`(wsPlace 배치·tcWalk 경로, **실제 shuffleArr 의미**), 배선 `.logs/wire_check.mjs`, 런타임 `.logs/runtime_probe.mjs`(4종 start 무예외). 라이브 스모크 필요(특히 ws/trace 드래그 모바일, pitch 오디오).
- 다음 후보: 개인정보처리방침(로그인 도입 시 필수), ko 전용 언어게임(끝말잇기/속담) 후보.
- **언어 축 결정(2026-07-11)**: vocab/typing은 **재활성 안 함**(소스 보존, 주석 비활성 유지). 언어감각(lang) 축은 **신규 anagram(글자 맞추기)로 대체** —
  ko=음절 타일·en=알파벳 타일 동일 엔진(**ko+en 동시 출시**로 vocab/typing의 ko전용 한계 해결), th 보류. 정답 선지정→오픈사전/욕설 리스크 0·콘텐츠 파이프라인 불필요.
  braintype 언어가형 추천은 anagram으로 갱신 예정. `ABILITY_MAP.anagram={lang:70,memory:20,focus:10}`. 상세: **`신규게임-기획-능력영역별.md`** §4.
- **능력영역별 신규 기획(2026-07-11)**: `신규게임-기획-능력영역별.md` — 얇은 축(관찰·협응·청각) + 언어(대체) + 논리/공간/집중/계산/기억 각 1종.
  Wave 배포(1:odd/catch/rhythm → 2:fit/flank → 3:anagram/nono/guess/rev), 1종씩 배포·확인. 순발력은 신규 보류(3종 충분).
- 설계 상세: **`기억축-게임-스펙.md`**, **`주의속도-게임-스펙.md`**, **`바이럴-게임-스펙.md`**, **`유연성-게임-스펙.md`**.

## 서비스 운영 (LIVE)
- **2026-07-10 출시**: https://playmallow.com (Vercel, 가비아 도메인+네임서버 위임 ns1/ns2.vercel-dns.com).
  git push origin master:main → Vercel 자동 배포. www는 308→apex. DNS TXT 추가는 Vercel 대시보드 DNS Records에서.
- 배포 트러블슈팅 교훈: 네임서버 위임 후 Vercel이 'DNS zone not enabled'면 기다려도 안 됨 —
  팀 레벨 Domains에서 존 활성화 또는 도메인 재추가로 해결(레지스트리 상태는 RDAP rdap.verisign.com으로 확인).
- 남은 출시 후속: Search Console·네이버 서치어드바이저 등록(TXT), GA4, 블로그 시딩.

## 조사 자료
- NDS 두뇌 트레이닝 웹구현 판정 요약은 `기억축-게임-스펙.md` §4에 통합(핵심: 음성/카메라 전제 게임은
  웹 이식 불가로 폐기, 기억·주의·속도 축을 탭 기반으로 이식). 별도 조사 파일은 없음.

## 디자인 컨벤션 (2026-07-11 외부 UX 리뷰 반영)
- 접근성 기준선: `--text3`=#6b7794(AA 대비), 전역 `:focus-visible` 링 존재 — 새 CSS에서 이 둘을 깨지 말 것.
- `.mg-timer`=파스텔 핑크 칩+로즈 텍스트(과채도 금지), 경고는 JS의 red 오버라이드로만.
- 신규 게임 CSS는 기존 토큰(--space류는 없음: 간격은 기존 게임 값 재사용)과 시맨틱 색 토큰만 사용 — one-off 색·크기 남발 금지.
- 기각된 제안(재론 불필요): 픽셀 마스코트↔플랫 UI 통일론(의도된 개성), 간격/타이포 전면 토큰화(회귀 리스크), 홈 밀도(레이더·백업은 이미 내기록 탭).

## 운영 메모
- **⚠️ 시뮬 교훈(2026-07-12)**: 로직 시뮬은 **앱의 실제 헬퍼 의미**를 그대로 써야 함. sort 멈춤 버그(soGen이 `shuffleArr` 반환값 미사용 → 정렬된 완성판 생성)를
  초기 시뮬이 *제자리 변형* shuffleArr로 대체해 놓쳐 false pass. `shuffleArr(arr)`는 **원본 불변, 섞인 새 배열 반환** — 반드시 반환값 사용. 재현: `.logs/sort_fix_check.mjs`.
- 포트 범위 **8025-8029**. 정적 프리뷰 서버는 8025 사용(테스트용 일회성).
- 이 환경 Git Bash엔 `setsid`/`webread`/로컬 `playwright`가 **없음**. 정적 서버 기동:
  `nohup python -m http.server 8025 --bind 127.0.0.1 >.logs/x.log 2>&1 </dev/null & disown`.
- 검증: `node --check`(JS문법) + 순수 로직 불변식 테스트(`.logs/logic.mjs` 패턴). `.logs/`는 gitignore.
