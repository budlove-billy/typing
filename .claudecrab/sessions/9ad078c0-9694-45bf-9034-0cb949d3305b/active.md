# Active Session State

## Current task
(완료) Phase A 코드: Mallow 리브랜딩+SEO+PWA+?lang=. 사용자 playmallow.com 구매 진행 중.

## Decisions
- 브랜드 Mallow / 서브 "말랑말랑 두뇌게임" / 도메인 playmallow.com. 아이콘=파랑 라운드+M, OG 1200x630 생성(PIL).
- sw.js=HTML network-first. manifest.webmanifest. robots/sitemap(hreflang ko/en/th). 언어: ?lang= → localStorage brain.lang.
- 남은 것(사용자): 도메인 결제, Cloudflare Pages 연결(GitHub repo typing), Search Console/Naver Advisor/GA4 계정 등록.

## Open questions
- 도메인 구매 완료 여부 → 완료 시 배포 안내.
