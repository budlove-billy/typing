# Active Session State

## Current task
완료 — AI 배경 전면 적용 (인앱 34종 게임 + 홈 + 신기록 = 36개 자산) 모두 배포

## 최종 완료 (all pushed, latest 4a435ea)
- **AI 배경 34종 완성**: 모든 인앱 아케이드 게임 플레이 배경 AI 이미지화
  (c36a398~c96ccea 일련 커밋, 각 3종씩). rev/run이 마지막.
- **git push 파이프라인 확립**: .env의 GITHUB_TOKEN(Fine-grained PAT, Contents RW)
  → `git push "https://x-access-token:${TOKEN}@github.com/..." master:main`
- **MEMORY/CLAUDE 문서화 완료** (4a435ea)

## 누적 전체 작업 (이 세션)
1. A~E 기능개편: 사운드12종/능력치10축+등급/홈데일리+개인화/등급진행/전환연출
2. 씬 SVG: 전체 34종 인트로 장식
3. AI 배경: 34종 게임 + 홈 히어로 + 신기록 = 36개
4. 인원수세기 캐릭터 위치 수정
5. git push 토큰 설정

## Key facts
- AI 배경 파이프라인: __media__(gpt-image-2-t2i) → generated_images → PIL(900px, q82)
  → assets/<id>-bg.jpg → CSS #<id>-game-card에 오버레이 배경
- 신기록: bt_recordScore → markRecordCard() → is-record 클래스
- 검증: .logs/errcheck.mjs (BASE=8156, ALL 34 CLEAN)
- 정적 서버: 포트 8156 (python http.server, detached)

## 후속 후보
- 애드센스 (pub-id 대기)
- GA 데이터 기반 콘텐츠/최적화
- 외부 정적 페이지(queens/tango/운세류)에도 배경 적용 가능
