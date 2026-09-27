/* 사운드 v2 통합 검증: 34게임 시작 시 음악 분위기·GO 소리, 중단 시 음악 정지, 끝 소리·메달 팡파르,
   주요 시그니처 호출, 음량 패널·소리 끄기, 오류 0. (포트 8226 서버 필요) */
import pw from 'file:///c:/Users/budlo/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const b=await pw.chromium.launch({args:['--autoplay-policy=no-user-gesture-required']});
const ctx=await b.newContext({viewport:{width:390,height:900},serviceWorkers:'block'}); const p=await ctx.newPage();
const errs=[]; p.on('pageerror',e=>errs.push(String(e).slice(0,160)));
await p.goto('http://127.0.0.1:8226/index.html?lang=ko',{waitUntil:'domcontentloaded'}); await p.waitForTimeout(900);
await p.mouse.click(5,5);
const fail=[]; const ok=(c,m)=>{ if(!c) fail.push(m); };
const res=await p.evaluate(async()=>{
  const wait=ms=>new Promise(r=>setTimeout(r,ms)); const log=[]; const orig=window.sfx; window.sfx=function(k,a){ if(k!=='__tick'&&k!=='tap') log.push(k); return orig.apply(this,arguments); };
  const out={};
  for(const id of Object.keys(PG_START)){ showScreen(id); log.length=0; try{ window[PG_START[id]](); }catch(e){ out[id]={err:e.message}; continue; }
    await wait(350); out[id]={bgm:BGM.on, go:log.includes('go'), ctx:_AC&&_AC.state}; haltRunningGames(); out[id].afterHalt=BGM.on; }
  // 끝 소리 + 신기록 + 메달
  showScreen('flank'); setFlankDiff('normal'); startFlank(); await wait(200); log.length=0; FK.score=7000; finishFlank(); await wait(1800);
  out._end={log:log.slice(), bgm:BGM.on};
  showScreen('flank'); startFlank(); await wait(200); log.length=0; FK.score=10; finishFlank(); await wait(300); out._end2=log.slice();
  // 시그니처
  showScreen('run'); setRunDiff('normal'); startRun(); log.length=0; rnJump(); await wait(900); out._run=log.slice(); haltRunningGames();
  showScreen('trail'); startTrail(); await wait(150); log.length=0; [...document.querySelectorAll('#tr-board .tr-node')].find(n=>n.textContent==='1').onclick(); out._trail=log.slice(); haltRunningGames();
  showScreen('stroop'); setStroopDiff('hard'); startStroop(); await wait(1150); out._dl=log.includes('dltick'); haltRunningGames();
  // 마지막 10초 심장박동
  showScreen('stroop'); setStroopDiff('normal'); startStroop(); await wait(100); ST.timeLeft=9; updateStTimerDisplay(); out._urgent={u:BGM.urgent, lv:BGM.level}; haltRunningGames();
  // 음량·소리 끄기
  openSndPanel(); out._panel=!!document.getElementById('snd-panel'); setSndVol('music',0.2); await wait(400); out._musGain=+_AM.mus.gain.value.toFixed(3); openSndPanel();
  showScreen('stroop'); startStroop(); await wait(100); toggleSound(); out._mutedBgm=BGM.on; toggleSound(); haltRunningGames(); setSndVol('music',0.6);
  return out; });
const TH={run:'arcade',chop:'arcade',whack:'arcade',catch:'arcade',react:'arcade',fit:'arcade',flash:'memory',count:'memory',cards:'memory',sudoku:'puzzle',nono:'puzzle',sort:'puzzle',slide:'puzzle',merge:'puzzle',iq:'puzzle',trace:'puzzle',melody:null,rhythm:null,pitch:null,rev:null};
const NOGO=['react','melody','rhythm','pitch','rev'];
for(const [id,v] of Object.entries(res)){ if(id[0]==='_') continue;
  const want=id in TH?TH[id]:'focus';
  if(id==='pitch'){ ok(v.bgm===null,'pitch music'); continue; }   // 소리 켜짐 확인 안내가 뜨면 시작 안 함
  ok(!v.err && v.bgm===want && v.afterHalt===null && v.go===!NOGO.includes(id), id+' '+JSON.stringify(v)); }
ok(res._end.log.includes('record') && res._end.log.includes('medal') && res._end.bgm===null, 'end record/medal '+JSON.stringify(res._end));
ok(res._end2.includes('end'), 'end sting '+JSON.stringify(res._end2));
ok(res._run.includes('jump') && res._run.includes('land'), 'run '+JSON.stringify(res._run));
ok(res._trail.includes('good'), 'trail '+JSON.stringify(res._trail));
ok(res._dl, 'deadline tick');
ok(res._urgent.u>=6 && res._urgent.lv===2, 'urgent '+JSON.stringify(res._urgent));
ok(res._panel && Math.abs(res._musGain-0.034)<0.01, 'panel '+res._musGain);
ok(res._mutedBgm===null, 'mute stops music');
ok(!errs.length, 'errors '+errs.join(' | '));
console.log(JSON.stringify({end:res._end, run:res._run, urgent:res._urgent}));
console.log(fail.length?'FAIL\n - '+fail.join('\n - '):'ALL PASS');
await b.close();
