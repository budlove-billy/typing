# brain

## Project Identity

- **Project:** brain
- **Working Directory:** D:\claude\brain
- **Model:** claude-opus-4-8

## Boundaries

1. **NEVER modify files outside your working directory** (`D:\claude\brain`). You may read external files if needed, but all writes must stay within your project directory.

2. **Save all memory and notes in your working directory** — MEMORY.md, TODO.md, and any other persistent data belong here, not in global or system directories.

3. **You are responsible for this project only** — do not interfere with other projects, other users' files, or system-level configurations.

## Agent Rules

1. **Every task must end with a git commit** (unless told otherwise):
   ```bash
   git add -A
   git commit -m "feat/fix/chore: describe changes"
   ```

2. **Keep CLAUDE.md updated** — append significant changes to the changelog at the bottom.

3. **Read before writing** — understand existing code before modifying it.

4. **One file, one responsibility** — don't cram multiple unrelated changes into one file.

5. **Respond concisely** — no walls of text, no full file dumps unless asked.

## Session Startup

When starting a new session, read these files in order:
1. `CLAUDE.md` (this file — project rules)
2. `SOUL.md` (your personality)
3. `USER.md` (who you're helping)
4. `MEMORY.md` (long-term memory from past sessions)
5. `TODO.md` (pending tasks)

Do this silently — don't tell the user you're reading files, just do it.

## Memory Protocol — the file is the memory, the conversation is ephemeral

This project has a hook-driven memory system. Your **active state file is per-session**: the session-start hook **automatically injects** it at every session start and right before any compaction, and prints its exact path (e.g. `.claudecrab/sessions/<your-session-id>/active.md`). Treat it as your durable working memory. Because it is per-session, a 分身/clone's memory never pollutes the main session, and promoting a clone to main carries its own memory.

**You MUST:**

1. **Update your active state file immediately** after every significant decision, plan, file change, or open question — don't batch, don't wait until "the end". The compaction can hit at any moment; assume the conversation will be lost. Always write to the **exact path the session-start hook printed** (it is per-session — do NOT hardcode `.claudecrab/active.md`).
2. **Before any Write/Edit**, briefly state intent: "I'm going to write `<path>`: <one-line reason>". This makes the decision survive compaction even if the write fails.
3. **Active vs MEMORY**:
   - your per-session `active.md` — *current* task state (changes constantly)
   - `MEMORY.md` — *durable* knowledge (architecture decisions, conventions, things you'd want to know in 3 months). Promote from active → MEMORY when something becomes long-lived knowledge.
4. **When you finish a task**, clear the corresponding lines from your active state file and (if knowledge was gained) append to `MEMORY.md`.
5. **`.claudecrab/session-log.md`** is the archive — it's auto-written when the session ends; you generally don't write to it directly.

If the model is asking "where was I?" the answer is always: **read the active state file path the session-start hook gave you**.

## Changelog

- 2026-07-31 — **애드센스 연결 코드 삽입(pub-8615421634491307)**: 사용자가 신청해 받은 퍼블리셔 ID로 심사 요청 준비 완료. ① **배포 27개 페이지 전부** `<head>`에 `<meta name="google-adsense-account">` + `adsbygoogle.js` 연결 스니펫 삽입 — 신청 URL만 보는 게 아니라 **사이트 전체를 심사**하므로(구글 공식) 랜딩·가이드·운세·프라이버시까지 빠짐없이. 앵커는 27개 파일 전부에 정확히 1회씩 존재하는 GA4 `googletagmanager` 줄(사전 검사로 확인) → 그 앞에 삽입, `.logs/patch_ads.mjs`가 파일별 CRLF/LF를 자동 판별하고 삽입 횟수 불일치 시 전체 중단. `index.html`만 `<!-- Google tag -->` 주석이 GA 줄과 떨어지게 되어 순서 복원. ② **루트 `ads.txt`** 생성(`google.com, pub-…, DIRECT, f08c47fec0942fa0`) — 없으면 승인 후 "소유권 미확인"으로 수익이 제한됨. ③ **2048 랜딩의 "팝업 광고 없이 깔끔합니다" 문구 정정** — 전 페이지 grep 결과 광고 부재를 주장하는 카피는 이 한 곳뿐이었고, 광고가 붙는 순간 거짓 문구가 되므로 "주소만 열면 브라우저에서 바로 시작됩니다"로 교체. ④ **광고 슬롯(광고 단위)은 아직 배치하지 않음** — 승인 전에는 빈 자리만 생기고, 배치 위치는 승인 후 실제 노출을 보며 정하는 게 안전. 승인되면 `애드센스-신청-가이드.md`의 안전 위치(랜딩·가이드 본문 하단, 운세/게임 **결과 화면**, 홈·내기록 하단)에만 넣고 **게임 플레이 화면·버튼 근처·팝업 위는 영구 금지**(오클릭 → 계정 정지 위험). 참고: `.logs/`는 gitignore라 실서버 404 — 그 안의 남의 pub-id 샘플 파일이 노출될 여지 없음을 확인. 검증: `.logs/ads_check.mjs` 27쪽 스니펫 누락 0·pageerror 0·`ads.txt` 200, `errcheck8176.mjs` 34종 pageerror 0.

- 2026-07-31 — **애드센스 심사 대비 — 본문 없던 3페이지 콘텐츠 보강**: 신청 전 27개 색인 페이지의 *렌더 후 본문 글자수*를 전수 측정(`.logs/ads_ready.mjs`) → 중앙값 826자인데 **persona 226자·queens 331자·tango 335자** 세 곳만 게임판뿐이고 글이 없었음. 구글 공식 탈락 사유 1순위가 "insufficient content — 이미지·동영상 위주로 텍스트가 너무 적음"이고 심사는 신청 URL이 아니라 **사이트 전체 페이지**를 보므로 실질 리스크. 2026-07-21 운세 4종 보강과 동일 패턴으로 소개·규칙·풀이 요령·판 크기·FAQ 4문·내부링크 6블록을 고정 HTML로 추가 → **1,693 / 1,786 / 1,758자**. 다국어 페이지라 타로(2026-07-29) 선례대로 `data-lang-only="ko"` + `applyLang()` 토글 1줄 → en/th 화면 한글 0자(언어 선택기의 "한국어" 3자만). `.seo` CSS는 3파일 공통. 검증: ko/en/th 9조합 pageerror 0·가로 넘침 0·H1 1개 유지. 참고: 홈 내부링크 22개·robots·sitemap 27쪽·`/privacy/` 정상이라 나머지 심사 요건은 이미 충족, **트래픽 최소 기준은 구글 공식 문서상 존재하지 않음**(자격은 오리지널 콘텐츠·정책 준수·만 18세뿐).

- 2026-07-30 — **전 게임 난이도·점수 공정성 재설계 + 지속성/경쟁 구조 신설(지인 테스트 피드백 5건)**:
  **① 점수 역전(어려움일수록 점수가 낮음)** — 원인=25개 지급 지점이 난이도와 무관한 `+= 10+(combo-1)*2` 고정식. 어려움은 처리량이 줄어 점수만 낮아짐(anagram의 `AG_MULT`만 예외적으로 배수 보유). 수정=공통 `DMULT{easy:1, normal:1.4, hard:2}` + `dmScore(diff,pts,game)` 도입해 25곳 일괄 적용(BB/CM×2/DF/FK/GU/NB/OD/PT/RT/SP/ST/SW/WS×2/CA/WK/RC×2/TC/ML/RH/RV/TR/FM). 난이도=판 크기라 총점 규모 자체가 수십 배 다른 **merge(2048)** 는 기본 배수로 보정 불가 → `.logs/merge_sim.mjs`(실제 `mrMove`/`spawn` 포팅 + 일반 플레이어 휴리스틱, 판당 400회) 시뮬로 중앙값 easy 20916 / normal 2880 / hard 272 측정 → `DMULT_GAME={merge:{easy:1,normal:7,hard:70}}` 산출. 그 외 눈금 자체가 틀렸던 3종: **chop** 한 입 1점→`10/14/20`(+`GAME_REF` 130→1300), **run** 거리 점수에 난이도 배수, **nono** 시간 페널티가 판 크기와 무관해 보통·어려움이 최저점 50에 붙박여 있던 것을 `NO_CFG{base,rate}` 난이도별로 분리.
  **② 눈금 변경에 따른 기존 기록 환산** — 그냥 두면 업데이트 직후 아무 판이나 한 번 하면 무조건 '신기록'이 떠 기록이 무의미해지고, chop은 `GAME_REF` 상승으로 능력치가 오히려 *떨어져* 보임. `migrateScales()` 1회성 IIFE(`brain.scaleMigr` 플래그)를 **모든 게임 상태 const보다 앞**(=`bt_recordScore` 직전)에 배치해 저장된 `best[diff].all/day`를 새 눈금으로 환산. nono는 옛 점수가 바닥에 고정돼 정직한 환산 계수가 없어 **의도적으로 제외**. 검증: chop 60/40/25→600/560/500, merge 20000/2800/270→20000/19600/18900, stroop 300/250/200→300/350/400(=어려움이 최상단으로 정렬), 재로드 시 중복 적용 없음.
  **③ 1분 제한이 안 맞던 완주형 게임** — 난이도가 오르면 '해야 할 양'이 늘어나는데 시간이 고정이라 어려움에선 완주 자체가 불가능했음. `WS_TIME` 60→`60/80/100`, `PT_TIME` 60→`60/75/90`, `CM_TIME` 신설 `60/75/90`, `DF_TIME` 30→`30/40/50`(판마다 리셋). 안내문의 고정 초("60초 동안…")는 ko/en/th 3언어 + 인라인 HTML 모두 "제한 시간 안에 / 난이도가 오르면 시간도 늘어납니다"로 교체.
  **④ 어려움이 보통과 사실상 동일했던 설계 버그** — `RV_CFG` hard start 4(=normal), `RH_CFG` hard start 3(=normal), `PT_CFG` hard nStart 4(=normal) → 각각 5/4/5로 한 단계 위에서 시작하도록 수정.
  **⑤ 재도전 동기·경쟁요소 신설** — 결과 화면 공통 블록(`afterGame(id,r)`)을 `missionMark`(아케이드 31종, `renderRecs`보다 먼저 삽입)와 `saveFlatBest`(난이도 없는 5종)에 훅으로 달아 34종 전부에 적용. 구성=㉠**같은 난이도 내 최고 기록까지 몇 점**(첫 기록이면 축하 문구) ㉡**말로우 봇** — 게임마다 목표치를 손으로 정하지 않고 *내 첫 기록*에서 출발(`×1.05`)해 이길 때마다 `×1.07`씩 오르는 사다리(`brain.bot.<id>`, 게임×난이도별) → 34종 어디서든 항상 아슬아슬한 상대, 0점 판에서는 봇을 만들지 않음 ㉢**주간 챌린지**(`brain.week`, 한국시간 월요일 리셋) — 한 판 10점·개인기록 경신 +15·봇 승리 +10으로 *지난 주의 나*와 대결, 5단계 티어(브론즈~챌린저), 홈 상단 카드로 노출 ㉣**바로 다시** 버튼(인트로로 돌아가지 않고 같은 난이도 즉시 재시작) ㉤기존 친구 도전장 링크를 결과 화면에 상시 노출. 주간 점수는 **플레이했다는 사실**로만 오르게 설계 — 게임별 임의 임계값 등급/메달 재도입 금지 원칙(MEMORY.md 2026-07-25) 유지. i18n 20키 ko/en/th 추가.
  검증: `errcheck8176.mjs` 34종 pageerror 0, `pg_check.mjs`(34종 강제 종료) 공통 블록·재시작 버튼 100% 삽입·주간 점수 정상 누적, `flow_check.mjs`(환산→봇 시드→봇 승리 2연속→바로 다시→홈 카드→390px 가로 넘침 0).

- 2026-07-30 — **모아모아 인게임 시계 제거 + 좁은 폭(≤360px) 최적화**: ① **모아모아** — 플레이 화면의 경과 시계(`#playTime`)가 *제한시간*처럼 읽혀 압박을 준다는 지적. 데일리 퍼즐에 시간 압박은 불필요하므로 **화면 표시만 삭제**(HTML/CSS/`render()` 라인), 측정은 그대로 유지해 결과 모달 `걸린 시간`·`최단`·공유카드 기록으로만 사용. 실패 시엔 시간 언급 자체를 제거(`내일 새 퍼즐로 다시 만나요`) — 짧게 진 기록을 들이미는 게 조롱처럼 읽힘. ② **≤359px 상단바** — `lang-select-wrap`이 `flex-shrink:0`이라 350px 미만에서 상단바가 문서를 넘김(280/300/320/340에서 +66/+46/+26/+6px). `@media(max-width:359px)`로 `.nav-tagline` 접기·마스코트 30px·`lang-select-wrap{flex-shrink:1;min-width:0}`·`lang-select{max-width:82px}`·`.screen{padding:.7rem}`. **360px 이상은 손대지 않음**(갤럭시 실기기 레이아웃 보존). ③ **`fit`(블록 채우기) 보드** — `ftCellPx()`가 `340/n` 하드코딩이라 320px에서 판이 화면을 넘김(docSW 379). 컨테이너 `clientWidth` 기반으로 전환(`min(344, parentW) - 보드padding4 - gap2*(n-1)`, 최소 20px) + 디바운스 `resize` 재렌더(diff 선례) + `.ft-board{justify-content:center}`로 컬럼 중앙정렬. 검증: 280/320/390px 전 34종 오버플로 0, errcheck 34종 pageerror 0, 모아모아 승·패 시나리오 pageerror 0. **참고**: 사용자 첨부(PC 에뮬 우측 잘림)는 CSS 폭 자체는 정상이고 에뮬 프레임이 렌더 폭보다 좁게 크롭한 것 — 그래도 280px까지 깨지지 않게 만들어 크롭된 프레임에서도 온전히 보이게 함.

- 2026-07-29 — **지적 5종 수정(모아모아 3·타로 1·앱 1)**: ① **게임 중 화면 좌우 흔들림** — 원인=`nav`의 세 자식(`nav-exit`/`nav-logo`/`lang-select-wrap`)이 모두 `flex-shrink:0`이라 게임명이 붙는 순간 상단바가 화면보다 넓어짐(390px 뷰포트에서 문서폭 429~469px). 홈은 게임명이 비어 정상. 수정=`body.ingame .nav-logo{flex-shrink:1;min-width:0}`+`.nav-game` 말줄임, ≤480px 게임 중 브랜드명·마스코트 숨김·`lang-select` 76px, `body{overflow-x:clip;overscroll-behavior-x:none}`. 검증: 34종 전부 docSW=cw(390/360 모두 타이틀 잘림 0). ② **타로 태국어에 한글 혼출** — 원인=`tarot/index.html`의 `<section class="seo">`(타로란?/FAQ 등 한국어 고정 HTML)를 `applyLang()`이 건드리지 않음. 카드 데이터(CARD_TH 78장)는 정상. 수정=zodiac 선례대로 `data-lang-only="ko"`+토글 1줄 → th 화면 한글 0자, ko는 h2 6개 유지. ③ **모아모아 제한시간** — 실제로 시간 개념 자체가 없었음(유일한 시간 UI는 결과모달의 '다음 퍼즐까지' 대기 카운트다운). 신설=첫 선택에 시작하는 플레이 경과 타이머(탭 전환 시 정지, 10초마다 저장, 종료 시 정지) + 최단 기록(`stats.bestSec`) + 결과/공유 문구에 시간. 데일리 퍼즐 특성상 하드 제한 대신 '기록'으로 설계. ④ **모아모아 난이도** — `MAX_MISS` 4→3, "하나만 달라요" 힌트를 판당 2회로 제한(`MAX_ONEAWAY`). ⑤ **모아모아 공유 이미지** — 기존엔 이미지가 아예 없고 텍스트+이모지뿐이었음. `buildShareCard()` canvas 카드 신설(DPR 2~3배, 480×H, 이모지 대신 색 블록 직접 렌더 → 기기별 흐림 제거), 결과 모달 미리보기 + `navigator.share({files})` → 다운로드 → 텍스트 순 폴백.

- 2026-07-29 — **SEO 진단 지적사항 수정**: ① H1 부재/계층 오류 — 홈 `div.home-hi` → `h1.home-hi`(문서 첫 제목, i18n `home.title` 유지, `.home-hi` 클래스가 UA 기본값을 덮어 시각 변화 0) → H1 1개·H1→H2→H3 정상 ② `bt-share-img` `alt=""` → 의미있는 alt + `loading="lazy"`, 카드 생성 시 실제 유형명으로 alt 갱신(i18n `braintype.shareAlt` 신설) ③ 보안헤더 3종(X-Frame-Options SAMEORIGIN·X-Content-Type-Options nosniff·Referrer-Policy strict-origin-when-cross-origin) — 호스팅이 **Vercel**임을 응답헤더로 확인, `vercel.json` 신규 생성(배포 후 적용). 검증: 헤드리스 H1/스타일/alt/i18n 확인 + errcheck 34종 pageerror 0. 참고: `brain_app.html`은 미링크 레거시 사본(canonical=루트), `privacy/`는 ko/en 블록으로 H1 2개(의도된 다국어 구조).

- 2026-07-27 — **탭 사운드 스크롤 오발 수정**: 홈 데일리·운세 카드를 스크롤(터치)할 때 `sfx('tap')`이 울리던 버그. 원인=UI 탭 사운드 위임이 `pointerdown`(손 닿는 순간)에 발생 → 스크롤 시작 터치도 트리거. 수정=`pointerdown`에서 후보만 기록하고 `pointerup`에서 이동량 ≤10px & 동일 요소일 때만 재생(`pointercancel`로 취소). 헤드리스 검증: 스크롤/드래그 0, 진짜 탭 1, pageerror 0.

- 2026-07-27 — **글자 맞추기(anagram) 전면 개선(7종)**: ① 터치 버튼 44→56px(모바일 60px)·폰트 1.65rem·gap .55rem·그라데+광택·진동, used 타일 hidden→흐리게(위치 고정) ② 정답 조립 영역 `.ag-assemble` 박스(min-h 96px)+안내문구로 하단 이동 ③ 셔플백(`AG.bag` key=lang|diff, 재셔플 첫 단어≠직전)으로 단어 반복 차단(검증 6/6 고유) ④ ko ABAB 반복어(말랑말랑 등) 전량 제거 ⑤ 난이도 재설계 `AG_LEN` 쉬움 ko[2,3]/en[3,4]·보통 ko[4]/en[5]·어려움 ko[5,6]/en[6], ko 2/5/6글자 pool 신설 ⑥ `AG_HINTS`{3,2,1}·`AG_PENALTY`{0,1,2}s 오답 시간차감·`AG_MULT`{1.0,1.4,2.0}+속도보너스(≤10) ⑦ i18n `anagram.prompt`+난이도 설명 갱신. 헤드리스 스모크(easy/normal/hard 각 6판+오답+힌트) pageerror 0.

- 2026-07-24 — **AI 배경 전면 적용(34종 완성)**: 인앱 아케이드 34종 플레이 배경 전부 AI 이미지화 + 홈 히어로·신기록 배경 = 36개 자산(`assets/*.jpg`). gpt-image-2-t2i 생성→PIL 최적화(900px·~45KB)→CSS 오버레이 배경. 테마 매칭(2048=타일, whack=구멍마시멜로, trail=번호경로 등). 인원수세기 캐릭터 문 쪽 이동 수정. git push용 Fine-grained PAT(`.env`의 GITHUB_TOKEN, Contents RW 권한) 설정. 상세=MEMORY.md.

- 2026-07-23 — **UX·성장 구조 개편 5종**: ① 사운드 팩(`_tone` 레이어드 신스, sfx 12종, UI 탭 위임, 신기록 팡파르, 타이머 틱) ② 능력치 10축(+협응/청각/관찰) + overall=숙련도70%+커버리지30% ③ 등급 배지 6단계(🐣~💎) 내 기록 칩 + 결과 화면 다음 등급까지 N점 ④ 홈 '오늘의 데일리' 섹션 + 인기게임 하드코딩→개인화 추천 ⑤ 화면 전환 애니메이션. 검증 errcheck 34종 무결. 상세=MEMORY.md.

- 2026-07-21 — **수익화(애드센스) 준비 + SEO 강화 배치**: ① 개인정보처리방침 `/privacy/`(ko/en) 신설 — 애드센스 승인 하드블로커 제거(쿠키·GA·AdSense 제3자쿠키 고지+opt-out, 홈푸터·sitemap). ② 정적 랜딩 **17/17 구조화데이터(JSON-LD) 완비** + 가이드 6종 Article schema. ③ **운세 4종(unse/zodiac/ttirank/tarot) 크롤 콘텐츠 대폭 보강** — 얇은 위젯(100~449자)→리치(865~1223자), 소개·날짜표·FAQ·내부링크·면책 고정HTML로 랭킹·애드센스 저품질반려 완화. ④ 홈 푸터 운세 내부링크. ⑤ `애드센스-신청-가이드.md`·`트래픽-실행-플레이북.md`. 애드센스는 신규신청 대기(pub-id 받으면 head스니펫+ads.txt+슬롯 삽입, 게임 플레이화면 광고 금지). 상세=MEMORY.md.

- 2026-07-17 — **데일리 논리퍼즐 2종(글로벌·언어무관)**: LinkedIn 트렌드(Queens·Tango) 벤치마크로 자체 구현. **말로우 크라운(`/queens/`)** = 행·열·색구역에 왕관 1개·인접금지(N6/7/8), **말로우 탱고(`/tango/`)** = 해/달 Binairo(3연속 금지·개수균형, N6/8). 둘 다 `kstDate()` 데일리 시드·유일해 100% 보장(백트래킹 솔버)·결정적·공유카드·● 뱃지·ko/en/th. 생성기 선검증(`.logs/queens_sim.mjs`·`tango_sim.mjs`: Queens는 랜덤성장+균형필터+시드재시도, Tango는 given제거 유일화). HOME_GAMES cat.daily(langs 3언어)로 모아모아 옆 배치.

- 2026-07-17 — **말로우 페르소나 다국어(ko/en/th)**: `TX`(3언어 UI)+`AXL`(축 극명)+`Q_i18n`(en/th 24문항)+`TYPES_i18n`(en/th 16유형)+`GNAME_i18n`. 접근자 qText/typeOf/poleName/gameName로 언어 분기, detectLang(?lang→brain.lang)+langSel+setLang(결과중 언어변경 재렌더). 채점은 언어무관(Q 극/축 공유, 시뮬로 ko=en=th 동일코드 확인). 홈 persona langs ko/en/th·funByLang 3언어·goExternal ?lang. (질문 상황문구 15px·퀴즈/결과 태그라인 숨김 포함)

- 2026-07-16 — **말로우 페르소나(`/persona/`)**: 심층 성격 유형 진단(재미·cat.fun). 24문항 시나리오형(축당 6: EI/SN/TF/JP)→16유형, 축별 % 바 + 유형 풀 프로필(강점·약점·연애·일·스트레스·성장·궁합·추천게임). 추천게임 `/?game=<id>` 딥링크 funnel, **결과 공유카드**(코드+별명+4축바). braintype와 분리(그건 6문항 게임추천). MBTI® 미표기·유형설명 자체작성(저작권). v1 ko 전용. 채점 시뮬 검증(극단값·랜덤2000·16종 도달).

- 2026-07-13 — **운세 다국어 마감**: ① 홈→운세 정적페이지 이동 시 현재 앱 언어를 `?lang=`로 전달(`goExternal`) → 별자리 영어 자동 적용 문제 해소.
  ② **타로 태국어(ko/th)** 전면 이식: `TX`(ko/th UI)+`CARD_TH`(78장 태국어=메이저22 개별+마이너56 슈트·랭크 조합)+언어 선택기+`detectLang`(?lang→brain.lang)+`CF(pick)` 언어별 카드. 별자리는 ko/en/th 기완비. 타로 en은 저작권 신중으로 제외.

- 2026-07-12 — **말로우 운세(`/unse/`)**: 재미(cat.fun) 게임 — 생년월일→띠·오행(양력 연주 기반 라이트) + 오늘 날짜 시드 데일리 운세(총운/애정·금전·건강·일/행운색·숫자·아이템/한마디)+공유카드.
  moamoa식 별도 정적 페이지(koOnly·external, 기록/능력치/미션 제외), 재미 톤·면책 문구. HOME_GAMES/sitemap 등재. 기획=`재미게임-운세-기획.md`.

- 2026-07-12 — **디자인 상용화 리프트(캐릭터·오브젝트·손맛·입체·테마)**: 전 34종 화면 검토 후 5단계 보완.
  ① Mallow 인라인 SVG 마스코트(표정 5종·몸통 6색, `mallowSVG()`)로 통일·픽셀PNG 폐기 ② whack 굴/catch Mallow·포크·바구니 SVG/count 인원=Mallow(이모지 제거)
  ③ 공통 손맛 FX(`sfx('good'/'win')`→파티클 자동, 38지점) +점수팝·콤보배지 ④ 버튼·타일 입체화(그라데+그림자) ⑤ 축별 테마 배경(`body[data-axis]`). 검증 `.logs/errcheck.mjs`(34종 pageerror 0). 상세=MEMORY.md 디자인 시스템.

- 2026-07-12 — **얇은 영역 4종(2차) 배포** → 활성 33종, 모든 인지 영역 ≥2종. wordsearch(언어·단어탐색)/diff(관찰·틀린그림)/pitch(청각·음높이변별)/trace(협응·경로드래그).
  선검증은 **실제 앱 헬퍼 의미**로(shuffleArr 교훈): `.logs/gen_sim2.mjs`+`wire_check.mjs`+`runtime_probe.mjs`. 능력치/공유/도전장/미션풀/추천 연동.

- 2026-07-12 — **신규 7종 일괄 배포(Wave2-3)** → 활성 30종. flank(집중·플랭커)/guess(계산·어림)/rev(기억·역순)/rhythm(청각·박자)/catch(협응·받기)/fit(공간·블록)/nono(논리·노노그램)/anagram(언어·글자맞추기, vocab·typing 대체 ko+en).
  생성형은 선검증(nono 라인솔버 유일해·fit 데드락·guess 보기·rhythm 판정·anagram 셔플, `.logs/gen_sim.mjs`) + 배선 정합성(`.logs/wire_check.mjs`). 능력치/공유/도전장/미션풀 연동. 라이브 스모크 테스트 필요.

- 2026-07-11 — **다른 모양 찾기(odd)**: 관찰력 축 2호 — spot(색차) 대비 형태(회전)차. n×n 화살표 중 각도 다른 1개 탭.
  spot 구조 미러링(판 확대+각도차 감소, 유일성 delta>0 보장), 60초·오답 -2s. 능력치/공유/도전장/미션B 연동. 활성 22종. (Wave1 1호, 로드맵=`신규게임-기획-능력영역별.md`)

- 2026-07-11 — **공략 가이드 6종**(`/guide/`): 스도쿠·2048·IQ·컬러소트·슬라이딩퍼즐 공략 + 두뇌게임 총정리 허브.
  SEO 롱테일 타깃 실전 콘텐츠, 딥링크 CTA·상호 내부링크·sitemap. 홈 푸터/랜딩에 연결.

- 2026-07-11 — **컬러 소트(sort)**: 논리 축 3호 — 워터소트류 정렬 퍼즐(4/6/8색+빈 병 2, 되돌리기 3회).
  생성마다 내장 솔버로 풀 수 있는 판 보증. 기록/공유/도전장/능력치 연동. 활성 21종.

- 2026-07-11 — **말로우 타워(chop)**: 순발력 축 3호 — 팀버맨류를 마시멜로 타워 깨물기로 재테마(포크 피하기,
  시간 게이지+가속). 공정성 생성 규칙 시뮬 검증. 기록/공유/도전장/능력치/미션B 연동. 활성 20종.

- 2026-07-11 — **말랑 2048(merge)**: 계산 축 3호 — 2048 재구현(원작 MIT 규칙, 회사 게임 '매치냥'은 참고만).
  난이도=판 크기(5×5/4×4/3×3), 스와이프+방향키, 되돌리기 1회. 로직 시뮬 검증. 활성 19종.

- 2026-07-10 — **슬라이딩 퍼즐(slide)**: 공간지각 축 2호 — 3×3/4×4/5×5 15퍼즐류(완성형, 시간+이동수 점수).
  유효 이동 셔플로 전 판 해결 가능 보장(시뮬 검증). 기록/공유/도전장/능력치/미션C 연동. 활성 18종.

- 2026-07-10 — **다른 색 찾기(spot)**: 관찰력 축 신설 — 미묘하게 다른 색 타일 찾기(레벨↑=판 확대·색차 감소).
  앱인토스 인기 포맷('절대 색감') 조사 후 제작. 기록/공유/도전장/능력치/미션B 연동. 활성 17종.

- 2026-07-10 — **기록 백업**: 내 기록 화면에 내보내기/가져오기(코드 복사·붙여넣기, 서버 0원 기기 이전).
  더 좋은 로컬 기록 유지하는 스마트 병합. 로그인은 리텐션 신호 후 Phase C(백업 전용 설계)로 결정.

- 2026-07-10 — **버블 톡톡(bubble)**: 계산 축 신규 — 버블 숫자로 목표 합 만들기(단계별 난이도↑). 파스텔 버블·팝 연출,
  기록/공유/도전장/능력치 연동. 판 생성 불변식 시뮬 검증. 활성 16종.

- 2026-07-10 — **리뷰 반영 3종**: ① 키워드 랜딩 `/sudoku/` `/iq-test/` `/braintype/`(+`?game=` 딥링크, 홈 푸터 내부링크, sitemap)
  ② 도전장 링크(`?c=game.score.diff`, 11종 결과 버튼→공유, 수신 배너+승패 판정) ③ 공유카드 v2(흰 카드+마스코트+점수 강조).

- 2026-07-10 — **모아모아 편입**: 한국어 데일리 낱말 퍼즐을 `/moamoa/` 별도 페이지로 배치(브랜딩 Mallow·GA4·canonical),
  홈/게임탭에 ko 전용 카드(koOnly 필터, en/th 숨김) + 오늘 미완료 ● 뱃지, sitemap 추가. 퍼즐 30일치(D+25 추가 제작 필요).

- 2026-07-10 — 신규 축 2종: 협응 **말로우 팡팡(whack, 마스코트 활용)** + 청각 **멜로디 기억(melody, WebAudio)**. 활성 15종, 인지 축 8개.

- 2026-07-10 — **한글 타자·영단어 비활성화**(출시 범위 제외): 두뇌게임 포지셔닝 불일치+en/th 미대응. 소프트 비활성(HOME_GAMES 주석, 코드 보존). 언어가형 추천 vocab→nback. 활성 13종.
- 2026-07-10 — **Phase A 출시 준비**: Mallow 리브랜딩(로고/타이틀/공유카드 워터마크 playmallow.com),
  SEO(meta/OG/canonical/robots/sitemap/홈 소개문), PWA(manifest/sw.js/아이콘·OG 이미지 생성), URL 언어(?lang=)+언어 저장.

- 2026-07-06 — **UX 개편 Phase2**: 상단바 축소+하단 탭바(홈/게임/내기록), 홈=오늘의 추천 중심, 전체게임·내기록 화면. 랭킹 보류.
- 2026-07-06 — **UX 개편 Phase1**: 차분한 색 팔레트·게임 카드 통일·소프트 카테고리.
- 2026-07-06 — **오늘의 미션(Daily Workout)** 추가: 매일 축 섞은 3게임 자동 선정+진행체크. 재미/휴식 톤(FTC 회피).
- 2026-07-06 — 시각기억 **카드 짝 맞추기(cards)** + 반응억제 **반응 속도/Go-No-Go(react)** 추가. 게임 15종.
- 2026-07-06 — 공간지각 축 신설 **도형 회전(rotate)** + 작업기억 **엔백(nback)** 게임 추가. 게임 13종.
- 2026-07-06 — 유연성 축 게임 **규칙 바꾸기(switch)** 추가(홀짝↔크기 규칙 전환, 과제 전환/set-shifting).
- 2026-07-06 — **홈/대시보드** 기본 랜딩 추가(전체 바로가기 그리드 + 연속 출석 streak).
- 2026-07-06 — **공유카드 일반화**: `makeShareCard`/`shareOrDownload`로 5개 게임 결과에 공유 버튼. 설계: `유연성-게임-스펙.md`.
- 2026-07-06 — 바이럴 축 추가: **두뇌 유형 테스트(braintype)** + **canvas 결과 공유카드**.
  6문항→6유형(각 유형이 앱 내 게임 추천으로 연결), Web Share/PNG 다운로드. 설계: `바이럴-게임-스펙.md`.
- 2026-07-06 — 주의·속도 축 게임 2종 추가: **색깔 맞추기/스트룹(stroop)**, **순서 잇기/Trail(trail)**.
  60초 타임어택 + 오답 시간 페널티 + `localStorage` 최고기록. i18n에 색이름(`color.*`) 추가.
  설계: `주의속도-게임-스펙.md`.
- 2026-07-06 — 기억 축 게임 2종 추가: **순간기억(flash)**, **인원수 세기(count)**.
  `index.html`/`brain_app.html`에 nav·screen·CSS·i18n(ko/en/th)·JS 통합.
  적응형 난이도 + `localStorage` 최고기록. 설계: `기억축-게임-스펙.md`.

<!-- PORTS_BEGIN -->
## Service (MUST follow)

Ports **8176-8180** (5 total) are yours — ANY service you start MUST use one of them, never outside the range (need more → ask the user). Record the port-to-service mapping in `MEMORY.md`.

**Showing a web page:** put the page AND every asset it references (images, css, js, fonts) under `public/`, and reference them with RELATIVE paths (`./img/x.png`, not an absolute path or another folder) — a page in `public/` that points at `generated_images/` or elsewhere previews with broken images. Then give a clickable markdown link `[打开页面](/api/v1/media/fb690805-ecbb-4c17-b9d8-55981f8fd1ce/public/<file>.html)` (served directly; no server needed). If you generated an image into `generated_images/` and want it IN a page, copy it into `public/` first. Bare paths render as dead text; **NEVER** give a `http://localhost:<port>/…` link — only start a real server when a live backend is needed.

Env: `PROJECT_PORT_START=8176`, `PROJECT_PORT_COUNT=5`, `PROJECT_PORT_END=8180`
<!-- PORTS_END -->

<!-- BACKGROUND_SERVICES_BEGIN -->
## Long-running services (CRITICAL)

Each turn is a fresh subprocess; when it exits, SIGHUP kills its children — any dev
server/watcher/worker you started dies with the turn. Anything that must OUTLIVE the
turn MUST detach (plain `<cmd> &` is NOT enough):
```
mkdir -p .logs && setsid nohup <cmd> > .logs/<service>.log 2>&1 &
# or: nohup <cmd> > .logs/<service>.log 2>&1 < /dev/null & disown
```
Before starting, check it isn't already running (`ss -ltn | grep ":<port> "`); after
starting, record what runs on which port in `MEMORY.md`. One-shot commands that exit
on their own don't need any of this.
<!-- BACKGROUND_SERVICES_END -->

<!-- WEB_RESEARCH_BEGIN -->
## Web research (live internet)

- `websearch "<query>"` [-n 5] [--text] — keyless search, JSON title/url/snippet (DISCOVER).
- `WebFetch` tool — read a specific URL's content.
- `webread <url>` [--html|--screenshot out.png] — headless-browser render; use when
  WebFetch comes back empty or the page is a JS app (SPA).

**Prefer `websearch`** for discovery — the built-in WebSearch tool returns no results in this (gateway) deployment, so do not rely on it.

Workflow for 联网调研/fact-finding: search → WebFetch the top 2–5 (→ webread if
empty/JS-only) → synthesize, citing each source as a markdown link. Never invent facts
or URLs — say so when a search finds nothing useful.
<!-- WEB_RESEARCH_END -->

<!-- ROLES_TOOL_BEGIN -->
## Role library & sub-agents (`roles`) · your own identity (`identity`)

`roles` = a library of expert personas to DELEGATE to: `roles search <query>` /
`roles show <code|key>` / `roles add <code|key>` (installs `./.claude/agents/<name>.md`;
spawn via Task tool `subagent_type="<name>"`) / `roles create --label … --category …
--description … --body-file <file>` (new reusable role; auto-favorited). Codes `R0042`,
keys `engineering-backend-architect` — either works.

`identity` = YOUR OWN persona for THIS project (what ROLE.md holds). User says who to
be → `identity append "…"` (add) / `set "…"` (replace) / `show` / `clear`; `--file` for
long text. Applies on your NEXT message and keeps ROLE.md + settings UI in sync.
**Never hand-edit ROLE.md** (generated; edits get overwritten). Confirm before
replacing/clearing an identity the user didn't ask to change.
<!-- ROLES_TOOL_END -->
<!-- SKILLS_TOOL_BEGIN -->
## Skills — pluggable capabilities (`skills`)

A skill (SKILL.md + optional scripts) auto-loads by relevance once PLUGGED into this
project. Plug only what the task needs, unplug when done (keeps context lean).

- `skills search <query>` / `skills show <code|key>` / `skills list` (what's plugged).
- `skills add <code|key>` plug into `./.claude/skills/<key>/` · `skills remove` unplug.
- `skills create --dir <folder>` author a NEW skill (run `skills spec` for the format:
  SKILL.md with a strong *when-to-use* description + scripts). Given a site/repo/zip or a
  description, gather the material yourself and author a CLEAN skill — don't dump raw
  source. Added unfavorited; user favorites keepers.
- `skills update <code|key> [--dir <folder>] …` edit in place — **always `update`, never
  `create` a suffixed near-duplicate.** `skills delete` removes from the library.

Codes `S0042`, keys `mdbox-media` — either works.
<!-- SKILLS_TOOL_END -->

<!-- CLONE_TOOL_BEGIN -->
## Session clones — 分身 (`clone`)

A clone forks YOUR session (context up to the fork) and runs async in its own
session/memory inside the shared work_dir — for side-tasks that would clutter your
memory, parallel grind, or a promotable backup.

- `clone fork [--label L]` → prints `session` | `clone run <session> "<task>" [--report]`
  → async, prints `job`; with `--report` the result posts itself into the main chat |
  `clone result <job> [--wait]` | `clone list` | `clone discard <session>`.

### Parallel fan-out — 「同时/并行/分别做 A、B、C」 HARD RULES
1. **File-disjoint tasks only** — clones share this work_dir; overlapping edits clobber.
   Overlapping tasks run serially (say why). You too: don't touch files a clone is on.
2. **Show the split, get a YES first** (「我准备开 N 个分身:①…②…③…,互不冲突,确认?」).
   Never fan out silently or uninvited. **≤3 clones at once.**
3. **Dispatch each with `--report`, reply 「已派发,结果会自动出现在聊天里」, END your
   turn.** No `--wait` loops — unless the user wants ONE synthesized answer (then wait
   for all and merge).
4. Task briefs must be self-contained (clones don't see anything after the fork).
   `--report` clones auto-clean on success; `clone discard` the rest.
5. **Results reach you automatically**: 「[分身回报 …]」 is injected at your next turn —
   absorb before answering. Completion order is arbitrary; trickled dispatch is fine;
   you stay fully available meanwhile (`clone result <job>` / `clone list` to peek).
<!-- CLONE_TOOL_END -->

<!-- MCP_TOOL_BEGIN -->
## MCP servers (`mcp`)

MCP servers add `mcp__<name>__*` tools for external systems (GitHub/Postgres/APIs…).
`mcp add <name> [-e K=V …] -- <cmd> [args…]` (stdio) · `mcp add <name> --http <url>
[--header "K: V"]` · `mcp list` / `remove` / `enable|disable`. A new server loads on
your **NEXT message** — add it, tell the user, use its tools next turn. Secrets are
stored encrypted.
<!-- MCP_TOOL_END -->

<!-- PLUGINS_TOOL_BEGIN -->
## Plugins (`plugins`)

A plugin bundles commands/sub-agents/skills/hooks/MCP servers. `plugins list` (✓ =
enabled here) · `plugins enable|disable <key>`. Loads on your **NEXT message**.
Installing NEW plugins is admin-only; this only toggles library ones.
<!-- PLUGINS_TOOL_END -->
See WORKSPACE.md for related bots in this workspace.

<!-- MDBOX_MULTIMODAL_BEGIN -->
## Generating & delivering files (images, video, audio, documents)

**Save every user-facing file into `./generated_images/`** (`mkdir -p` first) — the only
publicly served folder. Then paste its REAL public URL `/api/v1/media/fb690805-ecbb-4c17-b9d8-55981f8fd1ce/generated_images/<name>.<ext>`
in chat, formatted by type (never just say "saved to generated_images/"):
- Image → `![alt](/api/v1/media/fb690805-ecbb-4c17-b9d8-55981f8fd1ce/generated_images/<name>.png)` (inline)
- Video/Audio → `[title](/api/v1/media/fb690805-ecbb-4c17-b9d8-55981f8fd1ce/generated_images/<name>.mp4)` (web embeds a player)
- PDF/HTML/Office/other → `[filename](/api/v1/media/fb690805-ecbb-4c17-b9d8-55981f8fd1ce/generated_images/<name>.<ext>)` (clickable link)

**Generate image/video/audio ONLY by emitting a `__media__` directive** on its own line,
once per file, then end your reply — the platform runs it, shows progress, and delivers
the result into chat. Never run a local binary for generation.

```
{"__media__": {"kind": "image", "model": "nano-banana-pro", "prompt": "a red fox in snow, cinematic"}}
```

- `kind`: image|video|audio; `prompt` required. Model defaults: image `nano-banana-pro`,
  video `sora-2`, audio `elevenlabs` (`mdbox models` lists all; prefer a specific
  `-t2i`/`-i2i` variant like `gpt-image-2-t2i` over a bare family name — bare aliases can
  be queue-bound and time out).
- Image-to-image / image-to-video: put the reference image's LOCAL path in
  `params.metadata.image` (file under `generated_images/`, a user attachment path, or an
  https URL; list for multiple refs). The platform uploads it — no `mdbox upload` needed:
  `{"__media__": {"kind":"image","model":"nano-banana","prompt":"make it a watercolor","params":{"metadata":{"image":"generated_images/photo.png"}}}}`

The `mdbox` CLI is for `mdbox models` / `mdbox upload <file>` / `mdbox guide` (full
reference incl. cutout & upscaling). `mdbox gen -o generated_images/<name>.png` runs a
BLOCKING generation — use it ONLY when the file is needed in this same turn (e.g. image
→ feed into video), never for a plain request.
<!-- MDBOX_MULTIMODAL_END -->

<!-- CAPABILITY_AUTOPILOT_BEGIN -->
## Capability autopilot (MUST follow)

Users are non-programmers who never browse the libraries — YOU notice what a task
needs: for an unfamiliar task kind, check `skills search <kw>` / `connectors search
<kw>` / `plugins list` first. Found a fit → SUGGEST in one line in the user's language
and WAIT; equip only after a YES (`skills add` / `connectors enable` / `plugins
enable`), never behind the user's back. If it needs the user's account/API key/money,
say so when asking. Suggest unplugging capabilities no longer needed (they cost
context). For deep domain sub-tasks: `roles search` → suggest → on OK `roles add
<code>` and delegate to that sub-agent.

A message starting with `[skill: <key>]` / `[connector: <key>]` / `[plugin: <key>]` /
`[mcp: <key>]` tags means the user explicitly picked that ability for this request — it's
already enabled; just use it, no need to ask.
<!-- CAPABILITY_AUTOPILOT_END -->
<!-- ROLE_REF_BEGIN -->
## Your role

Your role for this project is defined in [`ROLE.md`](./ROLE.md). **Read it first** before responding, and let it shape your tone, focus, and what you proactively bring up.
<!-- ROLE_REF_END -->

<!-- MEMORY_TOOL_BEGIN -->
## Retrievable memory — search, don't carry (`memory`)

MEMORY.md loads whole every session → keep only the few always-relevant lines there
(architecture, port map, active conventions). Everything else = one fact per file under
`.claudecrab/memory/facts/`, FTS-indexed: `memory search "<q>"` (**do FIRST** when a
question touches past decisions/conventions/preferences) · `memory add "<title>"
--body "<text>" [--tags a,b]` (one durable fact; specific titles) · `list` / `show
<slug>` / `forget <slug>` / `reindex` · `import-legacy` (one-time: split an overgrown
MEMORY.md's ## sections into facts). MEMORY.md past ~60 lines → import-legacy + trim.
<!-- MEMORY_TOOL_END -->