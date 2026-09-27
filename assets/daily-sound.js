/* ===== 오늘의 퍼즐 사운드 (모아모아·말로우 크라운·말로우 탱고 공용, 2026-09-28) =====
   index.html 사운드 엔진 v2(tools/sound/engine.js)의 축약판 — 같은 음색·같은 믹스 체인·같은 음량 키.
   효과음 버스(리버브 센드) + 음악 버스 → 컴프레서 → 리미터. 음원 파일 없이 합성.
   켜기/끄기: brain.sound(메인 사이트) + mallow_mute(퍼즐 페이지 예전 키) 둘 다 읽고 쓴다.
   음량: brain.vol.sfx / brain.vol.music (0~1) — 메인 사이트 음량 패널과 공유.
   사용: DS.play('crown', n) · DS.bgm('royal') · DS.level(0~2) · DS.stop() · DS.panel(btn) */
(function(){
'use strict';
let AC=null, AM=null, NZ=null;
function on(){ try{ return localStorage.getItem('brain.sound')!=='off' && localStorage.getItem('mallow_mute')!=='1'; }catch(e){ return true; } }
function vol(k){ try{ const v=parseFloat(localStorage.getItem('brain.vol.'+k)); if(!isNaN(v)) return Math.max(0,Math.min(1,v)); }catch(e){} return k==='music'?0.6:0.85; }
function ac(){
  if(!AC){ try{ AC=new (window.AudioContext||window.webkitAudioContext)(); }catch(e){ return null; } }
  if(AC.state==='suspended') AC.resume();
  if(!AM){ const A=AC;
    const comp=A.createDynamicsCompressor(); comp.threshold.value=-18; comp.knee.value=12; comp.ratio.value=4; comp.attack.value=0.003; comp.release.value=0.18;
    const lim=A.createDynamicsCompressor(); lim.threshold.value=-2; lim.ratio.value=20; lim.attack.value=0.001; lim.release.value=0.05;
    comp.connect(lim); lim.connect(A.destination);
    const verb=A.createConvolver(), len=Math.floor(A.sampleRate*1.6), ir=A.createBuffer(2,len,A.sampleRate);
    for(let c=0;c<2;c++){ const d=ir.getChannelData(c); for(let i=0;i<len;i++) d[i]=(Math.random()*2-1)*Math.pow(1-i/len,3); }
    verb.buffer=ir; const vg=A.createGain(); vg.gain.value=0.24; verb.connect(vg); vg.connect(comp);
    const sfx=A.createGain(), mus=A.createGain(), ms=A.createGain();
    sfx.connect(comp); sfx.connect(verb); mus.connect(comp); ms.gain.value=0.45; mus.connect(ms); ms.connect(verb);
    AM={sfx,mus}; applyVol(); }
  return AC;
}
function applyVol(){ if(!AM) return; const t=AC.currentTime;
  AM.sfx.gain.setTargetAtTime(vol('sfx')*1.1,t,0.05); AM.mus.gain.setTargetAtTime(vol('music')*0.17,t,0.05); }   // 음악은 효과음보다 6dB 이상 아래(메인 엔진과 같은 비)

/* ---- 음색 ---- */
function nz(){ if(NZ) return NZ; const b=AC.createBuffer(1,AC.sampleRate,AC.sampleRate), d=b.getChannelData(0); for(let i=0;i<d.length;i++) d[i]=Math.random()*2-1; return NZ=b; }
const J=(v,p)=>v*(1+(Math.random()*2-1)*(p==null?0.03:p));   // 같은 소리 반복의 기계감 줄이기
function env(g,t,a,peak,dec){ g.gain.setValueAtTime(0.0001,t); g.gain.linearRampToValueAtTime(peak,t+a); g.gain.exponentialRampToValueAtTime(0.0001,t+a+dec); }
function osc(type,f,t,dur,peak,dest,o){ o=o||{}; const x=AC.createOscillator(), g=AC.createGain(); x.type=type; x.frequency.setValueAtTime(f,t);
  if(o.glide) x.frequency.exponentialRampToValueAtTime(Math.max(20,f+o.glide),t+dur); if(o.det) x.detune.value=o.det;
  env(g,t,o.a||0.004,peak,dur); x.connect(g); g.connect(dest); x.start(t); x.stop(t+(o.a||0.004)+dur+0.05); }
function hit(t,v,dest,freq,dec,type){ const s=AC.createBufferSource(); s.buffer=nz(); const f=AC.createBiquadFilter(); f.type=type||'highpass'; f.frequency.value=freq; const g=AC.createGain(); env(g,t,0.001,v,dec); s.connect(f); f.connect(g); g.connect(dest); s.start(t, Math.random()*0.5); s.stop(t+dec+0.05); }
const T=dt=>AC.currentTime+(dt||0);
const SV={
  pluck(f,dt,v,dest){ const t=T(dt); dest=dest||AM.sfx; v=v==null?0.34:v; const f0=J(f,0.004);
    const lp=AC.createBiquadFilter(); lp.type='lowpass'; lp.Q.value=4; lp.frequency.setValueAtTime(f0*9,t); lp.frequency.exponentialRampToValueAtTime(f0*1.5,t+0.25); lp.connect(dest);
    osc('sawtooth',f0,t,0.32,v*0.5,lp); osc('triangle',f0*2,t,0.18,v*0.35,lp); osc('sine',f0/2,t,0.2,v*0.4,dest); },
  harp(f,dt,v,dest){ const t=T(dt); dest=dest||AM.sfx; v=v==null?0.26:v; osc('triangle',J(f,0.003),t,0.9,v,dest,{a:0.003}); osc('sine',f*2,t,0.5,v*0.3,dest,{a:0.003}); },
  bell(f,dt,v,dest){ const t=T(dt); dest=dest||AM.sfx; v=v==null?0.22:v; [1,2.76,5.4].forEach((r,i)=>osc('sine',f*r,t,[1.1,0.6,0.3][i],v*[1,0.4,0.2][i],dest)); },
  kick(dt,v,dest){ const t=T(dt); dest=dest||AM.sfx; v=v==null?0.85:v; osc('sine',150,t,0.28,v,dest,{a:0.002,glide:-105}); hit(t,v*0.16,dest,3000,0.02); },
  snare(dt,v,dest){ const t=T(dt); dest=dest||AM.sfx; v=v==null?0.35:v; hit(t,v,dest,1800,0.14,'bandpass'); osc('triangle',220,t,0.08,v*0.5,dest,{glide:-60}); },
  hat(dt,v,dest){ hit(T(dt),v==null?0.12:v,dest||AM.sfx,8000,0.04); },
  sub(dt,v){ const t=T(dt); v=v==null?0.8:v; osc('sine',110,t,0.55,v,AM.sfx,{glide:-70}); osc('sawtooth',55,t,0.4,v*0.25,AM.sfx,{glide:-25}); },
  whoosh(dt,v,up){ const t=T(dt), s=AC.createBufferSource(); s.buffer=nz(); const bp=AC.createBiquadFilter(); bp.type='bandpass'; bp.Q.value=1.2;
    bp.frequency.setValueAtTime(up===false?2800:500,t); bp.frequency.exponentialRampToValueAtTime(up===false?400:2800,t+0.2); const g=AC.createGain(); env(g,t,0.05,v==null?0.3:v,0.2); s.connect(bp); bp.connect(g); g.connect(AM.sfx); s.start(t); s.stop(t+0.35); },
  riser(dur,v){ const t=T(), s=AC.createBufferSource(); s.buffer=nz(); s.loop=true; const bp=AC.createBiquadFilter(); bp.type='bandpass'; bp.Q.value=3;
    bp.frequency.setValueAtTime(300,t); bp.frequency.exponentialRampToValueAtTime(6000,t+dur); const g=AC.createGain(); g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(v,t+dur*0.95); g.gain.exponentialRampToValueAtTime(0.0001,t+dur+0.05);
    s.connect(bp); bp.connect(g); g.connect(AM.sfx); s.start(t); s.stop(t+dur+0.1); },
  sparkle(dt,n,v){ for(let i=0;i<(n||10);i++) SV.bell(J(2600+i*190,0.08),(dt||0)+i*0.04,v||0.04); },
  glass(dt){ dt=dt||0; for(let i=0;i<7;i++) SV.bell(J(2400+Math.random()*2200,0.1),dt+i*0.018+Math.random()*0.02,0.07); hit(T(dt),0.3,AM.sfx,5000,0.12); },
};
const PENTA=[0,2,4,7,9];
const note=(i,base)=>(base||523.25)*Math.pow(2,(Math.floor(i/5)*12+PENTA[((i%5)+5)%5])/12);
const st=(f,s)=>f*Math.pow(2,s/12);
const LAST={}; function once(k,ms){ const n=performance.now(); if(LAST[k] && n-LAST[k]<ms) return false; LAST[k]=n; return true; }
function vib(p){ try{ if(on() && navigator.vibrate) navigator.vibrate(p); }catch(e){} }

/* ---- 효과음 ---- */
function play(kind,arg){
  if(!on() || !ac()) return;
  try{ const t0=T(), S=AM.sfx;
  switch(kind){
    /* 공통 */
    case 'bad': SV.kick(0,0.75); osc('sawtooth',J(116),t0,0.24,0.12,S,{det:-35,glide:-30}); osc('sawtooth',J(123),t0,0.24,0.1,S,{det:25,glide:-30}); vib([30,30,30]); break;
    case 'erase': if(once('erase',40)){ osc('sine',J(520),t0,0.1,0.5,S,{glide:-260}); hit(t0,0.2,S,2500,0.04,'bandpass'); } break;
    case 'clear': SV.whoosh(0,0.26,false); [7,4,0].forEach((d,k)=>SV.pluck(note(d,392),0.05+k*0.06,0.14)); break;
    case 'new': SV.whoosh(0,0.28); SV.bell(1046.5,0.12,0.12); SV.bell(1568,0.18,0.08); break;
    case 'ui': if(once('ui',40)){ hit(t0,0.4,S,3200,0.02,'bandpass'); osc('triangle',J(1600,0.04),t0,0.03,0.2,S); } break;
    case 'win': /* 풀이 완료 — 라이저 → 팡파르 → 반짝임. 판이 한 칸씩 빛나는 연출(약 0.6초)과 맞춘다 */
      SV.riser(0.55,0.16);
      [0,4,7,12,16,19].forEach((s,k)=>{ SV.pluck(st(523.25,s),0.55+k*0.07,0.26); SV.bell(st(1046.5,s),0.57+k*0.07,0.06); });
      SV.kick(0.55,1); SV.snare(0.55,0.4); [0,4,7].forEach(s=>SV.bell(st(1046.5,s),1.0,0.1)); SV.sparkle(1.05,12,0.035);
      vib([20,40,20,40,70]); break;
    /* 말로우 크라운 */
    case 'crown': { const i=Math.max(0,(arg||1)-1);   // 놓인 왕관 수만큼 음계가 오른다(n/N 진행감)
      SV.harp(note(i,392),0,0.24); SV.bell(note(i+5,392)*2,0.03,0.06); hit(t0,0.08,S,5000,0.05);
      vib(12); break; }
    case 'mark': if(once('mark',35)){ hit(t0,0.7,S,2400,0.035,'bandpass'); osc('triangle',J(1100,0.05),t0,0.05,0.4,S,{glide:-300}); } break;   // ✕ 연필 톡
    /* 말로우 탱고 */
    case 'sun': { const i=Math.min(arg||0,14); SV.bell(note(i,659.25),0,0.13); osc('triangle',note(i,659.25),t0,0.12,0.12,S); vib(10); break; }   // 밝고 높은 종
    case 'moon': { const i=Math.min(arg||0,14); osc('sine',note(i,261.63),t0,0.5,0.2,S,{a:0.02}); SV.bell(note(i+2,261.63)*2,0.02,0.05); vib(10); break; }   // 낮고 부드러운 울림
    case 'line': [0,7,12].forEach((s,k)=>SV.bell(st(987.77,s),0.09+k*0.05,0.09)); break;   // 가로·세로줄이 규칙대로 가득 참
    /* 모아모아 */
    case 'pick': { const i=Math.max(0,Math.min(3,(arg||1)-1)); hit(t0,0.26,S,1800,0.03,'bandpass'); SV.pluck(note(i*2,392),0,0.3); break; }   // 나무 낱말패 딸깍 — 고른 수만큼 한 칸씩 오름
    case 'unpick': hit(t0,0.4,S,1400,0.03,'bandpass'); osc('triangle',J(330),t0,0.1,0.45,S,{glide:-90}); break;
    case 'shuffle': for(let i=0;i<9;i++) hit(t0+i*0.028+Math.random()*0.012,0.1,S,1200+Math.random()*1600,0.025,'bandpass'); break;
    case 'group': { /* 그룹 정답 — 색(난이도)마다 다른 화음: 노랑 밝은 장조 → 보라 신비한 화음, 뒤로 갈수록 크게 */
      const d=arg||0, root=[523.25,466.16,440,392][d], ch=[[0,4,7,12],[0,4,7,11],[0,3,7,10],[0,5,7,14]][d];
      ch.forEach((s,k)=>{ SV.pluck(st(root,s),k*0.07,0.26); SV.bell(st(root*2,s),k*0.07+0.02,0.05+d*0.012); });
      SV.kick(0,0.45+d*0.12); if(d>=2) SV.sparkle(0.3,8,0.03); vib([15,30,20]); break; }
    case 'oneaway': [0,4,7].forEach((s,k)=>SV.pluck(st(392,s),k*0.09,0.2)); osc('triangle',st(392,11),t0+0.27,0.5,0.1,S); SV.hat(0.27,0.1); vib([20,40,20]); break;   // 세 음이 오르다 한 음이 매달림 — '거의!'
    case 'miss': SV.kick(0,0.8); osc('sawtooth',J(110),t0,0.28,0.12,S,{det:-30,glide:-35}); osc('sawtooth',J(117),t0,0.28,0.1,S,{det:25,glide:-35}); SV.glass(0.08); vib([40,30,40]); break;
    case 'lose': osc('sawtooth',440,t0,0.9,0.14,S,{glide:-330}); SV.sub(0.05,0.8); SV.bell(98,0.1,0.35); hit(t0+0.1,0.2,S,400,0.9,'lowpass'); vib(80); break;
  }
  }catch(e){}
}

/* ---- 배경음악: 게임마다 한 가지 분위기 × 강도 3단계 (퍼즐이라 잔잔하게, 끝이 가까우면 쌓인다) ---- */
const THEMES={
  study:  {root:293.66, bpm:80, prog:[[0,4,7],[-3,0,4],[-5,-1,2],[-7,-3,0]]},   // 모아모아 — 서재 로파이(오음 음계 멜로디)
  royal:  {root:293.66, bpm:74, prog:[[0,4,7],[5,9,12],[7,11,14],[-3,0,4]]},    // 크라운 — 하프 아르페지오 궁정풍
  sky:    {root:261.63, bpm:76, prog:[[0,4,11],[2,6,9],[-3,0,7],[5,9,12]]},     // 탱고 — 해·달 하늘(리디안 느낌)
};
const B={on:null,level:0,step:0,next:0,timer:0,paused:null};
function bgm(theme){ stop(); if(!on() || vol('music')<=0.001 || !THEMES[theme] || !ac()) return;
  B.on=theme; B.step=0; B.next=AC.currentTime+0.1; B.timer=setInterval(tick,25); }
function stop(){ clearInterval(B.timer); B.timer=0; B.on=null; }
function level(n){ B.level=Math.max(0,Math.min(2,n|0)); }
function tick(){ if(!B.on) return; if(!on()){ stop(); return; } const th=THEMES[B.on];
  while(B.next<AC.currentTime+0.12){ beat(B.step, B.next-AC.currentTime, th); B.next+=60/th.bpm/4; B.step++; } }
function beat(s,t,th){ const k=B.on, L=B.level, i=s%16, ch=th.prog[Math.floor(s/16)%4], D=AM.mus, f=n=>th.root*Math.pow(2,n/12), bar=60/th.bpm*4;
  if(i===0) ch.forEach(n=>osc('triangle',f(n)/2,AC.currentTime+t,bar*0.95,0.06,D,{a:0.45}));                        // 패드
  if(k==='royal'){ if(i%2===0) SV.harp(f(ch[(i/2)%3]+(i>=8?12:0)),t,0.07,D); if(i===0) osc('sine',f(ch[0])/4,AC.currentTime+t,bar*0.9,0.1,D,{a:0.05}); }
  else if(k==='sky'){ if(i%4===0) SV.bell(f(ch[(i/4)%3]+12),t,0.08,D); if(i===6||i===14) SV.bell(f(ch[2]+24),t,0.03,D); }
  else { if(i%4===2 && Math.random()<0.6) SV.pluck(f([0,2,4,7,9][(s*3)%5]+12),t,0.09,D); if(i%8===0) osc('sine',f(ch[0])/4,AC.currentTime+t,0.3,0.1,D); }
  if(L>=1){ if(i%8===4) SV.hat(t,0.05,D); if(k!=='royal' && i%4===0) osc('sine',f(ch[0])/4,AC.currentTime+t,0.18,0.07,D); }
  if(L>=2){ if(i%8===0) SV.kick(t,0.32,D); if(i%2===1) SV.hat(t,0.03,D); if(i===12) SV.snare(t,0.1,D); } }   // 끝이 가까울 때 — 맥박이 붙는다
document.addEventListener('visibilitychange',()=>{ if(document.hidden){ if(B.on){ B.paused=B.on; stop(); } } else if(B.paused){ const th=B.paused; B.paused=null; bgm(th); } });
['pointerdown','touchend','keydown'].forEach(ev=>document.addEventListener(ev,()=>{ if(AC && AC.state==='suspended') AC.resume(); },{passive:true}));

/* ---- 켜기/끄기 + 음량 패널 ---- */
const TXT={ko:{on:'소리 켜짐',off:'소리 꺼짐',music:'음악',sfx:'효과음'},en:{on:'Sound on',off:'Sound off',music:'Music',sfx:'Effects'},th:{on:'เปิดเสียง',off:'ปิดเสียง',music:'เพลง',sfx:'เสียงเอฟเฟกต์'}};
function setOn(v){ try{ localStorage.setItem('brain.sound',v?'on':'off'); localStorage.setItem('mallow_mute',v?'0':'1'); }catch(e){} if(!v){ B.paused=null; stop(); } }
function setVol(k,v){ try{ localStorage.setItem('brain.vol.'+k,String(v)); }catch(e){} applyVol(); if(k==='music' && v<=0.001) stop(); }
function css(){ if(document.getElementById('ds-css')) return; const s=document.createElement('style'); s.id='ds-css';
  s.textContent='.ds-panel{position:absolute;z-index:9999;display:flex;flex-direction:column;gap:.55rem;padding:.75rem .85rem;min-width:210px;border-radius:14px;background:#fff;border:1px solid #e3def0;box-shadow:0 10px 28px rgba(20,20,60,.25);font-family:inherit;color:#2a2140}'+
    '.ds-panel label{display:flex;align-items:center;justify-content:space-between;gap:.6rem;font-size:13px;font-weight:700}.ds-panel input{width:110px}'+
    '.ds-mute{font:inherit;font-weight:800;font-size:13px;border:1px solid #e3def0;background:#f6f4fb;border-radius:10px;padding:.45rem;cursor:pointer;color:#2a2140}';
  document.head.appendChild(s); }
function panel(btn,lang,onChange){ let p=document.getElementById('ds-panel'); if(p){ p.remove(); return; }
  css(); const L=TXT[lang]||TXT.ko, o=on(); p=document.createElement('div'); p.id='ds-panel'; p.className='ds-panel';
  p.innerHTML='<button class="ds-mute">'+(o?'🔊 '+L.on:'🔇 '+L.off)+'</button>'+
    '<label>🎵 '+L.music+'<input type="range" min="0" max="1" step="0.05" data-k="music" value="'+vol('music')+'"'+(o?'':' disabled')+'></label>'+
    '<label>🔔 '+L.sfx+'<input type="range" min="0" max="1" step="0.05" data-k="sfx" value="'+vol('sfx')+'"'+(o?'':' disabled')+'></label>';
  p.querySelector('.ds-mute').onclick=()=>{ setOn(!on()); if(on()) play('ui'); onChange&&onChange(on()); p.remove(); panel(btn,lang,onChange); };
  p.querySelectorAll('input').forEach(inp=>{ inp.oninput=()=>setVol(inp.dataset.k,+inp.value); if(inp.dataset.k==='sfx') inp.onchange=()=>play('crown',4); });
  document.body.appendChild(p); const r=btn.getBoundingClientRect();
  p.style.top=(r.bottom+window.scrollY+6)+'px'; p.style.right=Math.max(8,innerWidth-r.right)+'px';
  setTimeout(()=>document.addEventListener('pointerdown',function h(e){ if(!p.contains(e.target) && e.target!==btn){ p.remove(); document.removeEventListener('pointerdown',h); } }),0); }

window.DS={play,bgm,stop,level,on,setOn,vol,setVol,panel,playing:()=>B.on};
})();
