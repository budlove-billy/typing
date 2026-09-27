/* ===== 사운드 엔진 v2 (2026-09-27) — docs/사운드-점검-개선안.md · 데모 public/sound-demo.html =====
   효과음 버스(리버브 센드) + 드라이 버스(시험음: 멜로디·리듬·높은음·거꾸로 기억 — 울림 없이) + 음악 버스
   → 컴프레서 → 리미터. 음원 파일 없이 합성. 음량: brain.vol.sfx / brain.vol.music (0~1). */
let _AM=null;
function sndVol(k){ try{ const v=parseFloat(localStorage.getItem('brain.vol.'+k)); if(!isNaN(v)) return Math.max(0,Math.min(1,v)); }catch(e){} return k==='music'?0.6:0.85; }
function _ac(){
  if(!_AC) _AC=new (window.AudioContext||window.webkitAudioContext)();
  if(_AC.state==='suspended') _AC.resume();
  if(!_AM){ const A=_AC;
    const comp=A.createDynamicsCompressor(); comp.threshold.value=-18; comp.knee.value=12; comp.ratio.value=4; comp.attack.value=0.003; comp.release.value=0.18;
    const lim=A.createDynamicsCompressor(); lim.threshold.value=-2; lim.ratio.value=20; lim.attack.value=0.001; lim.release.value=0.05;
    comp.connect(lim); lim.connect(A.destination);
    const verb=A.createConvolver(), len=Math.floor(A.sampleRate*1.3), ir=A.createBuffer(2,len,A.sampleRate);
    for(let c=0;c<2;c++){ const d=ir.getChannelData(c); for(let i=0;i<len;i++) d[i]=(Math.random()*2-1)*Math.pow(1-i/len,3.2); }
    verb.buffer=ir; const vg=A.createGain(); vg.gain.value=0.2; verb.connect(vg); vg.connect(comp);
    const sfx=A.createGain(), dry=A.createGain(), mus=A.createGain(), ms=A.createGain();
    sfx.connect(comp); sfx.connect(verb); dry.connect(comp); mus.connect(comp); ms.gain.value=0.35; mus.connect(ms); ms.connect(verb);
    _AM={sfx,dry,mus}; sndApplyVol(); }
  return _AC;
}
function sndApplyVol(){ if(!_AM) return; const t=_AC.currentTime, s=sndVol('sfx'), m=sndVol('music');
  _AM.sfx.gain.setTargetAtTime(s*1.1,t,0.05); _AM.dry.gain.setTargetAtTime(s*1.25,t,0.05); _AM.mus.gain.setTargetAtTime(m*0.17,t,0.05); }   // 음악은 효과음보다 6dB 이상 아래(측정: .logs/sound_mix.mjs)
function setSndVol(k,v){ try{ localStorage.setItem('brain.vol.'+k,String(v)); }catch(e){} sndApplyVol(); if(k==='music' && BGM.on && v<=0.001) bgmStop(); }
function _sfxOut(){ _ac(); return _AM.sfx; }
function _dryOut(){ _ac(); return _AM.dry; }

/* ---- 음색 ---- */
let _NZ=null; function _nz(){ if(_NZ) return _NZ; const A=_ac(), b=A.createBuffer(1,A.sampleRate,A.sampleRate), d=b.getChannelData(0); for(let i=0;i<d.length;i++) d[i]=Math.random()*2-1; return _NZ=b; }
const _J=(v,p)=>v*(1+(Math.random()*2-1)*(p==null?0.03:p));   // 같은 소리 반복의 기계감 줄이기
function _env(g,t,a,peak,dec){ g.gain.setValueAtTime(0.0001,t); g.gain.linearRampToValueAtTime(peak,t+a); g.gain.exponentialRampToValueAtTime(0.0001,t+a+dec); }
function _osc(type,f,t,dur,peak,dest,o){ o=o||{}; const A=_AC, x=A.createOscillator(), g=A.createGain(); x.type=type; x.frequency.setValueAtTime(f,t);
  if(o.glide) x.frequency.exponentialRampToValueAtTime(Math.max(20,f+o.glide),t+dur); if(o.det) x.detune.value=o.det;
  _env(g,t,o.a||0.004,peak,dur); x.connect(g); g.connect(dest); x.start(t); x.stop(t+(o.a||0.004)+dur+0.05); }
function _hit(t,vol,dest,freq,dec,type){ const A=_AC, s=A.createBufferSource(); s.buffer=_nz(); const f=A.createBiquadFilter(); f.type=type||'highpass'; f.frequency.value=freq; const g=A.createGain(); _env(g,t,0.001,vol,dec); s.connect(f); f.connect(g); g.connect(dest); s.start(t); s.stop(t+dec+0.05); }
const SV={
  T(dt){ return _ac().currentTime+(dt||0); },
  pluck(f,dt,vol,dest){ const t=SV.T(dt); dest=dest||_AM.sfx; vol=vol==null?0.34:vol; const f0=_J(f,0.004);
    const lp=_AC.createBiquadFilter(); lp.type='lowpass'; lp.Q.value=4; lp.frequency.setValueAtTime(f0*9,t); lp.frequency.exponentialRampToValueAtTime(f0*1.5,t+0.25); lp.connect(dest);
    _osc('sawtooth',f0,t,0.32,vol*0.5,lp); _osc('triangle',f0*2,t,0.18,vol*0.35,lp); _osc('sine',f0/2,t,0.2,vol*0.4,dest); },
  bell(f,dt,vol,dest){ const t=SV.T(dt); dest=dest||_AM.sfx; vol=vol==null?0.22:vol; [1,2.76,5.4].forEach((r,i)=>_osc('sine',f*r,t,[1.1,0.6,0.3][i],vol*[1,0.4,0.2][i],dest)); },
  kick(dt,vol,dest){ const t=SV.T(dt); dest=dest||_AM.sfx; vol=vol==null?0.85:vol; _osc('sine',150,t,0.28,vol,dest,{a:0.002,glide:-105}); _hit(t,vol*0.16,dest,3000,0.02); },
  snare(dt,vol,dest){ const t=SV.T(dt); dest=dest||_AM.sfx; vol=vol==null?0.35:vol; _hit(t,vol,dest,1800,0.14,'bandpass'); _osc('triangle',220,t,0.08,vol*0.5,dest,{glide:-60}); },
  hat(dt,vol,dest){ _hit(SV.T(dt),vol==null?0.12:vol,dest||_AM.sfx,8000,0.04); },
  sub(dt,vol){ const t=SV.T(dt); vol=vol==null?0.8:vol; _osc('sine',110,t,0.55,vol,_AM.sfx,{glide:-70}); _osc('sawtooth',55,t,0.4,vol*0.25,_AM.sfx,{glide:-25}); },
  riser(dur,vol){ const t=SV.T(), A=_AC, s=A.createBufferSource(); s.buffer=_nz(); s.loop=true; const bp=A.createBiquadFilter(); bp.type='bandpass'; bp.Q.value=3;
    bp.frequency.setValueAtTime(300,t); bp.frequency.exponentialRampToValueAtTime(6000,t+dur); const g=A.createGain(); g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(vol,t+dur*0.95); g.gain.exponentialRampToValueAtTime(0.0001,t+dur+0.05);
    s.connect(bp); bp.connect(g); g.connect(_AM.sfx); s.start(t); s.stop(t+dur+0.1); _osc('sawtooth',180,t,dur,vol*0.25,_AM.sfx,{a:dur*0.9,glide:700}); },
  whoosh(dt,vol){ const t=SV.T(dt), A=_AC, s=A.createBufferSource(); s.buffer=_nz(); const bp=A.createBiquadFilter(); bp.type='bandpass'; bp.Q.value=1.2;
    bp.frequency.setValueAtTime(500,t); bp.frequency.exponentialRampToValueAtTime(2800,t+0.18); const g=A.createGain(); _env(g,t,0.05,vol==null?0.3:vol,0.18); s.connect(bp); bp.connect(g); g.connect(_AM.sfx); s.start(t); s.stop(t+0.3); },
  glass(dt){ dt=dt||0; for(let i=0;i<7;i++) SV.bell(_J(2400+Math.random()*2200,0.1),dt+i*0.018+Math.random()*0.02,0.07); _hit(SV.T(dt),0.3,_AM.sfx,5000,0.12); },
};
const _PENTA=[0,2,4,7,9];
function _note(i,base){ base=base||523.25; return base*Math.pow(2,(Math.floor(i/5)*12+_PENTA[((i%5)+5)%5])/12); }

/* ---- 공통 문법 상태: 연속 성공(streak) — 게임마다 콤보 규칙이 달라 소리는 '정답 연속'으로 센다 ---- */
const SND={ streak:0, lastEnd:0, medalAt:{}, last:{} };
function _once(k,ms){ const n=performance.now(); if(SND.last[k] && n-SND.last[k]<ms) return false; SND.last[k]=n; return true; }   // 같은 소리 폭주 방지
function _sndGood(step){ const i=Math.min(step,14); SV.pluck(_note(i),0,0.32); SV.bell(_note(i+5)*2,0.03,0.05);
  const c=SND.streak; if(step===c-1 && (c===5||c===10||(c>10&&c%10===0))){ [0,4,7,12].forEach((s,k)=>SV.pluck(_note(i)*Math.pow(2,s/12),0.12+k*0.06,0.24)); SV.hat(0.1,0.18); } }
function _sndBreak(){ const s=SND.streak; SND.streak=0; bgmLevelUpdate(); return s>=5; }

function sfx(kind, arg){
  if(kind==='__tick'){ try{ // 60초 게임 공통: 남은 10초 심장박동(점점 빨라짐) + 5초부터 틱 음이 오른다. 타이머 표시 함수가 부른다
    const st=arg;
    if(st && st.running && typeof st.timeLeft==='number'){
      BGM.urgent = st.timeLeft>0 && st.timeLeft<=15 ? (16-st.timeLeft) : 0; bgmLevelUpdate();
      if(st.timeLeft>0 && st.timeLeft<=10 && sndOn() && st.__lastTick!==st.timeLeft){ st.__lastTick=st.timeLeft; _ac();
        const n=st.timeLeft<=3?3:st.timeLeft<=6?2:1; for(let k=0;k<n;k++){ SV.kick(k/n*0.9,0.7); SV.kick(k/n*0.9+0.14,0.38); }
        if(st.timeLeft<=5){ SV.hat(0,0.2); _osc('square',900+(6-st.timeLeft)*180,SV.T(),0.05,0.05,_AM.sfx); } }
    }
  }catch(_){} return; }
  if(kind==='good'||kind==='merge'||kind==='cork'||kind==='lines'||kind==='rt'||kind==='clap') fxBurst(_fxXY.x,_fxXY.y,{count:9,spread:46});
  else if(kind==='win') fxBurst(_fxXY.x,_fxXY.y,{count:20,spread:95});
  const vib=(p)=>{ try{ navigator.vibrate&&navigator.vibrate(p); }catch(e){} };
  if(kind==='good'||kind==='merge'||kind==='cork'||kind==='lines'||kind==='rt'){ SND.streak++; bgmLevelUpdate(); }
  else if(kind==='bad'||kind==='bomb'||kind==='clang'||kind==='crash'||kind==='scrape'){ if(_sndBreak() && sndOn()){ try{ _ac(); SV.glass(0.1); [7,4,2,0].forEach((d,k)=>SV.pluck(_note(d,392),0.18+k*0.07,0.16)); }catch(e){} } }
  if(!sndOn()) return;
  try{ _ac(); const T0=SV.T();
  switch(kind){
    case 'good': _sndGood(typeof arg==='number'?arg:SND.streak-1); vib(12); break;                       // 정답 — 음계 계단, 5·10콤보 팡파르
    case 'bad': SV.kick(0,0.8); _osc('sawtooth',_J(116),T0,0.22,0.12,_AM.sfx,{det:-35,glide:-30}); _osc('sawtooth',_J(123),T0,0.22,0.1,_AM.sfx,{det:25,glide:-30}); vib([40,30,40]); break;
    case 'win': [0,4,7,12].forEach((s,k)=>{ SV.pluck(523.25*Math.pow(2,s/12),k*0.07,0.26); SV.bell(1046.5*Math.pow(2,s/12),k*0.07+0.02,0.05); }); SV.hat(0.28,0.15); vib([20,40,20,40,60]); break;
    case 'tap': if(_once('tap',40)) _hit(T0,0.07,_AM.dry,4000,0.025); break;
    case 'combo': [0,4,7,12].forEach((s,k)=>SV.pluck(_note(SND.streak)*Math.pow(2,s/12),k*0.06,0.24)); vib(18); break;
    case 'level': SV.riser(0.45,0.14); [0,4,7,12].forEach((s,k)=>SV.pluck(392*Math.pow(2,s/12),0.42+k*0.05,0.24)); SV.kick(0.42,0.6); vib([15,30,45]); break;
    case 'flip': _hit(T0,0.18,_AM.sfx,2500,0.03,'bandpass'); _osc('triangle',_J(520),T0,0.06,0.1,_AM.sfx,{glide:220}); break;
    case 'whoosh': SV.whoosh(0,0.22); break;
    case 'tick': SV.hat(0,0.18); _osc('square',1200,T0,0.025,0.04,_AM.sfx); break;
    case 'count': SV.kick(0,0.5); SV.bell(660,0,0.16); break;
    case 'go': SV.kick(0,0.9); SV.snare(0,0.35); [0,4,7,12].forEach(s=>SV.pluck(523.25*Math.pow(2,s/12),0,0.16)); vib(25); break;
    case 'record': SND.lastEnd=performance.now(); SV.riser(0.6,0.18);
      [0,4,7,12,16,19].forEach((s,k)=>SV.pluck(523.25*Math.pow(2,s/12),0.6+k*0.07,0.26)); SV.kick(0.6,1); SV.snare(0.6,0.45);
      [0,4,7].forEach(s=>SV.bell(1046.5*Math.pow(2,s/12),1.05,0.1)); for(let k=0;k<10;k++) SV.bell(_J(3000+k*180,0.1),1.1+k*0.04,0.035);
      vib([25,35,25,35,25,35,80]); break;
    case 'end': SND.lastEnd=performance.now(); _osc('sawtooth',440,T0,0.9,0.14,_AM.sfx,{glide:-330}); SV.sub(0.05,0.8); SV.bell(98,0.1,0.4); _hit(T0+0.1,0.2,_AM.sfx,400,0.9,'lowpass'); break;
    case 'medal': { const L={bronze:[0,4,7],silver:[0,4,7,12],gold:[0,4,7,12,16],diamond:[0,4,7,11,14,19,24]}[arg]||[0,4,7], b=arg==='diamond'?587.33:523.25;
      L.forEach((s,i)=>{ SV.pluck(b*Math.pow(2,s/12),i*0.075,0.26); SV.bell(b*2*Math.pow(2,s/12),i*0.075+0.02,arg==='diamond'?0.1:0.05); });
      if(arg==='gold'||arg==='diamond') SV.kick(0,0.7);
      if(arg==='diamond'){ SV.riser(0.5,0.12); for(let i=0;i<14;i++) SV.bell(_J(2500+i*230,0.08),0.55+i*0.035,0.05); } vib([20,30,20,30,60]); break; }
    case 'dltick': for(let i=0;i<4;i++){ _hit(T0+i*0.11,0.2,_AM.sfx,6000,0.03); _osc('square',1200+i*140,T0+i*0.11,0.025,0.045,_AM.sfx); } break;   // 어려움 문항 제한시간 임박
    // ---- 게임별 시그니처 ----
    case 'jump': SV.whoosh(0,0.26); _osc('triangle',260,T0,0.16,0.26,_AM.sfx,{glide:520}); break;
    case 'land': if(_once('land',120)){ SV.kick(0,0.32); _hit(T0,0.08,_AM.sfx,900,0.05,'lowpass'); } break;
    case 'crash': SV.kick(0,1); SV.snare(0,0.55); SV.sub(0.02,0.9); SV.glass(0.05); vib(60); break;
    case 'milestone': SV.bell(1318.5,0,0.18); SV.bell(1760,0.09,0.16); break;
    case 'beat': [0,4,7,12].forEach((s,k)=>SV.bell(1046.5*Math.pow(2,s/12),k*0.06,0.12)); SV.hat(0,0.2); break;   // 달리는 중 최고점 돌파
    case 'clap': [0,0.16].forEach(o=>{ for(let k=0;k<3;k++) _hit(T0+o+k*0.011,0.5,_AM.sfx,1300,0.045,'bandpass'); _hit(T0+o+0.03,0.3,_AM.sfx,1300,0.14,'bandpass'); }); vib(15); break;   // 박수 — 음정이 없어 멜로디 기억의 다음 멜로디와 섞이지 않는다
    case 'bite': _hit(T0,0.36,_AM.sfx,1200,0.05,'bandpass'); SV.kick(0,0.3); _osc('square',_J(180,0.1),T0,0.05,0.07,_AM.sfx,{glide:-60}); break;
    case 'heart': SV.kick(0,0.55); SV.kick(0.15,0.3); break;
    case 'pop': if(_once('pop',60)) _osc('sine',_J(300,0.08),T0,0.13,0.18,_AM.sfx,{glide:500}); break;
    case 'bonk': SV.kick(0,0.45); break;
    case 'bomb': SV.sub(0,1); _hit(T0,0.55,_AM.sfx,300,0.6,'lowpass'); _hit(T0,0.28,_AM.sfx,3000,0.2); vib([50,30,50]); break;
    case 'clang': SV.bell(1760,0,0.2); SV.bell(1864,0.01,0.14); SV.kick(0,0.6); vib([40,30,40]); break;
    case 'rt': { const f=Math.max(660,Math.min(1760,1900-2.4*(arg||400))); SV.pluck(f/2,0,0.3); SV.bell(f,0.02,0.18); vib(12); break; }   // 반응 속도: 빠를수록 높은 차임
    case 'bubble': _osc('sine',arg?_J(900-arg*22,0.04):420,T0,0.08,0.2,_AM.sfx,{glide:arg?260:-120}); _hit(T0,0.06,_AM.sfx,3000,0.03); break;
    case 'place': if(_once('place',50)){ SV.kick(0,0.32); _hit(T0,0.1,_AM.sfx,1400,0.04,'bandpass'); } break;
    case 'lines': SV.whoosh(0,0.32); for(let i=0;i<Math.min(arg||1,4);i++) [0,4,7].forEach(s=>SV.pluck(392*Math.pow(2,(s+i*5)/12),0.06+i*0.08,0.2)); if((arg||1)>=2) SV.kick(0.06,0.6); vib(18); break;
    case 'merge': { const s=Math.log2(Math.max(4,arg||4)); SV.pluck(196*Math.pow(2,Math.min(s,14)/4),0,0.3); _osc('sine',120+s*20,T0,0.12,0.22,_AM.sfx,{glide:160}); vib(12); break; }
    case 'blip': _osc('sine',660,T0,0.07,0.08,_AM.sfx); break;                                           // 엔백: 글자마다 같은 중립음(정보 없음)
    case 'unit': [0,7,12,16].forEach((s,k)=>SV.bell(784*Math.pow(2,s/12),k*0.05,0.12)); break;          // 스도쿠 행·열·박스 완성
    case 'brush': if(_once('brush',40)){ _hit(T0,0.12,_AM.sfx,2200,0.06,'bandpass'); _osc('triangle',_J(330,0.05),T0,0.05,0.05,_AM.sfx); } break;
    case 'cork': _osc('sine',_J(520),T0,0.09,0.3,_AM.sfx,{glide:-260}); _hit(T0,0.15,_AM.sfx,2000,0.03); SV.bell(1568,0.06,0.1); vib(12); break;
    case 'pour': { const t=T0; for(let i=0;i<5;i++) _osc('sine',_J(500+i*90,0.08),t+i*0.035,0.05,0.07,_AM.sfx,{glide:120}); break; }
    case 'click': if(_once('click',40)){ _hit(T0,0.14,_AM.sfx,3200,0.02,'bandpass'); _osc('square',_J(1800,0.05),T0,0.012,0.03,_AM.sfx); } break;
    case 'letter': SV.pluck(_note(arg||0,659.25),0,0.2); break;
    case 'trace': SV.bell(_note(Math.min(Math.floor((arg||0)/45),14),392),0,0.07); break;
    case 'scrape': _hit(T0,0.35,_AM.sfx,1400,0.22,'bandpass'); _osc('sawtooth',140,T0,0.22,0.12,_AM.sfx,{glide:-60}); vib([40,30,40]); break;
  }
  }catch(e){}
}

/* ---- 적응형 배경음악: 분위기 4종 × 강도 3단계(연속 성공·남은 시간·게임 속도) ---- */
const BGM_THEME={run:'arcade',chop:'arcade',whack:'arcade',catch:'arcade',react:'arcade',fit:'arcade',
  stroop:'focus',flank:'focus',switch:'focus',rotate:'focus',guess:'focus',math:'focus',bubble:'focus',trail:'focus',spot:'focus',odd:'focus',diff:'focus',nback:'focus',wordsearch:'focus',anagram:'focus',
  flash:'memory',count:'memory',cards:'memory',
  sudoku:'puzzle',nono:'puzzle',sort:'puzzle',slide:'puzzle',merge:'puzzle',iq:'puzzle',trace:'puzzle'};
/* 멜로디·리듬·높은음·거꾸로 기억은 소리가 문제라 음악을 틀지 않는다. 반응 속도·첫 제시가 바로 나오는 게임은 GO 소리를 내지 않는다(신호와 헷갈림) */
const SND_NO_GO={react:1,melody:1,rhythm:1,pitch:1,rev:1};
const BGM={on:null,level:0,forced:0,urgent:0,bpm:108,base:108,step:0,next:0,timer:0,paused:false};
const BGM_PROG={arcade:[[0,7,12],[-4,3,8],[-7,0,5],[-2,5,10]], focus:[[0,3,7],[-4,0,3],[-7,-3,0],[-5,-2,2]], memory:[[0,4,7],[-3,0,4],[-7,-3,0],[-5,-1,2]], puzzle:[[0,4,11],[5,9,16],[2,5,12],[7,11,14]]};
const BGM_ROOT={arcade:246.94, focus:220, memory:261.63, puzzle:261.63}, BGM_BPM={arcade:118, focus:100, memory:84, puzzle:78};
function bgmLevelUpdate(){ const s=SND.streak; BGM.level=Math.max(BGM.forced, s>=10?2:s>=5?1:0, BGM.urgent>=6?2:BGM.urgent>0?1:0); }
function sndIntensity(n){ BGM.forced=n|0; bgmLevelUpdate(); }
function bgmStart(theme){ bgmStop(); if(!sndOn() || sndVol('music')<=0.001 || !theme) return; _ac();
  BGM.on=theme; BGM.base=BGM.bpm=BGM_BPM[theme]; BGM.step=0; BGM.forced=0; BGM.urgent=0; bgmLevelUpdate(); BGM.next=_AC.currentTime+0.08; BGM.timer=setInterval(_bgmTick,25); }
function bgmStop(){ clearInterval(BGM.timer); BGM.timer=0; BGM.on=null; BGM.urgent=0; BGM.forced=0; }
function _bgmTick(){ if(!BGM.on) return; if(!sndOn()){ bgmStop(); return; }
  BGM.bpm=BGM.base*(1+Math.min(BGM.urgent,15)*0.02);                    // 남은 시간이 줄수록 템포가 오른다
  while(BGM.next<_AC.currentTime+0.12){ _bgm16(BGM.step, BGM.next-_AC.currentTime); BGM.next+=60/BGM.bpm/4; BGM.step++; } }
function _bgm16(s,t){ const k=BGM.on, L=BGM.level, bar=Math.floor(s/16)%4, i=s%16, ch=BGM_PROG[k][bar], D=_AM.mus, f=n=>BGM_ROOT[k]*Math.pow(2,n/12);
  if(k==='puzzle'){ if(i%8===0) ch.forEach(n=>SV.bell(f(n),t,0.1,D)); if(i%4===2&&Math.random()<0.55) SV.pluck(f(ch[(i/2|0)%3]+12),t,0.11,D); if(L>=1&&i%8===4) SV.hat(t,0.07,D); if(L>=2&&i===0) SV.kick(t,0.3,D); return; }
  if(k==='memory'){ if(i===0) ch.forEach(n=>_osc('triangle',f(n)/2,_AC.currentTime+t,60/BGM.bpm*4*0.95,0.07,D,{a:0.5})); if(i%4===0) SV.bell(f(ch[(i/4)%3]+12),t,0.09,D); if(L>=1&&i%8===4) SV.hat(t,0.06,D); if(L>=2&&i%8===0) SV.kick(t,0.3,D); return; }
  if(i%4===0) SV.kick(t,k==='focus'?0.3:0.45,D);
  if(i===0) ch.forEach(n=>_osc('sawtooth',f(n)/2,_AC.currentTime+t,60/BGM.bpm*4*0.95,0.022,D,{a:0.3}));      // 패드
  if(i%2===0) _osc('sawtooth',f(ch[0])/4,_AC.currentTime+t,0.12,k==='focus'?0.065:0.09,D);                   // 베이스 맥박
  if(L>=1){ if(i%4===2) SV.hat(t,0.07,D); if(i===4||i===12) SV.snare(t,0.2,D); }
  if(L>=2){ SV.pluck(f(ch[i%3]+12+(i%8>=4?12:0)),t,0.06,D); if(i%2===1) SV.hat(t,0.045,D); }
  if(BGM.urgent>=6&&i%2===0) SV.hat(t,0.09,D); }
document.addEventListener('visibilitychange',()=>{ try{ if(document.hidden){ if(BGM.on){ BGM.paused=BGM.on; bgmStop(); } } else if(BGM.paused){ const th=BGM.paused; BGM.paused=false; if(document.querySelector('.screen.active [id$="-game-card"]:not([style*="none"]), #iq-test-card:not([style*="none"])')) bgmStart(th); } }catch(e){} });

/* ---- 게임 시작·끝 훅: 34개 start 함수와 결과 공통 함수(afterGame)를 감싸 한 곳에서 처리 ---- */
function sndGameStart(id){ SND.streak=0; SND.medalAt[id]=(typeof medalState==='function')?medalState(id,gameBestVal(id)).index:-1;
  bgmStart(BGM_THEME[id]); if(!SND_NO_GO[id]) sfx('go'); }
function sndGameEnd(id, r){ bgmStop(); BGM.paused=false; SND.streak=0; if(!sndOn()) return;
  const was=SND.medalAt[id]; let up=null; try{ const st=medalState(id,gameBestVal(id)); if(was!=null && st.index>was) up=st.current.key; }catch(e){}
  const recent=performance.now()-SND.lastEnd<500;                    // 방금 신기록·클리어 팡파르가 울렸으면 마무리 음은 생략
  if(!recent) sfx('end');
  if(up) setTimeout(()=>sfx('medal',up), recent?1500:900); }
function skUnitDone(r,c){ const ok=(rr,cc)=>SK.board[rr][cc]===SK.solution[rr][cc]; let row=true,col=true,box=true; const br=r-r%3, bc=c-c%3;
  for(let i=0;i<9;i++){ if(!ok(r,i)) row=false; if(!ok(i,c)) col=false; if(!ok(br+Math.floor(i/3),bc+i%3)) box=false; } return row||col||box; }
window.addEventListener('DOMContentLoaded',()=>{ try{
  Object.keys(PG_START).forEach(id=>{ const name=PG_START[id], orig=window[name]; if(typeof orig!=='function') return;
    window[name]=function(){ const r=orig.apply(this,arguments);
      try{ const gc=document.getElementById(id==='iq'?'iq-test-card':id+'-game-card'); if(gc && gc.style.display!=='none') sndGameStart(id); }catch(e){} return r; }; });
  const ag=window.afterGame; if(typeof ag==='function') window.afterGame=function(id,r){ const x=ag.apply(this,arguments); try{ sndGameEnd(id,r); }catch(e){} return x; };
}catch(e){} });

/* ---- 음량 패널(🔊 버튼) ---- */
function openSndPanel(ev){ if(ev) ev.stopPropagation(); let p=document.getElementById('snd-panel');
  if(p){ p.remove(); return; }
  p=document.createElement('div'); p.id='snd-panel'; p.className='snd-panel';
  const on=sndOn();
  p.innerHTML='<button class="snd-mute" onclick="toggleSound();openSndPanel();openSndPanel()">'+(on?'🔊 '+t('snd.on'):'🔇 '+t('snd.off'))+'</button>'+
    '<label>🎵 '+t('snd.music')+'<input type="range" min="0" max="1" step="0.05" value="'+sndVol('music')+'" oninput="setSndVol(\'music\',+this.value)"'+(on?'':' disabled')+'></label>'+
    '<label>🔔 '+t('snd.sfx')+'<input type="range" min="0" max="1" step="0.05" value="'+sndVol('sfx')+'" oninput="setSndVol(\'sfx\',+this.value)" onchange="sfx(\'good\',4)"'+(on?'':' disabled')+'></label>';
  document.body.appendChild(p); const b=document.getElementById('snd-btn').getBoundingClientRect();
  p.style.top=(b.bottom+window.scrollY+6)+'px'; p.style.right=Math.max(8,innerWidth-b.right)+'px';
  setTimeout(()=>document.addEventListener('pointerdown',function h(e){ if(!p.contains(e.target) && e.target.id!=='snd-btn'){ p.remove(); document.removeEventListener('pointerdown',h); } }),0); }
