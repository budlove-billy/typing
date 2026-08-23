# 애드센스 재검토 요청 문안 (2026-08-23)

반려 사유: **가치가 별로 없는 콘텐츠 (Low value content)**
제출 위치: AdSense → 정책 센터 → 해당 사이트 **수정** → 발견된 문제 → **검토 프로세스 시작**

> 이 텍스트는 구글이 "문제를 검토할 때 사용한다"고 명시한 항목입니다. 사람 리뷰어가 읽을 수
> 있는 유일한 지점이므로, 무엇이 문제였는지 인정하고 무엇을 어떻게 고쳤는지 숫자로 적습니다.
> 재검토는 횟수 제한이 있고 반복 거절되면 버튼이 잠기므로 한 번에 통과시키는 것이 목표입니다.

---

## 권장 — 영문 (1,430자)

```
Thank you for the review. We agree with the assessment and have rebuilt the
site's content rather than making cosmetic changes.

What was wrong:
Many of our pages were short landing pages whose only purpose was to send the
visitor into the game app. Measured on rendered output, 18 of our 57 URLs had
under 1,200 characters of visible body text. The worst case, the Thai version
of our tarot page, rendered only 221 characters because its Thai content
section was missing and the Korean section was hidden in Thai mode.

What we changed:
1. Every one of our 57 URLs now has substantial original content. The shortest
   page is now 1,246 characters of rendered body text; the median is 2,454.
2. We did not pad word counts. Each page now carries information that exists
   only on that page - for example our Sudoku page explains hidden singles,
   naked singles, naked pairs and pointing pairs, and what each difficulty
   level actually requires; our Nonogram page explains the overlap calculation
   (clue x 2 - row length) and how to order rows by slack.
3. We wrote this content natively in Korean, English and Thai rather than
   machine-translating one version.
4. We added the missing Thai content section to the tarot page.
5. We corrected two pages that incorrectly stated the site had no ads.
6. We corrected an inconsistent game count across the site (33 / 31 / 36) to
   the verified figure of 36.

We verified every URL by rendering it in a real browser and measuring the
visible text, not by checking file size. We are happy to make further changes
if anything still falls short.
```

## 대안 — 국문 (960자)

```
검토 감사합니다. 지적에 동의하며, 표면적인 수정이 아니라 콘텐츠를 다시 만들었습니다.

무엇이 문제였는지:
저희 페이지 상당수가 방문자를 게임 앱으로 보내는 것만이 목적인 짧은 안내 페이지였습니다.
실제 렌더링 기준으로 57개 URL 중 18개가 본문 1,200자 미만이었고, 가장 심한 타로 페이지의
태국어 버전은 태국어 콘텐츠 섹션이 없어 한국어 본문이 숨겨지면서 221자만 표시됐습니다.

무엇을 고쳤는지:
1. 57개 URL 전부에 실질적인 자체 콘텐츠를 넣었습니다. 가장 짧은 페이지가 1,246자,
   중앙값은 2,454자입니다.
2. 글자수를 채운 것이 아니라, 각 페이지에서만 얻을 수 있는 내용을 넣었습니다. 예를 들어
   스도쿠 페이지는 숨은 단수·단독 후보·짝 후보·줄-박스 상호작용과 난이도별로 어떤 기법이
   필요한지를, 네모로직 페이지는 겹치기 계산과 여유가 적은 줄부터 푸는 순서를 설명합니다.
3. 한 언어를 기계번역한 것이 아니라 한국어·영어·태국어 각각으로 작성했습니다.
4. 타로 페이지에 누락돼 있던 태국어 콘텐츠 섹션을 추가했습니다.
5. 광고가 없다고 잘못 표기돼 있던 페이지 2곳을 수정했습니다.
6. 사이트 곳곳에서 33 / 31 / 36으로 어긋나 있던 게임 수를 실제 값인 36으로 통일했습니다.

파일 크기가 아니라 실제 브라우저로 렌더링해 보이는 텍스트를 측정하는 방식으로 전 URL을
검증했습니다. 미흡한 부분이 있다면 추가로 수정하겠습니다.
```

---

## 제출 전 체크리스트

- [ ] 정책 센터에서 **문제로 지목된 사이트가 playmallow.com 하나인지** 확인
      (여러 개면 각각 따로 요청해야 함)
- [ ] 배포 반영 확인 완료 — 2026-08-23 라이브 6개 페이지 200/본문량 확인함
- [ ] Search Console 사이트맵 재제출 (lastmod 39개가 오늘 날짜)
- [ ] **요청 후 심사가 끝날 때까지 사이트 구조를 바꾸지 않기**
      (일본어 등 신규 URL 추가는 승인 후에)

## 근거 수치 출처

`.logs/thin_audit.mjs` — 57 URL을 실제 브라우저로 렌더링해 보이는 텍스트만 계측.
최소 1,246자 · 중앙값 2,454자 · 최대 3,845자 · 1,200자 미만 0개 · 중복 0쌍.
