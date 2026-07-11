# Active Session State

## Current task
Wave2-3 신규 7종 일괄 구현 완료(odd 포함 총 8종 이번 세션). 활성 30종.
문법 컴파일 PASS, 배선/i18n 정합성 PASS(about.p1/p2는 숫자키 오탐). index=brain_app 동기화 후 커밋+push 배포 진행.

## Decisions
- flank/guess/rev/rhythm/catch/fit/nono/anagram 전부 기존 패턴 미러링 + 생성형 선검증(.logs/gen_sim.mjs) 후 이식.
- anagram = 언어 축(vocab/typing 대체). ko+en 동시, th 숨김(langs 필터). vocab/typing 소스 보존.
- nono 라인솔버 유일해 생성(5/8/10 즉시). fit 폴리오미노 탭배치. catch 4레인 낙하. rhythm 템포정규화(1.7 임계).
- 미션풀 A+rev,rhythm / B+flank,catch / C+fit. 능력치 8종 ABILITY_MAP/GAME_REF 추가.

## Open questions
- ⚠️ 라이브 스모크 테스트(실제 플레이) 미완 — 이 환경 playwright/webread 없음. 배포 후 사용자 확인 필요:
  nono 클루 레이아웃/판정, catch 낙하·바구니 타이밍, rhythm 오디오 첫탭 resume, fit 배치 감도, anagram ko 음절 타일.
- 튜닝 레버(난이도 수치)는 플레이 후 조정 대상.
