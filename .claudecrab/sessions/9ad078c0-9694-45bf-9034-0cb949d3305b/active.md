# Active Session State

## Current task
Wave 1 로드맵 진행 중. **odd(다른 모양 찾기) 구현 완료** — 검증(유일성+문법) PASS, index=brain_app 동기화, 커밋 예정.
다음: Wave1 2호 **catch(마시멜로 받기)**.

## Decisions
- odd = spot 미러링(회전차 버전). SVG 화살표 비대칭 → delta>0로 유일성 보장. 각도 하한 easy/normal/hard = 20/15/11°.
- 연동 전부 완료: HOME_GAMES(cat.sight)/ABILITY_MAP odd={focus:40,space:30,speed:30}/GAME_REF 400/CH_GAMES+chState/MISSION_B/haltRunningGames/gameShare/i18n 3개국어.
- 검증: `.logs/odd_sim.mjs`(불변식+인라인 스크립트 컴파일 체크) PASS.

## Open questions
- 사용자 라이브 확인: odd 화살표 회전차가 실제로 지각 잘 되는지(특히 hard 11°·큰 판).
- Wave1 순서(odd→catch→rhythm) 계속 진행 여부.
