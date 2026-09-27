/* ===== 공통 상단바 (2026-09-28) — 오늘의 퍼즐·운세 페이지에서 </header> 바로 뒤에 불러 첫 화면이 그려지기 전에 만든다(화면 밀림 없음).
   ← 홈 · 말로우 로고 · Mallow · 페이지 이름 · (소리) · (언어). 기존 #backHome·#muteBtn·#langSel은 그대로 옮겨 쓴다(id·기능 유지). ===== */
(function(){
  var head=document.querySelector('header'); if(!head || document.querySelector('.mtop')) return;
  var slug=(location.pathname.split('/').filter(Boolean)[0]||'');
  var NAMES={   // index.html의 nav.<id> 이름과 같게
    moamoa:{ko:'모아모아',en:'Moamoa',th:'โมอาโมอา'}, queens:{ko:'말로우 크라운',en:'Mallow Crown',th:'มาโลว์คราวน์'}, tango:{ko:'말로우 탱고',en:'Mallow Tango',th:'มาโลว์แทงโก้'},
    unse:{ko:'오늘의 운세',en:'Fortune',th:'ดวงวันนี้'}, zodiac:{ko:'별자리 운세',en:'Horoscope',th:'ดวงราศี'}, ttirank:{ko:'띠별 운세',en:'Zodiac Rank',th:'อันดับนักษัตร'},
    tarot:{ko:'타로 점',en:'Tarot',th:'ไพ่ทาโรต์'}, luckycolor:{ko:'태국 행운색',en:'Lucky Colour',th:'สีมงคลวันเกิด'}, persona:{ko:'성격 유형 진단',en:'Persona Type',th:'บุคลิกภาพ'}};
  var HOME={ko:'홈',en:'Home',th:'หน้าแรก'};
  function lang(){ var l=(document.documentElement.lang||'ko').slice(0,2); return HOME[l]?l:'ko'; }
  var nav=document.createElement('nav'); nav.className='mtop';
  var back=document.getElementById('backHome');
  if(!back){ back=document.createElement('a'); back.id='backHome'; back.href='/'; }
  var lbl=back.querySelector('#t-home');   // 페이지가 언어 전환 때 직접 바꾸는 글자는 그대로 둔다
  if(!lbl){ lbl=document.createElement('span'); lbl.className='mtop-home'; }
  back.textContent=''; var x=document.createElement('span'); x.className='mtop-x'; x.textContent='←';
  back.appendChild(x); back.appendChild(document.createTextNode(' ')); back.appendChild(lbl);
  back.setAttribute('aria-label','Mallow home');
  var logo=document.createElement('a'); logo.className='mtop-logo'; logo.href='/';
  logo.innerHTML='<img src="/assets/mallow-mint.svg" alt="" width="32" height="32"><span class="mtop-brand">Mallow</span><span class="mtop-name"></span>';
  var right=document.createElement('div'); right.className='mtop-right';
  ['muteBtn','langSel'].forEach(function(id){ var e=document.getElementById(id); if(e){ e.removeAttribute('style'); right.appendChild(e); } });
  nav.appendChild(back); nav.appendChild(logo); nav.appendChild(right);
  head.parentNode.insertBefore(nav, head);
  function paint(){ var l=lang(); var n=NAMES[slug]; logo.querySelector('.mtop-name').textContent=n?(n[l]||n.ko):'';
    if(lbl.className==='mtop-home') lbl.textContent=HOME[l]; }
  paint();
  try{ new MutationObserver(paint).observe(document.documentElement,{attributes:true,attributeFilter:['lang']}); }catch(e){}
})();
