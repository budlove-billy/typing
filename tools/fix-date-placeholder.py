# -*- coding: utf-8 -*-
"""<input type="date">의 빈 상태 표기가 페이지 언어를 따르게 만든다.

문제: 빈 date 입력의 'yyyy-mm-dd' 자리 표시는 브라우저가 그리는 네이티브 UI라서
      페이지의 placeholder/lang이 아니라 '브라우저 UI 언어'를 따른다.
      그래서 크롬 UI가 한국어인 사람이 영어판을 보면 '연도-월-일'이 뜬다.
해결: 값이 비었고 포커스도 없을 때만 네이티브 편집 텍스트를 투명하게 만들고,
      그 자리에 페이지 언어에 맞는 힌트를 겹쳐 보여준다. 포커스하면 원래 위젯이 보인다.
      ::-webkit-datetime-edit를 지원하지 않는 브라우저에서는 아무것도 하지 않는다(겹침 방지).
"""
import io, os, re

PH = {'ko': '연도-월-일', 'en': 'YYYY-MM-DD', 'th': 'ปปปป-ดด-วว'}

CSS = """
/* ===== date 입력의 빈 상태 표기를 페이지 언어에 맞춘다 =====
   네이티브 자리표시는 브라우저 UI 언어를 따라가므로(영어판에 '연도-월-일'이 뜨던 원인)
   비어 있을 때만 가리고 힌트를 겹쳐 준다. 포커스하면 원래 위젯이 그대로 보인다. */
.dfield{position:relative;}
.dfield .dhint{position:absolute;left:13.5px;top:50%;transform:translateY(-50%);
  font-size:16px;color:#9a92b3;pointer-events:none;display:none;font-family:inherit;}
.dfield.ph-on .dhint{display:block;}
.dfield.ph-on input[type=date]::-webkit-datetime-edit{color:transparent;}
"""

JS = """
/* date 입력 자리표시를 페이지 언어로 — 위 CSS 주석 참고 */
const DATE_PH={ko:'%(ko)s',en:'%(en)s',th:'%(th)s'};
function syncDatePlaceholder(){
  const el=document.getElementById('birth'); if(!el) return;
  const wrap=el.closest('.dfield'); if(!wrap) return;
  const hint=wrap.querySelector('.dhint'); if(hint) hint.textContent=DATE_PH[LANG]||DATE_PH.ko;
  /* 유사요소를 지원하지 않는 브라우저(파이어폭스 등)에서는 네이티브 표기를 가릴 수 없어
     힌트가 겹쳐 보이므로 아예 켜지 않는다. */
  const supported=(window.CSS&&CSS.supports&&CSS.supports('selector(::-webkit-datetime-edit)'));
  const empty=!el.value && document.activeElement!==el;
  wrap.classList.toggle('ph-on', !!supported && empty);
}
(function(){
  const el=document.getElementById('birth'); if(!el) return;
  ['input','change','focus','blur'].forEach(function(ev){ el.addEventListener(ev, syncDatePlaceholder); });
})();
"""


def patch(page):
    f = os.path.join(page, 'index.html')
    s = io.open(f, encoding='utf-8', newline='').read()
    assert 'syncDatePlaceholder' not in s, page + ' 이미 적용됨'

    # 1) CSS — date input 규칙 바로 뒤에 붙인다
    m = re.search(r'^input\[type=date\][^\n]*\n', s, re.M)
    assert m, page + ' input[type=date] 규칙 없음'
    s = s[:m.end()] + CSS.strip('\n') + '\n' + s[m.end():]

    # 2) HTML — input을 래퍼로 감싸고 힌트 span 추가
    old = '<input type="date" id="birth" min="1900-01-01">'
    assert s.count(old) == 1, page
    s = s.replace(old,
                  '<div class="dfield"><input type="date" id="birth" min="1900-01-01">'
                  '<span class="dhint" aria-hidden="true"></span></div>', 1)

    # 3) JS — applyLang 앞에 정의하고, applyLang 끝에서 호출되도록 감싼다
    m = re.search(r'^function applyLang\(', s, re.M)
    assert m, page + ' applyLang 없음'
    s = s[:m.start()] + (JS % PH).strip('\n') + '\n' + s[m.start():]

    # applyLang이 끝날 때마다 자리표시도 갱신 (초기 렌더·언어 전환 양쪽)
    anchor = "(function(){ const _a=applyLang; applyLang=function(){ const r=_a.apply(this,arguments); syncSEO(); return r; }; })();"
    assert anchor in s, page + ' syncSEO 래퍼 없음'
    s = s.replace(anchor,
                  "(function(){ const _a=applyLang; applyLang=function(){ const r=_a.apply(this,arguments); syncSEO(); syncDatePlaceholder(); return r; }; })();", 1)

    io.open(f, 'w', encoding='utf-8', newline='').write(s)
    print('ok', page)


for p in ['zodiac', 'luckycolor']:
    patch(p)
