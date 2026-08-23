# -*- coding: utf-8 -*-
"""홈 화면 본문 보강 — 애드센스 리뷰어가 가장 먼저 보는 페이지.

문제: 홈은 렌더 기준 1,178자이고 첫 화면에 보이는 글자는 73자뿐인 런처 UI다.
      읽을 것이 .home-about 두 문단밖에 없다.
해결: .home-about에 실제로 궁금해할 내용(능력치가 무엇인지, 기록이 어디 저장되는지,
      오프라인이 되는지)을 3언어로 추가한다. 접힌 자리(하단)라 앱 UX는 그대로 둔다.

겸사겸사 사실 오류도 고친다 — 카피가 ko·en "33가지", th "31"로 서로 다르고,
실제 스킬 게임은 HOME_GAMES 기준 36개(cat.daily 3·cat.fun 7 제외)이며
36개 전부 screen-<id> 화면이 존재함을 확인했다. 능력 축 10개는 카테고리 10개와 일치.

data-i18n은 <br> 또는 <strong>이 있을 때만 innerHTML로 넣으므로 Q&A는 그 형태로 쓴다.
"""
import io, re

f = 'index.html'
s = io.open(f, encoding='utf-8', newline='').read()
assert 'about.p3' not in s, '이미 적용됨'

# ---- 1) 게임 수 표기 통일 (33/31 → 36) ----
before = s
s = s.replace('까지 33가지 미니게임을 제공합니다', '까지 36가지 미니게임을 제공합니다')
s = s.replace('— 33 mini games in all', '— 36 mini games in all')
s = s.replace('รวม 31 มินิเกม', 'รวม 36 มินิเกม')
assert s != before, '게임 수 문구를 찾지 못함'

# ---- 2) 홈 본문에 문단 추가 ----
ANCHOR = '<p data-i18n="about.p2">'
i = s.index(ANCHOR)
end = s.index('</p>', i) + 4
ADD = """
    <p data-i18n="about.p3">게임마다 결과가 기억력·집중력·순발력·관찰력·공간감각·계산·논리·언어·청각·협응 열 가지 능력 축에 쌓입니다. 한 판만 해도 그 축의 점수가 움직이고, 여러 축을 고루 채울수록 종합 등급이 올라갑니다. 어떤 축이 비어 있는지는 '내 기록' 화면의 그래프에서 한눈에 보이니, 오늘 무엇을 할지 고르기 어려울 때 참고하시면 됩니다.</p>
    <p data-i18n="about.p4">기록은 서버가 아니라 <strong>지금 쓰는 기기 안에만</strong> 저장됩니다. 그래서 계정을 만들 필요가 없고, 대신 브라우저 데이터를 지우거나 다른 기기에서 열면 기록이 따라오지 않습니다. 옮기고 싶다면 '내 기록' 화면의 백업 기능으로 내보냈다가 새 기기에서 불러오면 됩니다.</p>
    <p data-i18n="about.faq1"><strong>설치하지 않아도 되나요?</strong><br>네. 주소만 열면 바로 플레이됩니다. 자주 하신다면 홈 화면에 추가해 앱처럼 쓸 수 있고, 한 번 열어 둔 뒤에는 인터넷이 끊겨도 대부분 그대로 실행됩니다.</p>
    <p data-i18n="about.faq2"><strong>몇 살부터 할 수 있나요?</strong><br>글을 읽을 수 있으면 대부분의 게임을 할 수 있습니다. 카드 짝 맞추기나 다른 색 찾기처럼 규칙이 한 줄인 게임은 더 어릴 때도 괜찮고, 스도쿠·픽셀 로직처럼 논리가 필요한 게임은 초등 고학년 이후가 편합니다.</p>
    <p data-i18n="about.faq3"><strong>매일 해야 하나요?</strong><br>그럴 필요는 없습니다. 다만 하루 3판 정도를 같은 시간대에 하면 기록끼리 비교가 되기 때문에 변화가 눈에 보입니다. 컨디션에 따라 점수가 오르내리는 것도 정상입니다.</p>
    <p data-i18n="about.disc">플레이말로우의 두뇌게임은 가볍게 즐기는 오락이며, 의학적 진단이나 치료를 대신하지 않습니다. 운세 콘텐츠 역시 재미로 보는 내용입니다.</p>"""
s = s[:end] + ADD + s[end:]

# ---- 3) I18N 항목 추가 ----
I18N = '''  "about.p3": {ko:"게임마다 결과가 기억력·집중력·순발력·관찰력·공간감각·계산·논리·언어·청각·협응 열 가지 능력 축에 쌓입니다. 한 판만 해도 그 축의 점수가 움직이고, 여러 축을 고루 채울수록 종합 등급이 올라갑니다. 어떤 축이 비어 있는지는 '내 기록' 화면의 그래프에서 한눈에 보이니, 오늘 무엇을 할지 고르기 어려울 때 참고하시면 됩니다.", en:"Every game you finish feeds ten skill axes: memory, focus, speed, perception, spatial sense, math, logic, language, hearing and coordination. A single round moves that axis, and filling several of them raises your overall grade. The graph on the Records screen shows which axes are still empty, which is a good way to pick what to play when nothing stands out.", th:"ผลของทุกเกมจะสะสมลงใน 10 ด้าน ได้แก่ ความจำ สมาธิ ความไว การสังเกต มิติสัมพันธ์ การคำนวณ ตรรกะ ภาษา การฟัง และการประสานงาน เล่นรอบเดียวคะแนนด้านนั้นก็ขยับ และยิ่งเติมได้หลายด้าน ระดับรวมก็ยิ่งสูงขึ้น กราฟในหน้าบันทึกจะบอกว่าด้านไหนยังว่างอยู่"},
  "about.p4": {ko:"기록은 서버가 아니라 <strong>지금 쓰는 기기 안에만</strong> 저장됩니다. 그래서 계정을 만들 필요가 없고, 대신 브라우저 데이터를 지우거나 다른 기기에서 열면 기록이 따라오지 않습니다. 옮기고 싶다면 '내 기록' 화면의 백업 기능으로 내보냈다가 새 기기에서 불러오면 됩니다.", en:"Scores are stored <strong>on this device only</strong>, never on a server. That is why no account is needed — and also why clearing your browser data or opening the site on another device leaves your records behind. Use the backup option on the Records screen to export them and load them on the new device.", th:"บันทึกจะเก็บไว้<strong>ในเครื่องนี้เท่านั้น</strong> ไม่ได้เก็บบนเซิร์ฟเวอร์ จึงไม่ต้องสมัครบัญชี แต่ถ้าล้างข้อมูลเบราว์เซอร์หรือเปิดจากเครื่องอื่น บันทึกจะไม่ตามไปด้วย หากต้องการย้าย ให้ใช้เมนูสำรองข้อมูลในหน้าบันทึก"},
  "about.faq1": {ko:"<strong>설치하지 않아도 되나요?</strong><br>네. 주소만 열면 바로 플레이됩니다. 자주 하신다면 홈 화면에 추가해 앱처럼 쓸 수 있고, 한 번 열어 둔 뒤에는 인터넷이 끊겨도 대부분 그대로 실행됩니다.", en:"<strong>Do I need to install anything?</strong><br>No. Open the address and you are playing. If you come back often you can add it to your home screen and use it like an app, and once it has loaded it keeps working even when you go offline.", th:"<strong>ต้องติดตั้งไหม</strong><br>ไม่ต้อง เปิดหน้าเว็บแล้วเล่นได้เลย ถ้าเล่นบ่อยสามารถเพิ่มลงหน้าจอโฮมเพื่อใช้เหมือนแอป และเมื่อเปิดครั้งแรกแล้ว แม้เน็ตหลุดก็ยังเล่นต่อได้"},
  "about.faq2": {ko:"<strong>몇 살부터 할 수 있나요?</strong><br>글을 읽을 수 있으면 대부분의 게임을 할 수 있습니다. 카드 짝 맞추기나 다른 색 찾기처럼 규칙이 한 줄인 게임은 더 어릴 때도 괜찮고, 스도쿠·픽셀 로직처럼 논리가 필요한 게임은 초등 고학년 이후가 편합니다.", en:"<strong>What age is this for?</strong><br>Anyone who can read can play most of them. Games with a one-line rule, like card match or odd colour, work for younger children too, while Sudoku and pixel logic sit more comfortably from upper primary age.", th:"<strong>เหมาะกับอายุเท่าไร</strong><br>ถ้าอ่านหนังสือได้ก็เล่นได้เกือบทุกเกม เกมที่มีกติกาบรรทัดเดียว เช่น จับคู่การ์ด หรือ หาสีต่าง เด็กเล็กก็เล่นได้ ส่วนซูโดกุและนอนแกรมเหมาะกับประถมปลายขึ้นไป"},
  "about.faq3": {ko:"<strong>매일 해야 하나요?</strong><br>그럴 필요는 없습니다. 다만 하루 3판 정도를 같은 시간대에 하면 기록끼리 비교가 되기 때문에 변화가 눈에 보입니다. 컨디션에 따라 점수가 오르내리는 것도 정상입니다.", en:"<strong>Do I have to play every day?</strong><br>Not at all. But playing about three rounds at a similar time of day makes your scores comparable, so changes become visible. Scores moving up and down with how rested you are is completely normal.", th:"<strong>ต้องเล่นทุกวันไหม</strong><br>ไม่จำเป็น แต่ถ้าเล่นราว 3 รอบในช่วงเวลาใกล้เคียงกันของแต่ละวัน คะแนนจะเทียบกันได้และเห็นความเปลี่ยนแปลงชัดขึ้น คะแนนขึ้นลงตามสภาพร่างกายเป็นเรื่องปกติ"},
  "about.disc": {ko:"플레이말로우의 두뇌게임은 가볍게 즐기는 오락이며, 의학적 진단이나 치료를 대신하지 않습니다. 운세 콘텐츠 역시 재미로 보는 내용입니다.", en:"Mallow's brain games are light entertainment and are not a substitute for medical diagnosis or treatment. The fortune content is for fun as well.", th:"เกมฝึกสมองของ Mallow เป็นความบันเทิงเบา ๆ ไม่ใช่การวินิจฉัยหรือการรักษาทางการแพทย์ ส่วนเนื้อหาดูดวงมีไว้เพื่อความสนุก"},
'''
m = re.search(r'^  "about\.p2":.*\n', s, re.M)
assert m, 'about.p2 항목 없음'
s = s[:m.end()] + I18N + s[m.end():]

io.open(f, 'w', encoding='utf-8', newline='').write(s)
print('ok index.html — 홈 본문 6문단 + I18N 6키 ×3언어, 게임 수 36으로 통일')
