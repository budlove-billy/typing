# MEMORY.md — Long-Term Memory
> Project: brain

_Write important context, decisions, and lessons here so future sessions can pick up where you left off._

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
- 다음 후보: 어림 계산, 개인정보처리방침(로그인 도입 시 필수).
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
- 포트 범위 **8025-8029**. 정적 프리뷰 서버는 8025 사용(테스트용 일회성).
- 이 환경 Git Bash엔 `setsid`/`webread`/로컬 `playwright`가 **없음**. 정적 서버 기동:
  `nohup python -m http.server 8025 --bind 127.0.0.1 >.logs/x.log 2>&1 </dev/null & disown`.
- 검증: `node --check`(JS문법) + 순수 로직 불변식 테스트(`.logs/logic.mjs` 패턴). `.logs/`는 gitignore.
