# Active Session State

## Current task
코드 전체 분석 (사용자 요청 4가지 축):
1. 대시보드(홈) 구성
2. 게임 구성 및 연결 구조
3. 게임 퀄리티 (그래픽 상용 업그레이드 + 사운드 보강 목표)
4. 랭킹 및 브레인 점수 구조 (게임 45종이라 개선 필요)

## Key facts gathered
- index.html = brain_app.html (바이트 동일, 780KB 단일 HTML SPA, 서버 없음)
- HOME_GAMES 45개 항목 (index.html:7282): 아케이드 34 + external 9(moamoa/queens/tango/unse/zodiac/ttirank/tarot/persona/suneung/newyear) + braintype + run
- 스크린 44개 div.screen, i18n 키 ~701개 (ko/en/th)
- 홈 구조: home-feature(미션 다음 게임) + 오늘의 목표(streak/plays/records) + home-cats(카테고리 칩) + home-popular(큐레이션 iq/sudoku/braintype 하드코딩) + home-fun(운세) + home-about + site-footer
- 게임 패턴: intro/game/result 3카드, 상태객체 2글자(FM/HC/ST/TR...), best=brain.<id>.best {easy|normal|hard:{all,day,date}}
- 사운드: WebAudio 단일 _beep() (osc sine/square 2종), sfx('good'|'bad'|'win') 3종뿐, good 30지점/bad 28/win 9. 파일 사운드 없음.
- FX: fxBurst/fxConfetti/fxScorePop/fxCombo/celebrateRecordScreen (DOM+WAAPI, 파티클 잘 되어 있음)
- 점수 구조: ABILITY_MAP(7축 가중치) + GAME_REF(레벨100 기준값) + gameLevel=best/ref*100 + abilityScores(핸 게임만 가중평균) + overallLevel(전체 평균, 안 한 게임=0)
- 랭킹: 서버 없어서 **없음** (localStorage만). 내 기록 탭 = 개인 기록/능력치 레이더/백업.
- 도전장: ?c=game.score.diff URL 챌린지 (친구 1:1)
- 미션: 날짜시드 A/B/C 풀에서 3개, missionMark 공통 훅 (GA game_finish + chCheck + renderRecs)

## Decisions
(분석 결과를 사용자에게 보고 예정 — 그래픽/사운드 업그레이드와 점수 개선 제안 포함)

## Files in progress
- D:\claude\brain\index.html (읽기 분석 중, 수정 없음)

## Open questions
- 랭킹: 서버 도입 의사 있는가? (Supabase 슬롯 문제로 보류 이력 있음 — MEMORY.md 2026-07-10)
- 그래픽 업그레이드 범위: 전 게임 공통 품질 리프트 vs 상위 인기 게임 집중?
- 사운드: WebAudio 합성 유지 보강 vs 사운드 파일(묶음) 도입?
