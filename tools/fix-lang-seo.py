# -*- coding: utf-8 -*-
"""언어별 self-canonical + hreflang 주입 — 다국어 페이지가 검색에서 ko로 통합돼 사라지는 문제 수정"""
import io, re, os

P = {
'zodiac': {'base':'https://playmallow.com/zodiac/','langs':['ko','en','th'],'seo':{
  'ko':("말로우 별자리 운세 — 오늘의 별자리 운세 | Mallow",
        "오늘 달이 지나는 별자리와 내 별자리의 각도로 보는 무료 별자리 운세. 지수 100점과 애정·금전·건강·일운.",
        "말로우 별자리 운세 — 오늘의 별자리 운세",
        "오늘 달의 위치로 보는 내 별자리 운세. 지수 100점·분야별 점수·이번 주 흐름까지 무료로."),
  'en':("Mallow Horoscope — Today's Zodiac Fortune",
        "Free daily horoscope from a real Moon transit: aspect, phase, 100-point score.",
        "Mallow Horoscope — Today's Zodiac Fortune",
        "Where the Moon is today vs your sign — aspect, lunar phase and a 100-point score."),
  'th':("ดวงราศี Mallow — ดูดวงราศีประจำวัน",
        "ดูดวงราศีประจำวันฟรี จากตำแหน่งดวงจันทร์วันนี้เทียบราศีคุณ พร้อมคะแนนเต็ม 100",
        "ดวงราศี Mallow — ดูดวงราศีประจำวัน",
        "ดวงจันทร์วันนี้อยู่ราศีใด เทียบกับราศีคุณ พร้อมคะแนน ความรัก การเงิน สุขภาพ")}},

'persona': {'base':'https://playmallow.com/persona/','langs':['ko','en','th'],'seo':{
  'ko':("말로우 페르소나 — 성격 유형 심층 진단 (16유형) | Mallow",
        "24개 상황 질문으로 보는 나의 성격 16유형. 4가지 축을 %로 진단하고 강점·연애·일·궁합·추천 게임까지.",
        "말로우 페르소나 — 성격 유형 심층 진단",
        "24문항으로 보는 나의 16유형! 축별 %와 상세 프로필, 결과를 친구와 공유해 보세요."),
  'en':("Mallow Persona — Personality Type Test (16 types) | Mallow",
        "24 situation questions reveal your personality type. 16 types, 4 axes in %.",
        "Mallow Persona — Personality Type Test (16 types)",
        "Find your type from 24 questions: strengths, love, work style and best matches."),
  'th':("Mallow เพอร์โซนา — แบบทดสอบบุคลิกภาพ (16 แบบ) | Mallow",
        "24 คำถามเผยบุคลิกภาพของคุณ 16 แบบ 4 แกน พร้อมเปอร์เซ็นต์ จุดแข็ง ความรัก การงาน",
        "Mallow เพอร์โซนา — แบบทดสอบบุคลิกภาพ (16 แบบ)",
        "รู้จักตัวเองจาก 24 คำถาม ทั้งจุดแข็ง ความรัก การงาน และคู่ที่เข้ากันได้")}},

'queens': {'base':'https://playmallow.com/queens/','langs':['ko','en','th'],'seo':{
  'ko':("말로우 크라운 — 오늘의 왕관 퍼즐 (Queens) | Mallow",
        "색 구역·행·열에 왕관을 하나씩, 서로 닿지 않게. 매일 새로 나오는 무료 논리 퍼즐 말로우 크라운.",
        "말로우 크라운 — 오늘의 왕관 퍼즐",
        "행·열·색 구역에 왕관 하나씩! 매일 바뀌는 논리 퍼즐을 풀고 기록을 공유해 보세요."),
  'en':("Mallow Crown — Daily Queens Puzzle | Mallow",
        "Free daily Queens logic puzzle: one crown per row, column and colour region.",
        "Mallow Crown — Daily Queens Puzzle",
        "One crown per row, column and colour, never touching. A new puzzle every day."),
  'th':("Mallow คราวน์ — ปริศนามงกุฎรายวัน | Mallow",
        "เกมปริศนามงกุฎฟรีทุกวัน วางมงกุฎหนึ่งอันต่อแถว คอลัมน์ และโซนสี ห้ามติดกัน",
        "Mallow คราวน์ — ปริศนามงกุฎรายวัน",
        "วางมงกุฎหนึ่งอันต่อแถว คอลัมน์ และโซนสี ปริศนาใหม่ทุกวัน เล่นฟรี")}},

'tango': {'base':'https://playmallow.com/tango/','langs':['ko','en','th'],'seo':{
  'ko':("말로우 탱고 — 오늘의 해·달 퍼즐 (Tango) | Mallow",
        "해와 달을 채우는 논리 퍼즐. 같은 것 3연속 금지, 줄마다 개수 균형. 매일 새로 나오는 무료 말로우 탱고.",
        "말로우 탱고 — 오늘의 해·달 퍼즐",
        "3연속 금지·개수 균형! 매일 바뀌는 논리 퍼즐을 풀고 공유해 보세요."),
  'en':("Mallow Tango — Daily Sun & Moon Puzzle | Mallow",
        "Free daily Tango puzzle: fill the grid with suns and moons, no three in a row.",
        "Mallow Tango — Daily Sun & Moon Puzzle",
        "Suns and moons, never three in a row, balanced in every line. New every day."),
  'th':("Mallow แทงโก้ — ปริศนาอาทิตย์จันทร์รายวัน | Mallow",
        "เกมแทงโก้ฟรีทุกวัน เติมดวงอาทิตย์และดวงจันทร์ ห้ามซ้ำสามช่องติดกัน สมดุลทุกแถว",
        "Mallow แทงโก้ — ปริศนาอาทิตย์จันทร์รายวัน",
        "ดวงอาทิตย์และดวงจันทร์ ห้ามซ้ำสามช่องติด สมดุลทุกแถว ปริศนาใหม่ทุกวัน")}},

'luckycolor': {'base':'https://playmallow.com/luckycolor/','langs':['ko','en','th'],'seo':{
  'ko':("태국 요일별 행운색 — 태어난 요일로 보는 행운의 색 | Mallow",
        "태국 전통 요일별 행운색(สีมงคล). 생년월일로 태어난 요일을 찾아 행운의 색·피할 색·수호 부처 확인.",
        "태국 요일별 행운색 — 태어난 요일로 보는 행운의 색",
        "태어난 요일로 보는 태국 전통 행운색. 행운의 색 7가지와 피할 색을 확인해 보세요."),
  'en':("Thai Lucky Colour by Birth Day | Mallow",
        "Thai lucky colour by the day you were born: 7 lucky colours and ones to avoid.",
        "Thai Lucky Colour by Birth Day",
        "Enter your birth date to find your day of week, lucky colours and guardian Buddha."),
  'th':("สีมงคลประจำวันเกิด — เช็กสีมงคลและสีกาลกิณี | Mallow",
        "สีมงคลประจำวันเกิดตามความเชื่อไทย ใส่วันเกิดดูสีมงคล สีกาลกิณี และพระประจำวัน",
        "สีมงคลประจำวันเกิด — เช็กสีมงคลและสีกาลกิณี",
        "ใส่วันเกิดเพื่อดูวันในสัปดาห์ สีมงคล 7 สี สีต้องห้าม และพระประจำวันเกิด")}},

'tarot': {'base':'https://playmallow.com/tarot/','langs':['ko','th'],'seo':{
  'ko':("말로우 타로 — 오늘의 카드 & 3카드 타로 | Mallow",
        "오늘의 타로 한 장과 과거·현재·미래를 보는 3카드 스프레드. 연애·일·재물 고민을 카드에 물어보세요.",
        "말로우 타로 — 오늘의 카드 & 3카드 타로",
        "오늘의 타로 카드와 3카드 스프레드로 보는 나의 하루. 친구와 결과를 공유해 보세요!"),
  'th':("Mallow ทาโรต์ — ไพ่วันนี้ & ไพ่ 3 ใบ",
        "ดูไพ่ทาโรต์ฟรี ไพ่ประจำวันนี้และไพ่ 3 ใบ อดีต ปัจจุบัน อนาคต ไม่ต้องสมัคร",
        "Mallow ทาโรต์ — ไพ่วันนี้ & ไพ่ 3 ใบ",
        "ไพ่ประจำวันนี้และไพ่ 3 ใบ อดีต ปัจจุบัน อนาคต ดูฟรีไม่ต้องสมัคร")}},
}

BLK = """/* ===== 언어별 SEO 동기화 =====
   canonical이 언어와 상관없이 ko 주소로 고정돼 있으면 검색엔진이 en/th 주소를
   ko 주소로 통합해 버려 영어·태국어 페이지가 색인에서 사라진다.
   그래서 언어를 바꿀 때마다 canonical·og:url·title·description을 그 언어의 주소로 맞춘다. */
const SEO_I18N={
 %s};
const SEO_BASE='%s';
function syncSEO(){
  const s=SEO_I18N[LANG]||SEO_I18N.ko;
  const url=SEO_BASE+(LANG==='ko'?'':'?lang='+LANG);
  const set=(sel,attr,v)=>{const e=document.querySelector(sel); if(e&&v) e.setAttribute(attr,v);};
  if(s.t) document.title=s.t;
  set('link[rel="canonical"]','href',url);
  set('meta[property="og:url"]','content',url);
  set('meta[name="description"]','content',s.d);
  set('meta[property="og:title"]','content',s.ot||s.t);
  set('meta[property="og:description"]','content',s.od||s.d);
}
/* applyLang은 초기 렌더와 언어 전환 양쪽에서 불리므로 여기서 한 번만 감싼다
   (함수 선언은 호이스팅되므로 정의보다 앞에 있어도 안전하다) */
(function(){ const _a=applyLang; applyLang=function(){ const r=_a.apply(this,arguments); syncSEO(); return r; }; })();
"""

def esc(s): return s.replace('\\', '\\\\').replace("'", "\\'")

for page, cfg in P.items():
    f = os.path.join(page, 'index.html')
    s = io.open(f, encoding='utf-8', newline='').read()
    base, langs, seo = cfg['base'], cfg['langs'], cfg['seo']
    ko = seo['ko']
    for c in seo.values():
        assert len(c[1]) <= 80, (page, len(c[1]))
    # 1) 정적 head = 기본 언어(ko). 라이브 URL(canonical)이 ko이므로 원본 HTML도 ko여야 한다.
    s = re.sub(r'<title>.*?</title>', lambda m: '<title>'+ko[0]+'</title>', s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")(.*?)(">)', lambda m: m.group(1)+ko[1]+m.group(3), s, count=1, flags=re.S)
    s = re.sub(r'(<meta property="og:title" content=")(.*?)(">)', lambda m: m.group(1)+ko[2]+m.group(3), s, count=1, flags=re.S)
    s = re.sub(r'(<meta property="og:description" content=")(.*?)(">)', lambda m: m.group(1)+ko[3]+m.group(3), s, count=1, flags=re.S)
    # 2) hreflang 클러스터 (JS 없이도 읽히도록 정적으로)
    if 'hreflang' not in s:
        cl = ''.join('\n<link rel="alternate" hreflang="%s" href="%s%s">' % (l, base, '' if l == 'ko' else '?lang='+l) for l in langs)
        cl += '\n<link rel="alternate" hreflang="x-default" href="%s">' % base
        can = '<link rel="canonical" href="%s">' % base
        assert can in s, f
        s = s.replace(can, can+cl, 1)
    # 3) 언어별 self-canonical 동기화
    if 'function syncSEO' not in s:
        tbl = ',\n '.join("%s:{t:'%s',d:'%s',ot:'%s',od:'%s'}" % (l, esc(seo[l][0]), esc(seo[l][1]), esc(seo[l][2]), esc(seo[l][3])) for l in langs)
        m = re.search(r'^function setLang\(', s, re.M)
        assert m, f
        s = s[:m.start()] + (BLK % (tbl, base)) + s[m.start():]
    io.open(f, 'w', encoding='utf-8', newline='').write(s)
    print('ok', page)
