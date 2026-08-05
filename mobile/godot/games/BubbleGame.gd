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
	root.add_theme_constant_override("separation", 14)
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(root)
	root.add_child(_label(I18n.t("bubble_ready"), 16, Color("#66738f"), HORIZONTAL_ALIGNMENT_CENTER))
	target_label = _label("", 42, Color("#4f7cff"), HORIZONTAL_ALIGNMENT_CENTER)
	root.add_child(target_label)
	current_label = _label("0", 18, Color("#182235"), HORIZONTAL_ALIGNMENT_CENTER)
	root.add_child(current_label)
	status = _label(I18n.t("tap_start"), 14, Color("#66738f"), HORIZONTAL_ALIGNMENT_CENTER)
	root.add_child(status)
	grid = GridContainer.new()
	grid.columns = 3
	grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
	grid.add_theme_constant_override("h_separation", 10)
	grid.add_theme_constant_override("v_separation", 10)
	root.add_child(grid)
	root.add_child(_label("5 rounds  ·  tap to add, tap again to remove", 12, Color("#98a3b8"), HORIZONTAL_ALIGNMENT_CENTER))

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
		child.queue_free()
	for i in range(numbers.size()):
		var bubble := Button.new()
		bubble.text = str(numbers[i])
		bubble.custom_minimum_size = Vector2(0, 76)
		bubble.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		bubble.add_theme_font_size_override("font_size", 25)
		bubble.add_theme_color_override("font_color", Color("#3d5eaf"))
		bubble.add_theme_stylebox_override("normal", ThemeKit.box(Color("#dbe7ff"), 30, Color("#b6caff"), 1, true))
		bubble.add_theme_stylebox_override("hover", ThemeKit.box(Color("#eef3ff"), 30, Color("#8fa8ff"), 1, true))
		bubble.pressed.connect(_bubble_pressed.bind(i, bubble))
		grid.add_child(bubble)
	target_label.text = str(target)
	current_label.text = "0"
	status.text = str(rounds + 1) + "/5"

func _bubble_pressed(index: int, bubble: Button) -> void:
	AudioDirector.tap()
	if index in selected:
		selected.erase(index)
		total -= numbers[index]
		bubble.add_theme_stylebox_override("normal", ThemeKit.box(Color("#dbe7ff"), 30, Color("#b6caff"), 1, true))
	else:
		selected.append(index)
		total += numbers[index]
		bubble.add_theme_stylebox_override("normal", ThemeKit.box(Color("#ffd7e4"), 30, Color("#ff7096"), 2, true))
	current_label.text = str(total)
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

func _label(text_value: String, font_size: int, color: Color, align: HorizontalAlignment) -> Label:
	var label := Label.new()
	label.text = text_value
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.horizontal_alignment = align
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	return label
