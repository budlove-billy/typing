# Active Session State

## Current task
(완료) 운세 다국어 마감: ① 홈→운세 카드 이동 시 현재 앱 언어를 `?lang=`로 전달(goExternal) ② 타로 태국어(ko/th) 전면 이식.
- 타로: TX(ko/th UI)+CARD_TH(78장 태국어: 메이저22 개별+마이너56 슈트·랭크 생성)+langSel+detectLang(?lang→brain.lang), 렌더/공유카드 CF(pick)로 언어별 카드.
- 별자리(ko/en/th)는 이미 완비 → 홈 ?lang 전달로 영어 자동 적용 문제 해소.
- 검증: node --check OK, CARD_TH 78장 전필드 채움, site_audit 클린(tarot 동적 src만 오탐), brain_app 동기화.

## Decisions
- 타로 en 제외(저작권 신중). unse/ttirank는 koOnly 유지.
- 라인업 수량 확장 종료, 데이터 기반 품질 단계.

## Open questions
- 모아모아 퍼즐 D+25(8월 초). 개인정보처리방침(로그인/애드센스 전).
