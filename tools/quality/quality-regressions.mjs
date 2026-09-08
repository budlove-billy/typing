import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {ROOT,gameRegistry} from './lib.mjs';
const html=readFileSync(new URL('index.html',ROOT),'utf8');
const store=new Map();
const ctx={localStorage:{getItem:k=>store.get(k)||null,setItem:(k,v)=>store.set(k,v)},_markNewRecord:()=>{}};
vm.createContext(ctx);
vm.runInContext(html.slice(html.indexOf('function bt_loadBest('),html.indexOf('/* ══════════ 점수 눈금 마이그레이션')),ctx);
const key='brain.flash.best', old=ctx.bt_loadBest(key);
old.normal={all:100,day:100,date:'2026-09-08'};
ctx.bt_saveBest(key,old);
const imported=JSON.parse(JSON.stringify(old));
imported.normal={all:1000,day:900,date:'2026-09-08'};
store.set(key,JSON.stringify(imported));
old.normal.all=200;old.normal.day=200;
ctx.bt_saveBest(key,old);
assert.equal(JSON.parse(store.get(key)).normal.all,1000);
assert.equal(JSON.parse(store.get(key)).normal.day,900);
assert.equal(old.normal.all,1000);
const start=html.indexOf('const MISSION_A=');
const end=html.indexOf('function missionLoad()',start);
let now=Date.UTC(2026,0,1);
class TestDate extends Date{constructor(...args){super(...(args.length?args:[now]));}}
const mission={HOME_GAMES:gameRegistry(html),CURRENT_LANG:'ko',Date:TestDate};
vm.createContext(mission);
vm.runInContext(html.slice(start,end),mission);
for(const lang of ['ko','en','th']){
  mission.CURRENT_LANG=lang;
  for(let day=0;day<366;day++){
    now=Date.UTC(2026,0,1+day);
    const ids=mission.missionToday();assert.equal(ids.length,3);assert.equal(new Set(ids).size,3);
    for(const id of ids){const g=mission.HOME_GAMES.find(g=>g.id===id);assert.ok(g&&(!g.langs||g.langs.includes(lang)));}
  }
}
console.log('PASS imported/stale-tab records preserved; same-day best preserved; 1098 language/date mission combinations');
