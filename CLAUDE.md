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
## Service

This project is allocated the port range **8131-8135** (5 ports total).

**Rules (MUST follow):**
- When starting ANY service (dev server, API, websocket, db, etc.), you MUST pick a port from `8131-8135`.
- **DO NOT** use any port outside this range.
- Decide the port-to-service mapping yourself, but record it in `MEMORY.md` once chosen so it stays consistent across sessions.
- If you need more ports, ask the user to expand the range — don't reach outside.

**Showing the user a web page / preview (MUST follow):**
- A static page or site (HTML/CSS/JS, no live backend) — save it (with its assets) under `public/` in your work dir, then give the user a **clickable markdown link** (never a bare path — a bare path renders as dead plain text the user can't click):
  `[打开页面](/api/v1/media/49f9dcf2-1663-4fc8-8f6f-bc4570df374c/public/<file>.html)`
  SmartJ serves that folder directly, so the link always opens — NO server and NO port needed. (`generated_images/` is served the same way.)
- **NEVER** hand the user a `http://localhost:<port>/…` link or hardcode a port like `:8000` — they cannot reach your local dev server that way.
- Only start a real server (on a port from the range above) when the page needs a live backend/API; for anything static, always use the `public/` link.

**Env vars injected into your shell:** `PROJECT_PORT_START=8131`, `PROJECT_PORT_COUNT=5`, `PROJECT_PORT_END=8135`
<!-- PORTS_END -->

<!-- BACKGROUND_SERVICES_BEGIN -->
## Long-running services (CRITICAL)

Each chat turn spawns a fresh `claude` subprocess. When the turn ends and the
subprocess exits, the OS sends SIGHUP to its children — **any dev server, watcher,
queue worker, or REPL you started in this turn dies with it**, and the next turn
will have no record of it.

**Rules:**

- For ANYTHING that should outlive the current turn (dev server, build watcher,
  test runner in watch mode, MCP servers, database, queue workers, etc.) you
  MUST detach from the controlling terminal. Use one of:
  ```
  setsid nohup <cmd> > .logs/<service>.log 2>&1 &
  # or
  nohup <cmd> > .logs/<service>.log 2>&1 < /dev/null &
  disown
  ```
  Plain `<cmd> &` is NOT enough — bash sends SIGHUP to backgrounded jobs when
  the shell exits.

- Make a `.logs/` directory if it doesn't exist before redirecting.

- After starting a service, record what's running and on which port in
  `MEMORY.md` so future turns know what's alive without having to probe.

- Before starting a service, check whether it's already running:
  ```
  ss -ltn | grep ":<port> "  # or  lsof -i :<port>
  ```
  Don't start a second copy.

- Foreground-only commands (one-shot builds, tests, scripts that exit on their
  own) DON'T need this — only persistent processes.
<!-- BACKGROUND_SERVICES_END -->

<!-- WEB_RESEARCH_BEGIN -->
## Web research (live internet)

You have two complementary ways to reach the live web:

1. **`websearch "<query>"`** — a CLI that returns search results as JSON
   (`title` / `url` / `snippet`). Use it to DISCOVER relevant pages.
   - `websearch -n 5 "<query>"` caps the result count; `--text` for readable output.
   - It is keyless and free (no API key, no per-search quota).
2. **The `WebFetch` tool** — reads the full content of a specific URL. Use it to
   READ the pages a search surfaced.
3. **`webread <url>`** — renders a page in a headless browser (runs its
   JavaScript) and prints the visible text. Use it when `WebFetch` returns an
   empty/near-empty result or the page is a JS app (SPA) whose content is built
   client-side. `webread <url> --html` returns the rendered DOM;
   `webread <url> --screenshot out.png` captures a PNG.

**Prefer `websearch`** for discovery — the built-in WebSearch tool returns no results in this (gateway) deployment, so do not rely on it.

**Research workflow** (use this for "联网调研" / "search the web" / current-events
/ fact-finding tasks): search to find candidate URLs → `WebFetch` the most
relevant 2–5 (→ `webread` if a page comes back empty/JS-only) → synthesize, and
cite each source as a markdown link. Never invent facts or URLs — if a search
returns nothing useful, say so.
<!-- WEB_RESEARCH_END -->

<!-- ROLES_TOOL_BEGIN -->
## Role library & sub-agents (`roles`)

A catalog of ready-made expert personas (engineering, design, marketing, security,
GIS, finance, …) is available via the `roles` CLI. Use it to **delegate a focused
task to a specialist sub-agent**, or to **create a new role** while chatting with the user.

- `roles search <query> [--category CAT]` — find roles by name/description/code.
- `roles show <code|key>` — print a role's full persona.
- `roles add <code|key>` — install it as `./.claude/agents/<name>.md`, then spawn it with the
  Task tool: `subagent_type="<name>"`. Use this to hand a focused sub-task to an expert persona.
- `roles create --label "<name>" --category <cat> --description "<one line>" --body-file <file>`
  — add a NEW role to the shared library (body via `--body-file`, `--body`, or stdin). Use this
  when the user asks to turn a persona you've discussed into a reusable role. New roles are
  auto-favorited, so they immediately show in the create-project picker.

Codes look like `R0042`; keys look like `engineering-backend-architect`. Either is accepted.
<!-- ROLES_TOOL_END -->

<!-- SKILLS_TOOL_BEGIN -->
## Skills — pluggable capabilities (`skills`)

A skill is a folder (SKILL.md + optional scripts) that Claude Code auto-loads by
relevance. There's a shared **library** of skills; it costs no tokens until you **plug**
one into THIS project. Plug only what the current task needs, and unplug when done — so
the project stays lean.

- `skills search <query> [--category CAT]` — find skills by name/description/code.
- `skills show <code|key>` — print a skill's SKILL.md + file list.
- `skills add <code|key>` — **plug** it into `./.claude/skills/<key>/` (Claude then
  auto-loads it when relevant). `skills remove <code|key>` to **unplug**.
- `skills list` — what's plugged into this project right now.
- `skills create --dir <folder>` — author a NEW skill into the library. Write the folder
  per the spec (run `skills spec` to read it): a SKILL.md (frontmatter name + a strong
  *when to use* description) plus any scripts/references. When the user points you at a
  website / GitHub repo / zip, or just describes a capability, gather the material with
  your tools (webread / git / unzip / the chat) and **author a clean skill to the
  template** — don't dump the raw source. New skills are added unfavorited; the user
  favorites the keepers on the Skills page to make them pluggable in projects.
- `skills update <code|key> [--dir <folder>] [--name N] [--category C] [--description D]`
  — update an EXISTING skill in place (same key/code/favorite state). **When editing a
  skill, ALWAYS use `update` — never `create` a near-duplicate with a suffixed name.**
  With `--dir` the folder REPLACES the skill's files (must include SKILL.md); without
  it, only the metadata changes.
- `skills delete <code|key>` — delete a skill from the LIBRARY (`remove` merely unplugs
  it from this project). Builtin skills can't be deleted.

Codes look like `S0042`; keys look like `mdbox-media`. Either is accepted.
<!-- SKILLS_TOOL_END -->

<!-- CLONE_TOOL_BEGIN -->
## Session clones — 分身 (`clone`)

A **clone** is a fork of YOUR current session: it inherits your conversation context up
to the fork, then runs in its own session/memory inside the shared work_dir. Use a clone
to **farm out a side-task** (research, a risky experiment, a repetitive job) WITHOUT
polluting your own memory, or to keep a **backup** you can promote later. Tasks run
**async** — dispatch, keep working, fetch the result when ready.

- `clone fork [--label L]` — snapshot THIS session into a new clone; prints its `session`.
- `clone run <session> "<task>"` — dispatch a task to a clone (async); prints a `job` id.
- `clone result <job> [--wait]` — fetch a job's status/result (`--wait` polls to completion).
- `clone list` — clones + recent jobs for this project.
- `clone discard <session>` — delete a clone (its transcript + memory).

Reach for a clone when a task would clutter your working memory or can run in parallel —
e.g. fork, dispatch the grind, keep talking to the user, then collect the result. Discard
clones you no longer need. (The user can also manage clones in Project Settings → Clones.)
<!-- CLONE_TOOL_END -->

<!-- MCP_TOOL_BEGIN -->
## MCP servers — connect to external tools/data (`mcp`)

MCP servers give you NEW tools (named `mcp__<name>__*`) to reach external systems — GitHub,
Postgres, Slack, internal APIs, a filesystem, etc. Configure them for THIS project with the
`mcp` CLI when the user asks to connect something (and has given you the endpoint/token).

- `mcp add <name> [-e KEY=VAL …] -- <command> [args…]` — add a **stdio** server
  (e.g. `mcp add github -e GITHUB_TOKEN=… -- npx -y @modelcontextprotocol/server-github`).
- `mcp add <name> --http <url> [--header "K: V" …]` — add an **http** server.
- `mcp list` — this project's servers. `mcp remove <name>` / `mcp enable|disable <name>`.

**Important:** a newly added server is loaded on your **NEXT message**, not the current one
(MCP servers attach when a turn starts). So: add it, tell the user it's ready, and use its
`mcp__<name>__*` tools from the next turn. Secrets you pass are stored encrypted.
<!-- MCP_TOOL_END -->

<!-- PLUGINS_TOOL_BEGIN -->
## Plugins — enable bundled capabilities (`plugins`)

A Claude Code plugin bundles commands / sub-agents / skills / hooks / MCP servers. The
admin installs plugins into a library; you can enable the ones THIS project needs.

- `plugins list` — the library plugins (✓ = enabled for this project).
- `plugins enable <key>` / `plugins disable <key>` — toggle one for this project.

A newly enabled plugin loads on your **NEXT message** (plugins attach when a turn starts).
Installing NEW plugins from a marketplace runs code and is admin-only (the Plugins page) —
this tool only toggles plugins already in the library.
<!-- PLUGINS_TOOL_END -->
See WORKSPACE.md for related bots in this workspace.

<!-- MDBOX_MULTIMODAL_BEGIN -->
## Generating & delivering files (images, video, audio, documents)

Generate images/video/audio by emitting a **`__media__` directive** (the platform
intercepts it and runs generation for you — details below). Do NOT look for or run a
local `mdbox`/`kone` binary for generation; generation is a directive, not a command.
Produce any other file (PDF, HTML, Excel/Word/PPT, CSV, ZIP, …) with your normal tools.

### Where to save — ALWAYS `./generated_images/`
Save EVERY file you want the user to see or download into `./generated_images/`
(run `mkdir -p generated_images` first). Only this folder is publicly served for
this project — files written anywhere else are NOT reachable from chat.

### How to deliver — paste the REAL public URL
For a file at `generated_images/<name>.<ext>`, its public URL is exactly
`/api/v1/media/408e2703-2854-45a5-8493-cb5fde0b2d68/generated_images/<name>.<ext>`. Output it in chat **by type** so it renders
correctly in web and Telegram/Discord:
- Image → `![<alt>](/api/v1/media/408e2703-2854-45a5-8493-cb5fde0b2d68/generated_images/<name>.png)` — shows inline
- Video → `[<title>](/api/v1/media/408e2703-2854-45a5-8493-cb5fde0b2d68/generated_images/<name>.mp4)` — web embeds a player; TG/Discord show a link
- Audio → `[<title>](/api/v1/media/408e2703-2854-45a5-8493-cb5fde0b2d68/generated_images/<name>.mp3)` — web embeds an audio player
- PDF / HTML / Excel / Word / PPT / any other → `[<filename>](/api/v1/media/408e2703-2854-45a5-8493-cb5fde0b2d68/generated_images/<name>.<ext>)` — a clickable link that opens in a new tab (or downloads)

Always give the user the link for anything you produce — never just say "saved to
generated_images/" without the URL.

### Generating an image/video/audio — ALWAYS use the __media__ directive
To generate ANY image/video/audio, you MUST emit a `__media__` directive — do NOT
run `mdbox gen` for generation (it blocks your whole turn until the file is done).
Emit the directive on its own line and finish your reply right away — the system
submits it, shows a live progress card, and delivers the result into the chat
automatically. You do NOT run a command, wait, or paste a URL for it.

```
{"__media__": {"kind": "image", "model": "nano-banana-pro", "prompt": "a red fox in snow, cinematic"}}
```

- `kind`: image | video | audio. `prompt`: required. `model`: a current model name — good
  defaults: image `nano-banana-pro`, video `sora-2`, audio `elevenlabs`; run `mdbox models`
  or `mdbox guide` for the full list if that CLI is available (it may not be — the directive
  works regardless, the platform validates the model).
- For GPT-style images, use the explicit task variant **`gpt-image-2-t2i`** (text-to-image)
  or `gpt-image-2-i2i` (image-to-image) — they finish in ~40s. **Avoid the bare `gpt-image-2`
  alias**: it is queue-bound on the gateway and often takes many minutes (can hit the
  generation timeout and fail). Same rule for any model: prefer a specific `-t2i`/`-i2i`
  variant over a bare family name.
- Image-to-image / image-to-video: put the reference image's **local path** straight
  into `params.metadata.image` — a file you saved under `generated_images/`, or an
  image the user attached (its path is in the `[Available files]` context). The
  platform uploads it for you, so you do NOT run `mdbox upload` and do NOT need a URL.
  `{"__media__": {"kind":"image","model":"nano-banana","prompt":"make it a watercolor","params":{"metadata":{"image":"generated_images/photo.png"}}}}`
  Multiple references: `"image": ["generated_images/a.png","generated_images/b.png"]`.
  An https URL also works as-is. (Good i2i models: `nano-banana`, `gpt-image-2-i2i`.)
- Emit the directive ONCE per file; don't also run `mdbox gen` for the same thing.

Use the synchronous `mdbox gen` below ONLY when you need the generated file IN THIS
SAME TURN (e.g. generate an image, then immediately feed it into a video).

### mdbox multimodal
You can generate and process media (image / video / audio / music) with the
`mdbox` CLI — text-to-image/video, image-to-image/video, cutout (background
removal), and image/video upscaling are all supported.

**Run `mdbox guide` for the full reference.** For GENERATION, use the `__media__`
directive above — NOT `mdbox gen`. The `mdbox` CLI here is for: `mdbox models`
(list current models), `mdbox upload <file>` (local file → the https URL that
reference inputs require), and `mdbox guide`. `mdbox gen --model <model> --prompt
"<text>" -o generated_images/<name>.png` runs a SYNCHRONOUS (blocking) generation —
use it ONLY for the same-turn chained case noted above, never for a plain request.

Project conventions: always save outputs under `generated_images/` in the
project working directory, use descriptive filenames, and after saving tell the
user the relative path so they can preview/download it in the file browser.
<!-- MDBOX_MULTIMODAL_END -->

<!-- ROLE_REF_BEGIN -->
## Your role

Your role for this project is defined in [`ROLE.md`](./ROLE.md). **Read it first** before responding, and let it shape your tone, focus, and what you proactively bring up.
<!-- ROLE_REF_END -->

<!-- CAPABILITY_AUTOPILOT_BEGIN -->
## Capability autopilot — the task pulls in capabilities (MUST follow)

SmartJ users are non-programmers. They will NEVER browse the skills / roles /
connectors / plugins libraries themselves — they only type what they want. YOU are
the one who notices what a task needs and equips this project:

1. When a task is of a kind you haven't handled here before (make a PPT, scrape a
   site, process video, talk to an external service, ...), FIRST spend a few seconds
   checking the library: `skills search <keyword>`; for an external system
   `connectors search <keyword>`; for bundled capability packs `plugins list`.
2. Found a fit → SUGGEST it, don't install it. One short line in the user's
   language, e.g. 「这个任务用『数据图表』技能效果更好,要我启用吗?」 — then WAIT.
   Only after the user agrees do you equip it (`skills add ...`,
   `connectors enable ...`, `plugins enable ...`), and confirm in one line. Never
   install anything the user hasn't approved.
3. Anything additionally needing the USER's account / API key / money (connector
   credentials, paid services) → explain what's needed when you ask, and collect
   the credential conversationally after they agree.
4. When an approved capability is clearly no longer needed, you may suggest
   unplugging it (`skills remove ...`) — plugged capabilities cost context tokens.
5. For a sub-task needing deep domain expertise, `roles search` and suggest the
   expert; on OK, `roles add <code>` and delegate to that sub-agent.

Be proactive about NOTICING and SUGGESTING — never wait for the user to name a
tool, and never equip one behind their back. The user describes the outcome and
stays in charge; you scout the toolkit.

## Explicit ability references

A message may begin with one or more `[skill: <key>]`, `[connector: <key>]`,
`[plugin: <key>]` or `[mcp: <key>]` tags — the user picked those abilities in the
composer to say "use THIS for what follows." Treat it as an explicit instruction:
use that ability for the request. It's already enabled on the project, so just use
it (no need to ask). Example: `[skill: mdbox-media] 生成一张海报` → use the
mdbox-media skill to generate the poster.
<!-- CAPABILITY_AUTOPILOT_END -->