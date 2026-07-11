# Active Session State

## Current task
2차 신규 4종(wordsearch/diff/pitch/trace) 구현 완료 → 활성 33종. 검증 PASS 후 배포.
모든 인지 영역 ≥2종 달성(언어 anagram+wordsearch=2, 관찰 spot+odd+diff=3, 청각 melody+rhythm+pitch=3, 협응 whack+catch+trace=3).

## Decisions
- 생성 선검증은 반드시 실제 앱 shuffleArr 의미(비변형)로(.logs/gen_sim2.mjs). wsPlace 500/500·tcWalk 안정.
- wordsearch=ko+en(langs 필터, th 숨김), AG_WORDS 재활용. pointer 드래그+elementFromPoint.
- 검증 3종 통과: 문법 컴파일 / wire_check(배선·chState·i18n, about.p1/p2는 숫자키 오탐) / runtime_probe(4종 start 무예외).

## Open questions
- ⚠️ 라이브 스모크: ws/trace 모바일 드래그 정밀도, pitch 오디오 첫재생, diff 큰 판 가독성. 배포 후 확인.
- 후속 후보: ko 전용 언어게임(끝말잇기/속담), 개인정보처리방침(로그인 시).
