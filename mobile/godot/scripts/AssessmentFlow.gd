class_name AssessmentFlow
extends Control

signal completed(scores: Dictionary)
signal skipped

const TOTAL_STEPS := 4
const MEMORY_SYMBOLS := ["●", "◆", "▲"]

var content: VBoxContainer
var stage_index := -1
var scores := {}
var rng := RandomNumberGenerator.new()
var flow_token := 0

var memory_sequence: Array[String] = []
var memory_next := 0
var memory_correct := 0
var memory_wrong := 0
var memory_status: Label
var memory_display: Label
var memory_grid: GridContainer
var memory_buttons: Array[Button] = []

var focus_round := 0
var focus_total_ms := 0
var focus_false := 0
var focus_started_at := 0
var focus_waiting := false
var focus_can_tap := false
var focus_status: Label
var focus_arena: Button

var calc_round := 0
var calc_correct := 0
var calc_target := 0
var calc_values: Array[int] = []
var calc_selected: Array[int] = []
var calc_total := 0
var calc_status: Label
var calc_target_label: Label
var calc_total_label: Label
var calc_grid: GridContainer
var calc_buttons: Array[Button] = []

var coord_stage: CoordStage

func _ready() -> void:
	rng.randomize()
	custom_minimum_size = Vector2(320, 640)
	size_flags_horizontal = Control.SIZE_EXPAND_FILL
	size_flags_vertical = Control.SIZE_EXPAND_FILL
	_show_intro()

func _show_intro() -> void:
	flow_token += 1
	_clear()
	var hero := PanelContainer.new()
	hero.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.BLUE_SOFT, 26, 20))
	content.add_child(hero)
	var hero_box := VBoxContainer.new()
	hero.add_child(hero_box)
	var avatar := MallowAvatar.new()
	avatar.mood = "good"
	avatar.custom_minimum_size = Vector2(112, 112)
	avatar.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	hero_box.add_child(avatar)
	hero_box.add_child(_label(I18n.t("assessment_eyebrow"), 10, ThemeKit.BLUE, HORIZONTAL_ALIGNMENT_CENTER))
	hero_box.add_child(_label(I18n.t("assessment_title"), 24, ThemeKit.INK, HORIZONTAL_ALIGNMENT_CENTER, true))
	hero_box.add_child(_label(I18n.t("assessment_intro"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_CENTER, true))

	var note := _pill(I18n.t("assessment_note"), ThemeKit.SURFACE, ThemeKit.MUTED, 11, true)
	note.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	content.add_child(note)

	var start := _button(I18n.t("assessment_start"), ThemeKit.BLUE, 58)
	start.add_theme_color_override("font_color", Color.WHITE)
	start.add_theme_color_override("font_hover_color", Color.WHITE)
	start.pressed.connect(_begin)
	content.add_child(start)
	var skip := _button(I18n.t("assessment_skip"), Color.WHITE, 50)
	skip.add_theme_color_override("font_color", ThemeKit.MUTED)
	skip.pressed.connect(_skip)
	content.add_child(skip)

func _begin() -> void:
	AudioDirector.tap()
	stage_index = 0
	_show_task()

func _skip() -> void:
	AudioDirector.tap()
	skipped.emit()

func _show_task() -> void:
	flow_token += 1
	_clear()
	var header := HBoxContainer.new()
	header.alignment = BoxContainer.ALIGNMENT_CENTER
	header.add_theme_constant_override("separation", 8)
	content.add_child(header)
	var step := _pill(I18n.t("assessment_step").replace("{step}", str(stage_index + 1)), ThemeKit.BLUE_SOFT, ThemeKit.BLUE, 11)
	header.add_child(step)
	var progress := ProgressBar.new()
	progress.max_value = TOTAL_STEPS
	progress.value = stage_index
	progress.show_percentage = false
	progress.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	progress.custom_minimum_size = Vector2(0, 8)
	progress.add_theme_stylebox_override("background", ThemeKit.box(Color("#dfe6fb"), 8))
	progress.add_theme_stylebox_override("fill", ThemeKit.box(ThemeKit.BLUE, 8))
	header.add_child(progress)

	match stage_index:
		0: _show_memory()
		1: _show_focus()
		2: _show_calculation()
		3: _show_coordination()

func _show_memory() -> void:
	content.add_child(_task_intro(I18n.t("assessment_memory_title"), I18n.t("assessment_memory_desc"), ThemeKit.PINK_SOFT, ThemeKit.PINK))
	memory_status = _pill(I18n.t("assessment_memory_show"), ThemeKit.PINK_SOFT, ThemeKit.PINK, 12)
	memory_status.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	content.add_child(memory_status)
	memory_display = _label("   ".join(MEMORY_SYMBOLS), 42, ThemeKit.PINK, HORIZONTAL_ALIGNMENT_CENTER)
	memory_display.custom_minimum_size = Vector2(0, 112)
	memory_display.add_theme_stylebox_override("normal", ThemeKit.panel_style(Color.WHITE, 24, 16, true))
	content.add_child(memory_display)
	memory_sequence.clear()
	for symbol in MEMORY_SYMBOLS:
		memory_sequence.append(symbol)
	memory_next = 0
	memory_correct = 0
	memory_wrong = 0
	flow_token += 1
	var token := flow_token
	await get_tree().create_timer(1.15).timeout
	if token != flow_token or stage_index != 0:
		return
	memory_display.text = "?   ?   ?"
	memory_status.text = I18n.t("assessment_memory_tap")
	memory_grid = GridContainer.new()
	memory_grid.columns = 3
	memory_grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	memory_grid.add_theme_constant_override("h_separation", 9)
	memory_grid.add_theme_constant_override("v_separation", 9)
	content.add_child(memory_grid)
	memory_buttons.clear()
	var options := MEMORY_SYMBOLS.duplicate()
	options.append("■")
	options.append("★")
	options.shuffle()
	for symbol in options:
		var button := _button(symbol, Color.WHITE, 76)
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		button.add_theme_font_size_override("font_size", 28)
		button.add_theme_color_override("font_color", ThemeKit.PINK)
		button.add_theme_color_override("font_hover_color", ThemeKit.PINK)
		button.pressed.connect(_memory_pick.bind(symbol, button))
		memory_grid.add_child(button)
		memory_buttons.append(button)

func _memory_pick(symbol: String, button: Button) -> void:
	if memory_next >= memory_sequence.size() or button.disabled:
		return
	if symbol == memory_sequence[memory_next]:
		AudioDirector.good()
		memory_correct += 1
		memory_next += 1
		button.disabled = true
		button.add_theme_stylebox_override("normal", ThemeKit.box(ThemeKit.PINK_SOFT, 16, ThemeKit.PINK, 2, false))
		memory_status.text = I18n.t("correct")
		if memory_next >= memory_sequence.size():
			scores["memory"] = clampi(int(round(float(memory_correct) / 3.0 * 100.0)) - memory_wrong * 7, 0, 100)
			_advance_task()
	else:
		AudioDirector.bad()
		memory_wrong += 1
		memory_status.text = I18n.t("try_again")

func _show_focus() -> void:
	content.add_child(_task_intro(I18n.t("assessment_focus_title"), I18n.t("assessment_focus_desc"), ThemeKit.AMBER_SOFT, ThemeKit.AMBER))
	focus_status = _pill(I18n.t("assessment_ready"), ThemeKit.AMBER_SOFT, ThemeKit.AMBER, 12)
	focus_status.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	content.add_child(focus_status)
	focus_arena = _button(I18n.t("react_wait"), ThemeKit.AMBER_SOFT, 310)
	focus_arena.add_theme_font_size_override("font_size", 30)
	focus_arena.add_theme_color_override("font_color", ThemeKit.AMBER)
	focus_arena.add_theme_color_override("font_hover_color", ThemeKit.AMBER)
	focus_arena.pressed.connect(_focus_pressed)
	content.add_child(focus_arena)
	content.add_child(_label("WAIT FOR BLUE  |  TAP ONCE", 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))
	focus_round = 0
	focus_total_ms = 0
	focus_false = 0
	_focus_start_round()

func _focus_start_round() -> void:
	flow_token += 1
	var token := flow_token
	focus_waiting = true
	focus_can_tap = false
	focus_arena.text = I18n.t("react_wait")
	focus_arena.add_theme_stylebox_override("normal", ThemeKit.button_style(ThemeKit.AMBER_SOFT, 26, Color("#f2d59c")))
	focus_arena.add_theme_color_override("font_color", ThemeKit.AMBER)
	focus_status.text = I18n.t("assessment_ready")
	await get_tree().create_timer(0.45 + rng.randf_range(0.3, 0.8)).timeout
	if token != flow_token or stage_index != 1:
		return
	focus_waiting = false
	focus_can_tap = true
	focus_started_at = Time.get_ticks_msec()
	focus_arena.text = I18n.t("react_go")
	focus_arena.add_theme_stylebox_override("normal", ThemeKit.button_style(ThemeKit.BLUE, 26, ThemeKit.BLUE_DARK))
	focus_arena.add_theme_color_override("font_color", Color.WHITE)
	focus_status.text = I18n.t("react_go")
	var pulse := create_tween()
	pulse.set_loops(2)
	pulse.tween_property(focus_arena, "scale", Vector2(1.015, 1.015), 0.12).set_trans(Tween.TRANS_SINE)
	pulse.tween_property(focus_arena, "scale", Vector2.ONE, 0.18).set_trans(Tween.TRANS_SINE)

func _focus_pressed() -> void:
	if focus_waiting:
		AudioDirector.bad()
		flow_token += 1
		focus_waiting = false
		focus_can_tap = false
		focus_false += 1
		focus_round += 1
		focus_status.text = I18n.t("react_false")
		if focus_round >= 3:
			_finish_focus()
		else:
			await get_tree().create_timer(0.35).timeout
			_focus_start_round()
		return
	if not focus_can_tap:
		return
	AudioDirector.good()
	focus_can_tap = false
	flow_token += 1
	focus_total_ms += maxi(1, Time.get_ticks_msec() - focus_started_at)
	focus_round += 1
	focus_status.text = str(focus_total_ms if focus_round == 1 else int(round(float(focus_total_ms) / float(focus_round)))) + " " + I18n.t("react_ms")
	if focus_round >= 3:
		_finish_focus()
	else:
		await get_tree().create_timer(0.35).timeout
		_focus_start_round()

func _finish_focus() -> void:
	var average := int(round(float(focus_total_ms) / float(maxi(1, focus_round))))
	scores["focus"] = clampi(100 - int(maxf(0.0, float(average - 180)) / 6.0) - focus_false * 12, 0, 100)
	_advance_task()

func _show_calculation() -> void:
	content.add_child(_task_intro(I18n.t("assessment_calc_title"), I18n.t("assessment_calc_desc"), ThemeKit.BLUE_SOFT, ThemeKit.BLUE))
	calc_status = _pill(I18n.t("assessment_ready"), ThemeKit.BLUE_SOFT, ThemeKit.BLUE, 12)
	calc_status.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	content.add_child(calc_status)
	var target_card := PanelContainer.new()
	target_card.add_theme_stylebox_override("panel", ThemeKit.soft_panel(Color("#eef3ff"), 22, 12))
	content.add_child(target_card)
	var target_box := VBoxContainer.new()
	target_box.alignment = BoxContainer.ALIGNMENT_CENTER
	target_card.add_child(target_box)
	target_box.add_child(_label("TARGET", 10, ThemeKit.BLUE, HORIZONTAL_ALIGNMENT_CENTER))
	calc_target_label = _label("", 38, ThemeKit.BLUE_DARK, HORIZONTAL_ALIGNMENT_CENTER)
	target_box.add_child(calc_target_label)
	calc_total_label = _label("0", 12, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_CENTER)
	target_box.add_child(calc_total_label)
	calc_grid = GridContainer.new()
	calc_grid.columns = 3
	calc_grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	calc_grid.add_theme_constant_override("h_separation", 9)
	calc_grid.add_theme_constant_override("v_separation", 9)
	content.add_child(calc_grid)
	calc_round = 0
	calc_correct = 0
	_calc_new_round()

func _calc_new_round() -> void:
	if calc_round >= 3:
		scores["calculation"] = clampi(int(round(float(calc_correct) / 3.0 * 100.0)), 0, 100)
		_advance_task()
		return
	calc_selected.clear()
	calc_total = 0
	var first := rng.randi_range(3, 8)
	var second := rng.randi_range(3, 8)
	calc_target = first + second
	calc_values = [first, second, rng.randi_range(1, 5), rng.randi_range(8, 12), rng.randi_range(2, 6), rng.randi_range(6, 10)]
	calc_values.shuffle()
	calc_target_label.text = str(calc_target)
	calc_total_label.text = "0"
	calc_status.text = I18n.t("assessment_ready")
	for child in calc_grid.get_children():
		calc_grid.remove_child(child)
		child.queue_free()
	calc_buttons.clear()
	for i in range(calc_values.size()):
		var button := _button(str(calc_values[i]), Color.WHITE, 72)
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		button.add_theme_font_size_override("font_size", 24)
		button.add_theme_color_override("font_color", ThemeKit.BLUE_DARK)
		button.add_theme_color_override("font_hover_color", ThemeKit.BLUE_DARK)
		button.pressed.connect(_calc_pick.bind(i, button))
		calc_grid.add_child(button)
		calc_buttons.append(button)
	calc_round += 1

func _calc_pick(index: int, button: Button) -> void:
	if button.disabled:
		return
	AudioDirector.tap()
	if index in calc_selected:
		calc_selected.erase(index)
		calc_total -= calc_values[index]
		button.add_theme_stylebox_override("normal", ThemeKit.button_style(Color.WHITE, 16, ThemeKit.BORDER))
	else:
		if calc_selected.size() >= 2:
			return
		calc_selected.append(index)
		calc_total += calc_values[index]
		button.add_theme_stylebox_override("normal", ThemeKit.button_style(ThemeKit.PINK_SOFT, 16, ThemeKit.PINK))
	calc_total_label.text = str(calc_total)
	if calc_selected.size() < 2:
		return
	if calc_total == calc_target:
		AudioDirector.good()
		calc_correct += 1
		calc_status.text = I18n.t("correct")
		for item in calc_buttons:
			item.disabled = true
		await get_tree().create_timer(0.35).timeout
		_calc_new_round()
	else:
		AudioDirector.bad()
		calc_status.text = I18n.t("try_again")
		await get_tree().create_timer(0.25).timeout
		for item in calc_buttons:
			item.add_theme_stylebox_override("normal", ThemeKit.button_style(Color.WHITE, 16, ThemeKit.BORDER))
		calc_selected.clear()
		calc_total = 0
		calc_total_label.text = "0"

func _show_coordination() -> void:
	content.add_child(_task_intro(I18n.t("assessment_coord_title"), I18n.t("assessment_coord_desc"), ThemeKit.TEAL_SOFT, ThemeKit.TEAL))
	var status := _pill(I18n.t("assessment_ready"), ThemeKit.TEAL_SOFT, ThemeKit.TEAL, 12)
	status.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	content.add_child(status)
	coord_stage = CoordStage.new()
	coord_stage.custom_minimum_size = Vector2(0, 340)
	coord_stage.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	coord_stage.finished.connect(_coord_finished.bind(status))
	content.add_child(coord_stage)
	content.add_child(_label("TAP THE GLOWING DOTS IN ORDER", 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _coord_finished(score: int, status: Label) -> void:
	AudioDirector.win()
	status.text = str(score) + " / 100"
	scores["coordination"] = score
	_advance_task()

func _advance_task() -> void:
	flow_token += 1
	var token := flow_token
	await get_tree().create_timer(0.45).timeout
	if token != flow_token:
		return
	stage_index += 1
	if stage_index >= TOTAL_STEPS:
		AudioDirector.win()
		completed.emit(scores.duplicate(true))
	else:
		_show_task()

func _clear() -> void:
	for child in get_children():
		remove_child(child)
		child.queue_free()
	content = VBoxContainer.new()
	content.add_theme_constant_override("separation", 12)
	content.custom_minimum_size = Vector2(320, 0)
	content.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	content.size_flags_vertical = Control.SIZE_EXPAND_FILL
	add_child(content)

func _task_intro(title: String, description: String, fill: Color, accent: Color) -> PanelContainer:
	var panel := PanelContainer.new()
	panel.add_theme_stylebox_override("panel", ThemeKit.soft_panel(fill, 20, 14))
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 4)
	panel.add_child(box)
	box.add_child(_label(I18n.t("assessment_eyebrow"), 9, accent))
	box.add_child(_label(title, 21, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
	box.add_child(_label(description, 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true))
	return panel

func _pill(text_value: String, fill: Color, color: Color, font_size: int, wrap: bool = false) -> Label:
	var label := _label(text_value, font_size, color, HORIZONTAL_ALIGNMENT_CENTER, wrap)
	var style := ThemeKit.box(fill, 18)
	style.content_margin_left = 12
	style.content_margin_right = 12
	style.content_margin_top = 7
	style.content_margin_bottom = 7
	label.add_theme_stylebox_override("normal", style)
	return label

func _button(text_value: String, fill: Color, height: int) -> Button:
	var button := Button.new()
	button.text = text_value
	button.custom_minimum_size = Vector2(0, height)
	button.add_theme_font_size_override("font_size", 15)
	button.add_theme_color_override("font_color", ThemeKit.INK)
	button.add_theme_color_override("font_hover_color", ThemeKit.INK)
	button.add_theme_color_override("font_pressed_color", ThemeKit.INK)
	button.add_theme_stylebox_override("normal", ThemeKit.button_style(fill, 16, ThemeKit.BORDER if fill == Color.WHITE else Color.TRANSPARENT))
	button.add_theme_stylebox_override("hover", ThemeKit.button_style(fill.lightened(0.04), 16, ThemeKit.BORDER if fill == Color.WHITE else Color.TRANSPARENT))
	button.add_theme_stylebox_override("pressed", ThemeKit.button_style(fill.darkened(0.04), 16))
	button.pressed.connect(_button_motion.bind(button))
	return button

func _button_motion(button: Button) -> void:
	button.pivot_offset = button.size * 0.5
	var tween := create_tween()
	tween.tween_property(button, "scale", Vector2(0.97, 0.97), 0.06)
	tween.tween_property(button, "scale", Vector2.ONE, 0.16).set_trans(Tween.TRANS_BACK)

func _label(text_value: String, font_size: int, color: Color, align: HorizontalAlignment = HORIZONTAL_ALIGNMENT_LEFT, wrap: bool = false) -> Label:
	var label := Label.new()
	label.text = text_value
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.horizontal_alignment = align
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	if wrap:
		label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	else:
		label.autowrap_mode = TextServer.AUTOWRAP_OFF
	return label

class CoordStage extends Control:
	signal finished(score: int)

	var points := PackedVector2Array()
	var current := 0
	var wrong := 0
	var started_at := 0
	var pulse := 0.0
	var complete := false

	func _ready() -> void:
		mouse_filter = Control.MOUSE_FILTER_STOP
		set_process(true)
		call_deferred("_make_points")

	func _notification(what: int) -> void:
		if what == NOTIFICATION_RESIZED and size.x > 30 and size.y > 30 and points.is_empty():
			_make_points()

	func _process(delta: float) -> void:
		pulse += delta
		queue_redraw()

	func _make_points() -> void:
		if size.x <= 30 or size.y <= 30:
			return
		points = PackedVector2Array([
			Vector2(size.x * 0.18, size.y * 0.76),
			Vector2(size.x * 0.26, size.y * 0.28),
			Vector2(size.x * 0.52, size.y * 0.16),
			Vector2(size.x * 0.82, size.y * 0.38),
			Vector2(size.x * 0.72, size.y * 0.78)
		])
		queue_redraw()

	func _gui_input(event: InputEvent) -> void:
		if complete:
			return
		if event is InputEventScreenTouch and event.pressed:
			_tap(event.position)
			accept_event()
		elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
			_tap(event.position)
			accept_event()

	func _tap(position: Vector2) -> void:
		if points.is_empty():
			return
		if started_at == 0:
			started_at = Time.get_ticks_msec()
		var target := points[current]
		if position.distance_to(target) > 52.0:
			wrong += 1
			AudioDirector.bad()
			return
		AudioDirector.good()
		current += 1
		if current >= points.size():
			complete = true
			var elapsed := maxf(0.0, float(Time.get_ticks_msec() - started_at) / 1000.0)
			var score := clampi(100 - wrong * 13 - maxi(0, int((elapsed - 5.0) * 2.0)), 0, 100)
			finished.emit(score)
		queue_redraw()

	func _draw() -> void:
		draw_style_box(ThemeKit.box(Color("#f7fcfa"), 24, Color("#d3eee2"), 1, false), Rect2(Vector2.ZERO, size))
		if points.size() > 1:
			draw_polyline(points, Color("#cfe5db"), 18.0, true)
			draw_polyline(points, Color.WHITE, 8.0, true)
		for i in range(points.size()):
			var point := points[i]
			var active := i == current and not complete
			if active:
				var glow := 27.0 + sin(pulse * 4.0) * 4.0
				draw_circle(point, glow, Color(0.12, 0.62, 0.47, 0.14))
				draw_circle(point, 18.0, ThemeKit.TEAL)
				draw_circle(point, 7.0, Color.WHITE)
			else:
				draw_circle(point, 15.0, ThemeKit.BLUE if i < current else Color("#c6d9d1"))
				draw_circle(point, 6.0, Color.WHITE)
