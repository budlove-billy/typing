# Active Session State

## Current task
운세 고도화 — `/unse/` 십성(十星) 기반 상세 운세 엔진으로 교체. 구현·검증 완료, 커밋 대기.

## 이번 작업 (unse/index.html 단일 파일)
**문제**: 총운 별점·분야 등급이 전부 독립 난수 → 근거 없음. 각 항목 1문장 = 라이트.
**해결**: 이미 계산 중이던 일주(60갑자)를 활용 → 오늘 일진 × 내 일간 = 십성 관계로 산출.
- `sipsungOf(meIdx,tIdx)` — 오행 생극(eGen/eKe/eGenBy) + 음양 동/이로 10종 판별
- `SIP` 10종 프로필(base 48~80, 분야 가중치 w, total 2종, did/avoid, 분야별 렌즈 4문장)
- `branchRel` 삼합(+8)/육합(+6)/같음(+4)/충(-10)/none + `BREL` 해설
- `dayFortune()` = base + 지지보정 + ±6 → 28~96 지수, `starOf()` 별점
- 신설 UI: 일진 뱃지·십성명·지수 100점·분야별 점수바·길잡이(할것/피할것)·좋은시간/조심시간/방위/도움띠·주간 7일 막대·내일 미리보기
- 공유카드에 십성 뱃지+지수 추가(세로 좌표 재배치, URL 704 < 카드바닥 720)
- SEO 카드 2개 신설(일진·십성 설명 / 결과 항목) + FAQ 1문 + JSON-LD·meta 갱신

## 검증
- `.logs/unse_deep_check.mjs` ALL PASS: 일주 앵커 3케이스(1900-01-01 갑술/2000-01-01 무오/1900-01-31 갑진), 갑·을 일간 십성 표준 대조, 오행 생극 3표, 지지관계 5종, 200명 지수 34~90·십성 10종 분포, 1인 30일 십성 10종 변화, 렌더 전 항목, 결정성(같은입력=같은결과), 390/320px 넘침 0, 공유카드 생성
- `.logs/errcheck8176.mjs` 34종 pageerror 0
- 정적서버: **포트 8176** (python http.server, detached)

## 남은 것
- MEMORY.md/CLAUDE.md 체인지로그 추가 → git commit & push

## 이전 완료 (pushed)
AI 배경 36개 자산 / A~E 기능개편 / 파비콘 투명화(cd4299e) / tstory 추적 제외(18881e2)
git push: `.env`의 GITHUB_TOKEN → `git push "https://x-access-token:${TOKEN}@github.com/..." master:main`
