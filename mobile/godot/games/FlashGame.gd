extends Control

signal finished(result: Dictionary)

const SYMBOLS := ["M", "A", "L", "O"]
const CARD_BACK := Color("#edf1ff")
const CARD_OPEN := Color("#ffffff")

var grid: GridContainer
var status: Label
var move_label: Label
var cards: Array[Button] = []
var values: Array[String] = []
var open_indices: Array[int] = []
var matched: Array[int] = []
var moves := 0
var locked := false

func _ready() -> void:
	_build()

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
	intro_box.add_child(_label("MEMORY  |  4 PAIRS", 10, ThemeKit.PINK))
	intro_box.add_child(_label(I18n.t("flash_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))

	var state_row := HBoxContainer.new()
	state_row.alignment = BoxContainer.ALIGNMENT_CENTER
	state_row.add_theme_constant_override("separation", 8)
	root.add_child(state_row)
	status = _label(I18n.t("tap_start"), 13, ThemeKit.PINK)
	status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	state_row.add_child(status)
	move_label = _pill("0 " + I18n.t("moves"), ThemeKit.BLUE_SOFT, ThemeKit.BLUE)
	state_row.add_child(move_label)

	grid = GridContainer.new()
	grid.columns = 2
	grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
	grid.add_theme_constant_override("h_separation", 10)
	grid.add_theme_constant_override("v_separation", 10)
	root.add_child(grid)

	root.add_child(_label("MATCH ALL PAIRS", 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))
	_start_round()

func _start_round() -> void:
	values.clear()
	for symbol in SYMBOLS:
		values.append(symbol)
		values.append(symbol)
	values.shuffle()
	for child in grid.get_children():
		grid.remove_child(child)
		child.queue_free()
	cards.clear()
	open_indices.clear()
	matched.clear()
	moves = 0
	locked = false
	for i in range(values.size()):
		var card := Button.new()
		card.custom_minimum_size = Vector2(0, 98)
		card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		card.size_flags_vertical = Control.SIZE_EXPAND_FILL
		card.add_theme_font_size_override("font_size", 30)
		card.add_theme_color_override("font_color", ThemeKit.BLUE_DARK)
		card.add_theme_color_override("font_hover_color", ThemeKit.BLUE_DARK)
		card.add_theme_stylebox_override("normal", ThemeKit.box(CARD_BACK, 18, Color("#d6def8"), 1, false))
		card.add_theme_stylebox_override("hover", ThemeKit.box(Color("#f4f6ff"), 18, Color("#afc0ff"), 1, false))
		card.add_theme_stylebox_override("pressed", ThemeKit.box(Color("#e2e8ff"), 18, ThemeKit.BLUE, 1, false))
		card.add_theme_stylebox_override("focus", ThemeKit.box(CARD_BACK, 18, ThemeKit.BLUE, 2, false))
		card.text = "?"
		card.pressed.connect(_card_pressed.bind(i))
		grid.add_child(card)
		cards.append(card)
	status.text = I18n.t("tap_start")
	move_label.text = "0 " + I18n.t("moves")

func _card_pressed(index: int) -> void:
	if locked or index in matched or index in open_indices:
		return
	AudioDirector.tap()
	open_indices.append(index)
	_reveal(index)
	if open_indices.size() < 2:
		return
	moves += 1
	move_label.text = str(moves) + " " + I18n.t("moves")
	locked = true
	var first := open_indices[0]
	var second := open_indices[1]
	if values[first] == values[second]:
		matched.append(first)
		matched.append(second)
		AudioDirector.good()
		status.text = I18n.t("correct")
		locked = false
		open_indices.clear()
		if matched.size() == values.size():
			_finish()
	else:
		AudioDirector.bad()
		status.text = I18n.t("try_again")
		await get_tree().create_timer(0.55).timeout
		_hide(first)
		_hide(second)
		open_indices.clear()
		locked = false

func _reveal(index: int) -> void:
	if index < cards.size():
		cards[index].text = values[index]
		cards[index].add_theme_stylebox_override("normal", ThemeKit.box(CARD_OPEN, 18, ThemeKit.PINK, 2, false))

func _hide(index: int) -> void:
	if index < cards.size() and index not in matched:
		cards[index].text = "?"
		cards[index].add_theme_stylebox_override("normal", ThemeKit.box(CARD_BACK, 18, Color("#d6def8"), 1, false))

func _finish() -> void:
	status.text = I18n.t("new_record")
	var score := maxi(100, 1000 - (moves - 4) * 55)
	finished.emit({"score": score, "detail": str(moves) + " " + I18n.t("moves")})

func _pill(text_value: String, fill: Color, color: Color) -> Label:
	var label := _label(text_value, 11, color, HORIZONTAL_ALIGNMENT_CENTER)
	var style := ThemeKit.box(fill, 18)
	style.content_margin_left = 10
	style.content_margin_right = 10
	style.content_margin_top = 5
	style.content_margin_bottom = 5
	label.add_theme_stylebox_override("normal", style)
	return label

func _label(text_value: String, font_size: int, color: Color, align: HorizontalAlignment = HORIZONTAL_ALIGNMENT_LEFT, wrap: bool = false) -> Label:
	var label := Label.new()
	label.text = text_value
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.horizontal_alignment = align
	if wrap:
		label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	else:
		label.autowrap_mode = TextServer.AUTOWRAP_OFF
	return label
