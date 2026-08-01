# Active Session State

## 진행 중인 작업 — 공유 미리보기가 항상 한국어로 나오는 문제
**원인 확정**: 카톡·페북·라인 등 공유 미리보기 크롤러는 **자바스크립트를 실행하지 않는다**.
앱은 `syncLanguageSEO()`에서 og:title/description을 JS로 바꾸지만 크롤러는 원본 HTML만 읽으므로
언제나 한국어. `curl "https://playmallow.com/?lang=en"` → og:title 한국어 확인.
og 이미지(`og/home.png`)는 글자가 없어 언어 무관 — 텍스트 태그만 문제.

**범위(전수 조사)**: 언어 선택기가 있는 페이지는 6개 —
`/`(ko/en/th, og를 JS로 갱신하지만 무의미), `/persona/` `/queens/` `/tango/` `/zodiac/`(ko/en/th),
`/tarot/`(ko/th). 이 5개는 og 갱신 JS조차 없고 URL 동기화도 없음(주소가 그대로라 공유 불가).

**해결 설계**: 언어별 **공유용 얇은 페이지**(`/en`, `/th`, `/queens/en` …) 신설.
- 실제 앱을 복제하지 않는다(index.html 823KB — 복제하면 수정 때마다 낡은 사본 위험).
- 얇은 페이지 = 해당 언어 title/description/og/twitter + `noindex,follow` + JS 즉시 이동
  (`/en` → `/?lang=en`, 쿼리·해시 보존). 크롤러는 JS를 안 돌리므로 og만 읽고 멈춤.
- 앱은 언어 변경 시 주소창을 `?lang=en` 대신 `/en`으로 `replaceState` → 주소창을 복사해
  공유해도 올바른 미리보기. **슬래시 없는 경로라 상대경로 자산이 그대로 동작**(`/en` 기준
  디렉터리 = `/`). 하위 페이지도 `/queens/en` → 기준 `/queens/` 로 동일.
- canonical·hreflang은 기존 `?lang=` 유지(SEO 흔들지 않음). 얇은 페이지는 noindex.
- `vercel.json` rewrite로 `/en` → `/en.html`, `/:dir/en` → `/:dir/en.html`.
- 도전장 링크·공유 문구의 URL도 언어 경로를 포함하도록 수정.

## 배포 방법(확인됨)
로컬 브랜치는 `master`, 원격 배포 브랜치는 `main`. 푸시는
`git push "https://x-access-token:$GITHUB_TOKEN@github.com/budlove-billy/typing.git" master:main`
(토큰은 `.env`의 `GITHUB_TOKEN`). 푸시 후 1분이면 Vercel 반영.

## 미결(사용자 결정 대기)
- **애드센스 — 사용자 차례(심사 요청).** 퍼블리셔 ID `ca-pub-8615421634491307` 받아
  2026-07-31 연결 코드 삽입 완료: 배포 27쪽 head 스니펫 + 루트 `ads.txt` + 2048 랜딩
  "광고 없이" 문구 정정. 배포까지 마침. 이제 사용자가 **애드센스 대시보드에서 "검토 요청"**
  버튼을 눌러야 심사 시작. 승인 통보가 오면 내가 할 일 = 광고 단위(슬롯) 배치
  — `애드센스-신청-가이드.md`의 안전 위치만, **게임 플레이 화면엔 영구 금지**.
- 레거시 `brain_app.html` 정리 여부(미배포·미링크. 애드센스 코드도 안 넣음)
- GA4 리뷰 리마인더 미실행(사용자 확인 없이는 실행 금지)
- GA4 리뷰 리마인더 미실행(사용자 확인 없이는 실행 금지)

## 다음에 이어서 볼 만한 것
- 신규 개선(봇·주간 챌린지)이 실제 재방문율을 올리는지 GA4로 2~3주 뒤 확인
- nono는 점수 눈금이 새로 잡혔지만 옛 기록 환산에서는 제외됨(정직한 환산 기준이 없어서).
  사용자가 "노노그램 기록이 이상하다"고 하면 이 사실을 먼저 설명할 것
