# Active Session State

## Current task
(완료) 암산 수정(3a91abf) — 내기록·게임카드가 flat 저장(math/iq/sudoku)을 누락하던 버그를 gameBestVal()로 통일, 정답/오답 sfx 추가. 배포·라이브 확인.

## Decisions
- 기록 조회는 어디서든 gameBestVal(id) 사용(best/flat 모두 처리). braintype만 제외.

## Open questions
- 백로그: 시각탐색, 어림계산, 도전장 링크, 개인정보처리방침.
