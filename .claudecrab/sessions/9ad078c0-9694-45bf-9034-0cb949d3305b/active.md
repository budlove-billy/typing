# Active Session State

## Current task
(완료) **말로우 페르소나**(`/persona/`) 심층 성격 유형 진단 신규 배포.
- 24문항 시나리오형(축당 6: EI/SN/TF/JP) → 16유형. 축별 % 바 + 유형 풀 프로필(강점/약점/연애/일/스트레스/성장/궁합/추천게임).
- 추천 게임은 `/?game=<id>` 딥링크(앱 showScreen 진입 funnel). 결과 공유카드(600x820, 코드+별명+4축바) 필수 반영.
- 홈 배선: HOME_GAMES persona(koOnly,cat.fun) + funByLang.ko + nav.persona i18n + 최초방문 dot(persona_seen) + sitemap + brain_app 동기화.
- 검증: node --check OK, 16유형·24문항·궁합/게임 참조 무결, 채점 시뮬(극단값 정확·랜덤 2000회 전부 유효·16종 도달). site_audit ld+json 오탐 제외 패치.

## Decisions
- braintype(6문항·게임추천)와 분리: persona=심층 진단. MBTI® 미표기·유형 설명 자체작성(저작권).
- v1 ko 전용(langSel 없음), 반응 좋으면 en/th·인지기능(v2).

## Open questions
- 모아모아 퍼즐 D+25(8월 초). 개인정보처리방침(로그인/애드센스 전).
- persona 반응 보고 en/th 확장 여부 결정.
