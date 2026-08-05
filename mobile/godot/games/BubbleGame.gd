extends Control

signal finished(result: Dictionary)

var target_label: Label
var current_label: Label
var status: Label
var grid: GridContainer
var selected: Array[int] = []
var numbers: Array[int] = []
var target := 0
var total := 0
var score := 0
var rounds := 0
var rng := RandomNumberGenerator.new()

func _ready() -> void:
	rng.randomize()
	_build()
	_new_round()

func _build() -> void:
	var root := VBoxContainer.new()
	root.add_theme_constant_override("separation", 12)
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(root)

	var target_card := PanelContainer.new()
	target_card.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.BLUE_SOFT, 20, 14))
	root.add_child(target_card)
	var target_box := VBoxContainer.new()
	target_box.alignment = BoxContainer.ALIGNMENT_CENTER
	target_box.add_theme_constant_override("separation", 3)
	target_card.add_child(target_box)
	target_box.add_child(_label("TARGET", 10, ThemeKit.BLUE, HORIZONTAL_ALIGNMENT_CENTER))
	target_label = _label("", 40, ThemeKit.BLUE_DARK, HORIZONTAL_ALIGNMENT_CENTER)
	target_box.add_child(target_label)
	target_box.add_child(_label(I18n.t("bubble_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_CENTER, true))

	var state_row := HBoxContainer.new()
	state_row.alignment = BoxContainer.ALIGNMENT_CENTER
	state_row.add_theme_constant_override("separation", 8)
	root.add_child(state_row)
	status = _pill("01 / 05", ThemeKit.PINK_SOFT, ThemeKit.PINK)
	state_row.add_child(status)
	current_label = _pill("0", ThemeKit.TEAL_SOFT, ThemeKit.TEAL)
	current_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	state_row.add_child(current_label)

	grid = GridContainer.new()
	grid.columns = 3
	grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
	grid.add_theme_constant_override("h_separation", 9)
	grid.add_theme_constant_override("v_separation", 9)
	root.add_child(grid)
	root.add_child(_label("TAP TO ADD  |  TAP AGAIN TO REMOVE", 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_round() -> void:
	selected.clear()
	numbers.clear()
	total = 0
	var seed_numbers := [rng.randi_range(3, 8), rng.randi_range(3, 8), rng.randi_range(3, 8)]
	target = seed_numbers[0] + seed_numbers[1] + seed_numbers[2]
	for number in seed_numbers:
		numbers.append(number)
	for i in range(6):
		numbers.append(rng.randi_range(1, 9))
	numbers.shuffle()
	for child in grid.get_children():
		grid.remove_child(child)
		child.queue_free()
	for i in range(numbers.size()):
		var bubble := Button.new()
		bubble.text = str(numbers[i])
		bubble.custom_minimum_size = Vector2(0, 72)
		bubble.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		bubble.size_flags_vertical = Control.SIZE_EXPAND_FILL
		bubble.add_theme_font_size_override("font_size", 24)
		bubble.add_theme_color_override("font_color", ThemeKit.BLUE_DARK)
		bubble.add_theme_color_override("font_hover_color", ThemeKit.BLUE_DARK)
		bubble.add_theme_stylebox_override("normal", ThemeKit.box(Color("#e5ecff"), 28, Color("#c9d5ff"), 1, false))
		bubble.add_theme_stylebox_override("hover", ThemeKit.box(Color("#f1f4ff"), 28, Color("#9fb2ff"), 1, false))
		bubble.add_theme_stylebox_override("pressed", ThemeKit.box(Color("#d8e2ff"), 28, ThemeKit.BLUE, 2, false))
		bubble.add_theme_stylebox_override("focus", ThemeKit.box(Color("#e5ecff"), 28, ThemeKit.BLUE, 2, false))
		bubble.pressed.connect(_bubble_pressed.bind(i, bubble))
		grid.add_child(bubble)
	target_label.text = str(target)
	current_label.text = "0 / " + str(target)
	status.text = "%02d / 05" % (rounds + 1)

func _bubble_pressed(index: int, bubble: Button) -> void:
	AudioDirector.tap()
	if index in selected:
		selected.erase(index)
		total -= numbers[index]
		bubble.add_theme_stylebox_override("normal", ThemeKit.box(Color("#e5ecff"), 28, Color("#c9d5ff"), 1, false))
	else:
		selected.append(index)
		total += numbers[index]
		bubble.add_theme_stylebox_override("normal", ThemeKit.box(ThemeKit.PINK_SOFT, 28, ThemeKit.PINK, 2, false))
	current_label.text = str(total) + " / " + str(target)
	if total > target:
		AudioDirector.bad()
		status.text = I18n.t("try_again")
		await get_tree().create_timer(0.28).timeout
		_new_round()
	elif total == target:
		AudioDirector.good()
		score += 100 + maxi(0, 30 - selected.size() * 5)
		rounds += 1
		status.text = I18n.t("correct")
		if rounds >= 5:
			_finish()
		else:
			await get_tree().create_timer(0.4).timeout
			_new_round()

func _finish() -> void:
	finished.emit({"score": score, "detail": str(rounds) + " rounds"})

func _pill(text_value: String, fill: Color, color: Color) -> Label:
	var label := _label(text_value, 12, color, HORIZONTAL_ALIGNMENT_CENTER)
	var style := ThemeKit.box(fill, 18)
	style.content_margin_left = 10
	style.content_margin_right = 10
	style.content_margin_top = 6
	style.content_margin_bottom = 6
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
