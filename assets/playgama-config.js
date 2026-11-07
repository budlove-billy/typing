/* Playgama 파트너 연동 설정 — 켜고 끄는 곳은 이 파일 하나뿐이다. (docs/playgama-plan.md)
   - enabled=false 이거나 clid가 비어 있으면 허브(/arcade/)의 게임 목록과 홈 진입 카드가 그려지지 않는다.
   - 게임 하나를 내릴 때(Playgama 요청 시 즉시): 그 항목의 "enabled"를 false로 바꾸거나 지운다.
   - "url"은 Playgama 대시보드(widgets.playgama.com)의 게임 카드에서 복사한 iframe src를 그대로 넣는다(clid 포함).
     지금 들어 있는 값은 공개 export 주소(수익 추적 없음)라 오픈 전에 반드시 바꿔야 한다 — tools/playgama/check.mjs가 경고한다.
   - 값을 바꾼 뒤: python tools/playgama/build.py (허브 HTML·사이트맵·llms.txt·개인정보처리방침 반영) → 품질 검사 → 배포.
   - 아래 CONFIG 표시와 END 표시 사이는 엄격한 JSON이어야 한다(빌드 스크립트가 읽는다). */
window.PLAYGAMA = /*CONFIG*/{
  "enabled": false,
  "clid": "",
  "homeEntry": true,
  "games": [
    {"id": "fruit-merge", "enabled": true, "url": "https://playgama.com/export/game/fruit-merge-playgama", "thumb": "https://static.playgama.com/p-img/pg/fruit-merge-playgama/big_preview/f88e2107d6554e668566d486ba0518a4?width=480"},
    {"id": "bubble-blast", "enabled": true, "url": "https://playgama.com/export/game/bubble-blast", "thumb": "https://static.playgama.com/p-img/pg/bubble-blast/big-preview/48be0e1ca5354daa8378d69daea53114?width=480"},
    {"id": "mahjong-lines", "enabled": true, "url": "https://playgama.com/export/game/mahjong-lines", "thumb": "https://static.playgama.com/p-img/pg/mahjong-lines/big_preview/96269817997541b48d15ed462ff66d47?width=480"},
    {"id": "find-the-frog", "enabled": true, "url": "https://playgama.com/export/game/find-the-frog--hidden-objects", "thumb": "https://static.playgama.com/p-img/pg/find-the-frog--hidden-objects/big_preview/541792f4c5354ef88be0646eb9be4b1b?width=480"},
    {"id": "good-sort", "enabled": true, "url": "https://playgama.com/export/game/good-sort-master", "thumb": "https://static.playgama.com/p-img/pg/good-sort-master/big-preview/87153c5702e14ce994b208df2c0a5f61?width=480"},
    {"id": "vega-mix", "enabled": true, "url": "https://playgama.com/export/game/vega-mix-2-adventure", "thumb": "https://static.playgama.com/p-img/pg/vega-mix-2-adventure/big-preview/46f5bcaca15b411382afc96ac1c38132?width=480"},
    {"id": "wood-blocks", "enabled": true, "url": "https://playgama.com/export/game/wood-blocks-jam", "thumb": "https://static.playgama.com/p-img/pg/wood-blocks-jam/big-preview/f8a46a136d1043fd8ab89994b49ec933?width=480"},
    {"id": "jigsaw", "enabled": true, "url": "https://playgama.com/export/game/favorite-puzzles", "thumb": "https://static.playgama.com/p-img/pg/favorite-puzzles/big_preview/400025cc8973444fac031e1cb75faf61?width=480"}
  ]
}/*END*/;
