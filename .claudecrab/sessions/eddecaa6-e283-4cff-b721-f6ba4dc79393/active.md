# Active Session State

## Current task
(완료) **말로우 런(Mallow Run)** 신규 — 원버튼 엔들리스 러너(순발력·집중력), 앱 내부 게임.
- 캔버스: 마스코트가 달리며 포크 장애물 점프, 가속(cap), 하이스코어(거리/12), 난이도 3단.
- 물리 G=0.9·JV=15(peak 125>장애물46), 장애물 spawn=safeGap(spd)=spd*airTime+폭+여유 → 항상 통과 가능.
- 선검증 `.logs/run_sim.mjs`: 완벽플레이어 3난이도 200/200 생존.
- 입력: 캔버스 pointerdown / Space·↑ / 점프버튼. 종료=충돌. 결과·공유·도전장.
- 배선: HOME_GAMES cat.speed(chop 뒤)·ABILITY_MAP run{speed80,focus20}·GAME_REF run:600·gameShare·haltRunningGames(resetRun)·i18n run.*(ko/en/th)·nav.run. 능력칩/철학콜아웃 자동.
- 검증: node --check OK, 배선 정합 grep 확인, site_audit 클린, brain_app 동기화, 배포 ad1dbb5.

## 라이브 스모크 필요
- 실제 브라우저에서 점프 타이밍·충돌·모바일 탭·캔버스 리사이즈(dpr) 체감. GAME_REF run:600 실측 후 보정 가능.

## Open questions
- 모아모아 퍼즐 D+25(8월 초). 개인정보처리방침(로그인/애드센스 전).
- run 반응 보고 조작(낮은 장애물 숙이기/새 장애물) v2 여부.
