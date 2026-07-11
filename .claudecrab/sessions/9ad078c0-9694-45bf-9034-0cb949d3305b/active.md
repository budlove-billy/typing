# Active Session State

## Current task
능력 영역별 신규 게임 기획서 작성 → `신규게임-기획-능력영역별.md`.
라이브 서비스이므로 코드는 손대지 않고 기획 문서만 작성/커밋. 영역별 신규 1종씩 + 우선순위 로드맵.

## Decisions
- 커버리지 진단: 얇은 축=관찰(spot 1)·협응(whack 1)·청각(melody 1), 공백=언어(0, vocab/typing 비활성) → 우선순위.
- 기억(4)·순발력(3)은 두터움 → 신규는 결 다른 1종만, 남발 금지.
- 언어 축은 레이더에 있으나 활성 0 — 신규는 로케일별 사전(anagram/word-search)으로 en/th 대응 or ko-only 판단 필요(제품 사인오프).
- 신규 후보 매핑: memory=거꾸로기억, focus=화살표집중(flanker), space=블록채우기(폴리오미노), calc=어림계산, logic=노노그램, lang=글자뒤죽박죽(anagram), sight=다른모양찾기(회전/거울), coord=마시멜로받기(catch), sound=리듬따라하기.
- 모든 신규는 기존 패턴 필수 준수: HOME_GAMES/ABILITY_MAP/GAME_REF/best키/공유/도전장/미션풀 연동 + 생성 불변식 시뮬 검증 + node --check + index=brain_app 동기화.

## Open questions
- 언어 축 재개 여부(포지셔닝) — 사용자 결정 필요.
- 어떤 영역부터 실제 구현 착수할지 사용자 우선순위 확인.
