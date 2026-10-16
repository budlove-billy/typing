# -*- coding: utf-8 -*-
"""홈 로비에 Hi5Games(앱테크 게임) 앱 다운로드 배너 (2026-10-02 사용자 요청, 기간: 오늘 ~ 2026-11-30 KST).
- 위치: '오늘의 퍼즐' 아래, '오늘의 운세' 위. 한국어 화면에서만(스토어 링크가 한국 스토어).
- 이미지가 아니라 HTML로 그린다(글자가 선명하고 검색에 읽힌다). '광고' 표기(표시·광고법), rel="sponsored".
- 표시 여부는 배너 바로 뒤 인라인 스크립트가 그리는 순간 정한다 → 레이아웃 흔들림(CLS) 없음. 언어를 바꾸면 renderHome이 다시 정한다.
- 기간이 지나면 저절로 숨는다(HI5_END). 클릭은 GA 이벤트 hi5_click으로 센다.
- 끝난 뒤 지우려면: index.html에서 <!--hi5--> ~ <!--/hi5--> 블록과 CSS의 /* hi5 */ 블록, renderHome의 hi5Show() 한 줄을 지운다."""
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'daily-redesign')); from _patch import Patch
p = Patch(os.path.join(os.path.dirname(__file__), '..', '..', 'index.html')); R = p.R

PLAY = 'https://play.google.com/store/apps/details?id=com.tinycell.hi5games.aos'
IOS = 'https://apps.apple.com/kr/app/id6760527702'

R('.lb-h2 small,.lb-more{', '''/* hi5 — Hi5Games 앱 배너(~2026-11-30) */
.hi5{position:relative;display:none;margin:1.3rem 0 .2rem;padding:1.05rem 1.1rem 1.1rem;border-radius:20px;overflow:hidden;color:#fff;
  background:radial-gradient(120% 140% at 100% 0%,#6d3cf0 0%,#3b1d9a 45%,#1a1046 100%);border:1px solid rgba(160,130,255,.45);box-shadow:0 10px 26px rgba(20,8,60,.45)}
.hi5.on{display:block}
.hi5-ad{position:absolute;top:.7rem;right:.8rem;font-size:.68rem;font-weight:800;color:#d9d0ff;border:1px solid rgba(217,208,255,.5);border-radius:6px;padding:.05rem .35rem;letter-spacing:.02em}
.hi5-top{display:flex;align-items:center;gap:.85rem}
.hi5-hp{flex-shrink:0;width:64px;height:64px;filter:drop-shadow(0 4px 8px rgba(0,0,0,.35))}
.hi5-kw{display:inline-block;font-size:.74rem;font-weight:800;color:#5ef2c8;background:rgba(94,242,200,.12);border:1px solid rgba(94,242,200,.35);border-radius:999px;padding:.12rem .55rem;margin-bottom:.3rem}
.hi5-t{margin:0;font-size:1.12rem;font-weight:900;line-height:1.35;letter-spacing:-.02em}
.hi5-t em{font-style:normal;color:#5ef2c8}
.hi5-d{margin:.55rem 0 .8rem;font-size:.9rem;line-height:1.6;color:#e6e0ff}
.hi5-btns{display:flex;gap:.55rem}
.hi5-b{flex:1;display:flex;align-items:center;justify-content:center;gap:.45rem;min-height:48px;padding:.4rem .6rem;border-radius:13px;text-decoration:none;color:#fff;
  background:linear-gradient(180deg,#7b4dff,#5a2fe0);border:1.5px solid #5ef2c8;box-shadow:0 3px 0 rgba(0,0,0,.3)}
.hi5-b:active{transform:translateY(2px);box-shadow:0 1px 0 rgba(0,0,0,.3)}
.hi5-b svg{width:20px;height:20px;flex-shrink:0}
.hi5-b span{display:flex;flex-direction:column;line-height:1.15;text-align:left}
.hi5-b small{font-size:.66rem;font-weight:600;color:#e6e0ff}
.hi5-b b{font-size:.98rem;font-weight:800;white-space:nowrap}
@media (max-width:360px){.hi5-hp{width:52px;height:52px}.hi5-t{font-size:1.02rem}.hi5-b{gap:.35rem;padding:.4rem .4rem}.hi5-b b{font-size:.86rem}.hi5-b svg{width:17px;height:17px}}
.lb-h2 small,.lb-more{''')

R('''  <p class="lb-count" id="lb-count">&nbsp;</p>
''', f'''  <p class="lb-count" id="lb-count">&nbsp;</p>
  <!--hi5--><aside class="hi5" id="hi5" aria-label="광고: Hi5Games 앱테크 게임">
    <span class="hi5-ad">광고</span>
    <div class="hi5-top">
      <svg class="hi5-hp" viewBox="0 0 64 64" aria-hidden="true"><defs><linearGradient id="hi5g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a98bff"/><stop offset="1" stop-color="#6a3cf5"/></linearGradient></defs>
        <path d="M32 3 L57 17.5 V46.5 L32 61 L7 46.5 V17.5 Z" fill="#3a1fa8" stroke="#c9b8ff" stroke-width="2.5" stroke-linejoin="round"/>
        <path d="M32 9 L52 20.5 V43.5 L32 55 L12 43.5 V20.5 Z" fill="url(#hi5g)"/>
        <text x="32" y="40.5" text-anchor="middle" font-size="20" font-weight="900" fill="#fff" font-family="system-ui,sans-serif" stroke="#3a1fa8" stroke-width=".8">HP</text></svg>
      <div><span class="hi5-kw">앱테크 게임 · Hi5Games</span>
        <p class="hi5-t">게임하고 모은 <em>HP</em>를<br>상품권으로 바꿔 쓰세요</p></div>
    </div>
    <p class="hi5-d">Hi5Games에서 게임 미션을 깨면 HP 포인트가 쌓여요. 모은 HP는 상품권으로 교환해 편의점·커피숍 등에서 쓸 수 있어요.</p>
    <div class="hi5-btns">
      <a class="hi5-b" href="{PLAY}" target="_blank" rel="sponsored noopener" onclick="hi5Click('android')"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 2.5 L13.6 12 L4 21.5 Z" fill="#34d399"/><path d="M4 2.5 L16.9 9.4 L13.6 12 Z" fill="#60a5fa"/><path d="M4 21.5 L16.9 14.6 L13.6 12 Z" fill="#f87171"/><path d="M16.9 9.4 L21 12 L16.9 14.6 L13.6 12 Z" fill="#fbbf24"/></svg><span><small>다운로드하기</small><b>Google Play</b></span></a>
      <a class="hi5-b" href="{IOS}" target="_blank" rel="sponsored noopener" onclick="hi5Click('ios')"><svg viewBox="0 0 24 24" aria-hidden="true" fill="#fff"><path d="M16.4 12.6c0-2.3 1.9-3.4 2-3.5-1.1-1.6-2.8-1.8-3.4-1.8-1.4-.1-2.8.9-3.5.9s-1.8-.8-3-.8C7 7.4 5.5 8.3 4.7 9.8c-1.6 2.8-.4 7 1.2 9.3.8 1.1 1.7 2.4 2.9 2.3 1.2 0 1.6-.7 3-.7s1.8.7 3 .7c1.3 0 2.1-1.1 2.8-2.3.9-1.3 1.3-2.6 1.3-2.6s-2.5-1-2.5-3.9zM14.2 5.8c.6-.8 1.1-1.9 1-3-.9 0-2.1.6-2.7 1.4-.6.7-1.1 1.8-1 2.9 1 .1 2.1-.5 2.7-1.3z"/></svg><span><small>다운로드하기</small><b>App Store</b></span></a>
    </div>
  </aside>
  <script>
  /* Hi5Games 배너: 한국어 화면 + 2026-11-30(KST)까지만. 그리는 순간 정해서 화면이 밀리지 않게 한다. */
  var HI5_END='2026-11-30';
  function hi5Show(){{ var el=document.getElementById('hi5'); if(!el) return;
    var lang=(typeof CURRENT_LANG!=='undefined'&&CURRENT_LANG)||new URLSearchParams(location.search).get('lang')||'';   // 앱 언어 > 주소 ?lang > 저장된 언어
    if(!lang){{ try{{ lang=localStorage.getItem('brain.lang')||''; }}catch(e){{}} }}
    var kst=new Date(Date.now()+9*3600e3).toISOString().slice(0,10);
    el.classList.toggle('on', (lang===''||lang==='ko') && kst<=HI5_END); }}
  function hi5Click(store){{ try{{ gtag('event','hi5_click',{{store:store}}); }}catch(e){{}} }}
  hi5Show();
  </script><!--/hi5-->
''')

R('''function renderHome(){
  const v=homeVisit(), ms=lbMission();''', '''function renderHome(){
  try{ hi5Show(); }catch(e){}   // Hi5Games 배너(한국어·기간 한정)
  const v=homeVisit(), ms=lbMission();''')
p.save()
