extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")

const PUZZLES_KO = [
	[
		{"name": "김치의 종류", "words": ["배추김치", "깍두기", "동치미", "총각김치"]},
		{"name": "바람이 들어가는 말", "words": ["바람개비", "봄바람", "바람둥이", "칼바람"]},
		{"name": "전래동화 속 인물", "words": ["콩쥐", "흥부", "심청", "홍길동"]},
		{"name": "○박 — 앞에 붙는 말", "words": ["수", "쪽", "대", "함지"]}
	],
	[
		{"name": "십이지 동물", "words": ["토끼", "원숭이", "호랑이", "돼지"]},
		{"name": "윷놀이 끗수", "words": ["도", "개", "걸", "모"]},
		{"name": "판소리 다섯 마당", "words": ["춘향가", "심청가", "흥보가", "수궁가"]},
		{"name": "눈으로 시작하는 말", "words": ["눈치", "눈썰미", "눈웃음", "눈도장"]}
	]
]

const PUZZLES_EN = [
	[
		{"name": "Kinds of kimchi", "words": ["BAECHU", "KKAKDUGI", "DONGCHIMI", "CHONGGAK"]},
		{"name": "Words with wind", "words": ["WINDMILL", "BREEZE", "WINDY", "CROSSWIND"]},
		{"name": "Story characters", "words": ["CINDERELLA", "ROBIN", "ALICE", "PETERPAN"]},
		{"name": "Starts with sun", "words": ["SUNSET", "SUNRISE", "SUNFLOWER", "SUNDAY"]}
	],
	[
		{"name": "Planets", "words": ["MARS", "VENUS", "EARTH", "SATURN"]},
		{"name": "Board games", "words": ["CHESS", "GO", "CHECKERS", "CARDS"]},
		{"name": "Ocean animals", "words": ["WHALE", "DOLPHIN", "OCTOPUS", "SEAL"]},
		{"name": "Starts with star", "words": ["STARFISH", "STARLIGHT", "STARSHIP", "STARBOARD"]}
	]
]

var status: Label
var round_label: Label
var board: GridContainer
var group_labels: Array[Label] = []
var buttons: Array[Button] = []
var groups: Array = []
var tile_group: Array[int] = []
var selected: Array[int] = []
var solved: Array[bool] = []
var mistakes := 0
var rng := RandomNumberGenerator.new()

func _ready() -> void:
	rng.randomize()
	_build()
	_new_puzzle()

func _build() -> void:
	var root := VBoxContainer.new()
	root.add_theme_constant_override("separation", 10)
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(root)
	var intro := PanelContainer.new()
	intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.AMBER_SOFT, 18, 14))
	root.add_child(intro)
	var intro_box := VBoxContainer.new()
	intro_box.add_theme_constant_override("separation", 4)
	intro.add_child(intro_box)
	intro_box.add_child(GameTools.label("LANGUAGE  |  MOAMOA", 10, ThemeKit.AMBER))
	intro_box.add_child(GameTools.label(I18n.t("moamoa_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
	var row := HBoxContainer.new()
	root.add_child(row)
	status = GameTools.label(I18n.t("moamoa_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
	status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(status)
	round_label = GameTools.pill("0 / 4", ThemeKit.AMBER_SOFT, ThemeKit.AMBER)
	row.add_child(round_label)
	board = GridContainer.new()
	board.columns = 4
	board.size_flags_vertical = Control.SIZE_EXPAND_FILL
	board.add_theme_constant_override("h_separation", 7)
	board.add_theme_constant_override("v_separation", 7)
	root.add_child(board)
	var groups_panel := PanelContainer.new()
	groups_panel.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 18, 10, true))
	root.add_child(groups_panel)
	var groups_box := VBoxContainer.new()
	groups_box.add_theme_constant_override("separation", 3)
	groups_panel.add_child(groups_box)
	for index in range(4):
		var group_label := GameTools.label("•  " + I18n.t("moamoa_unsolved"), 11, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_LEFT, true)
		group_label.custom_minimum_size = Vector2(0, 22)
		groups_box.add_child(group_label)
		group_labels.append(group_label)
	root.add_child(GameTools.label(I18n.t("moamoa_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER, true))

func _new_puzzle() -> void:
	var date := Time.get_date_dict_from_system()
	var day := int(date.get("day", 1)) + int(date.get("month", 1)) + int(date.get("year", 2026))
	var source: Array = PUZZLES_EN if I18n.language == "en" else PUZZLES_KO
	groups = source[day % source.size()].duplicate(true)
	var words: Array[String] = []
	tile_group.clear()
	for group_index in range(groups.size()):
		for word in groups[group_index]["words"]:
			words.append(str(word))
			tile_group.append(group_index)
	var order := []
	for index in range(words.size()):
		order.append(index)
	order.shuffle()
	var shuffled_words: Array[String] = []
	var shuffled_groups: Array[int] = []
	for index in order:
		shuffled_words.append(words[index])
		shuffled_groups.append(tile_group[index])
	tile_group = shuffled_groups
	solved = [false, false, false, false]
	selected.clear()
	mistakes = 0
	round_label.text = "0 / 4"
	for label in group_labels:
		label.text = "•  " + I18n.t("moamoa_unsolved")
		label.add_theme_color_override("font_color", ThemeKit.SUBTLE)
	for child in board.get_children():
		child.queue_free()
	buttons.clear()
	for index in range(shuffled_words.size()):
		var button: Button = GameTools.button(shuffled_words[index], ThemeKit.AMBER_SOFT, ThemeKit.INK, 54, ThemeKit.AMBER)
		button.custom_minimum_size = Vector2(0, 58)
		button.add_theme_font_size_override("font_size", 13)
		button.pressed.connect(_tile_pressed.bind(index))
		board.add_child(button)
		buttons.append(button)
	status.text = I18n.t("moamoa_round_ready")

func _tile_pressed(index: int) -> void:
	if solved[tile_group[index]] or index in selected:
		return
	selected.append(index)
	buttons[index].modulate = Color(0.72, 0.86, 1.0)
	AudioDirector.tap()
	if selected.size() < 4:
		status.text = I18n.t("moamoa_selected") % selected.size()
		return
	await _submit_selection()

func _submit_selection() -> void:
	var target := tile_group[selected[0]]
	var correct := true
	for index in selected:
		if tile_group[index] != target:
			correct = false
			break
	if correct and not solved[target]:
		solved[target] = true
		for index in selected:
			buttons[index].disabled = true
			buttons[index].modulate = Color(0.72, 1.0, 0.83)
		group_labels[target].text = "✓  " + str(groups[target]["name"])
		group_labels[target].add_theme_color_override("font_color", ThemeKit.TEAL)
		AudioDirector.good()
		status.text = I18n.t("moamoa_good")
	else:
		mistakes += 1
		AudioDirector.bad()
		status.text = I18n.t("moamoa_wrong")
		for index in selected:
			buttons[index].modulate = Color(1.0, 0.78, 0.82)
		await get_tree().create_timer(0.32).timeout
		for index in selected:
			buttons[index].modulate = Color.WHITE
	selected.clear()
	var solved_count := 0
	for item in solved:
		if item:
			solved_count += 1
	round_label.text = "%d / 4" % solved_count
	if solved_count == 4:
		_finish()

func _finish() -> void:
	var score := clampi(1000 - mistakes * 75, 100, 1000)
	finished.emit({"score": score, "detail": "4/4 · %d" % mistakes})
