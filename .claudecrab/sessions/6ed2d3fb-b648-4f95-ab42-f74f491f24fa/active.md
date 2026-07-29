# Active Session State

## Current task
(완료) GSC 색인 리포트 진단 + IPA 404 청소.
- IPA 404 수정 배포됨(862f2a5): vocab 발음 /ipa/→[ipa] (index.html line 4794 render + line 1115 placeholder /—/→[—]). index=brain_app 동기화. 라이브 확인.
- GSC 6개 카테고리 중 5개는 오류 아님(신생 SPA 정상): ?game=slide 대체페이지, http/www 리디렉션, guide 발견-미크롤, ?lang=en 중복(i18n 한계), 크롤됨/발견됨-미색인(도메인 신생). → 시간+홍보로 해결.
- 새 랜딩 5종+stroop: 다른 세션이 JSON-LD 추가함. 되돌리지 말 것.

## Decisions
- 색인 지연은 오류 아님. 재검증 남발 금지. 처방=시간+홍보(트래픽/링크).
- GSC 기존 404들은 자연 소멸 대기(구글 재크롤 시 사라짐). 급하면 "수정 검증" 1회.

## Open questions
- (없음) 다음: 2주 데이터 리뷰(리마인더 7/27 예약됨) 또는 홍보 시딩.
