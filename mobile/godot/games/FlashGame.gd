extends Control

signal finished(result: Dictionary)

const SYMBOLS := ["●", "◆", "★", "✿"]
const CARD_BACK := Color("#e9efff")
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
	root.add_theme_constant_override("separation", 14)
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(root)
	root.add_child(_label(I18n.t("flash_ready"), 16, Color("#66738f"), HORIZONTAL_ALIGNMENT_CENTER))
	status = _label(I18n.t("tap_start"), 14, Color("#4f7cff"), HORIZONTAL_ALIGNMENT_CENTER)
	root.add_child(status)
	move_label = _label("0 " + I18n.t("moves"), 13, Color("#66738f"), HORIZONTAL_ALIGNMENT_CENTER)
	root.add_child(move_label)
	grid = GridContainer.new()
	grid.columns = 2
	grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
	grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	grid.add_theme_constant_override("h_separation", 12)
	grid.add_theme_constant_override("v_separation", 12)
	root.add_child(grid)
	var hint := _label("4 pairs  ·  memory warm-up", 12, Color("#98a3b8"), HORIZONTAL_ALIGNMENT_CENTER)
	root.add_child(hint)
	_start_round()

func _start_round() -> void:
	values.clear()
	for symbol in SYMBOLS:
		values.append(symbol)
		values.append(symbol)
	values.shuffle()
	for child in grid.get_children():
		child.queue_free()
	cards.clear()
	open_indices.clear()
	matched.clear()
	moves = 0
	locked = false
	for i in range(values.size()):
		var card := Button.new()
		card.custom_minimum_size = Vector2(0, 118)
		card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		card.add_theme_font_size_override("font_size", 34)
		card.add_theme_color_override("font_color", Color("#4f7cff"))
		card.add_theme_stylebox_override("normal", ThemeKit.box(CARD_BACK, 18, Color("#c8d5ff"), 1, true))
		card.add_theme_stylebox_override("hover", ThemeKit.box(Color("#f2f5ff"), 18, Color("#8fa8ff"), 1, true))
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
		cards[index].add_theme_stylebox_override("normal", ThemeKit.box(CARD_OPEN, 18, Color("#b8c8ff"), 2, true))

func _hide(index: int) -> void:
	if index < cards.size() and index not in matched:
		cards[index].text = "?"
		cards[index].add_theme_stylebox_override("normal", ThemeKit.box(CARD_BACK, 18, Color("#c8d5ff"), 1, true))

func _finish() -> void:
	status.text = I18n.t("new_record")
	var score := maxi(100, 1000 - (moves - 4) * 55)
	finished.emit({"score": score, "detail": str(moves) + " " + I18n.t("moves")})

func _label(text_value: String, font_size: int, color: Color, align: HorizontalAlignment) -> Label:
	var label := Label.new()
	label.text = text_value
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.horizontal_alignment = align
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	return label
