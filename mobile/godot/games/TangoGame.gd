extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const SOLUTIONS = [
	["001101", "110010", "011001", "100110", "010110", "101001"],
	["110010", "001101", "100110", "011001", "101001", "010110"]
]
const SIZE := 6

var board: GridContainer
var status: Label
var cells: Array[Button] = []
var state: Array[int] = []
var given: Array[bool] = []
var solution: Array = []
var mistakes := 0
var taps := 0

func _ready() -> void:
	_build()
	_new_puzzle()

func _build() -> void:
	var root := VBoxContainer.new()
	root.add_theme_constant_override("separation", 10)
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(root)
	var intro := PanelContainer.new()
	intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.BLUE_SOFT, 18, 14))
	root.add_child(intro)
	var intro_box := VBoxContainer.new()
	intro_box.add_theme_constant_override("separation", 4)
	intro.add_child(intro_box)
	intro_box.add_child(GameTools.label("DAILY LOGIC  |  TANGO", 10, ThemeKit.BLUE))
	intro_box.add_child(GameTools.label(I18n.t("tango_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
	status = GameTools.label(I18n.t("tango_round_ready"), 12, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_CENTER, true)
	root.add_child(status)
	board = GridContainer.new()
	board.columns = SIZE
	board.size_flags_vertical = Control.SIZE_EXPAND_FILL
	board.add_theme_constant_override("h_separation", 4)
	board.add_theme_constant_override("v_separation", 4)
	root.add_child(board)
	root.add_child(GameTools.label(I18n.t("tango_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER, true))

func _new_puzzle() -> void:
	var date := Time.get_date_dict_from_system()
	var day := int(date.get("day", 1)) + int(date.get("month", 1))
	solution = SOLUTIONS[day % SOLUTIONS.size()]
	state.clear()
	given.clear()
	for r in range(SIZE):
		for c in range(SIZE):
			var index := r * SIZE + c
			var is_given := (index + day) % 4 == 0 or (r == 0 and c % 2 == 0)
			given.append(is_given)
			state.append(int(solution[r][c]) if is_given else -1)
	mistakes = 0
	taps = 0
	for child in board.get_children():
		child.queue_free()
	cells.clear()
	for index in range(SIZE * SIZE):
		var cell: Button = GameTools.button("", ThemeKit.BLUE_SOFT, ThemeKit.BLUE_DARK, 50, ThemeKit.BLUE)
		cell.custom_minimum_size = Vector2(48, 48)
		cell.add_theme_font_size_override("font_size", 24)
		cell.pressed.connect(_cell_pressed.bind(index))
		board.add_child(cell)
		cells.append(cell)
	_refresh()

func _cell_pressed(index: int) -> void:
	if given[index]:
		return
	taps += 1
	if state[index] == -1:
		state[index] = 1
		AudioDirector.note(2)
	elif state[index] == 1:
		state[index] = 0
		AudioDirector.note(1)
	else:
		state[index] = -1
		AudioDirector.tap()
	var bad := _conflicts()
	if not bad.is_empty():
		mistakes += 1
		status.text = I18n.t("tango_wrong")
		AudioDirector.bad()
	else:
		status.text = I18n.t("tango_round_ready")
	_refresh()
	if _is_complete():
		_finish()

func _conflicts() -> Array[int]:
	var bad := {}
	for r in range(SIZE):
		var ones: Array[int] = []
		var zeros: Array[int] = []
		for c in range(SIZE):
			var index := r * SIZE + c
			if state[index] == 1:
				ones.append(index)
			elif state[index] == 0:
				zeros.append(index)
		if ones.size() > 3 or zeros.size() > 3:
			for index in ones + zeros:
				bad[index] = true
		for c in range(SIZE - 2):
			var a := r * SIZE + c
			var b := a + 1
			var d := a + 2
			if state[a] != -1 and state[a] == state[b] and state[a] == state[d]:
				bad[a] = true
				bad[b] = true
				bad[d] = true
	for c in range(SIZE):
		var ones: Array[int] = []
		var zeros: Array[int] = []
		for r in range(SIZE):
			var index := r * SIZE + c
			if state[index] == 1:
				ones.append(index)
			elif state[index] == 0:
				zeros.append(index)
		if ones.size() > 3 or zeros.size() > 3:
			for index in ones + zeros:
				bad[index] = true
		for r in range(SIZE - 2):
			var a := r * SIZE + c
			var b := (r + 1) * SIZE + c
			var d := (r + 2) * SIZE + c
			if state[a] != -1 and state[a] == state[b] and state[a] == state[d]:
				bad[a] = true
				bad[b] = true
				bad[d] = true
	var result: Array[int] = []
	for key in bad.keys():
		result.append(int(key))
	return result

func _refresh() -> void:
	var bad := _conflicts()
	for index in range(cells.size()):
		cells[index].text = "☀" if state[index] == 1 else ("☾" if state[index] == 0 else "")
		cells[index].modulate = Color(1.0, 0.68, 0.74) if index in bad else (Color(0.82, 0.86, 0.94) if given[index] else Color.WHITE)

func _is_complete() -> bool:
	for value in state:
		if value == -1:
			return false
	return _conflicts().is_empty()

func _finish() -> void:
	AudioDirector.win()
	var score := clampi(1000 - mistakes * 35 - maxi(0, taps - 12) * 2, 100, 1000)
	finished.emit({"score": score, "detail": "%d taps · %d errors" % [taps, mistakes]})
