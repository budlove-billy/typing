/* 게임판 아래 장문 소개를 기본 접힘으로 유지한다. 원본 문서는 DOM에 보존한다. */
(function(){
  'use strict';
  var copy={
    ko:{closed:'게임 설명 보기',open:'게임 설명 접기'},
    en:{closed:'About this game',open:'Hide game details'},
    th:{closed:'ดูรายละเอียดเกม',open:'ซ่อนรายละเอียดเกม'}
  };
  function language(){var l=(document.documentElement.lang||'ko').toLowerCase().slice(0,2);return copy[l]?l:'ko';}
  function label(details){var text=copy[language()][details.open?'open':'closed'];var summary=details.querySelector('summary');if(summary)summary.textContent=text;}
  function fold(container,nodes){
    if(!nodes.length||container.dataset.seoFolded)return;
    container.dataset.seoFolded='true';
    var details=document.createElement('details'), summary=document.createElement('summary'), body=document.createElement('div'), anchor=nodes[0];
    details.className='seo-fold'; summary.className='seo-fold-summary'; body.className='seo-fold-body';
    container.insertBefore(details,anchor);
    nodes.forEach(function(node){body.appendChild(node);});
    details.appendChild(summary);details.appendChild(body);
    details.addEventListener('toggle',function(){label(details);}); label(details);
  }
  function init(){
    var seo=[].slice.call(document.querySelectorAll('section.seo'));
    if(seo.length){seo.forEach(function(section){fold(section,[].slice.call(section.childNodes));});return;}
    var main=document.querySelector('main');
    if(!main)return;
    fold(main,[].slice.call(main.children).filter(function(el){return el.tagName==='SECTION';}));
  }
  function installStyle(){
    if(document.getElementById('seo-fold-style'))return;
    var style=document.createElement('style');style.id='seo-fold-style';style.textContent='.seo-fold{display:block;border:1px solid rgba(139,111,240,.24);border-radius:18px;background:rgba(255,255,255,.78);overflow:hidden;margin-bottom:1rem}.seo-fold-summary{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:16px 18px;color:#7e62df;font-size:15px;font-weight:800;cursor:pointer;list-style:none;user-select:none}.seo-fold-summary::-webkit-details-marker{display:none}.seo-fold-summary::after{content:"▼";font-size:12px;transition:transform .18s ease}.seo-fold[open] .seo-fold-summary{border-bottom:1px solid rgba(139,111,240,.18)}.seo-fold[open] .seo-fold-summary::after{transform:rotate(180deg)}.seo-fold-body{padding:0 0 2px}.seo-fold-body>.card{margin:12px}.seo-fold-body>.card:last-child{margin-bottom:14px}@media(max-width:420px){.seo-fold-summary{padding:14px 15px;font-size:14px}.seo-fold-body>.card{margin:10px}}';document.head.appendChild(style);
  }
  installStyle();init();
  new MutationObserver(function(){document.querySelectorAll('.seo-fold').forEach(label);}).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
})();
