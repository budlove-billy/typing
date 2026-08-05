extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const REGION_COLORS = [Color("#f7d5e0"), Color("#d5e5f7"), Color("#d8f2dc"), Color("#f8e9ba"), Color("#e5d8f7"), Color("#cdeeed")]
const CROWN_PATTERNS = [[0, 2, 4, 1, 3, 5], [1, 3, 5, 0, 2, 4], [2, 4, 0, 3, 5, 1]]
const SIZE := 6

var board: GridContainer
var status: Label
var round_label: Label
var cells: Array[Button] = []
var state: Array[int] = []
var region: Array[int] = []
var crown_cols: Array = []
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
	intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.PINK_SOFT, 18, 14))
	root.add_child(intro)
	var intro_box := VBoxContainer.new()
	intro_box.add_theme_constant_override("separation", 4)
	intro.add_child(intro_box)
	intro_box.add_child(GameTools.label("DAILY LOGIC  |  CROWN", 10, ThemeKit.PINK))
	intro_box.add_child(GameTools.label(I18n.t("queens_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
	var row := HBoxContainer.new()
	root.add_child(row)
	status = GameTools.label(I18n.t("queens_round_ready"), 12, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
	status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(status)
	round_label = GameTools.pill("6 × 6", ThemeKit.PINK_SOFT, ThemeKit.PINK)
	row.add_child(round_label)
	board = GridContainer.new()
	board.columns = SIZE
	board.size_flags_vertical = Control.SIZE_EXPAND_FILL
	board.add_theme_constant_override("h_separation", 4)
	board.add_theme_constant_override("v_separation", 4)
	root.add_child(board)
	root.add_child(GameTools.label(I18n.t("queens_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER, true))

func _new_puzzle() -> void:
	var date := Time.get_date_dict_from_system()
	var day := int(date.get("day", 1)) + int(date.get("month", 1))
	crown_cols = CROWN_PATTERNS[day % CROWN_PATTERNS.size()].duplicate()
	_region_from_solution()
	state.clear()
	state.resize(SIZE * SIZE)
	for index in range(state.size()):
		state[index] = 0
	mistakes = 0
	taps = 0
	for child in board.get_children():
		child.queue_free()
	cells.clear()
	for index in range(state.size()):
		var cell: Button = GameTools.button("", REGION_COLORS[region[index] % REGION_COLORS.size()], ThemeKit.INK, 50, ThemeKit.PINK)
		cell.custom_minimum_size = Vector2(48, 48)
		cell.add_theme_font_size_override("font_size", 22)
		cell.pressed.connect(_cell_pressed.bind(index))
		board.add_child(cell)
		cells.append(cell)
	_refresh()

func _region_from_solution() -> void:
	region.clear()
	region.resize(SIZE * SIZE)
	for r in range(SIZE):
		for c in range(SIZE):
			var best_region := 0
			var best_distance := 999
			for g in range(SIZE):
				var distance: int = abs(r - g) + abs(c - int(crown_cols[g]))
				if distance < best_distance:
					best_distance = distance
					best_region = g
			region[r * SIZE + c] = best_region

func _cell_pressed(index: int) -> void:
	taps += 1
	state[index] = (state[index] + 1) % 3
	if state[index] == 2:
		AudioDirector.note(3)
	elif state[index] == 1:
		AudioDirector.tap()
	else:
		AudioDirector.tap()
	var bad := _conflicts()
	if not bad.is_empty():
		mistakes += 1
		AudioDirector.bad()
		status.text = I18n.t("queens_wrong")
	else:
		status.text = I18n.t("queens_round_ready")
	_refresh()
	if _is_complete():
		_finish()

func _conflicts() -> Array[int]:
	var bad := {}
	var rows := {}
	var cols := {}
	var regions := {}
	var crowns: Array[Vector2i] = []
	for r in range(SIZE):
		for c in range(SIZE):
			if state[r * SIZE + c] != 2:
				continue
			var index := r * SIZE + c
			crowns.append(Vector2i(r, c))
			if not rows.has(r):
				rows[r] = []
			rows[r].append(index)
			if not cols.has(c):
				cols[c] = []
			cols[c].append(index)
			if not regions.has(region[index]):
				regions[region[index]] = []
			regions[region[index]].append(index)
	for values in rows.values():
		if values.size() > 1:
			for index in values:
				bad[index] = true
	for values in cols.values():
		if values.size() > 1:
			for index in values:
				bad[index] = true
	for values in regions.values():
		if values.size() > 1:
			for index in values:
				bad[index] = true
	for left_index in range(crowns.size()):
		for right_index in range(left_index + 1, crowns.size()):
			var left := crowns[left_index]
			var right := crowns[right_index]
			if abs(left.x - right.x) <= 1 and abs(left.y - right.y) <= 1:
				bad[left.x * SIZE + left.y] = true
				bad[right.x * SIZE + right.y] = true
	var result: Array[int] = []
	for key in bad.keys():
		result.append(int(key))
	return result

func _refresh() -> void:
	var bad := _conflicts()
	for index in range(cells.size()):
		if state[index] == 2:
			cells[index].text = "♛"
		elif state[index] == 1:
			cells[index].text = "×"
		else:
			cells[index].text = ""
		cells[index].modulate = Color(1.0, 0.68, 0.74) if index in bad else Color.WHITE

func _is_complete() -> bool:
	var crown_count := 0
	for value in state:
		if value == 2:
			crown_count += 1
	if crown_count != SIZE or not _conflicts().is_empty():
		return false
	for r in range(SIZE):
		var count := 0
		for c in range(SIZE):
			if state[r * SIZE + c] == 2:
				count += 1
		if count != 1:
			return false
	for c in range(SIZE):
		var count := 0
		for r in range(SIZE):
			if state[r * SIZE + c] == 2:
				count += 1
		if count != 1:
			return false
	return true

func _finish() -> void:
	AudioDirector.win()
	var score := clampi(1000 - mistakes * 35 - maxi(0, taps - SIZE) * 2, 100, 1000)
	finished.emit({"score": score, "detail": "%d taps · %d errors" % [taps, mistakes]})
