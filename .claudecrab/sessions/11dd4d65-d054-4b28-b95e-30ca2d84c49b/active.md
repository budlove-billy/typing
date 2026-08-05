# Active Session State

## Current task
운세 3종 고도화 — `/unse/` 완료(푸시됨). 이제 **`/zodiac/` 별자리 + `/ttirank/` 띠별 순위**.

## 진단 (둘 다 unse와 동일한 병)
- **zodiac**: `starN=2+floor(rng()*4)`, 분야는 `lvl(rng)` → 총운·분야가 무관한 독립 난수.
  생년월일은 별자리 판정에만 쓰고 버림. 각 항목 1문장. ko/en/th 3언어.
- **ttirank**: `score=rng()` 12개 뽑아 정렬 → 순위에 근거 전무. ko 전용.

## 설계
### zodiac — 실제 서양 점성술 방식(트랜짓)
**오늘 달이 지나는 별자리 × 내 별자리 = 아스펙트** + 달의 위상 보정
- 아스펙트 7종: 합(0°)·반육각(30°)·육각(60°)·사각(90°)·삼각(120°)·퀸컹크스(150°)·대각(180°)
- 거리 d=((moonSign-mySign)+12)%12 → 0합 1/11반육각 2/10육각 3/9사각 4/8삼각 5/7퀸컹크스 6대각
- 달 황경: Meeus 저정밀(주요 6항) — **검증 완료 `.logs/moon_verify.mjs` ALL PASS**
  일식 3건·월식 3건 앵커 오차 0.06~0.15°, 삭망월 29.5271일, 일평균 13.1762°
  기준 시각 = 12:00 KST(=03:00 UTC)
- SIGN_META는 [0]=물병 시작이므로 `sIdx=(floor(lon/30)+2)%12` (황경 0°=양자리=index 2)
- 신설 UI: 달 뱃지·아스펙트명+근거·지수100·분야점수바·길잡이·달이 내 자리 오는 날·주간 7일·내일
- **3언어 전부 작성 필요** (아스펙트 7 × 8문장 × 3언어)

### ttirank — 실제 명리 방식
**오늘 일진의 지지 × 각 띠(지지) 관계**로 12띠 순위 산출
- 삼합+26 / 육합+22 / 같음(비화)+12 / 파-8 / 해-12 / 형-14 / 충-20
- 동점 해소 = 일간 오행 vs 띠 지지 오행 생극(+8/+5/+3/-4/-6)
- 각 순위행에 관계 뱃지 + 근거 한 줄 → "막힘없이 트이는 하루" 대신 "오늘 일진 午와 삼합"
- 내 띠 상세: 지수·관계설명·잘맞는띠/조심할띠·좋은시간·방위·주간7일·내일순위

## 진행 상황 — 완료
- **zodiac 완료** — 트랜짓 엔진 + 3언어 + 신규 UI + 공유카드 + SEO · `zodiac_deep_check.mjs` ALL PASS
- **ttirank 완료** — 일진×지지 관계 엔진(난수 0) + 신규 UI + 공유카드 + SEO · `ttirank_deep_check.mjs` ALL PASS
- `errcheck8176.mjs` 34종 pageerror 0 · CLAUDE.md changelog 기록 · 커밋/푸시

## 이전 완료 (pushed)
unse 십성 엔진(81d826e) / AI 배경 36개 / A~E 개편 / 파비콘(cd4299e) / tstory 제외(18881e2)
git push: `.env`의 GITHUB_TOKEN → `git push "https://x-access-token:${TOKEN}@github.com/..." master:main`
