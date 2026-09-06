/* SEO 랜딩 공통 측정 — 검색어 자체는 네이버에서 전달되지 않으므로
   랜딩 페이지·내부 이동·도구 완료 흐름을 익명 이벤트로 측정한다. */
(function(){
  'use strict';
  if(typeof window==='undefined') return;
  const page=(location.pathname||'/').replace(/\/index\.html$/,'/')||'/';
  const qs=new URLSearchParams(location.search||'');
  const context=qs.get('from')||'';
  function send(name,params){
    try{
      if(typeof window.gtag==='function') window.gtag('event',name,Object.assign({seo_page:page},params||{}));
    }catch(e){}
  }
  window.mallowSeoTrack=send;
  send('seo_landing_view',{entry_context:context||'direct',lang:document.documentElement.lang||'ko'});

  document.addEventListener('click',function(ev){
    const a=ev.target&&ev.target.closest?ev.target.closest('a[href]'):null;
    if(!a) return;
    const raw=a.getAttribute('href')||'';
    if(!raw || raw[0]!=='/' || raw.indexOf('//')===1) return;
    let url; try{ url=new URL(raw,location.origin); }catch(e){ return; }
    const target=(url.pathname||'/').replace(/\/index\.html$/,'/')||'/';
    if(target===page && !url.search) return;
    send('seo_cta_click',{
      target_path:target,
      target_query:url.search.slice(0,120),
      link_role:a.dataset.seoRole||'internal_link',
      anchor_text:(a.textContent||'').replace(/\s+/g,' ').trim().slice(0,80)
    });
  },{passive:true});

  const seenKey='mallow.seo.lastSeen';
  let previous=0;
  try{ previous=Number(localStorage.getItem(seenKey)||0); localStorage.setItem(seenKey,String(Date.now())); }catch(e){}
  if(previous && Date.now()-previous>86400000){
    send('seo_return_session',{days_since_last:Math.min(30,Math.floor((Date.now()-previous)/86400000))});
  }
})();
