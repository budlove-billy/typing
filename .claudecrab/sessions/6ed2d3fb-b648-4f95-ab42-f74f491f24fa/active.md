# Active Session State

## Current task
구글 서치콘솔 색인 리포트 6개 카테고리 진단.
- 정상(신생 SPA): ?game=slide=대체페이지(정상 canonical), http/www 리디렉션(정상), guide 발견-미크롤(크롤대기), ?lang=en 중복(클라이언트 i18n 한계), 크롤됨/발견됨-미색인(도메인 신생 7/10, 시간+트래픽 필요)
- **유일한 실질 항목**: 404 IPA URL 7개. 출처=vocab(비활성 영어단어게임) 발음필드 `p:'/ˈnjuːɑːns/'` → 앞뒤 슬래시가 루트상대 URL(/.../)처럼 보여 구글봇이 링크 오인 크롤. 404는 무해(구글이 올바로 버림). 크롤버짓 소량 낭비뿐.
- 새 랜딩 5종+stroop: 다른 세션이 JSON-LD(WebApplication+BreadcrumbList) 추가함. 되돌리지 말 것.

## Decisions
- 색인 지연은 오류 아님. 재검증 남발 금지. 처방=시간+홍보(트래픽/링크).
- IPA 404 수정 여부는 사용자 확인 후(발음이 href인지 텍스트인지에 따라).

## Open questions
- IPA 404 청소할지(선택) — 리포트만 지저분, 실제 피해 없음.
