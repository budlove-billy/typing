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
- 게임/콘텐츠 **총 15종**(플레이 게임 14 + 두뇌유형 테스트). 화면 16(홈 포함).
  축: 계산·타이핑·논리 / 기억(순간·인원·엔백·카드) / 주의·속도(스트룹·순서·반응) / 유연성 / 공간지각 / 언어 / 바이럴 + 홈.
- **두뇌 능력치(2026-07-06)**: 내 기록에 7능력 레이더+막대(ABILITY_MAP 가중치·GAME_REF 정규화, brain.ability.base 주간성장). 막대 탭→기여게임. saveFlatBest로 math/iq/vocab/sudoku/typing 최고점 저장(brain.<id>.flat). IQ점수=55+정답률^1.3*75+속도*15(55~145). FTC: '게임 수행 기반·실제 지능 아님'.
- 다음 후보: 사운드/햅틱, 주간 통계·목표, 난이도 보정 강화.
- 설계 상세: **`기억축-게임-스펙.md`**, **`주의속도-게임-스펙.md`**, **`바이럴-게임-스펙.md`**, **`유연성-게임-스펙.md`**.

## 조사 자료
- NDS 두뇌 트레이닝 웹구현 판정 요약은 `기억축-게임-스펙.md` §4에 통합(핵심: 음성/카메라 전제 게임은
  웹 이식 불가로 폐기, 기억·주의·속도 축을 탭 기반으로 이식). 별도 조사 파일은 없음.

## 운영 메모
- 포트 범위 **8025-8029**. 정적 프리뷰 서버는 8025 사용(테스트용 일회성).
- 이 환경 Git Bash엔 `setsid`/`webread`/로컬 `playwright`가 **없음**. 정적 서버 기동:
  `nohup python -m http.server 8025 --bind 127.0.0.1 >.logs/x.log 2>&1 </dev/null & disown`.
- 검증: `node --check`(JS문법) + 순수 로직 불변식 테스트(`.logs/logic.mjs` 패턴). `.logs/`는 gitignore.
