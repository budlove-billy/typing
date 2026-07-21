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

## 배포
- git push origin master:main → Vercel 자동배포. 이번 배치 push 예정.

## Open questions
- (해소) pub-id 신규신청, 이메일 확정.
