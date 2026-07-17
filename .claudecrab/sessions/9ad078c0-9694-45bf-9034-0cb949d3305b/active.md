# Active Session State

## Current task
(완료) **데일리 논리퍼즐 2종 배포** — 글로벌(언어무관) 확장.
- **말로우 크라운(`/queens/`)**: 행·열·색구역 왕관 1개+8방향 인접금지. N6/7/8. 생성=랜덤성장+균형필터(≤1.9×평균)+유일해 솔버+시드재시도.
- **말로우 탱고(`/tango/`)**: 해/달 Binairo. 3연속 금지·줄당 개수균형. N6/8. 생성=완성해→given제거 유일화.
- 공통: kstDate 데일리 시드·결정적·유일해 100%·타이머·충돌 하이라이트·공유카드·● 뱃지·ko/en/th·langSel+detectLang.
- 배선: HOME_GAMES cat.daily(langs 3언어)로 모아모아 옆 + nav i18n + dot(queens_done/tango_done) + sitemap. brain_app 동기화, site_audit 클린.
- 선검증: `.logs/queens_sim.mjs`(N6·7 365일 100%, ≤7.5ms/일), `.logs/tango_sim.mjs`(N6·8 200/200). 페이지 JS도 node --check + 생성기 단독 유일해 확인.

## Decisions
- 언어종속(Wordle/Connections/모아모아) 대신 **언어무관 로직퍼즐**로 en/th 데일리 공백 해소(2026 트렌드=LinkedIn Queens/Tango).
- Queens 균형 vs 유일해 상충 → 랜덤성장+사후 균형필터가 최적. N=8은 균형필터 시 느려 완화 여지.

## Open questions
- 모아모아 퍼즐 D+25(8월 초). 개인정보처리방침(로그인/애드센스 전).
- Queens/Tango 반응 보고 =/× 제약(정통 Tango)·난이도 튜닝 v2.
