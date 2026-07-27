# Active Session State

## Current task
글자 맞추기(anagram) 게임 전면 개선 — index.html. 7개 항목 전부 적용.

## Plan / Decisions
1. 터치 버튼 44→56px(모바일 60px), 폰트 1.3→1.65rem, gap .4→.55rem, used 타일 hidden→dim(위치 고정), :active+진동
2. 정답 조립 영역 아래로: .ag-assemble 박스(min-h 96px)+안내문구, 여백
3. 셔플백(AG.bag, key=lang|diff)으로 단어 반복 방지 + 재셔플 첫 단어≠직전
4. ko 반복형(ABAB) 단어 제거
5. AG_LEN 재설계 easy ko[2,3]/en[3,4], normal ko[4]/en[5], hard ko[5,6]/en[6]. ko:2/5/6 신규 pool. 셔플백은 length 합산 pool
6. AG_HINTS{3,2,1}, AG_PENALTY{0,1,2}s 오답 시간차감, AG_MULT{1.0,1.4,2.0}+속도보너스(최대10)
7. i18n anagram.prompt 추가

## Files
- index.html: CSS(618-625), 게임카드HTML(2688-2690), i18n(3227-3229), AG 로직(9202-9235)

## Status
편집 진행 중
