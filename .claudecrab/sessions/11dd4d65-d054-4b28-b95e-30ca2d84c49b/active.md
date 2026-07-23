# Active Session State

## Current task
완료 — UX·성장 구조 개편 5종 + D 2차(상위 게임 씬 SVG)까지 모두 배포

## D 2차 완료 (bb1a5fe, pushed)
- GAME_SCENES 맵 + initGameScenes(): merge/slide/react/cards/sudoku/stroop 6종 인트로 카드에
  테마 씬 SVG(2048타일/슬라이딩그리드/번개/카드팬/스도쿠판/스트룹텍스트 + 마스코트)
- 카드 우상단 배치, 텍스트 max-width로 겹침 방지. 파일 없는 인라인 SVG(이미지 생성 안 씀 — 가볍고 빠름)
- errcheck ALL 34 CLEAN, 스크린샷으로 시각 확인 후 push 완료

## Earlier completed (all pushed)
- A 사운드팩 5118482 / B 능력치10축 0ad74e9 / C 홈개편 7000ac3 / E 등급진행 21e9ece / D1차 전환 6a0dc74 / docs bd39c24

## 후속 후보
- 더 많은 게임에 씬 확장 (whack/catch/melody 등) 또는 AI 생성 배경 이미지로 한 단계 업
- 애드센스(pub-id 대기), GA 상위 게임 데이터 기반 콘텐츠

## Completed (committed)
- **A. 사운드 팩** (5118482): `_tone()` 레이어드 신스, sfx 12종, UI 탭 위임 리스너, 신기록 팡파르, 60초 게임 타이머 틱 11곳
- **B. 능력치 10축** (0ad74e9): +coord/sound/sight, overall=숙련도70%+커버리지30%, 등급 배지 6단계(gradeOf/gradeNext)
- **C. 홈 개편** (7000ac3): 오늘의 데일리 섹션(moamoa/queens/tango) + 인기게임 하드코딩→recommendGames 개인화
- **E. 등급 진행 표시** (21e9ece): 결과 화면 grade-line (다음 등급까지 N점)
- **D. 전환 연출** (6a0dc74): screenIn 키프레임 + 축 배경 transition
- **docs** (bd39c24): MEMORY.md + CLAUDE.md 체인지로그

## Verification
- errcheck.mjs: **ALL 34 CLEAN — no pageerrors** (BASE를 8156으로 수정함)
- sfx_check / ability_check / home_check / grade_check 모두 통과
- 정적 프리뷰 서버: 포트 **8156** 가동 중 (python http.server, detached)

## Key facts (변경된 구조)
- ABILITIES 10축 = memory,focus,speed,space,calc,logic,lang,coord,sound,sight
- overallLevel = round(핸게임평균레벨*0.7 + (핸게임수/전체)*100*0.3)
- GRADES 6단계 경계: 입문0/새싹10/브론즈30/실버50/골드70/다이아90 (% of GAME_REF)
- sfx 종류: good,bad,win,tap,combo,level,flip,whoosh,tick,count,go,record (+__tick 낮은수준)

## Open questions / 후속
- D 2차: 상위 게임 이미지 자산 리프트(생성 이미지 배경/스프라이트) 미착수 — GA 상위 게임 선정 후
- 배포: git push origin master:main → Vercel 자동배포 (push는 사용자 확인 후)
- 랭킹: 서버리스 대안은 "등급 진행"으로 해소. 실서버 랭킹은 Supabase 슬롯 문제로 보류 유지
