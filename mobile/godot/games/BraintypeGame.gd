extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")

const QUESTIONS_KO = [
	{"prompt": "짧은 쉬는 시간에 무엇이 끌리나요?", "options": [["기억 카드 뒤집기", "memory"], ["빠른 반응 누르기", "speed"], ["퍼즐 규칙 찾기", "logic"]]},
	{"prompt": "새 게임을 시작하면 먼저 무엇을 보나요?", "options": [["전체 판을 훑어요", "sight"], ["규칙을 읽어요", "logic"], ["손부터 움직여요", "coordination"]]},
	{"prompt": "가장 뿌듯한 순간은 언제인가요?", "options": [["연속 콤보를 이을 때", "focus"], ["어려운 계산을 맞힐 때", "calculation"], ["소리와 리듬을 맞힐 때", "sound"]]},
	{"prompt": "길에서 간판을 볼 때 더 잘 기억하는 것은?", "options": [["색과 모양", "sight"], ["숫자와 순서", "memory"], ["말의 뜻", "language"]]},
	{"prompt": "게임 난이도가 올라가면 어떻게 하나요?", "options": [["천천히 패턴을 분석해요", "logic"], ["속도를 더 높여요", "speed"], ["몇 번 직접 해봐요", "coordination"]]},
	{"prompt": "좋아하는 퍼즐의 느낌은?", "options": [["말랑하고 직관적", "sight"], ["차분하고 규칙적", "focus"], ["계산하고 조합하는 맛", "calculation"]]},
	{"prompt": "노래를 들을 때 먼저 잡는 것은?", "options": [["멜로디", "sound"], ["가사", "language"], ["박자", "focus"]]},
	{"prompt": "친구와 게임할 때 나는?", "options": [["힌트를 찾아줘요", "logic"], ["빠르게 먼저 풀어요", "speed"], ["분위기를 즐겨요", "coordination"]]},
	{"prompt": "숫자 암호를 받으면?", "options": [["순서를 외워요", "memory"], ["규칙을 추측해요", "logic"], ["대략적인 값을 먼저 봐요", "calculation"]]},
	{"prompt": "화면에서 작은 차이를 발견하는 편인가요?", "options": [["금방 찾아요", "sight"], ["끝까지 집중해요", "focus"], ["손으로 직접 표시해요", "coordination"]]},
	{"prompt": "새 단어를 배울 때 잘 맞는 방법은?", "options": [["소리 내어 반복", "sound"], ["글자로 써보기", "language"], ["문장 속에서 보기", "memory"]]},
	{"prompt": "오늘의 게임을 고른다면?", "options": [["나의 기록을 깨는 게임", "speed"], ["처음 보는 논리 퍼즐", "logic"], ["편안하게 감각을 쓰는 게임", "sound"]]}
]

const QUESTIONS_EN = [
	{"prompt": "What sounds fun in a short break?", "options": [["Flip memory cards", "memory"], ["Tap a fast reaction", "speed"], ["Find a puzzle rule", "logic"]]},
	{"prompt": "When you start a new game, what comes first?", "options": [["Scan the whole board", "sight"], ["Read the rules", "logic"], ["Move my hands", "coordination"]]},
	{"prompt": "Which moment feels best?", "options": [["Keeping a combo", "focus"], ["Solving a hard sum", "calculation"], ["Matching sound and rhythm", "sound"]]},
	{"prompt": "What do you remember from a sign?", "options": [["Its color and shape", "sight"], ["Numbers and order", "memory"], ["The meaning of words", "language"]]},
	{"prompt": "When a game gets harder, you…", "options": [["Analyze the pattern", "logic"], ["Move even faster", "speed"], ["Try it hands-on", "coordination"]]},
	{"prompt": "What puzzle feeling do you like?", "options": [["Soft and intuitive", "sight"], ["Calm and rule-based", "focus"], ["Calculating and combining", "calculation"]]},
	{"prompt": "When listening to music, what do you catch first?", "options": [["The melody", "sound"], ["The lyrics", "language"], ["The beat", "focus"]]},
	{"prompt": "When playing with friends, you…", "options": [["Find the hint", "logic"], ["Solve it first", "speed"], ["Enjoy the flow", "coordination"]]},
	{"prompt": "When you receive a number code, you…", "options": [["Remember the order", "memory"], ["Guess the rule", "logic"], ["Estimate the scale", "calculation"]]},
	{"prompt": "How are you with tiny visual differences?", "options": [["I spot them quickly", "sight"], ["I stay with it", "focus"], ["I mark them by hand", "coordination"]]},
	{"prompt": "What helps you learn a new word?", "options": [["Repeat its sound", "sound"], ["Write the letters", "language"], ["See it in a sentence", "memory"]]},
	{"prompt": "Choose today’s game mood.", "options": [["Beat my best time", "speed"], ["Meet a new logic puzzle", "logic"], ["Use my senses softly", "sound"]]}
]

var question_label: Label
var progress: Label
var options_box: VBoxContainer
var questions: Array = []
var counts: Dictionary = {}
var question_index := 0

func _ready() -> void:
	questions = QUESTIONS_EN if I18n.language == "en" else QUESTIONS_KO
	_build()
	_render_question()

func _build() -> void:
	var root := VBoxContainer.new()
	root.add_theme_constant_override("separation", 12)
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(root)
	var intro := PanelContainer.new()
	intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.PINK_SOFT, 18, 14))
	root.add_child(intro)
	var intro_box := VBoxContainer.new()
	intro_box.add_theme_constant_override("separation", 4)
	intro.add_child(intro_box)
	intro_box.add_child(GameTools.label("PLAY STYLE  |  12 QUESTIONS", 10, ThemeKit.PINK))
	intro_box.add_child(GameTools.label(I18n.t("braintype_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
	progress = GameTools.label("01 / 12", 12, ThemeKit.PINK, HORIZONTAL_ALIGNMENT_CENTER)
	root.add_child(progress)
	var question_panel := PanelContainer.new()
	question_panel.size_flags_vertical = Control.SIZE_EXPAND_FILL
	question_panel.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 24, 18, true))
	root.add_child(question_panel)
	var question_box := VBoxContainer.new()
	question_box.add_theme_constant_override("separation", 18)
	question_panel.add_child(question_box)
	question_label = GameTools.label("", 22, ThemeKit.INK, HORIZONTAL_ALIGNMENT_CENTER, true)
	question_label.size_flags_vertical = Control.SIZE_EXPAND_FILL
	question_box.add_child(question_label)
	options_box = VBoxContainer.new()
	options_box.add_theme_constant_override("separation", 10)
	question_box.add_child(options_box)
	root.add_child(GameTools.label(I18n.t("braintype_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER, true))

func _render_question() -> void:
	var item: Dictionary = questions[question_index]
	question_label.text = str(item["prompt"])
	progress.text = "%02d / %02d" % [question_index + 1, questions.size()]
	for child in options_box.get_children():
		child.queue_free()
	for option in item["options"]:
		var button: Button = GameTools.button(str(option[0]), ThemeKit.PINK_SOFT, ThemeKit.PINK, 56, ThemeKit.PINK)
		button.add_theme_font_size_override("font_size", 15)
		button.pressed.connect(_answer_pressed.bind(str(option[1]), button))
		options_box.add_child(button)

func _answer_pressed(axis: String, button: Button) -> void:
	GameTools.animate_press(button)
	counts[axis] = int(counts.get(axis, 0)) + 1
	AudioDirector.tap()
	await get_tree().create_timer(0.22).timeout
	question_index += 1
	if question_index >= questions.size():
		_finish()
	else:
		_render_question()

func _finish() -> void:
	var best_axis := "logic"
	var best_count := -1
	for axis in counts.keys():
		if int(counts[axis]) > best_count:
			best_axis = str(axis)
			best_count = int(counts[axis])
	var names_ko := {"memory": "기억형", "focus": "집중형", "calculation": "계산형", "coordination": "협응형", "speed": "순발형", "space": "공간형", "logic": "논리형", "language": "언어형", "sound": "청각형", "sight": "관찰형"}
	var names_en := {"memory": "Memory Mallow", "focus": "Focus Mallow", "calculation": "Number Mallow", "coordination": "Action Mallow", "speed": "Speed Mallow", "space": "Space Mallow", "logic": "Logic Mallow", "language": "Word Mallow", "sound": "Sound Mallow", "sight": "Sight Mallow"}
	var type_name := str((names_en if I18n.language == "en" else names_ko).get(best_axis, best_axis))
	var score := clampi(int(round(float(best_count) / float(questions.size()) * 1000.0)), 100, 1000)
	AudioDirector.win()
	finished.emit({"score": score, "detail": type_name})
