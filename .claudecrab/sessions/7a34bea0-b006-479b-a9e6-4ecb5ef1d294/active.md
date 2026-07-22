# Active Session State

## Current task
사이트 수익화(구글 애드센스) + 트래픽 유입. 사용자: 코드분석→살리기→유입→애드센스→꾸준한 수익. 긴박함 강함.

## 진단 (2026-07-21)
- 사이트는 **살아있음**(playmallow.com 정상, 33게임+운세+랜딩19+가이드6). "살리기"=트래픽/수익.
- **애드센스 미적용**(광고코드 0). **개인정보처리방침 없음**=승인 하드블로커. **ads.txt 없음**.
- GA4 있음(G-9EQEH5BF0C). 도메인 2026-07-10 출시=약11일 신생 → "저품질/트래픽부족" 반려 위험.
- index.html==brain_app.html 바이트동일(수정 시 둘 다 sync). 정적 랜딩 다수.

## 계획
1. (✅ 커밋 4578fbf) 개인정보처리방침 `/privacy/`(ko/en) + 홈푸터 링크 + sitemap.
2. 애드센스: **신규신청**으로 결정(pub-id 없음). 이메일=contact@playmallow.com 확정(나중에 연결). 가이드=`애드센스-신청-가이드.md`. pub-id 받으면 head 스니펫+ads.txt+슬롯 일괄 삽입.
   - ⚠️ 켜면 "광고없음" 카피 수정: 2048/·sudoku/·water-sort/.
3. 트래픽(진행): ✅ 운세4종(unse/zodiac/ttirank/tarot) JSON-LD 추가. 플레이북=`트래픽-실행-플레이북.md`.
   - 사용자 직접 액션(★): 서치콘솔·네이버 색인요청, 커뮤니티 시딩, 네이버블로그, 게임포털.
   - 다음 코드작업: 나머지 랜딩 JSON-LD, 운세 OG이미지, 내부링크, 시즌 랜딩(신년/수능).

## 배포 ✅ 완료
- 원격 main=33ba213, /privacy/ HTTP200·운세 JSON-LD 라이브 확인(2026-07-21). 사용자가 인증 리프레시 후 push 성공.
- 이 환경 push 재시도 시 hang 없이 exit0 → 자격증명 리프레시됨(다음 커밋 push 가능 추정).

## 진행 요약 (2026-07-21, 전부 배포됨 fd9e0c7)
- ✅ /privacy/ · 랜딩 17/17 JSON-LD · 가이드 6종 Article · 운세 4종 리치콘텐츠 · 홈푸터 · 문서

## 셋다 작업 — ✅ 전부 완료
- ✅ /stroop/ ✅ /suneung/ /newyear/ (라이브)
- ✅ 운세 4종 OG 이미지 완비: og/{zodiac,ttirank,unse,tarot}.png 1200x630 + og:image/twitter 메타 교체.
  - zodiac/ttirank=커밋0eda986(라이브). unse/tarot=**커밋 c18f3ac(push 대기)**.
- OG 크롭 워크플로 확립: __media__ 생성→generated_images/(gitignore) 낙하→PIL 크롭(정사각→하단/센터 밴드)→og/ 저장→메타 교체. box: zodiac autocrop, ttirank(66,306,962,716), unse(0,380,1024,918)하단, tarot(0,210,1024,748)센터.

## OG 마스코트 교체 ✅ 완료
- ✅ 운세 4종(unse/zodiac/ttirank/tarot) OG 전부 **실제 말로우 마스코트**(핑크 둥근+반짝이별)로 교체·라이브(커밋 4862e12, 원격 반영, 4장 HTTP200 확인).
- 방법: i2i(nano-banana, ref=icon-512.png) 재생성→PIL 크롭 1200x630→og/*.png 덮어쓰기. 크림큐브(AI오생성) 문제 해소.
- 캐시 주의: 카톡/페북은 옛 미리보기 캐시 → 카카오/페북 디버거서 초기화 또는 URL에 ?v= 붙여 재스크랩.

## 색인 요청 목록(✅ 사용자 색인 완료)
- 1순위: /stroop/ /suneung/ /newyear/ /privacy/  2순위: /unse/ /zodiac/ /ttirank/ /tarot/  3순위: 사이트맵.

## OG 추가 생성 ✅ (신규 랜딩 3종 완료)
- ✅ stroop/suneung/newyear 전용 OG(실제 마스코트) 생성·크롭·메타교체·라이브(커밋 7b418ff, HTTP200).
- ✅ home/sudoku/2048 OG 생성·크롭·메타교체·라이브(커밋 d2c5a80, 홈은 index+brain_app 동기화).
  - ⏳ **iq-test만 재생성 대기**(4장중 3장 낙하). i2i(ref=icon-512) IQ씬(전구+도형+물음표)→크롭→og/iq-test.png→iq-test/index.html line12 메타교체+twitter.
- 남은 og.png 폴백(핵심 4 이후): 게임랜딩 나머지 8종·가이드 6종·moamoa.

## Open questions
- (해소) pub-id 신규신청, 이메일 확정.
