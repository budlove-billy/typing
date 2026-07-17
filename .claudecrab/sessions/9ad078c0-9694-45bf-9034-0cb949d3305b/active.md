# Active Session State

## Current task
(완료) **말로우 페르소나 다국어(ko/en/th)** 확장 배포.
- TX(3언어 UI)+AXL(축 극명)+Q_i18n(en/th 24문항)+TYPES_i18n(en/th 16유형 9필드)+GNAME_i18n. 접근자 qText/typeOf/poleName/gameName로 렌더 분기. detectLang(?lang→brain.lang)+langSel+applyLang+setLang(결과중 언어변경 시 재렌더).
- 채점은 언어무관(Q 극/축 공유) — 시뮬로 ko=en=th 동일코드 확인. 홈: persona langs ko/en/th + funByLang 3언어 + goExternal ?lang 전달.
- 검증: node --check OK, 24문항×3 / 16유형×2 필드 무결, TX 키 동일, site_audit 클린, brain_app 동기화.

## Decisions
- persona=심층진단(24문항), braintype(6문항)와 분리. MBTI® 미표기·설명 자체작성.
- 앞선: 질문 상황문구 15px, 퀴즈/결과서 태그라인 숨김.

## Open questions
- 모아모아 퍼즐 D+25(8월 초). 개인정보처리방침(로그인/애드센스 전).

